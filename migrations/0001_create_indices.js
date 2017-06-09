'use strict';

const Bristol = require('bristol').Bristol;
const Promise = require('bluebird');
const config = require('config');
const mongodb = require('mongodb');


let logger = new Bristol();

logger.addTarget('console')
	.withFormatter('human')
	.withLowestSeverity('debug');


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
	})
])
	.then(function(result) {
		let [db] = result;

		return Promise.all([
			// `connections` collection
			db.db('explorer').collection('connections').createIndex({
				connection_id: 1
			}),

			db.db('explorer').collection('connections').createIndex({
				user_id: 1
			}),

			// `events` collection
			db.db('explorer').collection('events').createIndex({
				user_id: 1
			}),

			// `providers` collection
			db.db('explorer').collection('providers').createIndex({
				enabled: 1
			}),

			db.db('explorer').collection('providers').createIndex({
				provider_id: 1
			}),

			// `searches` collection
			db.db('explorer').collection('searches').createIndex({
				user_id: 1
			}),

			db.db('explorer').collection('searches').createIndex({
				hash: 1
			}),

			// `tags` collection
			db.db('explorer').collection('tags').createIndex({
				user_id: 1
			})
		]);
	})
	.catch(function(err) {
		logger.error(err);
		process.exit(1);
	})
	.then(function() {
		process.exit(0);
	});


process.stdin.resume();
