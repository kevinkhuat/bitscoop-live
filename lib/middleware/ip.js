'use strict';


module.exports = function(req, res, next) {
	let xff = req.get('x-forwarded-for');

	req.realIp = req.ip;

	if (xff) {
		let ips = xff.split(',').map(function(ip) {
			return ip.trim();
		});

		let ip = ips[0];

		if (ip) {
			req.realIp = ip;
		}
	}

	next();
};
