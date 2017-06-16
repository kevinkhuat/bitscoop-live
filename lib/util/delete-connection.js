'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const httpErrors = require('http-errors');

const callApi = require('./call-api');
const deleteDocuments = require('./delete-documents');
const gid = require('./gid');


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
	let connectionId;

	return mongo.db('live').collection('connections').findOne({
		_id: gid(hexId)
	})
		.then(function(connection) {
			if (!connection) {
				return Promise.reject(httpErrors(404));
			}

			connectionId = connection.remote_connection_id;

			return mongo.db('live').collection('connections').deleteOne({
				_id: gid(hexId)
			});
		})
		.then(function() {
			let path = 'connections/' + connectionId.toString('hex');

			return callApi(path, 'DELETE');
		})
		.then(function() {
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
