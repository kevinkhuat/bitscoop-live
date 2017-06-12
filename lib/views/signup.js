'use strict';

const express = require('express');

let router = express.Router();
let signup = router.route('/');

signup.get(function(req, res, next) {
    // TODO - update signup.html
    res.render('signup.html', {
        page_name: 'signup',
        mode: 'signup'
    });
});

signup.post(function(req, res, next) {

});

module.exports = router;
