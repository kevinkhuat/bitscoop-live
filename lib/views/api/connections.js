'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const express = require('express');
const httpErrors = require('http-errors');

const gid = require('explorer/lib/util/gid');
const loginRequired = require('explorer/lib/middleware/login-required');
const models = require('explorer/lib/models');


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

	return validate(hexId, '/types/uuid4')
		.catch(function() {
			return Promise.reject(httpErrors(404));
		})
		.then(function() {
			return mongo.db('bitscoop').collection('connections').findOne({
				_id: gid(hexId),
				user_id: req.user._id
			});
		})
		.then(function(document) {
			if (document == null) {
				return Promise.reject(httpErrors(404));
			}

			let response = new models.Connection(document);

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

	return mongo.db('bitscoop').collection('connections').find({
		user_id: req.user._id
	}).toArray()
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
