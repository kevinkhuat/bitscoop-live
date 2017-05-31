'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const config = require('config');
const moment = require('moment');

const callApi = require('explorer/lib/util/call-api');
const gid = require('explorer/lib/util/gid');
const sources = require('explorer/lib/worker/sources');


function updateSources(connectionId) {
	let mongo = env.databases.mongo;

	// Get sources for connection, run them, then return a promise when they're all done (or reject if some fail).
	// Need to hydrate provider to get its name.
	return mongo.db('explorer').collection('connections').findOne({
		_id: gid(connectionId)
	})
		.then(function(connection) {
			if (!connection) {
				return Promise.reject(new Error({
					data: {
						connection: {
							logCopy: null
						},
						source: null,
						endpoint: null
					}
				}));
			}

			return callApi('connections/' + connection.remote_connection_id.toString('hex'), 'GET')
				.then(function(remoteConnection) {
					remoteConnection = _.omit(remoteConnection, ['id', 'auth', 'provider_id']);

					_.assign(connection, remoteConnection);

					return Promise.resolve(connection);
				});
		})
		.then(function(connection) {
			return mongo.db('explorer').collection('providers').findOne({
				_id: connection.provider_id
			})
				.then(function(provider) {
					if (provider == null) {
						return Promise.reject(new Error({
							data: {
								connection: {
									logCopy: null
								},
								source: null,
								endpoint: null
							}
						}));
					}

					return callApi('providers/' + provider.remote_provider_id.toString('hex'), 'GET')
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
			let promises = _.map(connection.permissions, function(permission, name) {
				if (permission.enabled) {
					let source = new sources.Source(connection.provider.sources[name], connection);

					source.parse = require('explorer/lib/worker/sources/' + connection.provider_name.toLowerCase() + '/' + name.toLowerCase());

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
					return mongo.db('explorer').collection('connections').updateOne({
						_id: connection._id
					}, {
						$set: {
							last_run: moment.utc().toDate()
						}
					});
				});
		});
}


module.exports = function() {
	// TODO - Remove Queue. Need to replace with AWS Lambda
	// Previous code checked for job status
};
