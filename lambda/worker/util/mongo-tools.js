'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const moment = require('moment');
const uuid = require('uuid');

const amalgamateTags = require('./amalgamate-tags');
const gid = require('./gid');

const indexActionCache = {
		contacts: {
			index: {
				_index: 'explorer',
				_type: 'contacts'
			}
		},
		content: {
			index: {
				_index: 'explorer',
				_type: 'content'
			}
		},
		events: {
			index: {
				_index: 'explorer',
				_type: 'events'
			}
		},
		locations: {
			index: {
				_index: 'explorer',
				_type: 'locations'
			}
		},
		things: {
			index: {
				_index: 'explorer',
				_type: 'things'
			}
		}
	};


function MongoEvent(data) {
	this.connection = data.connection;
	this.contact_interaction_type = data.contact_interaction_type;
	this.context = data.context;
	this.datetime = data.datetime;
	this.identifier = data.identifier;
	//this.places = data.places;
	this.provider = data.provider;
	this.provider_name = data.provider_name;
	this.source = data.source;
	this.tagMasks = data.tagMasks;
	this.type = data.type;
	this.updated = data.updated;
	this.user_id = data.user_id;

	if (data.contacts) {
		this.contacts = new Array(data.contacts.length);

		for (let i = 0; i < data.contacts.length; i++) {
			this.contacts[i] = data.contacts[i]._id;
		}
	}

	if (data.content) {
		this.content = new Array(data.content.length);

		for (let i = 0; i < data.content.length; i++) {
			this.content[i] = data.content[i]._id;
		}
	}

	if (data.things) {
		this.things = new Array(data.things.length);

		for (let i = 0; i < data.things.length; i++) {
			this.things[i] = data.things[i]._id;
		}
	}

	if (data.location) {
		this.location = data.location._id;
	}

	if (this.tagMasks == null) {
		delete this.tagMasks;
	}
}

MongoEvent.prototype.toJSON = function() {
	return {
		id: this.id,
		connection: this.connection,
		contact_interaction_type: this.contact_interaction_type,
		context: this.context,
		contacts: this.contacts,
		content: this.content,
		created: this.created,
		datetime: this.datetime,
		location: this.location,
		places: this.places,
		provider_name: this.provider_name,
		tagMasks: this.tagMasks,
		things: this.things,
		type: this.type
	};
};

function bulkUpsert(type, dataList) {
	let mongo = env.databases.mongo;

	let bulk = mongo.db('explorer').collection(type).initializeUnorderedBulkOp();
	let identifiers = new Array(dataList.length);

	for (let i = 0; i < dataList.length; i++) {
		let data = dataList[i];
		let id = uuid();

		identifiers[i] = data.identifier;

		_.assign(data, {
			updated: moment.utc().toDate()
		});

		bulk.find({
			identifier: data.identifier
		})
		.upsert()
		.updateOne({
				$set: data,
				$setOnInsert: {
					_id: gid(id),
					created: data.updated
				}
			});
	}

	return bulk.execute().then(function() {
		return mongo.db('explorer').collection(type).find({
			identifier: {
				$in: identifiers
			}
		}).toArray();
	});
}

function bulkTagUpsert(dataList) {
	let mongo = env.databases.mongo;

	let bulk = mongo.db('explorer').collection('tags').initializeUnorderedBulkOp();
	let tags = new Array(dataList.length);

	for (let i = 0; i < dataList.length; i++) {
		let data = dataList[i];
		let id = uuid();

		tags[i] = data.tag;

		bulk.find({
			tag: data.tag
		})
			.upsert()
			.updateOne({
				$set: data,
				$setOnInsert: {
					_id: gid(id),
					created: data.updated
				}
			});
	}

	return bulk.execute().then(function() {
		return mongo.db('explorer').collection('tags').find({
			tag: {
				$in: tags
			}
		}).toArray();
	});
}

function mongoInsert(objects) {
	var contactsUpsert, contentUpsert, locationsUpsert, tagsUpsert, thingsUpsert;

	if (objects.contacts && objects.contacts.length > 0) {
		contactsUpsert = bulkUpsert('contacts', objects.contacts);
	}

	if (objects.content && objects.content.length > 0) {
		contentUpsert = bulkUpsert('content', objects.content);
	}

	if (objects.locations && objects.locations.length > 0) {
		locationsUpsert = bulkUpsert('locations', objects.locations);
	}

	if (objects.tags && objects.tags.length > 0) {
		tagsUpsert = bulkTagUpsert(objects.tags);
	}

	if (objects.things && objects.things.length > 0) {
		thingsUpsert = bulkUpsert('things', objects.thing);
	}

	return Promise.all([
		contactsUpsert,
		contentUpsert,
		locationsUpsert,
		tagsUpsert,
		thingsUpsert
	])
		.then(function(result) {
			let [hydratedContacts, hydratedContent, hydratedLocations, hydratedTags, hydratedThings] = result;

			if (hydratedContacts != null) {
				for (let i = 0; i < hydratedContacts.length; i++) {
					let index = _.findIndex(objects.contacts, function(contact) {
						return contact.identifier === hydratedContacts[i].identifier;
					});

					objects.contacts[index]._id = hydratedContacts[i]._id;
					objects.contacts[index].tagMasks = hydratedContacts[i].tagMasks;

					delete objects.contacts[index]['tagMasks.source'];
				}
			}

			if (hydratedContent != null) {
				for (let i = 0; i < hydratedContent.length; i++) {
					let index = _.findIndex(objects.content, function(content) {
						return content.identifier === hydratedContent[i].identifier;
					});

					objects.content[index]._id = hydratedContent[i]._id;
					objects.content[index].tagMasks = hydratedContent[i].tagMasks;

					delete objects.content[index]['tagMasks.source'];
				}
			}

			if (hydratedLocations != null) {
				for (let i = 0; i < hydratedLocations.length; i++) {
					let index = _.findIndex(objects.locations, function(location) {
						return location.identifier === hydratedLocations[i].identifier;
					});

					objects.locations[index]._id = hydratedLocations[i]._id;
					objects.locations[index].tagMasks = hydratedLocations[i].tagMasks;

					delete objects.locations[index]['tagMasks.source'];
				}
			}

			if (hydratedThings != null) {
				for (let i = 0; i < hydratedThings.length; i++) {
					let index = _.findIndex(objects.things, function(thing) {
						return thing.identifier === hydratedThings[i].identifier;
					});

					objects.things[index]._id = hydratedThings[i]._id;
					objects.things[index].tagMasks = hydratedThings[i].tagMasks;

					delete objects.things[index]['tagMasks.source'];
				}
			}

			let mongoEvents = new Array(objects.events.length);

			for (let i = 0; i < objects.events.length; i++) {
				mongoEvents[i] = new MongoEvent(objects.events[i]);
			}

			return bulkUpsert('events', mongoEvents);
		});
}


module.exports = {
	bulkUpsert: bulkUpsert,
	MongoEvent: MongoEvent,
	mongoInsert: mongoInsert
};
