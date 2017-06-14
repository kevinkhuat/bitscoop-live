'use strict';

const _ = require('lodash');
const moment = require('moment');

const mongoTools = require('../../util/mongotools');


let tagRegex = /#[^#\s]+/g;


module.exports = function(data) {
	var contacts, content, events, objectCache, tags;

	objectCache = {
		contacts: {},
		content: {},
		tags: {}
	};

	contacts = [];
	content = [];
	tags = [];
	events = [];

	if (data && data.length > 0) {
		for (let i = 0; i < data.length; i++) {
			let item = data[i];

			let newFile = {};
			let localFiles = [];
			let localFilesIds = {};
			let newContact = {};
			let localContacts = [];
			let localContactsIds = {};

			if (item.removed) {
				newFile = {
					identifier: this.connection._id.toString('hex') + ':::drive:::' + item.fileId,
					connection: this.connection._id,
					user_id: this.connection.user_id,
					remote_id: item.fileId,
					type: 'file'
				};

				if (!_.has(objectCache.content, newFile.identifier)) {
					objectCache.content[newFile.identifier] = newFile;

					localFiles.push(objectCache.content[newFile.identifier]);
					localFilesIds[newFile.identifier] = true;

					content.push(objectCache.content[newFile.identifier]);
				}
				else {
					if (!_.has(localFilesIds, newFile.identifier)) {
						localFiles.push(objectCache.content[newFile.identifier]);
						localFilesIds[newFile.identifier] = true;
					}
				}

				let newEvent = {
					type: 'edited',
					context: 'Deleted file',
					provider_name: 'google',
					identifier: this.connection._id.toString('hex') + ':::deleted:::google:::drive:::' + item.fileId,
					datetime: moment(item.time).utc().toDate(),
					content: [objectCache.content[newFile.identifier]],
					connection: this.connection._id,
					user_id: this.connection.user_id
				};

				events.push(newEvent);
			}
			else {
				if (item.file.mimeType !== 'application/vnd.google-apps.folder') {
					let newTags = [];
					let titleTags = item.file.name.match(tagRegex);

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

					newFile = {
						identifier: this.connection._id.toString('hex') + ':::drive:::' + item.fileId,
						connection: this.connection._id,
						user_id: this.connection.user_id,
						url: item.file.webViewLink,
						remote_id: item.fileId,
						embed_thumbnail: item.file.thumbnailLink,
						'tagMasks.source': newTags,
						title: item.file.name,
						type: 'file',
						mimetype: item.file.fullFileExtension != null ? item.file.fullFileExtension : item.file.mimeType
					};

					if (!_.has(objectCache.content, newFile.identifier)) {
						objectCache.content[newFile.identifier] = newFile;

						localFiles.push(objectCache.content[newFile.identifier]);
						localFilesIds[newFile.identifier] = true;

						content.push(objectCache.content[newFile.identifier]);
					}
					else {
						if (!_.has(localFilesIds, newFile.identifier)) {
							localFiles.push(objectCache.content[newFile.identifier]);
							localFilesIds[newFile.identifier] = true;
						}
					}

					let newEvent = {
						type: 'edited',
						provider_name: 'google',
						identifier: this.connection._id.toString('hex') + ':::edited:::google:::drive:::' + item.fileId,
						content: [objectCache.content[newFile.identifier]],
						connection: this.connection._id,
						user_id: this.connection.user_id
					};

					if (item.file.viewedByMeTime) {
						newEvent.datetime = moment(item.file.viewedByMeTime).utc().toDate();
					}
					else {
						newEvent.datetime = moment(item.file.createdTime).utc().toDate();
					}

					if (item.file.permissions) {
						for (let j = 0; j < item.file.permissions.length; j++) {
							let filePermission = item.file.permissions[j];

							if (filePermission.type === 'user' && !filePermission.me && filePermission.emailAddress) {
								newContact = {
									identifier: this.connection._id.toString('hex') + ':::' + filePermission.emailAddress,
									connection: this.connection._id,
									user_id: this.connection.user_id,
									handle: filePermission.emailAddress,
									name: filePermission.displayName,
									updated: moment().utc().toDate()
								};
								if (!_.has(objectCache.contacts, newContact.identifier)) {
									objectCache.contacts[newContact.identifier] = newContact;

									localContacts.push(objectCache.contacts[newContact.identifier]);
									localContactsIds[newContact.identifier] = true;

									contacts.push(objectCache.contacts[newContact.identifier]);
								}
								else {
									if (!_.has(localContactsIds, newContact.identifier)) {
										localContacts.push(objectCache.contacts[newContact.identifier]);
										localContactsIds[newContact.identifier] = true;
									}
								}

								newEvent.contacts = localContacts;
								newEvent.contact_interaction_type = 'with';
							}
						}
					}

					events.push(newEvent);
				}
			}
		}

		if (events.length > 0) {
			return mongoTools.mongoInsert({
				contacts: contacts,
				content: content,
				events: events,
				tags: tags
			});
		}
		else {
			return Promise.resolve(null);
		}
	}
	else {
		return Promise.resolve(null);
	}
};
