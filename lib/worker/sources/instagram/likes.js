'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const moment = require('moment');

const mongoTools = require('../../../util/mongo-tools');


module.exports = function(data) {
	var contacts, content, events, objectCache, tags;

	objectCache = {
		contacts: {},
		events: {},
		tags: {}
	};

	contacts = [];
	content = [];
	tags = [];
	events = new Array(data.length);

	if (data && data.length > 0) {
		for (let i = 0; i < data.length; i++) {
			let item = data[i];

			let newTags = [];

			for (let j = 0; j < item.tags.length; j++) {
				let tag = item.tags[j];

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

			let newMedia = {
				identifier: this.connection._id.toString('hex') + ':::instagram:::' + item.id,
				connection: this.connection._id,
				user_id: this.connection.user_id,
				url: item.link,
				remote_id: item.id,
				'tagMasks.source': newTags
			};

			if (item.caption) {
				newMedia.title = item.caption.text;
			}

			if (item.type === 'image') {
				newMedia.type = 'image';
				newMedia.embed_format = 'jpeg';
				newMedia.embed_content = item.images.standard_resolution.url;
				newMedia.embed_thumbnail = item.images.thumbnail.url;
			}
			else if (item.type === 'video') {
				newMedia.type = 'video';
				newMedia.embed_format = 'mp4';
				newMedia.embed_thumbnail = item.images.thumbnail.url;
				newMedia.embed_content = item.videos.standard_resolution.url;
			}

			content.push(newMedia);

			let localContacts = [];

			let newContact = {
				identifier: this.connection._id.toString('hex') + ':::instagram:::' + item.user.id,
				connection: this.connection._id,
				user_id: this.connection.user_id,
				avatar_url: item.user.profile_picture,
				remote_id: item.user.id,
				handle: item.user.username
			};

			if (item.user.full_name) {
				newContact.name = item.user.full_name;
			}

			if (!_.has(objectCache.contacts, newContact.identifier)) {
				objectCache.contacts[newContact.identifier] = newContact;
				contacts.push(newContact);
			}

			localContacts.push(objectCache.contacts[newContact.identifier]);

			let datetime = moment(parseInt(item.created_time) * 1000).utc().toDate();

			let newEvent = {
				type: 'commented',
				context: 'Liked',
				provider_name: 'instagram',
				identifier: this.connection._id.toString('hex') + ':::liked:::instagram:::' + item.id,
				datetime: datetime,
				content: [newMedia],
				contacts: localContacts,
				connection: this.connection._id,
				user_id: this.connection.user_id
			};

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
