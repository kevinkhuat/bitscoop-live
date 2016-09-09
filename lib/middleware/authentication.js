'use strict';

const Promise = require('bluebird');
const config = require('config');
const moment = require('moment');

const gid = require('explorer/lib/util/gid');


function getSession(req) {
	let redis = env.caches.sessions;
	let sessionid = req.cookies.sessionid;

	return redis.multi()
		.get(sessionid)
		.ttl(sessionid)
		.exec()
		.then(function(results) {
			let data = results[0][1];
			let delta = results[1][1];

			if (!data) {
				return Promise.resolve(null);
			}

			let session = JSON.parse(data);

			if (session.user_id) {
				session.user_id = gid(session.user_id);
			}

			session.token = sessionid;
			session.expires = moment.utc().add(delta, 'seconds').toDate();

			return Promise.resolve(session);
		});
}


module.exports = function(req, res, next) {
	let mongo = env.databases.mongo;

	if (!req.cookies.cookieconsent) {
		if (req.cookies.csrftoken) {
			res.clearCookie(config.csrf.cookieName, {
				domain: config.csrf.domain,
				secure: true,
				httpOnly: true
			});
		}

		if (req.cookies.sessionid) {
			res.clearCookie(config.sessions.cookieName, {
				domain: config.sessions.domain,
				secure: true,
				httpOnly: true
			});
		}

		next();
	}
	else {
		getSession(req)
			.then(function(session) {
				if (session && session.user_id) {
					return mongo.db('bitscoop').collection('users').findOne({
							_id: session.user_id
						}, {
							password: false
						})
						.then(function(user) {
							return Promise.resolve([session, user]);
						});
				}

				return Promise.resolve([session, null]);
			})
			.then(function(data) {
				req.session = data[0] || null;
				req.user = data[1] || null;

				next();
			})
			.catch(function(err) {
				next(err);
			});
	}
};
