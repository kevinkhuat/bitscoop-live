'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const express = require('express');
const httpErrors = require('http-errors');
const moment = require('moment');

const csrf = require('explorer/lib/middleware/csrf');
const gid = require('explorer/lib/util/gid');
const initializeEndpointData = require('explorer/lib/util/initialize-endpoint-data');
const loginRequired = require('explorer/lib/middleware/login-required');


let router = express.Router();
let connections = router.route('/');


connections.options(function(req, res, next) {
	res.setHeader('Allowed', 'OPTIONS,POST');

	res.sendStatus(204);
});

connections.post(loginRequired(404), csrf.validate, function(req, res, next) {
	let hexId = req.body.provider_id;
	let name = req.body.name;
	let mongo = env.databases.mongo;
	let validate = env.validate;

	return Promise.all([
		validate(hexId, '/types/uuid4'),
		validate(name, '/types/string')
	])
		.catch(function() {
			return Promise.reject(httpErrors(404));
		})
		.then(function() {
			return mongo.db('explorer').collection('providers').findOne({
				provider_id: gid(hexId),
				// TODO: Better controls on visibility.
				enabled: true
			})
				.then(function(provider) {
					return mongo.db('bitscoop').collection('providers').findOne({
						_id: provider.provider_id
					})
						.then(function(remoteProvider) {
							let merged = _.assign(provider, remoteProvider);

							return Promise.resolve(merged);
						});
				});
		})
		.then(function(provider) {
			let scopes = [];
			let connection = {
				auth_status: {
					complete: false
				},
				endpoint_data: {},
				frequency: 1,
				name: name,
				enabled: true,
				permissions: {},
				metadata: {},

				provider_id: provider._id
			};

			_.each(provider.sources, function(source, name) {
				if (req.body.hasOwnProperty(name)) {
					connection.permissions[name] = {
						enabled: true,
						frequency: 1
					};

					if (Array.isArray(source.scopes)) {
						Array.prototype.push.apply(scopes, source.scopes);
					}

					initializeEndpointData(provider, connection, name);
				}
			});

			if (provider.auth.scopes) {
				if (Array.isArray(provider.auth.scopes)) {
					Array.prototype.push.apply(scopes, provider.auth.scopes);
				}
			}

			_.assign(connection, {
				_id: gid(),
				user_id: req.user._id,
				scopes: _.uniq(scopes),
				created: moment.utc().toDate(),
				updated: moment.utc().toDate()
			});

			return mongo.db('bitscoop').collection('connections').insert(connection)
				.then(function() {
					return Promise.resolve(connection);
				});
		})
		.then(function(connection) {
			res.redirect('https://account.bitscoop.com/associate/' + connection._id.toString('hex'));
		})
		.catch(function(err) {
			next(err);
		});
});


module.exports = router;
