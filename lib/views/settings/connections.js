'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const express = require('express');
const httpErrors = require('http-errors');
const type = require('type-detect');

const callApi = require('../../util/call-api');
const csrf = require('../../middleware/csrf');
const deleteConnection = require('../../util/delete-connection');
const gid = require('../../util/gid');
const loginRequired = require('../../middleware/login-required');
const models = require('../../models');


let router = express.Router();
let connections = router.route('/');
let connection = router.route('/:id');


connections.options(function(req, res, next) {
	res.setHeader('Allowed', 'GET,OPTIONS');

	res.sendStatus(204);
});

connections.get(loginRequired(404), function(req, res, next) {
	let mongo = env.databases.mongo;

	// Return markup to avoid querying the database
    res.render('settings/connections.html', {
        title: 'Connection Settings',
        connections: [],
        settings_type: 'Connections',
        mode: 'home',
        page_name: 'settings connections',
        hide_advanced: true
    });

    // TODO - Discuss what needs to be changed
	mongo.db('explorer').collection('connections').find({
		user_id: req.user._id
	}).toArray()
		.then(function(connections) {
			let promises = _.map(connections, function(connection) {
				let path = 'connections/' + connection.remote_connection_id.toString('hex');

				return callApi(path, 'GET')
					.then(function(remoteConnection) {
						let merged = _.assign(remoteConnection, connection);

						return Promise.resolve(merged);
					});
			});

			return Promise.all(promises);
		})
		.then(function(connections) {
			let completedConnections = _.filter(connections, function(connection) {
				return connection.auth.status.complete === true;
			});

			return Promise.resolve(completedConnections);
		})
		.then(function(connections) {
			let providerList = [];

			_.each(connections, function(connection) {
				providerList.push(connection.provider_id);
			});

			return mongo.db('explorer').collection('providers').find({
				_id: {
					$in: providerList
				}
			}).toArray()
				.then(function(providers) {
					let promises = _.map(providers, function(provider) {
						let path = 'providers/' + provider.remote_provider_id.toString('hex');

						return callApi(path, 'GET')
							.then(function(remoteProvider) {
								let merged = _.assign(provider, remoteProvider);

								return Promise.resolve(merged);
							});
					});

					return Promise.all(promises);
				})
				.then(function(providers) {
					_.each(connections, function(connection) {
						connection.provider = _.find(providers, function(provider) {
							return provider._id.toString('hex') === connection.provider_id.toString('hex');
						});

						if (connection.provider == null) {
							return Promise.resolve(httpErrors(404));
						}
					});

					return Promise.resolve(connections);
				});
		})
		.then(function(connections) {
			let connectionData = [];

			_.forEach(connections, function(connection) {
				let permissions = [];
				let newConnection = new models.Connection(connection);

				// On the connection settings page, we need to show all of the available permissions, not just the
				// permissions that the connection knows about.  If a user initially did not give access to a permission,
				// it does not appear at all on the connection.  We need to get the permissions from the Provider
				// and overwrite the connection's list of permissions.
				_.each(connection.provider.sources, function(source, name) {
					permissions.push({
						name: name,
						source: source,
						enabled: name in connection.permissions && connection.permissions[name].enabled === true
					});
				});

				newConnection.permissions = permissions;

				connectionData.push(newConnection);
			});

			res.render('settings/connections.html', {
				title: 'Connection Settings',
				connections: connectionData,
				settings_type: 'Connections',
				mode: 'home',
				page_name: 'settings connections',
				hide_advanced: true
			});
		});
});


connection.options(function(req, res, next) {
	res.setHeader('Allowed', 'DELETE,OPTIONS,PATCH');

	res.sendStatus(204);
});

