'use strict';

const express = require('express');


let router = express.Router();


router.use('/api', require('./views/api'));
router.use('/connections', require('./views/connections'));
router.use('/explore', require('./views/explore'));
router.use('/providers', require('./views/providers'));
router.use('/settings', require('./views/settings'));
router.use('/start', require('./views/start'));

router.use('/health', function(req, res, next) {
	res.sendStatus(204);
});

if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
	router.use('/errors', require('./views/errors'));
}

router.use('/$', require('./views/home'));


module.exports = router;
