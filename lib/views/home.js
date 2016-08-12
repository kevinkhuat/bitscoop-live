'use strict';

const Promise = require('bluebird');
const express = require('express');


let router = express.Router();
let home = router.route('/');


home.options(function(req, res, next) {
	res.setHeader('Allowed', 'GET,OPTIONS');

	res.sendStatus(204);
});

home.get(function(req, res, next) {
	if (req.user == null) {
		res.redirect('https://bitscoop.com');
	}
	else {
		let mongo = env.databases.mongo;

		Promise.all([
			mongo.db('bitscoop').collection('connections').find({
				user_id: req.user._id,
				'auth_status.complete': true
			}).count(),

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
