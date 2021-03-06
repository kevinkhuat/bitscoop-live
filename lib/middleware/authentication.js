'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const config = require('config');
const moment = require('moment');


let $lookup = {
	$lookup: {
		from: 'users',
		localField: 'user_id',
		foreignField: '_id',
		as: 'users'
	}
};

let $project = {
	$project: {
		_id: false,
		token: true,
		csrf_secret: true,
		expires: true,
		'users._id': true,
		'users.handle': true,
		'users.email': true,
		'users.last_name': true,
		'users.first_name': true,
		'users.last_login': true,
		'users.settings': true
	}
};


module.exports = function(req, res, next) {
	let mongo = env.databases.mongo;

	let sessionid = config.sessions.cookieName;
	let cookieConsent = config.cookieConsent;

	if (!req.cookies[cookieConsent]) {
		if (req.cookies[sessionid]) {
			res.clearCookie(sessionid, {
				domain: config.sessions.domain,
				secure: true,
				httpOnly: true
			});
		}

		next();
	}
	else {
		let $match = {
			$match: {
				token: req.cookies[sessionid],
				expires: {
					$gt: moment.utc().toDate()
				},
				logout: null
			}
		};

		mongo.db('bitscoop').collection('sessions').aggregate([$match, $lookup, $project]).toArray()
			.then(function(sessions) {
				if (sessions.length > 1) {
					return Promise.reject(new Error('Duplicate session.'));
				}

				if (sessions.length === 0) {
					req.session = null;
				}
				else {
					let session = _.omit(sessions[0], 'users');
					let user = sessions[0].users[0];

					req.session = session;
					req.user = user || null;
				}

				next();
			})
			.catch(function(err) {
				next(err);
			});
	}
};
