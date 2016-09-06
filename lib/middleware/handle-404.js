'use strict';


module.exports = function(req, res, next) {
	res.status(404);
	res.render('errors/404.html', {
		code: 404,
		message: 'Page not found.'
	});
};
