'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const express = require('express');
const httpErrors = require('http-errors');

const callApi = require('explorer/lib/util/call-api');
const csrf = require('explorer/lib/middleware/csrf');
const gid = require('explorer/lib/util/gid');
const hmac = require('explorer/lib/util/hmac');
const loginRequired = require('explorer/lib/middleware/login-required');


let router = express.Router();
let complete = router.route('/complete');
let connection = router.route('/:id');
let connections = router.route('/');


function completeConnection(req, res, next) {
	let mongo = env.databases.mongo;

	Promise.all([
		mongo.db('explorer').collection('connections').findOne({
			remote_connection_id: gid(req.body.connection_id)
		}),

		mongo.db('explorer').collection('providers').findOne({
			remote_provider_id: gid(req.body.provider_id)
		})
	])
		.spread(function(connection, provider) {
			if (!connection || !provider) {
				return Promise.reject(httpErrors(404));
			}

			let path = 'providers/' + req.body.provider_id;

			return callApi(path, 'GET')
				.then(function(remoteProvider) {
					let merged = _.assign(provider, remoteProvider);

					connection.provider = merged;

					return Promise.resolve(connection);
				});
		})
		.then(function(connection) {
			let path = 'connections/' + req.body.connection_id;

			return callApi(path, 'GET')
				.then(function(remoteConnection) {
					let merged = _.assign(remoteConnection, connection);

					return Promise.resolve(merged);
				});
		})
		.then(function(connection) {
			let signature = hmac(JSON.stringify(req.body), connection.provider.webhook_secret_key.toString('hex'));

			if (signature !== req.headers['x-bitscoop-signature']) {
				return Promise.reject(httpErrors(401));
			}

			return mongo.db('explorer').collection('connections').updateOne({
				_id: connection._id
			}, {
				$set: {
					'auth.status.complete': true
				}
			});
		})
		.then(function() {
			res.sendStatus(200);
		})
		.catch(function(err) {
			next(err);
		});
}

function deleteConnection(req, res, next) {
	let mongo = env.databases.mongo;

	mongo.db('explorer').collection('providers').findOne({
		remote_provider_id: gid(req.body.provider_id)
	})
		.then(function(provider) {
			if (!provider) {
				return Promise.reject(httpErrors(404));
			}

			let signature = hmac(JSON.stringify(req.body), provider.webhook_secret_key.toString('hex'));

			if (signature !== req.headers['x-bitscoop-signature']) {
				return Promise.reject(httpErrors(401));
			}
		})
		.then(function() {
			return mongo.db('explorer').collection('connections').deleteOne({
				remote_connection_id: gid(req.body.connection_id)
			});
		})
		.then(function() {
			res.sendStatus(200);
		})
		.catch(function(err) {
			next(err);
		});
}

function reauthorizeConnection(req, res, next) {
	let mongo = env.databases.mongo;

	Promise.all([
		mongo.db('explorer').collection('connections').findOne({
			remote_connection_id: gid(req.body.connection_id)
		}),

		mongo.db('explorer').collection('providers').findOne({
			remote_provider_id: gid(req.body.provider_id)
		})
	])
		.spread(function(connection, provider) {
			if (!connection || !provider) {
				return Promise.reject(httpErrors(404));
			}

			let path = 'providers/' + req.body.provider_id;

			return callApi(path, 'GET')
				.then(function(remoteProvider) {
					let merged = _.assign(provider, remoteProvider);

					connection.provider = merged;

					return Promise.resolve(connection);
				});
		})
		.then(function(connection) {
			let path = 'connections/' + req.body.connection_id;

			return callApi(path, 'GET')
				.then(function(remoteConnection) {
					let merged = _.assign(remoteConnection, connection);

					return Promise.resolve(merged);
				});
		})
		.then(function(connection) {
			let signature = hmac(JSON.stringify(req.body), connection.provider.webhook_secret_key.toString('hex'));

			if (signature !== req.headers['x-bitscoop-signature']) {
				return Promise.reject(httpErrors(401));
			}

			return mongo.db('explorer').collection('connections').updateOne({
				_id: connection._id
			}, {
				$set: {
					'auth.status.authorized': true
				}
			});
		})
		.then(function() {
			res.sendStatus(200);
		})
		.catch(function(err) {
			next(err);
		});
}


complete.options(function(req, res, next) {
	res.setHeader('Allowed', 'DELETE,OPTIONS,POST');

	res.sendStatus(204);
});

complete.post(function(req, res, next) {
	let validate = env.validate;

	validate(req.body.event, '/types/webhook-events')
		.catch(function() {
			return Promise.reject(httpErrors(400));
		})
		.then(function() {
			return Promise.all([
				validate(req.body.connection_id, '/types/uuid4'),
				validate(req.body.provider_id, '/types/uuid4')
			])
				.catch(function() {
					return Promise.reject(httpErrors(404));
				});
		})
		.then(function() {
			if (req.body.event === 'connection_reauthorized') {
				reauthorizeConnection(req, res, next);
			}
			else if (req.body.event === 'connection_deleted') {
				deleteConnection(req, res, next);
			}
			else if (req.body.event === 'connection_created') {
				completeConnection(req, res, next);
			}
			else {
				return Promise.reject(httpErrors(400));
			}
		});
});

