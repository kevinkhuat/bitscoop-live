'use strict';

const path = require('path');

const _ = require('lodash');
const mongodb = require('mongodb');

const fs = require('./util/fs');
const gid = require('./util/gid');


exports.handler = function(event, context, callback) {
	let db;

	return Promise.all([
		new Promise(function(resolve, reject) {
			let address = process.env.MONGO_ADDRESS;
			let options = {
				poolSize: 5
			};

			mongodb.MongoClient.connect(address, options, function(err, database) {
				if (err) {
					reject(err);
				}
				else {
					db = database;
					resolve();
				}
			});
		}),

		fs.find('./fixtures/mongo/live/providers/*.json')
	])
		.then(function(result) {
			let [, files] = result;

			return Promise.all([
				// `connections` collection
				db.db('live').collection('connections').createIndex({
					connection_id: 1
				}),

				db.db('live').collection('connections').createIndex({
					user_id: 1
				}),

				// `events` collection
				db.db('live').collection('events').createIndex({
					user_id: 1
				}),

				// `providers` collection
				db.db('live').collection('providers').createIndex({
					enabled: 1
				}),

				db.db('live').collection('providers').createIndex({
					provider_id: 1
				}),

				// `tags` collection
				db.db('live').collection('tags').createIndex({
					user_id: 1
				})
			])
				.then(function() {
					return Promise.resolve(files);
				});
		})
		.then(function(files) {
			let inserts = _.map(files, function(file) {
				console.log('Reading Provider information from "' + file + '".');

				return Promise.all([
					fs.readfile(file)
				])
					.then(function(result) {
						let [providerJson] = result;

						let provider = JSON.parse(providerJson);
						if (provider.remote_map_id == null) {
							return Promise.resolve();
						}

						provider._id = gid(provider._id);
						provider.remote_map_id = gid(provider.remote_map_id);

						return db.db('live').collection('providers').update({
							_id: provider._id
						}, {
							$setOnInsert: provider
						}, {
							upsert: true
						})
							.then(function(inserted) {
								console.log('New Provider <' + provider._id.toString('hex') + '> inserted.');

								return Promise.resolve(inserted);
							});
					});
			});

			return Promise.all(inserts);
		})
		.then(function() {
			console.log('Migrations succeeded.');

			db.close();

			callback(null, null);

			return Promise.resolve();
		})
		.catch(function(err) {
			console.log(err);

			if (db) {
				db.close();
			}

			return Promise.reject(err);
		});
};
