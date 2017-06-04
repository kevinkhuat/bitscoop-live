'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const express = require('express');

const callApi = require('../util/call-api');

let router = express.Router();
let home = router.route('/');


home.options(function(req, res, next) {
	res.setHeader('Allowed', 'GET,OPTIONS');

	res.sendStatus(204);
});

home.get(function(req, res, next) {
    if (req.user == null) {
		res.redirect(req.hostname);
	}
	else {
		let mongo = env.databases.mongo;

		Promise.all([
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

					return Promise.resolve(completedConnections.length);
				}),

			mongo.db('explorer').collection('events').find({
				user_id: req.user._id
			}).count(),

			mongo.db('explorer').collection('searches').find({
				user_id: req.user._id
			}).count()
		])
			.spread(function(connectionCount, eventCount, searchCount) {
				res.render('home.html', {
					counts: {
						connections: connectionCount,
						events: eventCount,
						searches: searchCount
					},
					page_name: 'home',
					mode: 'home'
				});
			})
			.catch(function(err) {
				next(err);
			});
	}
});


module.exports = router;
