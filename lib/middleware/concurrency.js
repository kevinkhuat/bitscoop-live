'use strict';

const Pool = require('poolq').Pool;
const onHeaders = require('on-headers');


module.exports = function(count) {
	if (count === -1) {
		return function(req, res, next) {
			next();
		};
	}

	let pool = new Pool({
		max: count
	});

	return function(req, res, next) {
		pool.acquire()
			.then(function(slot) {
				onHeaders(res, function() {
					pool.release(slot);
				});

				next();

				return null;
			});
	};
};
