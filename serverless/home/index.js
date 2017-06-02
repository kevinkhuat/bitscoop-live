var nunjucks = require('nunjucks');
var staticfiles = require('nunjucks-staticfiles');
var config = require('config');

exports.handler = function(event, context, callback) {
  // TODO - authenticate user. Redirect the user to the login page if they are not authenticated
  // TODO - Fetch template parameters from Mongo or Elastic Search
  var templateParameters =   {
      counts: {
          connections: 1,
          events: 2,
          searches: 3
      },
      page_name: 'home',
      mode: 'home'};

  // TODO - use helper function to set up template options
  let renderer = nunjucks.configure('templates', { autoescape: true });
  renderer.addFilter('date', require('nunjucks-date-filter'));
  renderer.addFilter('hex', require('./lib/filters/hex'));
  renderer.addFilter('is_before', require('./lib/filters/is-before'));
  renderer.addFilter('relative_time', require('./lib/filters/relative-time'));
  renderer.addFilter('slugify', require('./lib/filters/slugify'));
  // static files
  staticfiles.configure(config.staticfiles.directories, {
	nunjucks: renderer,
	path: config.staticfiles.path
  });

  // Assign markup with html return
  var markup = nunjucks.render('home.html', templateParameters);

  // Create response object to return
  const response = {
    statusCode: 200,
    headers: {
      'Content-Type': 'text/html',
    },
    body: markup
  };

  // TODO - check for errors

  // Invoke callback function to return a successful message
  callback(null, response);
}

