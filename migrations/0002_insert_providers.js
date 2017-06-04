'use strict';

const path = require('path');

const Bristol = require('bristol').Bristol;
const Promise = require('bluebird');
const _ = require('lodash');
const config = require('config');
const mongodb = require('mongodb');

const fs = require('../lib/util/fs');
const gid = require('../lib/util/gid');

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
			logger.info('Reading Provider information from "' + file + '".');

			let dirname = path.dirname(file);
			let basename = path.basename(file);
			let keyfile = path.join(dirname, 'keys', basename);

			return Promise.all([
				fs.readfile(file),
				fs.readfile(keyfile)
			])
				.spread(function(providerJson, keyfileJson) {
					let provider = JSON.parse(providerJson);

					if (provider.remote_provider_id == null) {
						return Promise.resolve();
					}

					let key = JSON.parse(keyfileJson);

					_.merge(provider, key);

					provider._id = gid(provider._id);
					provider.remote_provider_id = gid(provider.remote_provider_id);

					return db.db('explorer').collection('providers').update({
						_id: provider._id
					}, {
						$setOnInsert: provider
					}, {
						upsert: true
					})
						.then(function(inserted) {
							logger.info('New Provider <' + provider._id.toString('hex') + '> inserted.');

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
