'use strict';

const Promise = require('bluebird');
const moment = require('moment');

const mongoTools = require('explorer/lib/util/mongo-tools');


module.exports = function(data) {
	var things, events, objectCache;

	objectCache = {
		thing: {
			index: {
				_index: 'core',
				_type: 'things'
			}
		}
	};

	things = [];
	events = [];

	if (data && data.length > 0) {
		for (let i = 0; i < data.length; i++) {
			let item = data[i];

			if (item.value > 0) {
				for (let j = 0; j < item.food_today.length; j++) {
					let food = item.food_today[j];

					let newFood = {
						identifier: this.connection._id.toString('hex') + ':::fitbit:::' + food.loggedFood.brand + ':::' + food.loggedFood.name,
						connection: this.connection._id,
						user_id: this.connection.user_id,
						title: food.loggedFood.brand,
						text: food.loggedFood.name,
						type: 'food'
					};

					objectCache.things[newFood.identifier] = newFood;
					things.push(objectCache.things[newFood.identifier]);

					let newEvent = {
						type: 'ate',
						provider_name: 'fitbit',
						identifier: this.connection._id.toString('hex') + ':::ate:::fitbit:::' + food.logId,
						things: [objectCache.things[newFood.identifier]],
						connection: this.connection._id,
						user_id: this.connection.user_id
					};

					switch(food.loggedFood.mealTypeId) {
						case(1):
							newEvent.datetime = moment(food.logDate + 'T08:00:00.000Z').utc().toDate();
							break;

						case(2):
							newEvent.datetime = moment(food.logDate + 'T10:00:00.000Z').utc().toDate();
							break;

						case(3):
							newEvent.datetime = moment(food.logDate + 'T12:00:00.000Z').utc().toDate();
							break;

						case(4):
							newEvent.datetime = moment(food.logDate + 'T15:00:00.000Z').utc().toDate();
							break;

						case(5):
							newEvent.datetime = moment(food.logDate + 'T19:00:00.000Z').utc().toDate();
							break;

						default:
							newEvent.datetime = moment(food.logDate + 'T16:00:00.000Z').utc().toDate();
							break;
					}

					events.push(newEvent);
				}
			}
		}

		return mongoTools.mongoElasticInsert({
			events: events,
			things: things
		});
	}
	else {
		return Promise.resolve(null);
	}
};
