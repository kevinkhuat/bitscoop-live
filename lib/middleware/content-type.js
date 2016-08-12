'use strict';

const httpErrors = require('http-errors');


let defaultTypes = ['application/json', 'text/html'];


module.exports = function(types) {
	if (arguments.length === 0) {
		types = defaultTypes;
	}

	return function(req, res, next) {
		let contentType = req.accepts(types);

		if (contentType === false) {
			let error = httpErrors(406);

			next(error);
		}
		else {
			req.contentType = contentType;

			next();
		}
	};
};
