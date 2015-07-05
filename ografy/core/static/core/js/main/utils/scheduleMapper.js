//Module scheduleMapper
//This module contains functions for updating the endpoint of signals that are past their update frequency or that have never been pulled at all.
define ('scheduleMapper', function(require, exports, module) {
	var csrftoken;
	var estimation_method;
	/**
	 * Starts the process of getting the user's signals and calling the endpoints if their information is out-of-date
	 *
	 * @param {Integer} userId  The ID of the current user
	 */
	//TODO: Get userId from user endpoint and not signal
	function run(userId) {
		var signals;
		var signalsToRun = [];

		$.when(getSignals(signals)).done(function(signals, endpoints) {
			signalsToRun = checkAllSignalsLastRun(signals);
			if (signalsToRun.length > 0) {
				$.when(getEndpoints(signalsToRun, endpoints)).done(function(endpoints) {
					callEndpointsAndClean(endpoints.results, signalsToRun);
				});
				_.forEach(signalsToRun, function(signal) {
					var data = {};
					data.last_run = new Date().toJSON();
					$.ajax({
						url: 'opi/signal/' + signal.id,
						type: 'PATCH',
						data: data,
						dataType: 'json',
						headers: {
							'X-CSRFToken': csrftoken
						}
					}).done(function(data, xhr, response) {
						signals = data;
					});
				});
			}
		});
	}

	/**
	 * Runs the process of getting information for signals that are past their update frequency.
	 * Then sets a timer to run the process again at an interval specified as an input
	 *
	 * @param {Integer} time_ms  How often, in ms, this module should check
	 * @param {Integer} user_id  The ID of the current user
	 * @param {String} user_estimation_method The current user's method for estimating locations
	 * @param {String} csrfToken The user's csrf token
	 */
	//Schedules
	function schedule(time_ms, user_id, user_estimation_method, csrfToken) {
		csrftoken = csrfToken;
		estimation_method = user_estimation_method;
		run(user_id);
		setInterval(function() {
			run(user_id);
		}, time_ms);
	}

	/**
	 * Gets all of the user's signals from the database
	 *
	 * @param {Object} signals The list where the user's signals will be stored
	 * @returns {Object} A list of all the signals for the current user
	 */
	function getSignals(signals) {
		return $.ajax({
			url: 'opi/signal',
			type: 'GET',
			dataType: 'json',
			headers: {
				'X-CSRFToken': csrftoken
			}
		}).done(function(data, xhr, response) {
			signals = data;
		}).fail(function(data, xhr, response) {
			console.log('Failed initial signal GET');
		});
	}

	/**
	 * Iterates through each signal and calls checkOneSignalLastRun on each active one
	 *
	 * @param {Object} signalsList A list of all of the active signals for the current user
	 * @returns {Object} A list of all the signals that are out-of-date or new and therefore need to be run
	 */
	function checkAllSignalsLastRun(signalsList) {
		var signalsToRun = [];
		_.forEach(signalsList, function(signal) {
			if (signal.enabled) {
				var signalOutdated = checkOneSignalLastRun(signal);
				if (signalOutdated) {
					signalsToRun.push(signal);
				}
			}
		});
		return signalsToRun;
	}

	/**
	 * Checks the given signal's last_run field.
	 * If it's 'None', that means the signal has never had data pulled from its endpoints and needs to run through each enabled endpoint and pull all available data.
	 *
	 * If it's not, then last_run will be a datetime indicating when the endpoints were last hit.
	 *
	 * @param {Object} signal One of the user's active signals
	 * @returns {Boolean} Whether or not this signal needs to be run
	 */
	function checkOneSignalLastRun(signal) {
		//If last_run is 'None', then it is new and needs to be run
		if (signal.last_run === 'None' || signal.last_run === null) {
			return true;
		}
		//If last_run is not 'None', then check if the signal is out-of-date
		else {
			var oneDayAgo = new Date();
			var oneWeekAgo = new Date();

			oneDayAgo.setDate(oneDayAgo.getDate() - 1);
			oneDayAgo = oneDayAgo.toJSON();
			oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
			oneWeekAgo = oneWeekAgo.toJSON();

			return ((signal.frequency === 1 && signal.last_run < oneDayAgo) || (signal.frequency === 2 && signal.last_run < oneWeekAgo));
		}
	}

	/**
	 * Gets all of the Permissions for the given list of signals
	 *
	 * @param {Object} signals A list of the signals that need to be updated
	 * @param {Object} endpoints A list of the endpoints that will be filled by the results of the API call
	 * @returns {Object} A list of the endpoints that are associated with the input signals
	 */
	function getEndpoints(signals, endpoints) {
		var filterString = '';
		var firstIteration = true;

		//TODO: Does signal return endpoint list? Call getting endpoints using SET.
		_.forEach(signals, function(signal) {
			if (!firstIteration) {
				filterString += ' or ';
			}
			else {
				firstIteration = false;
			}
			filterString += '(signal exact ' + _.get(signal, 'id') + ')';
		});
		return $.ajax({
			url: 'opi/permissions?filter=' + filterString,
			type: 'GET',
			dataType: 'json',
			headers: {
				'X-CSRFToken': csrftoken
			}
		}).done(function(data, xhr, response) {
			endpoints = data;
		});
	}

	function parseSubMapping(dataDict, dataMap) {
		var field_location = _.get(dataMap, 'field_location');
		var transform = _.get(dataMap, 'transform');
		var transform_type = _.get(transform, 'type');

		if (transform_type === 'client_evaluate') {
			return _.get(dataDict, field_location);
		}
		else if (transform_type === 'reformat') {
			var transform_value = _.get(transform, 'value');
			return transform_value.replace('[$1]', _.get(dataDict, transform_value));
		}
		else {
			return field_location;
		}
	}


	/**
	 * Iterates through all of the Permissions for the given signal and calls callOneEndpoint on each one
	 *
	 * @param {Object} endpoints A list of all of the Permissions for the given signal.
	 * @param {Array} signals A list of all of the Permissions for the given signal.
	 */
	function callEndpointsAndClean(endpoints, signals) {
		_.forEach(endpoints, function(endpoint) {
			var endpointSignal = _.where(signals, { id: endpoint.signal.id })[0];
			callOneEndpoint(endpoint, endpointSignal);
		});
	}

	/**
	 * Call the endpoint as defined in the given Permission
	 *
	 * @param {Object} endpoint One of the Permissions for the given signal
	 * @param {Object} signal
	 * @returns {Object} The raw data returned from the endpoint
	 */
	function callOneEndpoint(endpoint, signal) {
		var url = 'https://p.ografy.io/call';
		var call_parameters = {};
		var parameter_list = _.get(endpoint, 'endpoint.parameter_description');
		var mapping = _.get(endpoint, 'endpoint.mapping');

		// Add parameters from endpoint definition to URL
		_.forEach(parameter_list, function(value, parameter) {
			call_parameters[parameter] = parseSubMapping(signal, value);
		});

		var callData = {
			permission_id: endpoint.id,
			parameters: JSON.stringify(call_parameters)
		};

		// Call the endpoint using its ID and parameters
		// Note the 'xhrFields' option; withCredentials:true allows for ajax to send cookies, particularly
		// the sessionid, as part of a cross-domain call.
		// The server must return the header 'Access-Control-Allow-Credentials' set to true for this to work.
		// Additionally, the header 'Access-Control-Allow-Origin' must be sent by the server and must be something
		// other than the wildcard '*' for this to work.
		$.ajax({
			url: url,
			type: 'GET',
			data: callData,
			dataType: 'text',
			headers: {
				'X-CSRFToken': csrftoken
			},
			xhrFields: {
				withCredentials: true
			}
		}).done(function(data, xhr, response) {
			var responseData = JSON.parse(data);
			mapModels(mapping, responseData, signal, endpoint);
		}).fail(function(data, xhr, response) {
			console.log('Signal call failure');
		});
	}

	/**
	 * Transform the raw data returned from the endpoint into Ografy's format, then post that data to the database.
	 *
	 * @param {Object} mapping The mapping of how the data retrieved from this endpoint matches to Ografy's Data schema
	 * @param {Object} responseData The data returned from the endpoint API
	 * @param {Object} signal
	 */
	function mapModels(mapping, responseData, signal, endpoint) {
		var propertyLocation = _.get(mapping, 'property_location');
		//If it's a list
		if (_.get(mapping, 'list.field_mapping')) {
			var responseObjects;

			//If the property_location field is a blank string, then the list is what the endpoint returned
			if (propertyLocation.field_mapping.length === 0) {
				responseObjects = responseData;
			}
			//Otherwise, the list of returned data is nested inside the object that the endpoint returned
			else {
				responseObjects = _.get(responseData, propertyLocation.field_mapping);
			}

			_.forEach(responseObjects, function(responseObject) {
				mapSingleModel(mapping, responseObject, signal, endpoint);
			});
			//If single object
		}
		else {
			mapSingleModel(mapping, _.get(responseData, propertyLocation.field_mapping), signal, endpoint);
		}
	}

	/**
	 * Transform the raw data returned from the endpoint into Ografy's format, then post that data to the database.
	 *
	 * @param {Object} mapping The mapping of how the data retrieved from this endpoint matches to Ografy's Data schema
	 * @param {Object} itemData The data returned from the endpoint API
	 * @param {Object} signal
	 * @param {Object} endpoint
	 */
	//TODO: Abstract posting into a callback passed into mapping a single model or after the mapping function returns the result
	function mapSingleModel(mapping, itemData, signal, endpoint) {
		var fieldMapping = _.get(mapping, 'field_mapping');
		var locationEstimated;
		var dataTypeMapping = _.get(fieldMapping, 'event');
		var dateNow = new Date();
		var datetime = _.get(dataTypeMapping, 'datetime');

		dateNow = dateNow.toJSON();
		//If a datetime is present, convert it to JSON format.
		if (datetime !== undefined) {
			datetime = new Date(parseSubMapping(itemData, datetime)).toJSON();
		}
		//If a datetime is not present, use the current time and convert it to JSON format.
		else {
			datetime = new Date().toJSON();
		}

		$.when(mapEvent(signal, itemData, datetime, fieldMapping)).done(function(event) {
			if (!(locationEstimated)) {
				mapLocation(fieldMapping, event);
			}
			$.when(mapData(itemData, event, signal)).done(function(data) {
				if (Object.keys(fieldMapping).length > 1) {
					mapSubtype(fieldMapping, data.event, signal, itemData);
				}
			});
		});


		function mapData(itemData, event, signal) {
			//Map Data Object
			//FIXME: Update Data Object with Event ID. Change Schema?
			var dateNow = new Date();
			dateNow = dateNow.toJSON();
			var dataObject = {
				created: dateNow,
				data_blob: itemData,
				event: event.id,
				updated: dateNow,
				user_id: signal.user_id
			};

			return $.ajax({
				url: 'opi/data',
				type: 'POST',
				data: JSON.stringify(dataObject),
				dataType: 'json',
				contentType: 'application/json; charset=utf-8',
				headers: {
					'X-CSRFToken': csrftoken
				}
			}).done(function(data, xhr, response) {
				console.log('Data Object mapped and posted successfully');
			});
		}

		function mapLocation(fieldMapping, event) {
			var locationObject = {
				source: event.id.toString()
			};

			var locationMapping = _.get(fieldMapping, 'location');

			_.forEach(locationMapping, function(fieldValue, fieldKey) {
				locationObject[fieldKey] = parseSubMapping(event, fieldValue);
			});

			locationObject.datetime = new Date(locationObject.datetime).toJSON();

			$.ajax({
				url: 'opi/location',
				type: 'POST',
				data: JSON.stringify(locationObject),
				dataType: 'json',
				contentType: 'application/json; charset=utf-8',
				headers: {
					'X-CSRFToken': csrftoken
				}
			}).done(function(data, xhr, response) {
				console.log('Location mapped and posted successfully');
			});
		}

		//TODO: Make entire parent function more programmatic, better debug success/fail messages with ids?
		function mapEvent(signal, itemData, datetime, mappingLocation) {
			var eventObject, tempCoordinates, tempLocation;

			tempCoordinates = _.get(itemData, _.get(mapping, mappingLocation));

			if (tempCoordinates !== undefined && tempCoordinates !== null) {
				tempLocation = {
					estimated: true,
					estimation_method: 'Between',
					geo_format: 'lat_lng',
					geolocation: {
						type: 'Point',
						coordinates: tempCoordinates
					}
				};
				locationEstimated = false;
			}
			else {
				locationEstimated = true;
				tempLocation = {};
			}

			eventObject = {
				permission: endpoint.id,
				created: dateNow,
				datetime: datetime,
				event_type: _.get(mapping, 'event_type.field_mapping'),
				location: tempLocation,
				name: parseSubMapping(itemData, _.get(dataTypeMapping, 'name')),
				provider: signal.provider.id,
				provider_name: signal.provider.name,
				signal: signal.id,
				updated: dateNow,
				user_id: signal.user_id
			};

			return $.ajax({
				url: 'opi/event',
				type: 'POST',
				data: JSON.stringify(eventObject),
				dataType: 'json',
				contentType: 'application/json; charset=utf-8',
				headers: {
					'X-CSRFToken': csrftoken
				}
			}).done(function(data, xhr, response) {
				console.log('Event Object mapped and posted successfully');
			}).fail(function(data, xhr, response) {
				console.log('Event Object mapping failed');
			});
		}

		function mapSubtype(fieldMapping, event, signal, itemData) {
			var subEventObject = {
				event: event.id,
				user_id: signal.user_id
			};
			var dataType = event.event_type;
			var dataTypeMapping = _.get(fieldMapping, dataType);

			_.forEach(dataTypeMapping, function(fieldValue, fieldKey) {
				subEventObject[fieldKey] = parseSubMapping(itemData, fieldValue);
			});

			return $.ajax({
				url: 'opi/' + dataType,
				type: 'POST',
				data: JSON.stringify(subEventObject),
				dataType: 'json',
				contentType: 'application/json; charset=utf-8',
				headers: {
					'X-CSRFToken': csrftoken
				}
			}).done(function(data, xhr, response) {
				console.log('Event subtype ' + dataType + ' mapped and posted successfully');
			});
		}
	}

	module.exports = {
		schedule: schedule,
		run: run,
		getSignals: getSignals,
		checkAllSignalsLastRun: checkAllSignalsLastRun,
		checkOneSignalLastRun: checkOneSignalLastRun,
		callEndpointsAndClean: callEndpointsAndClean,
		callOneEndpoint: callOneEndpoint,
		mapSingleModel: mapSingleModel,
		mapModel: mapModels
	};
});
