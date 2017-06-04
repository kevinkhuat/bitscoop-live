'use strict';

const url = require('url');

const Promise = require('bluebird');
const _ = require('lodash');
const config = require('config');
const express = require('express');
const httpErrors = require('http-errors');

const csrf = require('../../middleware/csrf');
const get = require('./templates/get');
const gid = require('../../util/gid');
const loginRequired = require('../../middleware/login-required');
const models = require('../../models');
const orderedMap = require('../../util/ordered-map');
const tag = require('./templates/tag');


let router = express.Router();
let event = router.route('/:id');
let tagging = router.route('/:id/tag');
let events = router.route('/');

let textFields = [
	'contacts.handle',
	'contacts.name',
	'content.type',
	'content.file_extension',
	'content.owner',
	'content.text',
	'content.title',
	'content.url',
	'things.title',
	'things.text',
	'type',
	'provider_name'
];

let specialSorts = {
	connection: {
		condition: 'connection',
		values: ['provider_name', 'connection']
	},
	rawType: {
		condition: 'type.raw',
		values: ['type.raw', 'context.raw']
	},
	emptyQueryRelevance: {
		values: [
			'datetime'
		]
	}
};


event.options(function(req, res, next) {
	res.setHeader('Allowed', 'GET,OPTIONS');

	res.sendStatus(204);
});

/**
 * Gets the event with the given ID. If a event with that ID does not exist, then it throws an error.
 *
 * @param {Boolean} id The ID of the saved search.
 * @returns {Object} An object containing the matching search and its attendant information. If no match, then an error
 *      is thrown.
 *      @returns {String} id The ID of the matching saved search.
 *      @returns {String} [name] The name of the matching saved search.
 *      @returns {String} [icon] The icon of the matching saved search.
 *      @returns {String} [iconColor] The icon color of the matching saved search.
 *      @returns {String} [query] The query of the matching saved search.
 *      @returns {String} filters The filters of the matching saved search.
 *      @returns {String} [favorited] The favorited status of the matching saved search.
 */
event.get(loginRequired(404), function(req, res, next) {
	get.one(req, 'events', models.Event)
		.then(function(response) {
			res.json(response);
		})
		.catch(function(err) {
			next(err);
		});
});


events.options(function(req, res, next) {
	res.setHeader('Allowed', 'GET,OPTIONS,SEARCH');

	res.sendStatus(204);
});

/**
 * Retrieves a list of events for the current user. Pagination is handled via limit and offset.
 *
 * @param {Number} limit Page limit for the results.
 * @param {Number} offset Offset from the first result.
 * @returns {Object} An object containing the search results along with attendant information about the search.
 *      @returns {Number} count The total number of results for this search.
 *      @returns {String} limit Page limit for the results
 *      @returns {String} next The URL to call for the next page of results, or null if there are no more results.
 *      @returns {String} offset The offset from the first result.
 *      @returns {String} prev The URL to call for the previous page of results, or null if there are no more results.
 *      @returns {Array} results The current page of results.
 */
events.get(loginRequired(404), function(req, res, next) {
	get.many(req, 'events', models.Event)
		.then(function(response) {
			res.json(response);
		})
		.catch(function(err) {
			next(err);
		});
});

/**
 * Searches for a list of events via an optional query and filters. Data is returned sorted via an optional sort field
 * and order. Pagination is handled via limit and offset parameters.
 *
 * @param {Object} [filters] Filters in DSL format.
 * @param {Number} limit Page limit for the results.
 * @param {Number} offset Offset from the first result.
 * @param {String} [query] Query text to search for.
 * @param {String} [sortField] Field on which to sort results.
 * @param {String} [sortOrder] Order in which to sort results.
 * @returns {Object} An object containing the search results along with attendant information about the search.
 *      @returns {Number} count The total number of results for this search.
 *      @returns {String} limit Page limit for the results
 *      @returns {String} next The URL to call for the next page of results, or null if there are no more results.
 *      @returns {String} offset The offset from the first result.
 *      @returns {String} prev The URL to call for the previous page of results, or null if there are no more results.
 *      @returns {Array} results The current page of results.
 */
