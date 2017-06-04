'use strict';

const Promise = require('bluebird');

const mongoTools = require('../../../util/mongo-tools');


module.exports = function(data) {
	var events;

	events = [];

	if (data && data.length > 0) {
		for (let i = 0; i < data.length; i++) {
			let item = data[i];

			if (item.value > 0) {
				for (let j = 0; j < item.sleep_today.length; j++) {
					let sleep = item.sleep_today[j];

					let newEvent = {
						type: 'slept',
						provider_name: 'fitbit',
						identifier: this.connection._id.toString('hex') + ':::slept:::fitbit:::' + sleep.logId,
						datetime: sleep.startTime,
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
