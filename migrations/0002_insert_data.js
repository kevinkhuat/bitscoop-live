'use strict';

const Bristol = require('bristol').Bristol;
const Promise = require('bluebird');
const _ = require('lodash');
const config = require('config');
const mongodb = require('mongodb');

const fs = require('explorer/lib/util/fs');
const gid = require('explorer/lib/util/gid');

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
	}),

	fs.find('fixtures/mongo/explorer/providers/*.json')
])
	.spread(function(db, files) {
		let inserts = _.map(files, function(file) {
			logger.info('Reading provider information from "' + file + '".');

			return fs.readfile(file)
				.then(function(json) {
					let provider = JSON.parse(json);

					provider._id = gid(provider._id);
					provider.provider_id = gid(provider.provider_id);

					return db.db('explorer').collection('providers').insert(provider)
						.then(function(inserted) {
							logger.info('New provider <' + provider._id.toString('hex') + '> inserted.');

							return Promise.resolve(inserted);
						});
				});
		});

		return Promise.all(inserts);
	})
	.catch(function(err) {
		logger.error(err);
		process.exit(1);
	})
	.then(function() {
		process.exit(0);
	});


process.stdin.resume();
