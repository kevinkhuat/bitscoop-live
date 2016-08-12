'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const httpErrors = require('http-errors');

const deleteDocuments = require('explorer/lib/util/delete-documents');
const gid = require('explorer/lib/util/gid');


let types = [
	'contacts',
	'content',
	'events',
	'locations',
	'organizations',
	'places',
	'things'
];


function deleteConnection(hexId, userId) {
	let mongo = env.databases.mongo;

	return mongo.db('bitscoop').collection('connections').deleteOne({
		_id: gid(hexId)
	})
		.then(function(data) {
			if (data.result.n === 0) {
				return Promise.reject(httpErrors(404));
			}

			let terms = {
				user_id: userId,
				connection: gid(hexId)
			};

			let promises = _.map(types, function(type) {
				return deleteDocuments('explorer', type, terms);
			});

			return Promise.all(promises)
				.then(function() {
					return Promise.resolve(null);
				});
		});
}


module.exports = deleteConnection;
