'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const express = require('express');
const httpErrors = require('http-errors');

const callApi = require('explorer/lib/util/call-api');
const gid = require('explorer/lib/util/gid');
const loginRequired = require('explorer/lib/middleware/login-required');
const models = require('explorer/lib/models');


let router = express.Router();
let provider = router.route('/:id');
let providers = router.route('/');


provider.options(function(req, res, next) {
	res.setHeader('Allowed', 'GET,OPTIONS');

	res.sendStatus(204);
});

provider.get(loginRequired(404), function(req, res, next) {
	let hexId = req.params.id;
	let mongo = env.databases.mongo;
	let validate = env.validate;

	return validate(hexId, '/types/uuid4')
		.catch(function() {
			return Promise.reject(httpErrors(404));
		})
		.then(function() {
			return mongo.db('explorer').collection('providers').findOne({
				_id: gid(hexId)
			});
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
		})
		.then(function(document) {
			if (document == null) {
				return Promise.reject(httpErrors(404));
			}

			let response = new models.Provider(document);

			return Promise.resolve(response);
		})
		.then(function(response) {
			res.json(response);
		})
		.catch(function(err) {
			next(err);
		});
});


providers.options(function(req, res, next) {
	res.setHeader('Allowed', 'GET,OPTIONS');

	res.sendStatus(204);
});

providers.get(loginRequired(404), function(req, res, next) {
	let mongo = env.databases.mongo;

	return mongo.db('explorer').collection('providers').find({}).toArray()
		.then(function(results) {
			let promises = _.map(results, function(provider) {
				let path = 'providers/' + provider.remote_provider_id.toString('hex');

				return callApi(path, 'GET')
					.then(function(remoteProvider) {
						let merged = _.assign(provider, remoteProvider);

						return Promise.resolve(merged);
					});
			});

			return Promise.all(promises);
		})
		.then(function(documents) {
			let response = _.map(documents, models.Provider.create);

			return Promise.resolve(response);
		})
		.then(function(response) {
			res.json(response);
		})
		.catch(function(err) {
			next(err);
		});
});


module.exports = router;
