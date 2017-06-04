'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const express = require('express');

const router = express.Router();
const providers = router.route('/');

const callApi = require('../util/call-api');
const loginRequired = require('../middleware/login-required');


providers.options(function(req, res, next) {
	res.setHeader('Allowed', 'GET,OPTIONS');

	res.sendStatus(204);
});

providers.get(loginRequired(404), function(req, res, next) {
	res.context.page_name = 'providers';

	// Rendering markup first to avoid querying the database
    res.render('providers.html', {
        title: 'Providers',
        providers: [],
        mode: 'provider'
    });

    // TODO - Discuss what needs to be changed
	/*
	let mongo = env.databases.mongo;

	let mergedProviders = mongo.db('explorer').collection('providers').find({}).toArray()
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
		});

	let mergedConnections = mongo.db('explorer').collection('connections').find({
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
		});

	Promise.all([
		mergedProviders,
		mergedConnections
	])
		.spread(function(providers, connections) {
			_.forEach(providers, function(provider) {
				provider.assoc_count = 0;

				_.forEach(connections, function(connection) {
					if (provider._id.toString('hex') === connection.provider_id.toString('hex') && connection.auth.status.complete === true) {
						provider.assoc_count += 1;
					}
				});
			});

			return Promise.resolve(providers);
		})
		.then(function(providers) {
			res.render('providers.html', {
				title: 'Providers',
				providers: providers,
				mode: 'provider'
			});
		})
		.catch(function(err) {
			next(err);
		});
	*/
});


module.exports = router;
