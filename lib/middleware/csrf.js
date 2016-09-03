'use strict';

const Promise = require('bluebird');
const Tokens = require('csrf');
const _ = require('lodash');
const config = require('config');
const httpErrors = require('http-errors');


let options = _.pick(config.csrf, ['saltLength', 'secretLength']);
let tokens = new Tokens(options);


function create(req, res, next) {
	if (req.session && req.session.csrf_secret) {
		let token = tokens.create(req.session.csrf_secret);

		if (!req.cookies[config.csrf.cookieName]) {
			res.cookie(config.csrf.cookieName, token, {
				domain: config.csrf.domain,
				secure: true,
				expires: 0
			});
		}

		res.context.csrf_token = token;
	}

	next();
}

function validate(req, res, next) {
	Promise.resolve()
		.then(function() {
			if (!req.session) {
				return Promise.reject(httpErrors(403, 'Missing session for CSRF validation.'));
			}

			if (!req.session.csrf_secret) {
				return Promise.reject(httpErrors(403, 'Missing CSRF secret for CSRF validation.'));
			}

			let csrftoken = (req.body && req.body.csrftoken) ||
				(req.query && req.query.csrftoken) ||
				(req.headers['x-csrftoken']) ||
				(req.headers['csrf-token']) ||
				(req.headers['xsrf-token']) ||
				(req.headers['x-csrf-token']) ||
				(req.headers['x-xsrf-token']);

			if (!tokens.verify(req.session.csrf_secret, csrftoken)) {
				return Promise.reject(httpErrors(403, 'Invalid CSRF token.'));
			}
		})
		.then(function() {
			next();
		})
		.catch(function(err) {
			next(err);
		});
}


module.exports = {
	create: create,
	validate: validate
};
