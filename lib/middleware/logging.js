'use strict';

const format = require('string-format');
const onHeaders = require('on-headers');


module.exports = function(logger) {
	return function middleware(req, res, next) {
		let start = new Date();

		logger.debug(format('Request from {0}: {1} {2}', req.realIp, req.method, req.originalUrl));

		onHeaders(res, function onResponse() {
			let duration = new Date() - start;
			let location = res.get('location');

			if (location) {
				logger.debug(format('Response with status {0} in {1} ms. Location: {2}', res.statusCode, duration, location));
			}
			else {
				logger.debug(format('Response with status {0} in {1} ms.', res.statusCode, duration));
			}
		});

		next();
	};
};
