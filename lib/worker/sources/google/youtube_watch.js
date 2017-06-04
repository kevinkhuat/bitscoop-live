'use strict';

const Promise = require('bluebird');
const _ = require('lodash');
const moment = require('moment');

const mongoTools = require('../../../util/mongo-tools');


let tagRegex = /#[^#\s]+/g;


module.exports = function(data) {
	var content, events, objectCache, tags;

	if (data && data.length > 0 && data[0].watch_history.length > 0) {
		objectCache = {
			tags: {}
		};

		content = new Array(data[0].watch_history.length);
		tags = [];
		events = new Array(data[0].watch_history.length);

		for (let i = 0; i < data[0].watch_history.length; i++) {
			let item = data[0].watch_history[i];
			let newTags = [];
			let titleTags = item.snippet.title.match(tagRegex);

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

			let descriptionTags = item.snippet.description.match(tagRegex);

			if (descriptionTags != null) {
				for (let j = 0; j < descriptionTags.length; j++) {
					let tag = descriptionTags[j].slice(1);

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

			let newMedia = {
				identifier: this.connection._id.toString('hex') + ':::youtube:::' + item.id,
				connection: this.connection._id,
				user_id: this.connection.user_id,
				url: item.url,
				remote_id: item.id,
				embed_content: item.oembed.html,
				embed_format: 'iframe',
				embed_thumbnail: item.oembed.thumbnail_url,
				'tagMasks.source': newTags,
				text: item.snippet.description,
				title: item.snippet.title,
				type: 'video'
			};

			content[i] = newMedia;

			let newEvent = {
				type: 'played',
				context: 'Watched',
				provider_name: 'google',
				identifier: this.connection._id.toString('hex') + ':::played:::youtube:::' + item.id,
				datetime: moment(item.snippet.publishedAt).utc().toDate(),
				content: [newMedia],
				connection: this.connection._id,
				user_id: this.connection.user_id
			};

			events[i] = newEvent;
		}

		return mongoTools.mongoElasticInsert({
			content: content,
			events: events,
			tags: tags
		});
	}
	else {
		return Promise.resolve(null);
	}
};
