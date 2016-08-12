'use strict';

const express = require('express');


let router = express.Router();


router.use('/connections', require('explorer/lib/views/api/connections'));
router.use('/providers', require('explorer/lib/views/api/providers'));
router.use('/searches', require('explorer/lib/views/api/searches'));

// Object API Endpoints
router.use('/contacts', require('explorer/lib/views/api/contacts'));
router.use('/content', require('explorer/lib/views/api/content'));
router.use('/events', require('explorer/lib/views/api/events'));
//router.use('/locations', require('explorer/lib/views/api/locations'));
//router.use('/organizations', require('explorer/lib/views/api/organizations'));
//router.use('/places', require('explorer/lib/views/api/places'));
//router.use('/things', require('explorer/lib/views/api/things'));
router.use('/tags', require('explorer/lib/views/api/tags'));


module.exports = router;
