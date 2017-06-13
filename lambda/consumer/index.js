'use strict';

const assert = require('assert');

const AWS = require('aws-sdk');
const _ = require('lodash');
const mongodb = require('mongodb');


let sqs = new AWS.SQS();
let lambda = new AWS.Lambda;


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
			let params = {
				QueueUrl: process.env.QUEUE_URL,
				MaxNumberOfMessages: 10
			};

			return new Promise(function(resolve, reject) {
				sqs.receiveMessage(params, function(err, data) {
					if (err) {
						reject(err);
					}
					else {
						resolve(data);
					}
				});
			})
				.then(function(messages) {
					let ids = _.map(messages, function(message) {
						let attr = message.MessageAttributes;

						return gid(attr.connectionId.StringValue);
					});

					return mongo.db('live').collection('connections').find({
						_id: {
							$in: ids
						}
					});
				})
				.then(function(connections) {
					let jobs = _.map(connections, function(connection) {
						let payload = {
							connectionId: connection._id.toString('hex')
						};

						let params = {
							FunctionName: process.env.WORKER_FUNCTION_NAME,
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
						})
							.catch(function(err) {
								let params = {
									QueueUrl: process.env.DEAD_MESSAGE_QUEUE_URL,
									MessageBody: 'Connection failed.',
									MessageAttributes: {
										error: err
									}
								};

								return new Promise(function(resolve, reject) {
									sqs.sendMessage(params, function(err, data) {
										if (err) {
											reject(err);
										}
										else {
											resolve();
										}
									});
								});
							});
					});

					return Promise.all(jobs);
				});
		})
		.then(function() {
			console.log('SUCCESSFUL');

			callback(null, null);

			return Promise.resolve();
		})
		.catch(function(err) {
			console.log('UNSUCCESSFUL');

			return Promise.reject(err);
		});
};
