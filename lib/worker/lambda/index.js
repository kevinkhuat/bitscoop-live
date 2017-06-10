'use strict';

const assert = require('assert');

const _ = require('lodash');
const AWS = require('aws-sdk');
const moment = require('moment');
const mongodb = require('mongodb');


let lambda = new AWS.Lambda();


exports.handler = function(event, context, callback) {
	return Promise.resolve()
		.then(function() {
			return new Promise(function(resolve, reject) {
				mongodb.MongoClient.connect(address, options, function(err, db) {
					if (err) {
						reject(err);
					}
					else {
						resolve(db);
					}
				});
			});
		})
		.then(function(mongo) {
			return mongo.db('live').collection('providers').find({}, {
				_id: true
			}).toArray()
				.then(function(results) {
					let ids = _.map(results, function(result) {
						return result._id;
					});

					return Promise.resolve(ids);
				})
				.then(function(ids) {
					let $match = {
						$and: [
							{
								'auth.status.complete': true,
								enabled: true,
								provider_id: {
									$in: ids
								}
							},
							{
								$or: [
									{
										last_run: {
											$lt: new Date(new Date() - 86400000)
										}
									},
									{
										last_run: {
											$exists: false
										}
									}
								]
							},
							{
								$or: [
									{
										run_started: {
											$gt: new Date(new Date() - 600000)
										}
									},
									{
										$not: {
											in_progress: true
										}
									}
								]
							}
						]
					};

					return mongo.db('live').collection('connections').find($match, {
						_id: true
					}).toArray()
						.then(function(connections) {
							if (!Array.isArray(connections)) {
								return Promise.resolve([]);
							}

							let jobs = _.map(connections, function(connection) {
								let payload = {
									connectionId: connection._id.toString('hex')
								};

								let params = {
									FunctionName: process.env.FETCH_FUNCTION_NAME,
									InvocationType: 'Event',
									Payload: new Buffer(JSON.stringify(payload))
								};

								return new Promise(function(resolve, reject) {
									lambda.invoke(params, function(err, data) {
										if (err) {
											reject(err);
										}
										else {
											resolve(data);
										}
									});
								});
							});

							return Promise.resolve(jobs);
						});
				});
		})
		.then(function(data) {
			console.log('SUCCESSFUL');

			callback(null, null);

			return Promise.resolve();
		})
		.catch(function(err) {
			console.log('UNSUCCESSFUL');

			return Promise.reject(err);
		});
};
