'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const express = require('express');

const router = express.Router();
const providers = router.route('/');

const loginRequired = require('explorer/lib/middleware/login-required');


providers.options(function(req, res, next) {
	res.setHeader('Allowed', 'GET,OPTIONS');

	res.sendStatus(204);
});

providers.get(loginRequired(404), function(req, res, next) {
	res.context.page_name = 'providers';

	let mongo = env.databases.mongo;

	let mergedProviders = mongo.db('explorer').collection('providers').find({
		enabled: true
	}).toArray()
		.then(function(results) {
			let promises = _.map(results, function(provider) {
				return mongo.db('bitscoop').collection('providers').findOne({
					_id: provider.provider_id
				})
					.then(function(remoteProvider) {
						let merged = _.assign(provider, remoteProvider);

						return Promise.resolve(merged);
					});
			});

			return Promise.all(promises);
		});

	let connections = mongo.db('bitscoop').collection('connections').find({
		user_id: req.user._id
	}).toArray();

	Promise.all([
		mergedProviders,
		connections
	])
		.spread(function(providers, connections) {
			_.forEach(providers, function(provider) {
				provider.assoc_count = 0;

				_.forEach(connections, function(connection) {
					if (provider._id.toString('hex') === connection.provider_id.toString('hex') && connection.auth_status.complete === true) {
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
});


module.exports = router;
