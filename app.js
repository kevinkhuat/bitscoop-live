'use strict';

const Deferred = require('deferred-ap');
const Promise = require('bluebird');
const Redis = require('ioredis');
const URL = require('url-parse');
const bristolConf = require('bristol-config');
const config = require('config');
const elasticsearch = require('elasticsearch');
const express = require('express');
const mongodb = require('mongodb');
const nunjucks = require('nunjucks');
const staticfiles = require('nunjucks-staticfiles');


let app = express();
let logger = bristolConf(config.logging);

let renderer = nunjucks.configure(config.templates.directory, {
	autoescape: true,
	express: app
});

renderer.addFilter('date', require('nunjucks-date-filter'));
renderer.addFilter('hex', require('explorer/lib/filters/hex'));
renderer.addFilter('is_before', require('explorer/lib/filters/is-before'));
renderer.addFilter('relative_time', require('explorer/lib/filters/relative-time'));
renderer.addFilter('slugify', require('explorer/lib/filters/slugify'));

staticfiles.configure(config.staticfiles.directories, {
	nunjucks: renderer,
	express: app,
	path: config.staticfiles.path,
	staticMiddleware: express.static
});

// Disable insecure header information.
app.disable('x-powered-by');

// Mount middleware.
app.use([
	// Relegate incoming requests to a queue if exceeding a specified concurrency rate.
	require('explorer/lib/middleware/concurrency')(config.concurrency),

	// IP tracking
	require('explorer/lib/middleware/ip'),

	// Add tracking/diagnostic metadata to the request.
	require('explorer/lib/middleware/meta'),

	// Parse (and possibly respond to) Content-Type
	require('explorer/lib/middleware/content-type')(),

	// Context processor
	require('explorer/lib/middleware/context-processor'),

	// Parse cookies.
	require('cookie-parser')(),

	// Body parsing (convert stream to completed buffer)
	require('body-parser').json({
		limit: 2500000 // bytes (2.5MB)
	}),

	// Body parsing for HTML forms (convert stream to completed buffer)
	require('body-parser').urlencoded({
		extended: false,
		limit: 2500000 // bytes (2.5MB)
	}),

	// Request logging
	require('explorer/lib/middleware/logging')(logger),

	// Load the current user onto the request
	require('explorer/lib/middleware/authentication'),

	// CSRF middleware
	require('explorer/lib/middleware/csrf').create,

	// Create initial searches
	require('explorer/lib/middleware/initial-searches'),

	// Mount main views
	require('explorer/lib/views'),

	// Send a 404 if the route is not otherwise handled.
	require('explorer/lib/middleware/handle-404'),

	// Send an error code corresponding to a handled application error.
	require('explorer/lib/middleware/handle-error')
]);


// SHUTDOWN
(function(process) {
	function shutdown(code) {
		process.exit(code || 0);
	}

	process.once('SIGINT', function() {
		logger.info('Gracefully shutting down from SIGINT (CTRL+C)');
		shutdown(0);
	});

	process.once('SIGTERM', function() {
		shutdown(0);
	});
})(process);


// BOOT
Promise.all([
	new Promise(function(resolve, reject) {
		let address = config.databases.mongo.address;
		let options = config.databases.mongo.options;

		mongodb.MongoClient.connect(address, options, function(err, db) {
			if (err) {
				reject(err);
			}
			else {
				resolve(db);
			}
		});
	}),

	new Promise(function(resolve, reject) {
		let address = config.caches.sessions.address;
		let redis = new Redis(address);

		redis.once('error', reject);
		redis.once('ready', function() {
			resolve(redis);
		});
	}),

	require('explorer/lib/validator').load(config.validationSchemas)
])
	.spread(function(mongo, sessions, validate) {
		global.env = {
			caches: {
				sessions: sessions
			},

			databases: {
				mongo: mongo,
				elastic: new elasticsearch.Client({
					host: config.databases.elastic.address,
					apiVersion: '2.2',
					maxSockets: 100,
					minSockets: 100,
					defer: function() {
						return new Deferred(Promise);
					}
				})
			},

			logger: logger,
			validate: validate
		};
	})
	.then(function() {
		return Promise.all([
			new Promise(function(resolve, reject) {
				let url = new URL(config.address);
				let hostname = (url.hostname === '0.0.0.0' || url.hostname === '') ? '*' : url.hostname;
				let port = parseInt(url.port);

				let server = (hostname === '*') ? app.listen(port) : app.listen(port, hostname);

				server.once('listening', function() {
					resolve(server);
				});

				server.once('error', reject);
			})
		]);
	})
	.spread(function(http) {
		logger.info('HTTP server listening.', http.address());
	})
	.catch(function(err) {
		logger.error(err);
		process.exit(1);
	});


process.stdin.resume();
