'use strict';

const express = require('express');

let router = express.Router();
let logout = router.route('/');

logout.get(function(req, res, next) {
    // TODO - update logout.html
    res.render('logout.html', {
        page_name: 'logout',
        mode: 'logout'
    });
});

logout.post(function(req, res, next) {

});

module.exports = router;
