'use strict';

const httpErrors = require('http-errors');


module.exports = function(err, req, res, next) {
	let context, template;

	if (err instanceof httpErrors.HttpError) {
		res.status(err.status);

		context = {
			code: err.status,
			message: err.message
		};
	}
	else {
		res.status(500);

		context = {
			code: 500,
			message: 'Internal server error.'
		};
	}

	if (context.code === 500) {
		env.logger.error(err, req.meta);
	}

	switch(context.code) {
		case 400:
			template = 'errors/400.html';
			break;

		case 403:
			template = 'errors/403.html';
			break;

		case 404:
			template = 'errors/404.html';
			break;

		default:
			template = 'errors/500.html';
			break;
	}

	res.render(template, context);
};
