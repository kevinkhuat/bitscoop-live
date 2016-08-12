'use strict';

const express = require('express');


let router = express.Router();


router.use('/connections', require('explorer/lib/views/settings/connections'));

router.use('/$', function(req, res, next) {
	res.redirect('/settings/connections');
});


module.exports = router;
