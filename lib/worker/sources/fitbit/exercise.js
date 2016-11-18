'use strict';

const Promise = require('bluebird');
const moment = require('moment');

const mongoTools = require('explorer/lib/util/mongo-tools');


module.exports = function(data) {
	var events;

	events = [];

	if (data && data.length > 0) {
		for (let i = 0; i < data.length; i++) {
			let item = data[i];

			if (item.value > 0) {
				for (let j = 0; j < item.activities_today.length; j++) {
					let activity = item.activities_today[j];

					let newEvent = {
						type: 'exercised',
						provider_name: 'fitbit',
						identifier: this.connection._id.toString('hex') + ':::exercised:::fitbit:::' + activity.logId,
						datetime: moment(item.dateTime + 'T' + activity.startTime + ':00.000Z').utc().toDate(),
						connection: this.connection._id,
						user_id: this.connection.user_id
					};

					events.push(newEvent);
				}
			}
		}

		return mongoTools.mongoElasticInsert({
			events: events
		});
	}
	else {
		return Promise.resolve(null);
	}
};
