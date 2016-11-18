'use strict';

const Promise = require('bluebird');
const _ = require('lodash');


module.exports = function() {
	let self = this;

	let mongo = env.databases.mongo;

	return mongo.db('explorer').collection('providers').find({}, {
		_id: true
	}).toArray()
		.then(function(results) {
			let ids = _.map(results, function(result) {
				return result._id;
			});

			return Promise.resolve(ids);
		})
		.then(function(ids) {
			let $match = {
				$and: [
					{
						'auth.status.complete': true,
						enabled: true,
						provider_id: {
							$in: ids
						}
					},
					{
						$or: [
							{
								last_run: {
									$lt: new Date(new Date() - 86400000)
								}
							},
							{
								last_run: {
									$exists: false
								}
							}
						]
					}
				]
			};

			return mongo.db('explorer').collection('connections').find($match, {
				_id: true
			}).toArray()
				.then(function(connections) {
					if (!Array.isArray(connections)) {
						return Promise.resolve([]);
					}

					let jobs = _.map(connections, function(connection) {
						return new self.queue.Job({
							data: {
								type: 'fetch',
								connectionId: connection._id.toString('hex')
							},
							unique: ['connectionId']
						});
					});

					return Promise.resolve(jobs);
				});
		});
};
