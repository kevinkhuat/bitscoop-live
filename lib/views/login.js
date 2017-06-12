'use strict';

const express = require('express');

let router = express.Router();
let login = router.route('/');

login.get(function(req, res, next) {
    // TODO - update login.html
    res.render('login.html', {
        page_name: 'login',
        mode: 'login'
    });
});

login.post(function(req, res, next) {

});

module.exports = router;
