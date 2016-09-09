'use strict';

const path = require('path');

const Bristol = require('bristol').Bristol;
const Deferred = require('deferred-ap');
const Promise = require('bluebird');
const _ = require('lodash');
const config = require('config');
const elasticsearch = require('elasticsearch');

const fs = require('explorer/lib/util/fs');


let logger = new Bristol();

logger.addTarget('console')
	.withFormatter('human')
	.withLowestSeverity('debug');


Promise.all([
	new Promise(function(resolve, reject) {
		let elastic = new elasticsearch.Client({
			host: config.databases.elastic.address,
			apiVersion: '2.2',
			maxSockets: 100,
			minSockets: 100,
			defer: function() {
				return new Deferred(Promise);
			}
		});

		resolve(elastic);
	}),

	fs.readfile('fixtures/elasticsearch/explorer/settings/es-settings.json'),

	fs.find('fixtures/elasticsearch/explorer/mappings/*.json')
])
	.spread(function(elastic, settings, mappings) {
		return elastic.indices.close({
			index: 'explorer'
		})
			.then(function() {
				return elastic.indices.putSettings({
					index: 'explorer',
					body: JSON.parse(settings)
				});
			})
			.then(function() {
				return elastic.indices.open({
					index: 'explorer'
				});
			})
			.then(function() {
				let inserts = _.map(mappings, function(file) {
					return fs.readfile(file)
						.then(function(mapping) {
							let type = path.basename(file, '.json');

							return elastic.indices.putMapping({
								index: 'explorer',
								type: type,
								body: JSON.parse(mapping)
							})
								.then(function() {
									logger.info('Index created for ' + type);
								});
						});
				});

				return Promise.all(inserts);
			});
	})
	.catch(function(err) {
		logger.error(err);
		process.exit(1);
	})
	.then(function() {
		process.exit(0);
	});


process.stdin.resume();
