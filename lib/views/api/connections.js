'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const express = require('express');
const httpErrors = require('http-errors');

const callApi = require('../../util/call-api');
const gid = require('../../util/gid');
const loginRequired = require('../../middleware/login-required');
const models = require('../../models');


let router = express.Router();
let connection = router.route('/:id');
let connections = router.route('/');


connection.options(function(req, res, next) {
	res.setHeader('Allowed', 'GET,OPTIONS');

	res.sendStatus(204);
});

connection.get(loginRequired(404), function(req, res, next) {
	let hexId = req.params.id;
	let mongo = env.databases.mongo;
	let validate = env.validate;

	return validate('#/types/uuid4', hexId)
		.catch(function() {
			return Promise.reject(httpErrors(404));
		})
		.then(function() {
			return mongo.db('live').collection('connections').findOne({
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
					let merged = _.assign(remoteConnection, connection);

					return Promise.resolve(merged);
				});
		})
		.then(function(connection) {
			let response = new models.Connection(connection);

			return Promise.resolve(response);
		})
		.then(function(response) {
			res.json(response);
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

	return mongo.db('live').collection('connections').find({
		user_id: req.user._id
	}).toArray()
		.then(function(results) {
			let promises = _.map(results, function(connection) {
				let path = 'connections/' + connection.remote_connection_id.toString('hex');

				return callApi(path, 'GET')
					.then(function(remoteConnection) {
						let merged = _.assign(remoteConnection, connection);

						return Promise.resolve(merged);
					});
			});

			return Promise.all(promises);
		})
		.then(function(documents) {
			let connections = _.map(documents, models.Connection.create);

			return Promise.resolve(connections);
		})
		.then(function(response) {
			res.json(response);
		})
		.catch(function(err) {
			next(err);
		});
});


module.exports = router;