connection.options(function(req, res, next) {
	res.setHeader('Allowed', 'OPTIONS,PATCH');

	res.sendStatus(204);
});

connection.patch(loginRequired(404), csrf.validate, function(req, res, next) {
	let hexId = req.params.id;
	let mongo = env.databases.mongo;
	let validate = env.validate;

	validate(hexId, '/types/uuid4')
		.catch(function() {
			return Promise.reject(httpErrors(404));
		})
		.then(function() {
			return mongo.db('explorer').collection('connections').findOne({
				_id: gid(hexId),
				user_id: req.user._id
			})
				.then(function(connection) {
					if (!connection) {
						return Promise.reject(httpErrors(404));
					}

					let path = 'connections/' + connection.remote_connection_id.toString('hex');

					return callApi(path, 'GET')
						.then(function(remoteConnection) {
							let merged = _.assign(remoteConnection, connection);

							return Promise.resolve(merged);
						});
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
							let merged = _.assign(provider, remoteProvider);

							connection.provider = merged;

							return Promise.resolve(connection);
						});
				});
		})
		.then(function(connection) {
			let endpoints = [];

			_.each(connection.provider.sources, function(source, name) {
				if (connection.permissions.hasOwnProperty(name) && connection.permissions[name].enabled) {
					endpoints.push(source.mapping);
				}
			});

			endpoints = _.uniq(endpoints);

			let path = 'connections/' + connection.remote_connection_id.toString('hex');
			let body = {
				endpoints: endpoints,
				provider_id: connection.provider.remote_provider_id.toString('hex')
			};

			return callApi(path, 'PATCH', body)
				.then(function(authObj) {
					let promise = Promise.resolve();
					if (connection.auth.type === 'oauth2') {
						promise = promise.then(function() {
							let $set = {
								'auth.status.authorized': false
							};

							return mongo.db('explorer').collection('connections').updateOne({
								_id: gid(hexId),
								user_id: req.user._id
							}, {
								$set: $set
							});
						});
					}

					return promise.then(function() {
						return Promise.resolve(authObj);
					});
				});
		})
		.then(function(authObj) {
			res.json(authObj);
		})
		.catch(function(err) {
			next(err);
		});
});


connections.options(function(req, res, next) {
	res.setHeader('Allowed', 'OPTIONS,POST');

	res.sendStatus(204);
});

connections.post(loginRequired(404), csrf.validate, function(req, res, next) {
	let hexId = req.body.provider_id;
	let name = req.body.name;
	let mongo = env.databases.mongo;
	let validate = env.validate;

	Promise.all([
		validate(hexId, '/types/uuid4'),
		validate(name, '/types/string')
	])
		.catch(function() {
			return Promise.reject(httpErrors(404));
		})
		.then(function() {
			return mongo.db('explorer').collection('providers').findOne({
				_id: gid(hexId)
			})
				.then(function(provider) {
					if (!provider) {
						return Promise.reject(httpErrors(404));
					}

					let path = 'providers/' + provider.remote_provider_id.toString('hex');

					return callApi(path, 'GET')
						.then(function(remoteProvider) {
							let merged = _.assign(provider, remoteProvider);

							return Promise.resolve(merged);
						});
				});
		})
		.then(function(provider) {
			let endpoints = [];
			let connection = {
				frequency: 1,
				enabled: true,
				permissions: {},

				provider: provider,
				provider_id: provider._id
			};

			_.each(provider.sources, function(source, name) {
				if (req.body.hasOwnProperty(name)) {
					connection.permissions[name] = {
						enabled: true,
						frequency: 1
					};

					endpoints.push(source.mapping);
				}
			});

			endpoints = _.uniq(endpoints);

			let path = 'providers/' + provider.remote_provider_id.toString('hex') + '/connections';
			let body = {
				name: name,
				endpoints: _.uniq(endpoints)
			};

			return Promise.all([
				callApi(path, 'POST', body),

				Promise.resolve(connection)
			])
				.spread(function(authObj, connection) {
					return mongo.db('explorer').collection('connections').insertOne({
						_id: gid(),
						auth: {
							status: {
								complete: false
							}
						},
						frequency: 1,
						enabled: true,
						permissions: connection.permissions,
						provider_name: provider.name,
						provider_id: connection.provider_id,
						remote_connection_id: gid(authObj.id),
						user_id: req.user._id
					})
						.then(function() {
							res.redirect(authObj.redirectUrl);
						});
				});
		})

		.catch(function(err) {
			next(err);
		});
});


module.exports = router;