events.search(loginRequired(404), function(req, res, next) {
	let elastic = env.databases.elastic;
	let mongo = env.databases.mongo;
	let validate = env.validate;

	let filters = req.body.filters;
	let suppliedFilters = filters;

	if (filters == null) {
		filters = {
			bool: {
				must: [],
				must_not: [],
				should: []
			}
		};
	}

	let query = {
		filters: filters,
		limit: req.query.limit || req.body.limit,
		offset: req.query.offset || req.body.offset,
		q: req.query.q || req.body.q,
		sortField: req.query.sortField || req.body.sortField,
		sortOrder: req.query.sortOrder || req.body.sortOrder
	};

	let suppliedSortField = query.sortField;
	let suppliedSortOrder = query.sortOrder;

	let validation = Promise.all([
		validate(query, '/requests/search'),
		validate(query.filters, '/searchdsl/types/event'),
		validate(query.sortField, '/searchdsl/sorts/event')
	])
		.spread(function(query, filters, sortField) {
			if (query.limit > config.objectMaxLimit) {
				query.limit = config.objectMaxLimit;
			}

			switch(query.sortOrder) {
				case '+':
					query.sortOrder = 'asc';
					break;

				case '-':
					query.sortOrder = 'desc';
					break;
			}

			return Promise.resolve(query);
		})
		.catch(function(err) {
			// TODO: Improve error report for bad validation.

			return Promise.reject(httpErrors(400));
		});

	return validation
		.then(function(query) {
			let esQuery = {
				query: {
					bool: {
						filter: {
							and: [
								query.filters,
								{
									bool: {
										must: {
											term: {
												user_id: req.user._id.toString('hex')
											}
										}
									}
								}
							]
						}
					}
				},
				size: query.limit,
				from: query.offset
			};

			let specialSort = false;

			for (let key in specialSorts) {
				if (!specialSorts.hasOwnProperty(key)) {
					break;
				}

				let field = specialSorts[key];

				if ((key === 'emptyQueryRelevance' && query.sortField === '_score' && query.q == null) || query.sortField === field.condition) {
					specialSort = true;
					esQuery.sort = new Array(field.values.length);

					for (let i = 0; i < field.values.length; i++) {
						let value = field.values[i];

						esQuery.sort[i] = {
							[value]: {
								order: query.sortOrder
							}
						};
					}
				}
			}

			if (specialSort === false) {
				esQuery.sort = [
					{
						[query.sortField]: {
							order: query.sortOrder
						}
					}
				];
			}

			if (query.q != null) {
				esQuery.query.bool.must = {
					multi_match: {
						query: query.q,
						type: 'most_fields',
						fields: textFields
					}
				};
			}

			return elastic.search({
				index: 'explorer',
				type: 'events',
				body: esQuery
			});
		})
		.then(function(data) {
			let count = data.hits.total;
			let results = data.hits.hits;

			let hexIds = new Array(results.length);
			let binIds = new Array(results.length);

			for (let i = 0; i < results.length; i++) {
				let hexId = results[i]._id;

				hexIds[i] = hexId;
				binIds[i] = gid(hexId);
			}

			return mongo.db('explorer').collection('events').find({
				_id: {
					$in: binIds
				},
				user_id: req.user._id
			}).toArray()
				.then(function(documents) {
					let idMap = {};

					for (let i = 0; i < documents.length; i++) {
						let document = documents[i];
						let object = new models.Event(document);

						idMap[object.id] = object;
					}

					let results = _.map(hexIds, function(id) {
						return idMap[id];
					});

					let promises = _.map(results, function(event) {
						let contacts, content, location, things;

						if (event.contacts && event.contacts.length > 0) {
							contacts = mongo.db('explorer').collection('contacts').find({
								_id: {
									$in: event.contacts
								}
							}).toArray()
								.then(function(results) {
									event.contacts = orderedMap(event.contacts, results, models.Contact.create);

									return Promise.resolve(null);
								});
						}
						else {
							contacts = Promise.resolve();
						}

						if (event.content && event.content.length > 0) {
							content = mongo.db('explorer').collection('content').find({
								_id: {
									$in: event.content
								}
							}).toArray()
								.then(function(results) {
									event.content = orderedMap(event.content, results, models.Content.create);

									return Promise.resolve(null);
								});
						}
						else {
							content = Promise.resolve();
						}

						if (event.location) {
							location = mongo.db('explorer').collection('locations').findOne({
								_id: event.location
							})
								.then(function(result) {
									event.location = new models.Content.create(result);

									return Promise.resolve(null);
								});
						}
						else {
							location = Promise.resolve();
						}

						if (event.things && event.things.length > 0) {
							things = mongo.db('explorer').collection('thing').find({
								_id: {
									$in: event.things
								}
							}).toArray()
								.then(function(results) {
									event.things = orderedMap(event.things, results, models.Thing.create);

									return Promise.resolve(null);
								});
						}
						else {
							things = Promise.resolve();
						}

						return Promise.all([contacts, content, location, things]);
					});

					return Promise.all(promises).then(function() {
						return Promise.resolve([results, count]);
					});
				});
		})
		.spread(function(results, count) {
			let query = validation.value();
			let q = query.q;
			let sortField = query.sortField;
			let sortOrder = query.sortOrder;
			let limit = query.limit;
			let offset = query.offset;
			let prev = null;
			let next = null;

			if (offset !== 0) {
				prev = {
					url: url.format({
						protocol: 'https',
						hostname: 'live.bitscoop.com',
						pathname: 'api/events'
					}),
					method: 'SEARCH',
					body: {
						limit: limit,
						offset: Math.max(0, offset - limit),
						q: q,
						filters: suppliedFilters,
						sortField: sortField,
						sortOrder: sortOrder
					}
				};
			}

			if (limit + offset < count) {
				next = {
					url: url.format({
                        protocol: 'https',
                        hostname: 'live.bitscoop.com',
						pathname: 'api/events'
					}),
					method: 'SEARCH',
					body: {
						limit: limit,
						offset: offset + limit,
						q: q,
						filters: suppliedFilters,
						sortField: suppliedSortField,
						sortOrder: suppliedSortOrder
					}
				};
			}

			return Promise.resolve({
				count: count,
				limit: limit,
				offset: offset,
				sortField: sortField,
				sortOrder: sortOrder,
				prev: prev,
				next: next,
				results: results
			});
		})
		.then(function(response) {
			res.json(response);
		})
		.catch(function(err) {
			next(err);
		});
});


tagging.options(function(req, res, next) {
	res.setHeader('Allowed', 'DELETE,OPTIONS,POST');

	res.sendStatus(204);
});

tagging.delete(loginRequired(404), csrf.validate, function(req, res, next) {
	tag.remove(req, 'events')
		.then(function() {
			res.sendStatus(204);
		})
		.catch(function(err) {
			next(err);
		});
});

tagging.post(loginRequired(404), csrf.validate, function(req, res, next) {
	tag.add(req, 'events')
		.then(function() {
			res.sendStatus(204);
		})
		.catch(function(err) {
			next(err);
		});
});


module.exports = router;
