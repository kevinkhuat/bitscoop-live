'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const express = require('express');
const httpErrors = require('http-errors');
const moment = require('moment');
const type = require('type-detect');

const csrf = require('explorer/lib/middleware/csrf');
const deleteConnection = require('explorer/lib/util/delete-connection');
const gid = require('explorer/lib/util/gid');
const initializeEndpointData = require('explorer/lib/util/initialize-endpoint-data');
const loginRequired = require('explorer/lib/middleware/login-required');
const models = require('explorer/lib/models');


let router = express.Router();
let connection = router.route('/:id');
let connections = router.route('/');


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
			return mongo.db('bitscoop').collection('connections').findOne({
				_id: gid(hexId),
				user_id: req.user._id
			});
		})
		.then(function(connection) {
			if (!connection) {
				return Promise.reject(httpErrors(404));
			}

			return mongo.db('bitscoop').collection('providers').findOne({
				_id: connection.provider_id
			})
				.then(function(provider) {
					if (!provider) {
						return Promise.reject(httpErrors(404));
					}

					connection.provider = provider;

					return Promise.resolve(connection);
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
			return mongo.db('bitscoop').collection('connections').findOne({
				_id: gid(hexId),
				user_id: req.user._id
			});
		})
		.then(function(connection) {
			if (!connection) {
				return Promise.reject(httpErrors(404));
			}

			return mongo.db('explorer').collection('providers').findOne({
				provider_id: connection.provider_id
			})
				.then(function(provider) {
					if (!provider) {
						return Promise.reject(httpErrors(404));
					}

					return mongo.db('bitscoop').collection('providers').findOne({
						_id: provider.provider_id
					})
						.then(function(remoteProvider) {
							if (!remoteProvider) {
								return Promise.reject(httpErrors(404));
							}

							connection.provider = _.assign(provider, remoteProvider);

							return Promise.resolve(connection);
						});
				});
		})
		.then(function(connection) {
			if (req.body.name) {
				connection.name = req.body.name;
			}

			if ('enabled' in req.body) {
				connection.enabled = req.body.enabled;
			}

			let sourcesUpdated = false;

			_.each(sources, function(value, name) {
				if (!connection.permissions.hasOwnProperty(name)) {
					connection.permissions[name] = {
						enabled: value,
						frequency: 1
					};

					initializeEndpointData(connection.provider, connection, name);

					if (value === true) {
						sourcesUpdated = true;
					}
				}
				else if (value !== connection.permissions[name].enabled) {
					connection.permissions[name].enabled = value;
					sourcesUpdated = true;
				}
			});

			if (sourcesUpdated && connection.provider.auth_type === 'oauth2') {
				connection.auth_status.authorized = false;
			}

			let scopes = [];

			_.each(connection.provider.sources, function(source, name) {
				if (connection.permissions.hasOwnProperty(name) && connection.permissions[name].enabled && Array.isArray(source.scopes)) {
					Array.prototype.push.apply(scopes, source.scopes);
				}
			});

			if (connection.provider.auth.scopes) {
				if (Array.isArray(connection.provider.auth.scopes)) {
					Array.prototype.push.apply(scopes, connection.provider.auth.scopes);
				}
			}

			connection.scopes = _.uniq(scopes);
			connection.updated = moment.utc().toDate();

			return mongo.db('bitscoop').collection('connections').updateOne({
				_id: connection._id
			}, {
				$set: connection
			})
				.then(function() {
					return Promise.resolve(connection);
				});
		})
		.then(function(connection) {
			res.json({
				reauthorize: _.get(connection, 'auth_status.authorized', null) === false
			});
		})
		.catch(function(err) {
			next(err);
		});
});


connections.options(function(req, res, next) {
	res.setHeader('Allowed', 'GET,OPTIONS');

	res.sendStatus(204);
});

connections.get(loginRequired(404), function(req, res, next) {
	let mongo = env.databases.mongo;

	mongo.db('bitscoop').collection('connections').find({
		user_id: req.user._id,
		'auth_status.complete': true
	}).toArray()
		.then(function(connections) {
			let providerList = [];

			_.each(connections, function(connection) {
				providerList.push(connection.provider_id);
			});

			return mongo.db('explorer').collection('providers').find({
				provider_id: {
					$in: providerList
				}
			}).toArray()
				.then(function(providers) {
					let promises = _.map(providers, function(provider) {
						return mongo.db('bitscoop').collection('providers').findOne({
							_id: provider.provider_id
						})
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


module.exports = router;