connection.delete(loginRequired(404), csrf.validate, function(req, res, next) {
	let mongo = env.databases.mongo;
	let hexId = req.params.id;
	let validate = env.validate;

	validate(hexId, '/types/uuid4')
		.catch(function() {
			return Promise.reject(httpErrors(404));
		})
		.then(function() {
			return mongo.db('explorer').collection('connections').findOne({
				_id: gid(hexId),
				user_id: req.user._id
			});
		})
		.then(function(connection) {
			if (!connection) {
				return Promise.reject(httpErrors(404));
			}

			let path = 'connections/' + connection.remote_connection_id.toString('hex');

			return callApi(path, 'GET')
				.then(function(remoteConnection) {
					if (!connection) {
						return Promise.reject(httpErrors(404));
					}

					let merged = _.assign(remoteConnection, connection);

					return Promise.resolve(merged);
				});
		})
		.then(function() {
			return deleteConnection(hexId, req.user._id);
		})
		.then(function() {
			res.sendStatus(204);
		})
		.catch(function(err) {
			next(err);
		});
});

connection.patch(loginRequired(404), csrf.validate, function(req, res, next) {
	let mongo = env.databases.mongo;
	let sources = req.body.sources;
	let hexId = req.params.id;
	let validate = env.validate;

	if (sources) {
		_.each(sources, function(enabled, source) {
			if (type(enabled) !== 'boolean') {
				next(new httpErrors(400));
			}
		});
	}

	validate(hexId, '/types/uuid4')
		.catch(function() {
			return Promise.reject(httpErrors(404));
		})
		.then(function() {
			return mongo.db('explorer').collection('connections').findOne({
				_id: gid(hexId),
				user_id: req.user._id
			});
		})
		.then(function(connection) {
			if (!connection) {
				return Promise.reject(httpErrors(404));
			}

			let path = 'connections/' + connection.remote_connection_id.toString('hex');

			return callApi(path, 'GET')
				.then(function(remoteConnection) {
					if (!remoteConnection) {
						return Promise.reject(httpErrors(404));
					}

					let merged = _.assign(remoteConnection, connection);

					return Promise.resolve(merged);
				});
		})
		.then(function(connection) {
			return mongo.db('explorer').collection('providers').findOne({
				_id: connection.provider_id
			})
				.then(function(provider) {
					if (!provider) {
						return Promise.reject(httpErrors(404));
					}

					let path = 'providers/' + provider.remote_provider_id.toString('hex');

					return callApi(path, 'GET')
						.then(function(remoteProvider) {
							if (!remoteProvider) {
								return Promise.reject(httpErrors(404));
							}

							connection.provider = _.assign(remoteProvider, provider);

							return Promise.resolve(connection);
						});
				});
		})
		.then(function(connection) {
			let bitscoopConnection = {
				provider_id: connection.provider_id.toString('hex')
			};

			let explorerConnection = {
				permissions: _.cloneDeep(connection.permissions)
			};

			if (req.body.name) {
				bitscoopConnection.name = req.body.name;
			}

			if ('enabled' in req.body) {
				explorerConnection.enabled = req.body.enabled;
			}

			let sourcesUpdated = false;

			_.each(sources, function(value, name) {
				if (!connection.permissions.hasOwnProperty(name)) {
					explorerConnection.permissions[name] = {
						enabled: value,
						frequency: 1
					};

					if (value === true) {
						sourcesUpdated = true;
					}
				}
				else if (value !== connection.permissions[name].enabled) {
					explorerConnection.permissions[name].enabled = value;
					sourcesUpdated = true;
				}
			});

			if (sourcesUpdated && connection.provider.auth.type === 'oauth2') {
				explorerConnection['auth.status.authorized'] = false;
			}

			let endpoints = [];

			_.each(connection.provider.sources, function(source, name) {
				if (req.body.sources.hasOwnProperty(name)) {
					connection.permissions[name] = {
						enabled: true,
						frequency: 1
					};

					endpoints.push(source.mapping);
				}
			});

			endpoints = _.uniq(endpoints);

			bitscoopConnection.endpoints = _.uniq(endpoints);

			let path = 'connections/' + connection.remote_connection_id.toString('hex');

			return Promise.all([
				mongo.db('explorer').collection('connections').updateOne({
					_id: connection._id
				}, {
					$set: explorerConnection
				}),

				callApi(path, 'PATCH', bitscoopConnection)
			])
				.then(function() {
					return Promise.resolve(explorerConnection);
				});
		})
		.then(function(connection) {
			res.json({
				reauthorize: _.get(connection, 'auth.status.authorized', null) === false
			});
		})
		.catch(function(err) {
			next(err);
		});
});


module.exports = router;
