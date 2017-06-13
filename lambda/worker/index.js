'use strict';

const assert = require('assert');

const AWS = require('aws-sdk');
const BitScoop = require('bitscoop-sdk');
const _ = require('lodash');
const moment = require('moment');
const mongodb = require('mongodb');

const sources = require('./sources');


let bitscoop = new BitScoop(process.env.BITSCOOP_API_KEY);
let sqs = new AWS.SQS();


exports.handler = function(event, context, callback) {
	let payload = JSON.parse(event.payload);
	let connectionId = payload.connectionId;

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
			return mongo.db('live').collection('connections').findOne({
				_id: connectionId
			})
				.then(function(connection) {
					if (connection == null) {
						return Promise.reject(new Error('No connection with ID ' + connectionId.toString('hex')))
					}

					return bitscoop.getConnection(connection.remote_connection_id.toString('hex'))
						.then(function(remoteConnection) {
							remoteConnection = _.omit(remoteConnection, ['id', 'auth', 'provider_id']);

							_.assign(connection, remoteConnection);

							return Promise.resolve(connection);
						})
				})
				.then(function(connection) {
					return mongo.db('live').collection('providers').findOne({
						_id: connection.provider_id
					})
						.then(function(provider) {
							if (provider == null) {
								return Promise.reject(new Error('Connection' + connectionId.toString('hex') + 'has an invalid Provider with ID ' + connection.provider_id.toString('hex') + '.'));
							}

							return bitscoop.getMap(provider.remote_map_id.toString('hex'))
								.then(function(remoteProvider) {
									remoteProvider = _.omit(remoteProvider, ['id', 'auth']);

									_.assign(provider, remoteProvider);

									_.assign(connection, {
										provider: provider
									});

									return Promise.resolve(connection);
								});
						});
				})
				.then(function(connection) {
					return mongo.db('live').collection('connections').updateOne({
						_id: connection._id
					}, {
						$set: {
							status: 'running'
						}
					})
						.then(function() {
							return Promise.resolve(connection);
						});
				})
				.then(function(connection) {
					let api = new bitscoop.api(connection.provider.remote_map_id);

					let promises = _.map(connection.permissions, function(permission, name) {
						if (permission.enabled) {
							let source = new sources.Source(connection.provider.sources[name], connection, api);

							source.parse = require('./sources/' + connection.provider_name.toLowerCase() + '/' + name.toLowerCase());

							return source.call(connection.remote_connection_id.toString('hex'))
								.then(function(data) {
									return source.parse(data);
								});
						}
						else {
							return Promise.resolve();
						}
					});

					return Promise.all(promises)
						.then(function() {
							return mongo.db('live').collection('connections').updateOne({
								_id: connection._id
							}, {
								$set: {
									last_run: moment.utc().toDate(),
									status: 'ready'
								}
							});
						});
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
