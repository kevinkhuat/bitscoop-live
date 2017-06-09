'use strict';

const Consumer = require('poolq').Consumer;
const Deferred = require('deferred-ap');
const Generator = require('poolq').Generator;
const Promise = require('bluebird');
const Queue = require('poolq').Queue;
const Redis = require('ioredis');
const _ = require('lodash');
const bristolConf = require('bristol-config');
const config = require('config');
const elasticsearch = require('elasticsearch');
const mongodb = require('mongodb');
const noop = require('node-noop').noop;


let logger = bristolConf(config.logging);


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
		let address = config.caches.jobs.address;
		let redis = new Redis(address);

		redis.once('error', reject);
		redis.once('ready', function() {
			resolve(redis);
		});
	})
])
	.then(function(result) {
		let [mongo, jobs] = result;

		global.env = {
			caches: {
				jobs: jobs
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

			logger: logger
		};
	})
	.then(function() {
		let consumerList = _.get(config, 'tasks.consumers', null);
		let generatorList = _.get(config, 'tasks.generators', null);

		let consumers = _.map(consumerList, function(name) {
			return new Consumer({
				interval: 5000,
				consume: require(name)
			});
		});

		let generators = _.map(generatorList, function(name) {
			return new Generator({
				interval: 5,
				create: require(name),
				queue: new Queue({
					cache: config.caches.jobs.address,
					stream: 'connection'
				})
			});
		});

		return Promise.resolve([consumers, generators]);
	})
	.then(function(result) {
		let [consumers, generators] = result;

		if (consumers.length > 0) {
			for (let i = 0; i < consumers.length; i++) {
				consumers[i].resume();
			}

			logger.info('Task consumer running.');
		}

		if (generators.length > 0) {
			_.map(generators, function(generator) {
				generator.queue.on('created', function(job) {
					logger.info('Job created', job);
				});

				generator.queue.on('completed', function(job) {
					logger.info('Job completed', job);
				});

				return setInterval(function() {
					generator.next()
						.then(function(jobs) {
							for (let i = 0; i < jobs.length; i++) {
								generator.queue.enqueue(jobs[i])
									.catch(Queue.UniqueConflictError, noop)
									.catch(function(err) {
										logger.error(err);
									});
							}
						});
				}, generator.interval * 1000);
			});

			logger.info('Task generator running.');
		}
	})
	.catch(function(err) {
		logger.error(err);
		process.exit(1);
	});


process.stdin.resume();
