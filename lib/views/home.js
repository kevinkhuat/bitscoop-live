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
	console.log(req.user);
	console.log(req.hostname);
    if (req.user == null) {
		res.redirect('/');
	}
	else {
		let mongo = env.databases.mongo;

		Promise.all([
			mongo.db('live').collection('connections').find({
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

			mongo.db('live').collection('events').find({
				user_id: req.user._id
			}).count(),

			mongo.db('live').collection('searches').find({
				user_id: req.user._id
			}).count()
		])
			.then(function(result) {
				let [connectionCount, eventCount, searchCount] = result;

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
