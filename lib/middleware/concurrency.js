'use strict';

const onHeaders = require('on-headers');


module.exports = function(count) {
	if (count === -1) {
		return function(req, res, next) {
			next();
		};
	}

	return function(req, res, next) {
		// TODO - Removed poolq. Needs to be replaced by AWS Lambda
		// Previous code sets and releases pool resources
		next();
	};
};
