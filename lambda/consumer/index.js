'use strict';

const assert = require('assert');

const AWS = require('aws-sdk');
const _ = require('lodash');
const mongodb = require('mongodb');

const gid = require('./util/gid');


let sqs = new AWS.SQS();
let lambda = new AWS.Lambda;
let receiptHandleMap = {};


exports.handler = function(event, context, callback) {
	let db;

	return Promise.resolve()
		.then(function() {
			return new Promise(function(resolve, reject) {
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
			});
		})
		.then(function() {
			let params = {
				QueueUrl: process.env.QUEUE_URL,
				MaxNumberOfMessages: 10,
				MessageAttributeNames: [
					'All'
				]
			};

			return new Promise(function(resolve, reject) {
				sqs.receiveMessage(params, function(err, data) {
					if (err) {
						reject(err);
					}
					else {
						resolve(data);
					}
				});
			})
				.then(function(result) {
					let messages = result.Messages;

					if (messages == null) {
						return Promise.resolve([]);
					}

					let ids = _.map(messages, function(message) {
						let attr = message.MessageAttributes;

						console.log(message);
						console.log(message.ReceiptHandle);

						receiptHandleMap[attr.connectionId.StringValue] = message.ReceiptHandle;

						return gid(attr.connectionId.StringValue);
					});

					return db.db('live').collection('connections').find({
						_id: {
							$in: ids
						}
					}).toArray();
				})
				.then(function(connections) {
					if (connections.length === 0) {
						return Promise.resolve();
					}

					let jobs = _.map(connections, function(connection) {
						let stringId = connection._id.toString('hex');

						let payload = {
							connectionId: stringId,
							receiptHandle: receiptHandleMap[stringId]
						};

						let params = {
							FunctionName: process.env.WORKER_FUNCTION_NAME,
							InvocationType: 'Event',
							Payload: JSON.stringify(payload)
						};

						return new Promise(function(resolve, reject) {
							console.log('Invoking Lambda');

							lambda.invoke(params, function(err, data) {
								if (err) {
									reject(err);
								}
								else {
									resolve(data);
								}
							});
						})
							.catch(function(err) {
								let params = {
									QueueUrl: process.env.DEAD_MESSAGE_QUEUE_URL,
									MessageBody: 'Connection failed.',
									MessageAttributes: {
										error: {
											DataType: 'String',
											StringValue: JSON.stringify(err)
										}
									}
								};

								return new Promise(function(resolve, reject) {
									sqs.sendMessage(params, function(err, data) {
										if (err) {
											reject(err);
										}
										else {
											resolve();
										}
									});
								});
							});
					});

					return Promise.all(jobs);
				});
		})
		.then(function() {
			console.log('SUCCESSFUL');

			db.close();

			callback(null, null);

			return Promise.resolve();
		})
		.catch(function(err) {
			console.log('UNSUCCESSFUL');

			if (db) {
				db.close();
			}

			callback(err, null);

			return Promise.reject(err);
		});
};
