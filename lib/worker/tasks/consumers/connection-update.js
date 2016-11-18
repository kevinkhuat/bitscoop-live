'use strict';

const Pool = require('poolq').Pool;
const Promise = require('bluebird');
const Queue = require('poolq').Queue;
const _ = require('lodash');
const config = require('config');
const moment = require('moment');

const callApi = require('explorer/lib/util/call-api');
const gid = require('explorer/lib/util/gid');
const sources = require('explorer/lib/worker/sources');


let queue = new Queue({
	cache: config.caches.jobs.address,
	stream: 'connection'
});

let pool = new Pool({
	max: 2
});

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
	queue.length()
		.then(function(n) {
			if (n === 0) {
				env.logger.debug('Job queue empty.');

				return Promise.resolve();
			}

			while (pool.count < pool.max) {
				let acquisition = pool.acquire();
				let task = queue.dequeue();

				acquisition.then(function() {
					env.logger.debug('Acquired work slot.');
				});

				task.then(function(job) {
					if (!job) {
						env.logger.debug('No available job.');
					}
				});

				Promise.all([acquisition, task])
					.spread(function(slot, job) {
						if (job) {
							env.logger.info('Processing connection update job ' + job.id + '.');

							return updateSources(job.data.connectionId)
								.then(function() {
									env.logger.info('Processed connection update job ' + job.id + '.');

									return job.done();
								});
						}
					})
					.catch(function(err) {
						let job = task.isFulfilled() ? task.value() : null;

						if (job) {
							let connection = _.get(err, 'data.connection', null);

							if (connection) {
								connection = {
									id: connection._id.toString('hex'),
									name: connection.name,
									provider: {
										id: connection.provider._id.toString('hex'),
										name: connection.provider.name
									}
								};
							}

							let logObj = {
								connection: connection,
								source: _.get(err, 'data.source', null),
								endpoint: _.get(err, 'data.endpoint', null)
							};

							if (err && err.code === 'ETIMEDOUT') {
								env.logger.info('Timed out job will be re-queued.', logObj);

								return job.done();
							}
							else {
								env.logger.error('Processing failed for connection update job ' + job.id + '.', err, logObj);
							}
						}
						else {
							env.logger.error(err);
						}
					})
					.then(function() {
						if (acquisition.isFulfilled()) {
							let slot = acquisition.value();

							pool.release(slot);

							env.logger.debug('Released work slot.');
						}
					});
			}
		})
		.catch(function(err) {
			env.logger.error(err);
		});
};
