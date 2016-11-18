'use strict';

const Promise = require('bluebird');
const _ = require('lodash');

const mongoTools = require('explorer/lib/util/mongo-tools');


let tagRegex = /#[^#\s]+/g;


module.exports = function(data) {
	var contacts, content, events, objectCache, tags;

	objectCache = {
		contacts: {},
		tags: {}
	};

	contacts = [];
	content = new Array(data.length);
	tags = [];
	events = new Array(data.length);

	if (data && data.length > 0) {
		for (let i = 0; i < data.length; i++) {
			let item = data[i];

			let newThread = {
				identifier: this.connection._id.toString('hex') + ':::reddit:::' + item.data.name,
				connection: this.connection._id,
				user_id: this.connection.user_id,
				type: 'text',
				text: item.data.selftext,
				url: 'https://www.reddit.com' + item.data.permalink,
				remote_id: item.data.id,
				title: item.data.title
			};

			if (item.data.thumbnail) {
				newThread.thumbnail = item.data.thumbnail;
			}


			let newTags = [];
			let titleTags = newThread.title.match(tagRegex);

			if (titleTags != null) {
				for (let j = 0; j < titleTags.length; j++) {
					let tag = titleTags[j].slice(1);

					let newTag = {
						tag: tag,
						user_id: this.connection.user_id
					};

					if (!_.has(objectCache.tags, newTag.tag)) {
						objectCache.tags[newTag.tag] = newTag;

						tags.push(objectCache.tags[newTag.tag]);
					}

					if (newTags.indexOf(newTag.tag) === -1) {
						newTags.push(newTag.tag);
					}
				}
			}

			if (newThread.text) {
				let messageTags = newThread.text.match(tagRegex);

				if (messageTags != null) {
					for (let j = 0; j < messageTags.length; j++) {
						let tag = messageTags[j].slice(1);

						let newTag = {
							tag: tag,
							user_id: this.connection.user_id
						};
						if (!_.has(objectCache.tags, newTag.tag)) {
							objectCache.tags[newTag.tag] = newTag;

							tags.push(objectCache.tags[newTag.tag]);
						}

						if (newTags.indexOf(newTag.tag) === -1) {
							newTags.push(newTag.tag);
						}
					}
				}

				newThread['tagMasks.source'] = newTags;
			}

			content[i] = newThread;

			let newEvent = {
				type: 'commented',
				context: 'Upvoted',
				provider_name: 'reddit',
				identifier: this.connection._id.toString('hex') + ':::upvoted:::reddit:::' + item.data.name,
				content: [newThread],
				connection: this.connection._id,
				user_id: this.connection.user_id
			};

			if (item.data.author !== this.connection.metadata.name) {
				let newContact = {
					identifier: this.connection._id.toString('hex') + ':::reddit:::' + item.data.author,
					connection: this.connection._id,
					user_id: this.connection.user_id,
					handle: item.data.author
				};

				if (!_.has(objectCache.contacts, newContact.identifier)) {
					objectCache.contacts[newContact.identifier] = newContact;
					contacts.push(objectCache.contacts[newContact.identifier]);
				}

				newEvent.contacts = [objectCache.contacts[newContact.identifier]];
			}

			events[i] = newEvent;
		}

		return mongoTools.mongoElasticInsert({
			contacts: contacts,
			content: content,
			events: events,
			tags: tags
		});
	}
	else {
		return Promise.resolve(null);
	}
};
