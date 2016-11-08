'use strict';

const express = require('express');


let router = express.Router();


router.use('/api', require('explorer/lib/views/api'));
router.use('/connections', require('explorer/lib/views/connections'));
router.use('/explore', require('explorer/lib/views/explore'));
router.use('/providers', require('explorer/lib/views/providers'));
router.use('/settings', require('explorer/lib/views/settings'));
router.use('/start', require('explorer/lib/views/start'));

router.use('/health', function(req, res, next) {
	res.sendStatus(204);
});

if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
	router.use('/errors', require('explorer/lib/views/errors'));
}

router.use('/$', require('explorer/lib/views/home'));


module.exports = router;
