'use strict';

const Promise = require('bluebird');
const Tokens = require('csrf');
const _ = require('lodash');
const config = require('config');
const moment = require('moment');

const csrf = require('explorer/lib/middleware/csrf');
const gid = require('explorer/lib/util/gid');


let options = _.pick(config.csrf, ['saltLength', 'secretLength']);
let tokens = new Tokens(options);


function getSession(sessionid) {
	let redis = env.caches.sessions;

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
		let mongo = env.databases.mongo;
		let sessionid = req.cookies.sessionid;

		getSession(sessionid)
			.then(function(session) {
				if (!session) {
					let data = {
						ip: req.realIp,
						agent: req.headers['user-agent']
					};

					return env.rpc.accounts.call('createSession', [data])
						.then(function(result) {
							res.cookie(result.name, result.value, result.options);

							return getSession(result.value);
						});
				}

				return Promise.resolve(session);
			})
			.then(function(session) {
				let tokenValid = tokens.verify(session.csrf_secret, req.cookies[config.csrf.cookieName]);

				if (!req.cookies[config.csrf.cookieName] || !tokenValid) {
					delete req.cookies[config.csrf.cookieName];
					req.session = session;

					return new Promise(function(resolve, reject) {
						function innerNext(err) {
							if (err) {
								reject(err);
							}
							else {
								resolve(session);
							}
						}

						csrf.create(req, res, innerNext);
					});
				}

				return Promise.resolve(session);
			})
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
