$(document).ready(function() {
    var base_framework = nunjucks.render('static/core/templates/main/base.html');
    $('main').html(base_framework);



});