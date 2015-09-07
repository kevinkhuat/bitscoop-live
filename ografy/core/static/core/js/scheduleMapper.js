//Module scheduleMapper
//This module contains functions for updating the eventSource of signals that are past their update frequency or that have never been pulled at all.
define ('scheduleMapper', ['jquery', 'lodash', 'jquery-cookie', 'jquery-deparam'], function($, _) {
	var signals, signalsToRun, permissions;
	var eventSources = [];
	var endpointCache = {};


	/**
	 * Starts the process of getting the user's signals and calling the eventSources if their information is out-of-date
	 *
	 * @param {Integer} userId  The ID of the current user
	 */
	//TODO: Get userId from user eventSource and not signal
	function run(userId) {
		endpointCache = {};
		$.when(_getSignals(signals)).done(function() {
			_checkAllSignalsLastRun();
			if (signalsToRun.length > 0) {
				_processSignals();
			}
		});
	}

	/**
	 * Runs the process of getting information for signals that are past their update frequency.
	 * Then sets a timer to run the process again at an interval specified as an input
	 *
	 * @param {Integer} time_ms  How often, in ms, this module should check
	 * @param {Integer} user_id  The ID of the current user
	 */
	//Schedules
	function schedule(time_ms, user_id) {
		run(user_id);
		setInterval(function() {
			run(user_id);
		}, time_ms);
	}

	/**
	 * Gets all of the user's signals from the database
	 *
	 * @returns {Object} A list of all the signals for the current user
	 */
	function _getSignals() {
		return $.ajax({
			url: 'opi/signal',
			type: 'GET',
			dataType: 'json',
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			}
		}).done(function(data, xhr, response) {
			signals = data;
		}).fail(function(data, xhr, response) {
			console.log('Failed initial signal GET');
		});
	}

	/**
	 * Iterates through each signal and calls _checkOneSignalLastRun on each active one
	 *
	 * @returns {Object} A list of all the signals that are out-of-date or new and therefore need to be run
	 */
	function _checkAllSignalsLastRun() {
		signalsToRun = [];
		_.forEach(signals, function(signal) {
			if (signal.enabled) {
				var signalOutdated = _checkOneSignalLastRun(signal);
				if (signalOutdated) {
					signalsToRun.push(signal);
				}
			}
		});
	}

	/**
	 * Checks the given signal's last_run field.
	 * If it's 'None', that means the signal has never had data pulled from its eventSources and needs to run through each enabled eventSource and pull all available data.
	 *
	 * If it's not, then last_run will be a datetime indicating when the eventSources were last hit.
	 *
	 * @param {Object} signal One of the user's active signals
	 * @returns {Boolean} Whether or not this signal needs to be run
	 */
	function _checkOneSignalLastRun(signal) {
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
	 * This is used to extract data from a context based on an input propertyMapping.
	 * There are several different hydration methods.
	 *
	 * @param {Object} context The context for this endpoint call
	 * @param {Object} propertyMapping The mapping to be used to retrieve data from this context
	 * @returns {Object} Can be a string, an int, an array, or a promise
	 */
	function _hydrateField(context, propertyMapping) {
		var value = _.get(propertyMapping, 'value');
		var hydration_method = _.get(propertyMapping, 'hydration_method');
		var type = _.get(propertyMapping, 'type');
		var encoded = _.get(propertyMapping, 'encoded');

		//Hydration method translate
		if (hydration_method === 'translate') {
			var returnList = [];

			//If this property is supposed to be returned as a list
			if (type === 'list') {
				var values = _.get(context, value);

				//If there is more than one object, push them onto returnList separately
				if (typeof values === 'object') {
					_.forEach(values, function(value) {
						returnList.push(value);
					});
				}
				//If there is just one object, push it onto returnList
				else {
					returnList.push(values);
				}

				return returnList;
			}
			//If you need to construct a list out of multiple separate fields; for example,
			//Instagram does not return coordinates in an array, but rather two separate key-value pairs
			//for longitude and latitude, and we need to put them into an array.
			//In this situation, value needs to be an array where each entry is the path to the field to be mapped.
			else if (type === 'multi_value') {
				_.forEach(value, function(single_value) {
					var coordinate = _.get(context, single_value);
					returnList.push(coordinate);
				});

				return returnList;
			}
			//If this property is not returned as a list
			else {
				var returnValue;

				//Sometimes a value can potentially be in different places, such as the message body in Gmail.
				//In this case, value should be an array of the locations where the data could be.
				//This will iterate through each potential spot and stop as soon as it finds something other
				//than undefined or false.  False was created in response to reddit's edited field, which is false
				//if something hasn't been edited and a datetime if it has.
				if (typeof value === 'object') {
					var valueMatchFound = false;

					//Iterate through each possible field
					_.forEach(value, function(potential_value) {
						var tempHydration = _.get(context, potential_value);

						//If there is data in this spot, and you haven't already found data, set returnValue
						//and mark that you have found the data.
						if (tempHydration !== undefined && tempHydration !== false && !(valueMatchFound)) {
							returnValue = tempHydration;
							valueMatchFound = true;
						}
					});

					return returnValue;
				}
				//If there is only one place to find the data, and it's not to be returned as a list
				else {
					returnValue = _.get(context, value);

					//Mongoengine does not like empty strings for values.  In this case, just return undefined,
					//so that the field is not set at all.
					if (returnValue === '') {
						return undefined;
					}
					//If none of the above are true, return the value
					else {
						return returnValue;
					}
				}
			}
		}
		//If the data is coming from a parent endpoint, just get whatever the value is from the context
		else if (hydration_method === 'parent_endpoint') {
			return _.get(context, value);
		}
		//Sometimes the data needs to be retrieved from an endpoint that may have not been called yet.
		//This option will return a promise because we need to wait for the ajax call to the endpoint to finish.
		else if (hydration_method === 'endpoint') {
			var endpoint = _.get(context.endpoints, _.get(propertyMapping, 'value.endpoint'));
			var deferred = $.Deferred();
			var finalResponse;

			//Call the endpoint and pass through the data
			$.when(_callOneEndpoint(endpoint, context, {})).done(function(data) {
				var response = JSON.parse(data);

				//There may be more than one spot where the data can be stored
				_.forEach(propertyMapping.value.value_location, function(potential_value_location) {
					var tempResponse = JSON.parse(data);

					//Whittle down the full responseObject until you get to the data you're looking for
					_.forEach(potential_value_location, function(item) {
						//If the current mapping level is an object, then it will contain special instructions
						//for calling hydrateField, so you call hydrateField with that mapping
						if (typeof item === 'object') {
							context.childResponseObject = tempResponse;
							tempResponse = _hydrateField(context, item);
						}
						//If the current level is not an object, it'll be a string with the key tree to get to either
						//the right field or an array
						else {
							tempResponse = _.get(tempResponse, item);
						}
					});

					//If there is data where it was expected, set that data to finalResponse
					if (tempResponse !== undefined) {
						finalResponse = tempResponse;
					}
				});

				//Google sometimes returns lists of names in a comma-separated string instead of an array.
				//We want to work with arrays, so split the string on commas and trim the whitespace that results.
				if (type === 'list') {
					finalResponse = finalResponse.split(',');
					_.forEach(finalResponse, function(responseItem) {
						responseItem.trim();
					});
				}

				//Gmail message bodies are encoded, so decode them
				if (encoded === true) {
					try {
						//Gmail uses characters not in standard 64-bit encoding, so replace them with the 64-bit
						//characters before decoding the message
						deferred.resolveWith(this, [atob(finalResponse.replace(/-/g, '+').replace(/_/g, '/'))]);
					}
					catch(err) {
						console.log('Error: ' + err);
					}
				}
				else {
					//If the response is not encoded, just resolve the promise with the response
					deferred.resolveWith(this, [finalResponse]);
				}
			});

			//Return a promise.  It will not be resolved until the endpoint has been called and the data that was
			//returned has been parsed and formatted.
			return deferred.promise();
		}
		//This finds the one object in an array of objects that has a field value matching an input
		else if (hydration_method === 'find') {
			var selectorValue, selectorLocation;
			var selectorType = _.get(propertyMapping, 'selector_type');

			if (selectorType === 'translate') {
				selectorValue = _.get(context, _.get(propertyMapping, 'selector'));
			}
			else {
				selectorValue = _.get(propertyMapping, 'selector');
			}

			selectorLocation = _.get(propertyMapping, 'selector_location');

			return _.find(context.childResponseObject, function(item) {
				return selectorValue == _.get(item, selectorLocation);
			});
		}
		//If you need to add a variable to an otherwise static string
		//The variable will be inserted in place of [$1]
		else if (hydration_method === 'reformat') {
			var hydration_location = _.get(propertyMapping, 'hydration_location');

			return value.replace('[$1]', _.get(context, hydration_location));
		}
		//If the value is static, just pass back the value
		else if (hydration_method === 'literal') {
			return value;
		}
		//If the value needs to be provided by the server, just pass back the value that's there.
		//That value will be parsed by the server
		else if (hydration_method === 'server') {
			return value;
		}
		//If all else fails, return undefined.
		else {
			return undefined;
		}
	}

	/**
	 * Iterates through each signal to be run and calls processPermissions on them.
	 *
	 */
	function _processSignals() {
		_.forEach(signalsToRun, function(signalToRun) {
			_processPermissions(signalToRun);
		});
	}

	/**
	 * Iterates through all of the Permissions for the given signal and calls _processEventSource on each one
	 *
	 */
	function _processPermissions(signalToRun) {
		var permissionPromiseList = [];

		_.forEach(signalToRun.permissions, function(permission) {
			if (permission.enabled) {
				var eventSource = permission.event_source;
				var permissionDeferred = $.Deferred();

				//Each enabled permission will have a promise created for it.  This promise will only be resolved
				//if its event source runs successfully.
				permissionDeferred.promise();
				permissionPromiseList.push(permissionDeferred);

				$.ajax({
					url: 'opi/provider/' + signalToRun.provider,
					type: 'GET',
					dataType: 'json',
					headers: {
						'X-CSRFToken': $.cookie('csrftoken')
					}
				}).done(function(data, xhr, response) {
					signalToRun.provider = data;

					//Crude rate limiting
					//If the provider says to wait n seconds between calls, then wait n seconds between starting each event source.
					if (signalToRun.provider.hasOwnProperty('endpoint_wait_time')) {
						var timeoutTime = _.get(signalToRun.provider, 'endpoint_wait_time') * 1000;
						setTimeout(function() {
							_processEventSource(eventSource, signalToRun, permission, permissionDeferred);
						}, timeoutTime);
					}
				}).fail(function(data, xhr, response) {
					console.log('Failed initial signal GET');
				});
			}
		});

		//When all of a signal's permissions have run successfully, update the signal's lastRun field to the
		//the current datetime.  If any of them fail at any point, lastRun will not be updated so that we
		//do not lose any data.
		$.when.apply($, permissionPromiseList).done(function() {
			var data = {};

			data.last_run = new Date().toJSON();

			$.ajax({
				url: 'opi/signal/' + signalToRun.id,
				type: 'PATCH',
				data: data,
				dataType: 'json',
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				}
			}).done(function(data, xhr, response) {
				console.log('Signal ' + signalToRun.id + ' lastRun updated successfully');
			});
		});
	}

	/**
	 * Get data from an eventSource
	 *
	 * @param {Object} eventSource One of the eventSource
	 * @param {Object} signal The Signal associated with the permission that is calling this eventSource
	 * @param {Object} permission The Permission that is calling this eventsource
	 * @param {Object} permissionDeferred A promise that the event source will resolve when it is finished gathering data
	 * @returns {Object} The raw data returned from the eventSource
	 */
	function _processEventSource(eventSource, signal, permission, permissionDeferred) {
		//This is the mapping of fields
		var context = {
			endpoints: _.get(eventSource, 'endpoints'),
			mappings: _.get(eventSource, 'mappings'),
			signal: signal,
			permission: permission
		};

		var endpointAndMappingName = _.get(eventSource, 'initial_mapping');
		var initialMapping = _.get(context.mappings, endpointAndMappingName);

		//Start the mapping process with the initial endpoint mapping
		_processMapping(initialMapping, endpointAndMappingName, {}, undefined);

		function _processMapping(mapping, endpointName, parentResponseObject, inputDeferred) {
			var firstPass = true;
			var loopEnd = false;
			var responseData, responseObjectsList;

			//These are the variables relating to pagination
			var paginationAscending, paginationStartParameter, paginationEndParameter, paginationCheckMore, paginationVariableCursor, nextCursorLocation, cursorValue, newCursorStartValue, newCursorEndValue;
			var pageTokenLocation, nextPageLocation;
			var parameter_descriptions;
			var pagination = _.get(context.mappings, 'pagination');
			var paginationMethod = _.get(pagination, 'method');

			var endpoint = _.get(context.endpoints, endpointName);
			var eventSourcePromiseList = [];

			if (paginationMethod === 'cursor') {
				nextCursorLocation = _.get(pagination, 'next_cursor_location');
				paginationAscending = _.get(pagination, 'is_ascending');
				paginationStartParameter = _.get(pagination, 'start_cursor_parameter');
				paginationEndParameter = _.get(pagination, 'end_cursor_parameter');
				paginationCheckMore = _.get(pagination, 'check_if_more');
				paginationVariableCursor = _.get(pagination, 'variable_cursor');
				cursorValue = _.get(pagination, 'cursor_value');
			}
			else if (paginationMethod === 'pageToken') {
				pageTokenLocation = _.get(pagination, 'page_token_location');
			}
			else if (paginationMethod === 'nextPage' || paginationMethod === 'rfc5988') {
				nextPageLocation = _.get(pagination, 'next_link_location');
			}

			_processOneEndpointIteration(endpoint, mapping, context);

			/**
			 * Process one call of an endpoint
			 * At the end, it will check to see if it needs to be called again
			 */
			function _processOneEndpointIteration(endpoint, mapping, context) {
				//Call the endpoint, and when it is done act on the data that was passed back
				$.when(_callOneEndpoint(endpoint, context)).done(function(data) {
					var returnedDataLocation = _.get(mapping, 'returned_data_location');
					var patchData = {};
					var localDeferred;
					var conditionMapping = _.get(mapping, 'conditions');

					if (inputDeferred === undefined) {
						localDeferred = $.Deferred();
						localDeferred.promise();
						eventSourcePromiseList.push(localDeferred);
					}
					else {
						localDeferred = inputDeferred;
					}

					responseData = JSON.parse(data);

					//Extract the data we need from the response data
					//If returnedDataLocation is blank, that indicates that the top-level responseData is what we need, so do nothing.
					if (returnedDataLocation.length === 0) {
						responseObjectsList = responseData;
					}
					//Otherwise, the list of returned data is nested inside the object that the endpoint returned
					else {
						responseObjectsList = _.get(responseData, returnedDataLocation);
					}

					//Iterate through each mappable object that was returned
					_.forEach(responseObjectsList, function(responseObject) {
						var skipPost = false;
						
						//If there are any conditions
						_.forEach(conditionMapping, function(condition) {
							var conditionKey = Object.keys(condition)[0];
							var conditionVal = condition[conditionKey].value;
							var conditionField = condition[conditionKey].field;

							//Property exists
							//	Property equals
							if (conditionKey === 'equals') {
								if (_.get(context, conditionField) !== conditionVal) {
									skipPost = true;
								}
							}
							else if (conditionKey === 'notEquals') {
								if (_.get(responseObject, conditionField) === conditionVal) {
									skipPost = true;
								}
							}
							//	Property less than
							//	Property greater than
							//	Property typeof
						});

						if (!(skipPost)) {
							//If this endpoint was called solely to get data for another endpoint, call that endpoint
							if (mapping.hasOwnProperty('submapping')) {
								var endpointAndMappingName = _.get(mapping, 'submapping.endpoint');
								var newMapping = _.get(context.mappings, endpointAndMappingName);

								responseObject.parentResponseObject = parentResponseObject;
								context.responseObject = responseObject;

								_processMapping(newMapping, endpointAndMappingName, responseObject, localDeferred);
							}
							//Otherwise, update the global context and call mapSingleModel
							else {
								var localContext = $.extend({}, context);
								localContext.endpoint = endpoint;
								localContext.mapping = mapping;
								localContext.responseObject = responseObject;
								localContext.parentResponseObject = parentResponseObject;

								mapSingleModel(localContext, localDeferred);
							}
						}
						else {
							localDeferred.resolve();
						}
					});

					$.when(localDeferred).done(function() {
						//Some APIs use a cursor for their 'pagination'.  This cursor is usually the ID of an object that
						//API provides.  It can be used to get items that have IDs before or after that cursor.
						if (paginationMethod === 'cursor') {
							//Some cursor-based services, such as Twitter, start with the most recent changes.
							//This requires that you save the ID of the most recent item on your first pass through the data
							//so that the next time you call this event source you start from that most recent change.
							//You also have to save the ID of the oldest result in each iteration and use that as the endpoint
							//for further calls to the iteration, working your way from newest to oldest.
							if (firstPass && !(paginationAscending)) {
								//If there is at least one new data point, set the new start cursor to the appropriate value
								if (responseObjectsList.length > 0) {
									newCursorStartValue = _.get(responseObjectsList[0], cursorValue);
								}
								//If not, then newCursorStartValue needs to remain the same
								else {
									newCursorStartValue = _.get(context.signal.endpoint_data[eventSource.name][endpointName], paginationStartParameter);
								}

								firstPass = false;
							}

							//There are multiple ways that cursor-based pagination can be handled.  In some cases, all you
							//know is how many items you got back on this iteration, but not how many there should be in total.
							//In this situation, you have to iterate until you have gotten fewer items back than the maximum
							//number you asked for.  Here, check if there is a parameter 'count', which is that maximum value.
							if (_.get(endpoint, 'parameter_descriptions.count') !== undefined) {
								//If you got back fewer items than you asked for
								if (responseObjectsList.length < _.get(endpoint.parameter_descriptions, 'count.value')) {
									_.set(context.signal.endpoint_data[eventSource.name][endpointName], paginationStartParameter, newCursorStartValue);
									//In descending-order cursor pagination, we don't want to save the end value permanently; this
									//is only used while doing the pagination, and should not carry over to future searches.
									delete context.signal.endpoint_data[eventSource.name][endpointName][paginationEndParameter];
									loopEnd = true;
									patchData.endpoint_data = signal.endpoint_data;

									//Only update parameters that need to be saved for future runs once all of the endpoints
									//for that event source have finished running.
									$.when.apply($, eventSourcePromiseList).then(function() {
										$.ajax({
											url: 'opi/signal/' + context.signal.id,
											type: 'PATCH',
											data: JSON.stringify(patchData),
											contentType: 'application/json',
											dataType: 'json',
											headers: {
												'X-CSRFToken': $.cookie('csrftoken')
											}
										}).done(function(data, xhr, response) {
											permissionDeferred.resolve();
										});
									});
								}
								//If you got back as many items as you asked for
								else {
									//Some endpoints provide a field for the next cursor, so check if that is a parameter
									//that exists for this event source
									if (nextCursorLocation !== undefined) {
										var cursorLocation = _.get(responseData, nextCursorLocation);

										//If there is something at the location where you expect a new cursor value,
										//Then update the value
										if (cursorLocation.hasOwnProperty(cursorValue)) {
											newCursorEndValue = _.get(cursorLocation, cursorValue);
										}
										//If there isn't something there, then you have gotten to the end of new data
										//and need to stop iteration this event source
										else {
											loopEnd = true;
										}
									}
									//If the provider doesn't have a next cursor field, then the cursor is just the ID of
									//the last element in the responseObjectsList (this assumes that the provider returns
									//the most recent element at the start of the array)
									else {
										newCursorEndValue = _.get(responseObjectsList[responseObjectsList.length - 1], cursorValue);
									}
									_.set(context.signal.endpoint_data[eventSource.name][endpointName], paginationEndParameter, newCursorEndValue);
								}
							}
							//Some endpoints have a boolean field indicating whether there are more pages of data.
							//Check if this event source has a field indicating where that would be.
							else if (paginationCheckMore !== undefined) {
								newCursorStartValue = _.get(responseData, nextCursorLocation);
								_.set(context.signal.endpoint_data[eventSource.name][endpointName], paginationStartParameter, newCursorStartValue);

								//If the field is false, then you have gotten to the end of the new data.
								if (_.get(responseData, paginationCheckMore) === false) {
									loopEnd = true;
									patchData.endpoint_data = signal.endpoint_data;

									//Only update parameters that need to be saved for future runs once all of the endpoints
									//for that event source have finished running.
									$.when.apply($, eventSourcePromiseList).then(function() {
										$.ajax({
											url: 'opi/signal/' + context.signal.id,
											type: 'PATCH',
											data: JSON.stringify(patchData),
											contentType: 'application/json',
											dataType: 'json',
											headers: {
												'X-CSRFToken': $.cookie('csrftoken')
											}
										}).done(function(data, xhr, response) {
											permissionDeferred.resolve();
										});
									});
								}
							}
							//Some endpoints have a field that is either null if there is no more data, or contains the cursor
							//for the next page if there is more data.
							else if (paginationVariableCursor !== undefined) {
								newCursorStartValue = _.get(responseData, paginationVariableCursor);
								_.set(context.signal.endpoint_data[eventSource.name][endpointName], paginationStartParameter, newCursorStartValue);

								//If the field is null, then you have gotten to the end of the new data.
								if (_.get(responseData, paginationVariableCursor) === null) {
									loopEnd = true;
									patchData.endpoint_data = signal.endpoint_data;

									//Only update parameters that need to be saved for future runs once all of the endpoints
									//for that event source have finished running.
									$.when.apply($, eventSourcePromiseList).then(function() {
										$.ajax({
											url: 'opi/signal/' + context.signal.id,
											type: 'PATCH',
											data: JSON.stringify(patchData),
											contentType: 'application/json',
											dataType: 'json',
											headers: {
												'X-CSRFToken': $.cookie('csrftoken')
											}
										}).done(function(data, xhr, response) {
											permissionDeferred.resolve();
										});
									});
								}
								else {
									_.set(context.signal.endpoint_data[eventSource.name][endpointName], paginationStartParameter, newCursorStartValue);
								}
							}
						}
						//Some endpoints provide a page token for their pagination that is passed to future calls
						//as a parameter.  This page token is typically not related to any other information about the
						//endpoint call, i.e. it's not an ID of an entry nor is it a distinct datetime.
						else if (paginationMethod === 'pageToken') {
							//If the new page token is not present, then there is no more data after this
							if (_.get(responseData, pageTokenLocation) === undefined) {
								parameter_descriptions = _.get(endpoint, 'parameter_descriptions');

								loopEnd = true;

								delete context.signal.endpoint_data[eventSource.name][endpointName].pageToken;

								//Sometimes there are parameters outside of the pagination fields that need to be saved
								//to the signal for later use.  An example is that Gmail can use a date to only get messages
								//after that date.  This isn't used for normal pagination, but should be updated every time
								//the endpoint is run so we don't get mail that's already been retrieved.
								_.forEach(Object.keys(parameter_descriptions), function(parameter) {
									var thisParameter = parameter_descriptions[parameter];

									if (thisParameter.hasOwnProperty('save_to_signal')) {
										var updatedValue;
										var updateLocation = thisParameter.save_to_signal.location;
										if (updateLocation === 'date_now') {
											updatedValue = new Date().toJSON().split('T')[0].replace(/-/g, '/');
										}
										else {
											updatedValue = _.get(responseData, updateLocation);
										}

										_.set(context.signal.endpoint_data[eventSource.name][endpointName], parameter, updatedValue);
									}
								});

								patchData.endpoint_data = signal.endpoint_data;

								//Only update parameters that need to be saved for future runs once all of the endpoints
								//for that event source have finished running.
								$.when.apply($, eventSourcePromiseList).then(function() {
									$.ajax({
										url: 'opi/signal/' + context.signal.id,
										type: 'PATCH',
										data: JSON.stringify(patchData),
										contentType: 'application/json',
										dataType: 'json',
										headers: {
											'X-CSRFToken': $.cookie('csrftoken')
										}
									}).done(function(data, xhr, response) {
										permissionDeferred.resolve();
									});
								});
							}
							else {
								_.set(context.signal.endpoint_data[eventSource.name][endpointName], 'pageToken', _.get(responseData, pageTokenLocation));
							}
						}
						//Some endpoints give you the full URL for the next page
						else if (paginationMethod === 'nextPage') {
							if (_.get(responseData, nextPageLocation) === undefined || _.get(responseData, nextPageLocation) === null) {
								parameter_descriptions = _.get(endpoint, 'parameter_descriptions');

								loopEnd = true;

								delete context.signal.endpoint_data[eventSource.name][endpointName].next_url;

								//Sometimes there are parameters outside of the pagination fields that need to be saved
								//to the signal for later use.  An example is that Gmail can use a date to only get messages
								//after that date.  This isn't used for normal pagination, but should be updated every time
								//the endpoint is run so we don't get mail that's already been retrieved.
								_.forEach(Object.keys(parameter_descriptions), function(parameter) {
									var thisParameter = parameter_descriptions[parameter];

									if (thisParameter.hasOwnProperty('save_to_signal')) {
										var updatedValue;
										var updateLocation = thisParameter.save_to_signal.location;
										if (updateLocation === 'date_now') {
											updatedValue = new Date().toJSON().split('T')[0].replace(/-/g, '/');
										}
										else {
											updatedValue = _.get(responseData, updateLocation);
										}

										_.set(context.signal.endpoint_data[eventSource.name][endpointName], parameter, updatedValue);
									}
								});

								patchData.endpoint_data = signal.endpoint_data;

								//Only update parameters that need to be saved for future runs once all of the endpoints
								//for that event source have finished running.
								$.when.apply($, eventSourcePromiseList).then(function() {
									$.ajax({
										url: 'opi/signal/' + context.signal.id,
										type: 'PATCH',
										data: JSON.stringify(patchData),
										contentType: 'application/json',
										dataType: 'json',
										headers: {
											'X-CSRFToken': $.cookie('csrftoken')
										}
									}).done(function(data, xhr, response) {
										permissionDeferred.resolve();
									});
								});
							}
							else {
								_.set(context.signal.endpoint_data[eventSource.name][endpointName], 'next_url', _.get(responseData, nextPageLocation));
							}
						}
						else if (paginationMethod === 'rfc5988') {
							var linkDict = {};
							var stringLinks = _.get(responseData, 'Link').split(',');

							_.forEach(stringLinks, function(stringLink) {
								var linkParts = stringLink.split(';');
								_.forEach(linkParts, function(linkPart, index) {
									linkParts[index] = linkPart.trim().replace(/</g, '').replace(/>/g, '');
								});

								linkDict[linkParts[1]] = linkParts[0];
							});

							if (Object.keys(linkDict).indexOf(nextPageLocation) === -1) {
								parameter_descriptions = _.get(endpoint, 'parameter_descriptions');

								loopEnd = true;

								delete context.signal.endpoint_data[eventSource.name][endpointName].next_url;

								//Sometimes there are parameters outside of the pagination fields that need to be saved
								//to the signal for later use.  An example is that Gmail can use a date to only get messages
								//after that date.  This isn't used for normal pagination, but should be updated every time
								//the endpoint is run so we don't get mail that's already been retrieved.
								_.forEach(Object.keys(parameter_descriptions), function(parameter) {
									var thisParameter = parameter_descriptions[parameter];

									if (thisParameter.hasOwnProperty('save_to_signal')) {
										var updatedValue;
										var updateLocation = thisParameter.save_to_signal.location;
										if (updateLocation === 'date_now') {
											updatedValue = new Date().toJSON().split('T')[0].replace(/-/g, '/');
										}
										else {
											updatedValue = _.get(responseData, updateLocation);
										}

										_.set(context.signal.endpoint_data[eventSource.name][endpointName], parameter, updatedValue);
									}
								});

								patchData.endpoint_data = signal.endpoint_data;

								//Only update parameters that need to be saved for future runs once all of the endpoints
								//for that event source have finished running.
								$.when.apply($, eventSourcePromiseList).then(function() {
									$.ajax({
										url: 'opi/signal/' + context.signal.id,
										type: 'PATCH',
										data: JSON.stringify(patchData),
										contentType: 'application/json',
										dataType: 'json',
										headers: {
											'X-CSRFToken': $.cookie('csrftoken')
										}
									}).done(function(data, xhr, response) {
										permissionDeferred.resolve();
									});
								});
							}
							else {
								_.set(context.signal.endpoint_data[eventSource.name][endpointName], 'next_url', linkDict[nextPageLocation]);
							}
						}
						//Some endpoints give you a page number for the next page
						else if (paginationMethod === 'pageNumber') {
						}
						//Catch any issues by ending the endpoint iteration so we don't loop infinitely.  Some endpoints
						//do not have any pagination, so use the same resolution for them.
						else if (paginationMethod === undefined || paginationMethod === 'none') {
							loopEnd = true;
							permissionDeferred.resolve();
						}

						//If this isn't the last iteration through the endpoint
						if (!loopEnd) {
							//If we throttle endpoint calls for this provider, then wait n seconds before calling the
							//endpoint again.
							if (signal.provider.hasOwnProperty('endpoint_wait_time')) {
								var timeoutTime = _.get(signal.provider, 'endpoint_wait_time') * 1000;

								setTimeout(function() {
									_processOneEndpointIteration(endpoint, mapping, context);
								}, timeoutTime);
							}
						}
					});
				});
			}
		}
	}

	/**
	 * Call the endpoint as defined in the given Permission
	 *
	 * @param {Object} endpoint One of the Permissions for the given signal
	 * @param {Object} context
	 * @returns {Object} The raw data returned from the eventSource
	 */
	function _callOneEndpoint(endpoint, context) {
		var cacheKey, parameterPieces, parameters;
		var deferred = $.Deferred();
		var url = 'https://p.bitscoop.com/call';
		var parameter_descriptions = _.get(endpoint, 'parameter_descriptions');
		var header_descriptions = _.get(endpoint, 'header_descriptions');
		var callParameters = {};
		var callHeaders = {};
		var promiseList = [];

		if (_.has(endpoint.parameter_descriptions, 'next_url') && _.has(context, endpoint.parameter_descriptions.next_url.value)) {
			var parser = document.createElement('a');

			parser.href = _.get(context, endpoint.parameter_descriptions.next_url.value);
			parameters = parser.search.slice(1);

			callParameters = $.deparam(parameters);
		}

		//Add parameters to the endpoint URL
		_.forEach(parameter_descriptions, function(value, parameter) {
			if (parameter !== 'next_url' && !(_.has(callParameters, parameter))) {
				//If the parameter needs to be hydrated by calling an endpoint
				if (value.hydration_method === 'endpoint') {
					//Calling hydrateField will return a promise.  This promise will only be resolved when the endpoint
					//has been called successfully.
					var potentialPromise = _hydrateField(context, value);

					//Add the new promise to the list of promises for parameters on this endpoint
					promiseList.push(potentialPromise);
					//When this promise is done, add the parameter value to the list of parameters
					potentialPromise.done(function(response) {
						callParameters[parameter] = response;
					});
				}
				//If the parameter does not come from an endpoint call, then we do not need to wait for any promises
				//to be resolved and can get and add the parameter immediately.
				else {
					callParameters[parameter] = _hydrateField(context, value);
				}
			}
		});

		//Add header to the endpoint URL
		_.forEach(header_descriptions, function(value, header) {
			//If the header needs to be hydrated by calling an endpoint
			if (value.hydration_method === 'endpoint') {
				//Calling hydrateField will return a promise.  This promise will only be resolved when the endpoint
				//has been called successfully.
				var potentialPromise = _hydrateField(context, value);

				//Add the new promise to the list of promises for headers on this endpoint
				promiseList.push(potentialPromise);
				//When this promise is done, add the header value to the list of headers
				potentialPromise.done(function(response) {
					callHeaders[header] = response;
				});
			}
			//If the header does not come from an endpoint call, then we do not need to wait for any promises
			//to be resolved and can get and add the header immediately.
			else {
				callHeaders[header] = _hydrateField(context, value);
			}
		});

		//Wait until all of the parameters that come from endpoints have been hydrated.  If none do, then promiseList
		//will be empty; $.when interprets an empty promise list as having been resolved already.
		$.when.apply($, promiseList).done(function() {
			var callData = {
				signal_id: context.signal.id,
				permission_name: context.permission.event_source.name,
				endpoint_name: endpoint.name,
				parameters: JSON.stringify(callParameters),
				headers: JSON.stringify(callHeaders)
			};

			var parametersString = '';
			var callParametersList = objectSort(callParameters);

			//This is used to create the cache key.  The key needs to be the same no matter what order the parameters
			//were populated in, so this sorts them into alphabetical order and puts them into an array instead of
			//a dictionary.
			function objectSort(o) {
				var a = [], i;
				for (i in o) {
					if (o.hasOwnProperty(i)) {
						a.push([i, o[i]]);
					}
				}
				a.sort(function(a, b) {
					return a[0] > b[0] ? 1 : -1;
				});
				return a;
			}

			_.forEach(callParametersList, function(item) {
				parametersString += item[0] + item[1] + '';
			});

			//TODO: parameters need to be a sorted dictionary for uniqueness to be preserved
			cacheKey = callData.signal_id + callData.permission_name + callData.endpoint_name + parametersString;

			//Check if this call was made already, and if so pass back the cached value.
			if (endpointCache.hasOwnProperty(cacheKey)) {
				deferred.resolveWith(this, [endpointCache[cacheKey]]);
			}
			//If this call has not been made, then make it
			else {
				// Call the endpoint using its ID, parameters, and headers
				// Note the 'xhrFields' option; withCredentials:true allows for ajax to send cookies, particularly
				// the sessionid, as part of a cross-domain call.
				// The server must return the header 'Access-Control-Allow-Credentials' set to true for this to work.
				// Additionally, the header 'Access-Control-Allow-Origin' must be sent by the server and must be something
				// other than the wildcard '*' for this to work.
				return $.ajax({
					url: url,
					type: 'GET',
					data: callData,
					dataType: 'text',
					headers: {
						'X-CSRFToken': $.cookie('csrftoken')
					},
					xhrFields: {
						withCredentials: true
					}
				}).done(function(data, xhr, response) {
					endpointCache[cacheKey] = data;
					deferred.resolveWith(this, [data]);
				}).fail(function(data, xhr, response) {
					console.log('Endpoint ' + endpoint.name + ' call failure');
				});
			}
		});
		return deferred.promise();
	}


	/**
	 * Transform the raw data returned from the eventSource into Ografy's format, then post that data to the database.
	 *
	 * @param {Object} context
	 * @param {Object} eventSourceDeferred The deferred object that will be resolved once the item has been fully mapped.
	 */
	//TODO: Abstract posting into a callback passed into mapping a single model or after the mapping function returns the result
	function mapSingleModel(context, eventSourceDeferred) {
		var contentList = [];
		var contactsList = [];
		var location;
		var dataList = [];
		var dbEntryMapping = _.get(context.mapping, 'db_entry_mapping');
		var conditionMapping = _.get(context.mapping, 'conditions');

		//Used in geolocation logic
		var locationMapping = _.get(dbEntryMapping, 'location');
		var eventGeolocation = _.get(locationMapping, 'geolocation');
		var canHydrateLocation = _canHydrateLocation();

		var mapDataPromises = mapData();

		//Post the responseObject to the Data collection, then use the document that is returned to create all of the other documents.
		$.when.apply($, mapDataPromises).done(function() {
			//Call mapContent, mapContacts, and mapLocation.  Each of these can be run independently of the others.
			//The each return a promise (mapLocation) or a list of promises (the other two).  These promises are resolved
			//only when the mapping or mappings have been completed.
			//(mapContacts and mapContent may create multiple db entries from a single piece of data, so they have
			//a list of promises, one for each item they are creating).
			var mapContentPromises = mapContent();
			var mapContactsPromises = mapContacts();
			var mapLocationPromise = mapLocation();
			//Concatenate the list of promises from mapContent and mapContacts into one list and add on the promise from mapLocation.
			var totalPromises = mapContactsPromises.concat(mapContentPromises).concat(mapLocationPromise);

			$.when.apply($, totalPromises).done(function() {
				//On some endpoints, you can get the same contact back multiple times, e.g. if you created the reddit thread
				//and posted in it and replied to your own post.  We don't want the same contact showing up in the
				//list of contacts multiple times, so this wil assemble a list of unique contacts for the event
				//that is about to be posted.
				var uniqueContactsMap = [];
				var uniqueContactsList = [];

				_.forEach(contactsList, function(contact, index) {
					if (uniqueContactsMap.indexOf(contact.ografy_unique_id) === -1) {
						uniqueContactsMap.push(contact.ografy_unique_id);
						uniqueContactsList.push(contact);
					}
				});

				mapEvent(contentList, uniqueContactsList, location, eventSourceDeferred);
			}).fail(function() {
				//If something failed, then don't try to map the event, as we don't have the necessary information.
				//Just reject eventSourceDeferred so that this event source's information is not updated, and the next
				//time it runs it will try to map this again.
				eventSourceDeferred.reject();
			});
		});
		//Only map the event once all content and contacts have been created as well as the location (if possible)


		//Google Drive was returning dictionaries where some keys contained periods.
		//Mongoengine does not accept periods or dollar signs in keys, so this will replace those characters with
		//the value *dot*.
		function stripInvalidKeyCharacters(inputDict) {
			var returnDict;

			returnDict = _.mapKeys(inputDict, function(value, key) {
				if (typeof key === 'string') {
					key = key.replace(/[.]/g, '*dot*').replace(/[$]/g, '*dot*');
				}
				return key;
			});

			returnDict = _.mapValues(returnDict, function(value, key) {
				if (Array.isArray(value)) {
					_.forEach(value, function(oneValue) {
						oneValue = stripInvalidKeyCharacters(value);
					});
				}
				else if (typeof value === 'object' && value !== null) {
					value = stripInvalidKeyCharacters(value);
				}
				return value;
			});

			return returnDict;
		}


		//This checks if the data has the information needed to create a location.
		function _canHydrateLocation() {
			//Check if the mapping even describes how to create a location
			if (dbEntryMapping.hasOwnProperty('location')) {
				//If it does, then check if the mapping value is an object (really check if it's an array)
				//If it is, then we're doing a 'multi-value' hydration.  This means that the coordinates are not
				//provided in an array, but rather in separate fields, i.e. {'latitude': <x>, 'longitude': <y>}
				if (typeof eventGeolocation.value === 'object') {
					var returnValue = true;

					//Go to each field where a coordinate should be
					_.forEach(eventGeolocation.value, function(value) {
						//If the coordinate is not present, then we don't have enough data to create the location
						if (_.get(context, value) === undefined) {
							returnValue = false;
						}
					});

					//If any of the coordinates were missing, this will return false.
					//If they are all present this will return true
					return returnValue;
				}
				//If there's a single mapping value, then the coordinates will already be in an array.
				else {
					//If the coordinates are present, then return true.
					if (_.get(context, eventGeolocation.value) !== undefined && _.get(context, eventGeolocation.value) !== null) {
						return true;
					}
				}
			}

			//If the mapping does not describe how to create a location, then there is never enough data and we cannot do so.
			//Alternatively, the mapping does describe how to get the coordinates, but they are missing, so we
			//cannot create one.
			return false;
		}


		function mapData() {
			var dataObject;
			var deferredList = [];
			var dataMapping = _.get(dbEntryMapping, 'data');

			context.responseObject = stripInvalidKeyCharacters(context.responseObject);

			_.forEach(dataMapping, function(singleDataMapping) {
				var deferred = $.Deferred();

				//The ografy_unqiue_id is a way for us to tell this particular item apart from other items of its type.
				//While the item's ID is also unique, we can't reconstruct an ObjectID from the data we receive.
				//Constructing ografy_unique_id is repeatable.
				var ografy_unique_id = context.signal.user_id + '_' + context.signal.id + '_';

				//TODO: Hash the unique ID once we're comfortable that this is working properly
				_.forEach(singleDataMapping.unique_identifiers, function(identifier) {
					ografy_unique_id += _hydrateField(context, identifier) + '_';
				});
				ografy_unique_id = ografy_unique_id.substring(0, ografy_unique_id.length - 1);

				dataObject = {
					data_dict: context.responseObject,
					ografy_unique_id: ografy_unique_id,
					user_id: context.signal.user_id
				};

				deferred.promise();
				deferredList.push(deferred);

				$.ajax({
					url: 'opi/data',
					type: 'POST',
					data: JSON.stringify(dataObject),
					dataType: 'json',
					contentType: 'application/json; charset=utf-8',
					headers: {
						'X-CSRFToken': $.cookie('csrftoken')
					}
				}).done(function(data, xhr, response) {
					dataList.push(data.id);
					deferred.resolve();
				}).fail(function(data, xhr, response) {
					console.log('Data ' + data.id + ' mapping failed');
					deferred.reject();
				});
			});

			return deferredList;
		}

		//TODO: Make entire parent function more programmatic, better debug success/fail messages with ids?
		function mapEvent(contentList, contactsList, location, eventSourceDeferred) {
			var jsonDatetime, eventObject, potentialPromise;
			var eventMapping = _.get(dbEntryMapping, 'event');

			//If the mapping says the datetime field can be mapped
			if (eventMapping.mapped_fields.hasOwnProperty('datetime')) {
				var datetimeMapping = _.get(eventMapping.mapped_fields, 'datetime');

				//If the datetime needs to be obtained from an endpoint, then save the promise that is returned by
				//hydrateField, wait until the promise is resolved, then create the new datetime in JSON format.
				if (datetimeMapping.hydration_method === 'endpoint') {
					potentialPromise = _hydrateField(context, datetimeMapping);
					potentialPromise.done(function(response) {
						jsonDatetime = new Date(response).toJSON();
					});
				}
				//If the datetime can be obtained locally, do so.  We don't have to wait for any promises to be resolved.
				else {
					jsonDatetime = _hydrateField(context, datetimeMapping);

					//Some endpoints are not returned in normal datetime formats nor epoch time.  Convert these
					//non-standard times.
					if (datetimeMapping.hasOwnProperty('format')) {
						//TODO: Should conversion from unix time and similar conversions be done in hydrateField?
						//Unix time needs to be multiplied by 1000 to get to epoch time.
						if (datetimeMapping.format === 'unix_time') {
							jsonDatetime = new Date(jsonDatetime * 1000).toJSON();
						}
					}
					//If the datetime is in a normal, parseable format, just create a new date and convert it to JSON format.
					else {
						jsonDatetime = new Date(jsonDatetime).toJSON();
					}
				}
			}

			//When creating the embedded content list, strip off unnecessary fields from each content document.
			//Also convert the ID of the discrete content document into the embedded content's 'content' field, as
			//embedded documents do not have IDs.
			_.forEach(contentList, function(singleContent) {
				delete singleContent.user_id;
				delete singleContent.ografy_unique_id;
				delete singleContent.signal;
				delete singleContent.data_dict;
				singleContent.content = singleContent.id;
				delete singleContent.id;
			});

			//When creating the embedded contacts list, strip off unnecessary fields from each contact document.
			//Also convert the ID of the discrete contact document into the embedded contact's 'contact' field, as
			//embedded documents do not have IDs.
			_.forEach(contactsList, function(contact) {
				delete contact.user_id;
				delete contact.ografy_unique_id;
				delete contact.signal;
				delete contact.data_dict;
				contact.contact = contact.id;
				delete contact.id;
			});

			//When creating the embedded location, strip off unnecessary fields from the location document.
			//Also convert the ID of the discrete location document into the embedded location's 'location' field, as
			//embedded documents do not have IDs.
			if (location !== undefined) {
				delete location.data_dict;
				delete location.datetime;
				delete location.signal;
				delete location.user_id;
				location.location = location.id;
				delete location.id;
			}

			//Wait for the datetime to be retrieved from an endpoint if needed.
			//If not, this will be resolved immediately.
			$.when(potentialPromise).done(function() {
				//The ografy_unqiue_id is a way for us to tell this particular item apart from other items of its type.
				//While the item's ID is also unique, we can't reconstruct an ObjectID from the data we receive.
				//Constructing ografy_unique_id is repeatable.
				var ografy_unique_id = context.signal.user_id + '_' + context.signal.id + '_';

				//TODO: Hash the unique ID once we're comfortable that this is working properly
				_.forEach(eventMapping.unique_identifiers, function(identifier) {
					ografy_unique_id += _hydrateField(context, identifier) + '_';
				});
				ografy_unique_id = ografy_unique_id.substring(0, ografy_unique_id.length - 1);

				eventObject = {
					ografy_unique_id: ografy_unique_id,
					contact_interaction_type: _hydrateField(context, _.get(eventMapping.mapped_fields, 'contact_interaction_type')),
					content_list: contentList,
					data_dict: dataList,
					datetime: jsonDatetime,
					event_type: _.get(context.mapping, 'event_type'),
					location: location,
					contacts_list: contactsList,
					provider: context.signal.provider.provider_number,
					provider_name: context.signal.provider.name,
					signal: context.signal.id,
					user_id: context.signal.user_id
				};

				$.ajax({
					url: 'opi/event',
					type: 'POST',
					data: JSON.stringify(eventObject),
					dataType: 'json',
					contentType: 'application/json; charset=utf-8',
					headers: {
						'X-CSRFToken': $.cookie('csrftoken')
					}
				}).done(function(data, xhr, response) {
					//Resolve the deferred to indicate that this event has been fully mapped.
					//When all the events from this event source have been mapped, the endpoint_data
					//for that event source can be saved to the signal.
					eventSourceDeferred.resolve();
				}).fail(function(data, xhr, response) {
					//If an error is sent back, then the event was not posted successfully and was not already present.
					//In this case, reject the promise.  This will cause the event source's endpoint_data to not be
					//updated, and the next call to this event source will get all of the data from this run again
					//to make sure that nothing was skipped.
					eventSourceDeferred.reject();
				});
			});
		}


		//Create a location if possible
		function mapLocation() {
			var deferred = $.Deferred();

			//Only try to create a location if it's possible to do so
			if (canHydrateLocation) {
				var locationObject = {
					data_dict: dataList
				};

				//Map the location's fields as specified by the event source's mapping
				_.forEach(locationMapping, function(eventValue, eventKey) {
					if (eventKey === 'datetime') {
						var datetime = _hydrateField(context, eventValue);

						//Do any conversions of the datetime if needed before creating it and converting to JSON format.
						if (eventValue.hasOwnProperty('format')) {
							if (eventValue.format === 'unix_time') {
								locationObject[eventKey] = new Date(datetime * 1000).toJSON();
							}
						}
						else {
							locationObject[eventKey] = new Date(datetime).toJSON();
						}
					}
					else {
						locationObject[eventKey] = _hydrateField(context, eventValue);
					}
				});

				$.ajax({
					url: 'opi/location',
					type: 'POST',
					data: JSON.stringify(locationObject),
					dataType: 'json',
					contentType: 'application/json; charset=utf-8',
					headers: {
						'X-CSRFToken': $.cookie('csrftoken')
					}
				}).done(function(data, xhr, response) {
					location = data;
					deferred.resolve();
				}).fail(function(data, xhr, response) {
					console.log('Location mapping failed');
					deferred.reject();
				});
			}
			//If the location cannot be created, then just set it to undefined and resolve the promise.
			//The server will estimate the location when the event gets posted.
			else {
				location = undefined;
				deferred.resolve();
			}

			return deferred.promise();
		}


		//Create content documents in the DB from this item
		function mapContent() {
			var masterPromiseList = [];
			var contentObject;
			var contentMasterMapping = _.get(dbEntryMapping, 'content');
			var promiseList = [];

			//Some endpoints may provide multiple types of content, so map each of them as specified in their
			//individual mappings.
			_.forEach(contentMasterMapping, function(contentSingleMap) {
				var skipPost = false;
				var masterPromise = $.Deferred();
				var conditionMapping = _.get(contentSingleMap, 'conditions');
				var items;

				//If there are conditions on the mapping, check to see if this item matches each condition.
				//If any of them do not, then this item will not be posted to the DB.
				_.forEach(conditionMapping, function(condition) {
					var conditionKey = Object.keys(condition)[0];
					var conditionVal = condition[conditionKey].value;
					var conditionField = condition[conditionKey].field;

					//Property exists
					//	Property equals
					if (conditionKey === 'equals') {
						if (_.get(context, conditionField) !== conditionVal) {
							skipPost = true;
						}
					}
					else if (conditionKey === 'notEquals') {
						if (_.get(context, conditionField) === conditionVal) {
							skipPost = true;
						}
					}
					//	Property less than
					//	Property greater than
					//	Property typeof
				});

				if (contentSingleMap.hasOwnProperty('hydrate_list_location')) {
					items = _.get(context, contentSingleMap.hydrate_list_location);
				}
				else {
					items = [context];
				}

				_.forEach(items, function(item) {
					contentObject = {
						data_dict: dataList,
						signal: context.signal.id,
						user_id: context.signal.user_id
					};

					//The masterPromiseList holds a deferred for each content item we are trying to map.
					//For this item, push its deferred onto the list and create the promise.
					masterPromiseList.push(masterPromise);
					masterPromise.promise();

					//Map the fields for this content item.
					//As with other mappings like this, a promise is created if the field has to come from another
					//endpoint call, and that promise is resovled when that further endpoint call is finished.
					_.forEach(contentSingleMap.mapped_fields, function(contentValue, contentKey) {
						if (contentValue.hydration_method === 'endpoint') {
							var potentialPromise = _hydrateField(item, contentValue);

							promiseList.push(potentialPromise);
							potentialPromise.done(function(response) {
								contentObject[contentKey] = response;
							});
						}
						else {
							contentObject[contentKey] = _hydrateField(item, contentValue);
						}
					});

					//This waits for any field mapping promises to be resolved.
					$.when.apply($, promiseList).done(function() {
						var promiseList = [];
						//The ografy_unqiue_id is a way for us to tell this particular item apart from other items of its type.
						//While the item's ID is also unique, we can't reconstruct an ObjectID from the data we receive.
						//Constructing ografy_unique_id is repeatable.
						var ografy_unique_id = context.signal.user_id + '_' + context.signal.id + '_';

						//TODO: Hash the unique ID once we're comfortable that this is working properly
						_.forEach(contentSingleMap.unique_identifiers, function(identifier) {
							var potentialPromise;
							var newField = _hydrateField(item, identifier);

							if (identifier.hydration_method === 'endpoint') {
								potentialPromise = _hydrateField(item, identifier);
								promiseList.push(potentialPromise);
								potentialPromise.done(function(response) {
									newField = response;
								});
							}
							else {
								newField = _hydrateField(item, identifier);
							}

							$.when(potentialPromise).done(function() {
								if (newField === undefined || newField === null) {
									skipPost = true;
								}
								else {
									ografy_unique_id += newField + '_';
								}
							});
						});

						$.when.apply($, promiseList).done(function() {
							ografy_unique_id = ografy_unique_id.substring(0, ografy_unique_id.length - 1);

							contentObject.ografy_unique_id = ografy_unique_id;

							if (!skipPost) {
								$.ajax({
									url: 'opi/content',
									type: 'POST',
									data: JSON.stringify(contentObject),
									dataType: 'json',
									contentType: 'application/json; charset=utf-8',
									headers: {
										'X-CSRFToken': $.cookie('csrftoken')
									}
								}).done(function(data, xhr, response) {
									contentList.push(data);
									masterPromise.resolve();
								}).fail(function(data, xhr, response) {
									console.log('Content ' + data.id + ' mapping failed');
									masterPromise.reject();
								});
							}
							else {
								masterPromise.resolve();
							}
						});
					});
				});
			});

			return masterPromiseList;
		}


		function mapContacts() {
			var contactsMapping = _.get(dbEntryMapping, 'contacts');
			var masterPromiseList = [];

			_.forEach(contactsMapping, function(contactMapping) {
				var hydratePromise, contextHydrateList;
				//hydrateList is where potential contacts are listed on the object we are mapping.
				var hydrateList = _.get(contactMapping, 'hydrate_list_location');
				var deferred = $.Deferred();

				//If we need to call an endpoint to get more information for this contact, do so, and create
				//a promise that is only resolved when the endpoint call has finsihed.
				if (contactMapping.hasOwnProperty('call_endpoint')) {
					hydratePromise = _hydrateField(context, contactMapping.call_endpoint);
					hydratePromise.done(function(item) {
						context.childObject = item;
						deferred.resolve();
					});
				}
				else {
					deferred.resolve();
				}

				$.when(deferred).done(function() {
					//Get the list of contacts to be created
					contextHydrateList = _.get(context, hydrateList);

					//The contextHydrateList is supposed to be a list.  If it's a single contact, add them to a list
					//anyway so it can be iterated over.
					if (!(Array.isArray(contextHydrateList))) {
						contextHydrateList = [contextHydrateList];
					}

					_.forEach(contextHydrateList, function(contact) {
						var masterPromise = $.Deferred();
						var contactObject;
						var promiseList = [];
						var skipPost = false;

						//The masterPromiseList holds a deferred for each contact item we are trying to map.
						//For this item, push its deferred onto the list and create the promise.
						masterPromiseList.push(masterPromise);
						masterPromise.promise();

						contactObject = {
							data_dict: dataList,
							signal: context.signal.id,
							user_id: context.signal.user_id
						};

						//Map all of the fields shown in the mapping.
						//If a mapping needs to call an endpoint to get more data, create a promise that will be
						//resolved only when the endpoint has been called.
						_.forEach(contactMapping.mapped_fields, function(contactValue, contactKey) {
							if (contactValue.hydration_method === 'endpoint') {
								var potentialPromise = _hydrateField(context, contactValue);
								promiseList.push(potentialPromise);
								potentialPromise.done(function(response) {
									contactObject[contactKey] = response;
								});
							}
							else {
								contactObject[contactKey] = _hydrateField(contact, contactValue);
							}
						});

						$.when.apply($, promiseList).done(function() {
							var promiseList = [];
							//The ografy_unqiue_id is a way for us to tell this particular item apart from other items of its type.
							//While the item's ID is also unique, we can't reconstruct an ObjectID from the data we receive.
							//Constructing ografy_unique_id is repeatable.
							var ografy_unique_id = context.signal.user_id + '_' + context.signal.id + '_';

							//TODO: Hash the unique ID once we're comfortable that this is working properly
							_.forEach(contactMapping.unique_identifiers, function(identifier) {
								var newField, potentialPromise;

								if (identifier.hydration_method === 'endpoint') {
									potentialPromise = _hydrateField(context, identifier);
									promiseList.push(potentialPromise);
									potentialPromise.done(function(response) {
										newField = response;
									});
								}
								else {
									newField = _hydrateField(contact, identifier);
								}

								$.when(potentialPromise).done(function() {
									if (newField === undefined || newField === null) {
										skipPost = true;
									}
									else {
										ografy_unique_id += newField + '_';
									}
								});
							});

							$.when.apply($, promiseList).done(function() {
								ografy_unique_id = ografy_unique_id.substring(0, ografy_unique_id.length - 1);

								contactObject.ografy_unique_id = ografy_unique_id;

								if (!skipPost) {
									$.ajax({
										url: 'opi/contact',
										type: 'POST',
										data: JSON.stringify(contactObject),
										dataType: 'json',
										contentType: 'application/json; charset=utf-8',
										headers: {
											'X-CSRFToken': $.cookie('csrftoken')
										}
									}).done(function(data, xhr, response) {
										contactsList.push(data);
										masterPromise.resolve();
									}).fail(function(data, xhr, response) {
										console.log('Contact ' + data.id + ' mapping failed');
										masterPromise.resolve();
									});
								}
								else {
									masterPromise.resolve();
								}
							});
						});
					});
				});
			});

			return masterPromiseList;
		}
	}

	return {
		schedule: schedule,
		run: run
	};
});
