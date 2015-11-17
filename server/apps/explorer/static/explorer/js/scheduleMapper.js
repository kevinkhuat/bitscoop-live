//Module scheduleMapper
//This module contains functions for updating the eventSource of signals that are past their update frequency or that have never been pulled at all.
define ('scheduleMapper', ['jquery', 'lodash', 'jquery-cookie', 'jquery-deparam'], function($, _) {
	var signals, signalsToRun, permissions;
	var eventSources = [];
	var endpointCache = {};

	/**
	 * Starts the process of getting the user's signals and calling the eventSources if their information is out-of-date
	 *
	 */
	//TODO: Get userId from user eventSource and not signal
	function run() {
		endpointCache = {};
		$.when(_getSignals(signals)).done(function() {
			_checkAllSignalsLastRun();
			if (signalsToRun.length > 0) {
				_processSignal(0);
			}
		});
	}

	/**
	 * Runs the process of getting information for signals that are past their update frequency.
	 * Then sets a timer to run the process again at an interval specified as an input
	 *
	 * @param {Integer} time_ms  How often, in ms, this module should check
	 */
	//Schedules
	function schedule(time_ms) {
		run();
		setInterval(function() {
			run();
		}, time_ms);
	}

	/**
	 * Gets all of the user's signals from the database
	 *
	 * @returns {Object} A list of all the signals for the current user
	 */
	function _getSignals() {
		return $.ajax({
			url: '/opi/signal',
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
		var returnValue, deferred;
		var value = _.get(propertyMapping, 'value');
		var hydration_method = _.get(propertyMapping, 'hydration_method');
		var type = _.get(propertyMapping, 'type');
		var encoded = _.get(propertyMapping, 'encoded');

		//Many fields need to be copied over from the response object
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
			//for longitude an latitude, and we need to put them into an array.
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
						if (type === 'string' && typeof(returnValue) !== 'string' && returnValue !== null && returnValue !== undefined) {
							returnValue = returnValue.toString();
						}

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
			var finalResponse;

			deferred = $.Deferred();

			//Call the endpoint and pass through the data
			$.when(_callOneEndpoint(endpoint, context, {})).done(function(data) {
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
							if (type === 'string' && typeof(tempResponse) !== 'string') {
								tempResponse = tempResponse.toString();
							}
						}
					});

					//If there is data where it was expected, set that data to finalResponse
					if (tempResponse !== undefined && finalResponse === undefined) {
						finalResponse = tempResponse;

						//For fields such as types, we may need to translate data from the response via a mapping
						//dictionary that is specified in the provider definition.
						if (_.has(propertyMapping.value, 'translation')) {
							var typeMappings = _.get(context.mappings, 'type_mappings');

							finalResponse = _.get(_.get(typeMappings, propertyMapping.value.translation), finalResponse);
						}
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
		//Sometimes more than one field needs to be used to hydrate a parameter.
		//Some of these fields could require endpoint calls, so we need to use promises
		//to handle those cases.
		else if (hydration_method === 'concat') {
			var promiseList = [];
			var returnValues = [];
			deferred = $.Deferred();
			returnValue = '';

			//Iterate over each field and perform its hydration
			_.forEach(value, function(single_value, index) {
				if (single_value.hydration_method === 'endpoint') {
					var potentialPromise;
					potentialPromise = _hydrateField(context, single_value);

					promiseList.push(potentialPromise);
					potentialPromise.done(function(response) {
						returnValues[index] = response;
					});
				}
				else {
					returnValues[index] = _hydrateField(context, single_value);
				}
			});

			$.when.apply($, promiseList).done(function() {
				_.forEach(returnValues, function(value) {
					returnValue += value + ' ';
				});

				deferred.resolveWith(this, [returnValue]);
			});

			return deferred.promise();
		}
		else if (hydration_method === 'split') {
			var itemNumber, splitLocation, splitSeparator, splitArray, valueToSplit;
			splitLocation = _.get(value, 'location');
			splitSeparator = _.get(value, 'split_separator');
			valueToSplit = _.get(context, splitLocation);
			splitArray = valueToSplit.split(splitSeparator);

			itemNumber = _.get(value, 'item_number');
			if (itemNumber === 'last') {
				itemNumber = splitArray.length - 1;
			}

			return splitArray[itemNumber];
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
	function _processSignal(index) {
		var signalToRun, signalName;

		signalName = Object.keys(signalsToRun)[index];
		signalToRun = signalsToRun[signalName];

		$.when(_processPermissions(signalToRun)).done(function() {
			if (index < Object.keys(signalsToRun).length - 1) {
				index++;
				_processSignal(index);
			}
		});
	}

	/**
	 * Iterates through all of the Permissions for the given signal and calls _processEventSource on each one
	 *
	 */
	function _processPermissions(signalToRun) {
		var permissionPromiseList, signalPromise, signalData;

		permissionPromiseList = [];
		signalPromise = $.Deferred();
		signalData = {};

		function _postData(startIndex, eventList, promise) {
			var callData, eventSlice;

			eventSlice = eventList.slice(startIndex, startIndex + 1000);
			callData = {
				events: JSON.stringify(eventSlice)
			};

			console.log('Starting to post ' + eventSlice.length + ' events for ' + signalToRun.name + ' at ' + new Date());
			$.ajax({
				url: 'https://p.bitscoop.com/events',
				type: 'POST',
				data: callData,
				dataType: 'text',
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				},
				xhrFields: {
					withCredentials: true
				}
			}).done(function(data, xhr, response) {
				startIndex += 1000;

				console.log('Finished posting ' + eventSlice.length + ' events for ' + signalToRun.name + ' at ' + new Date());

				if (startIndex >= eventList.length - 1) {
					signalData.endpoint_data = signalToRun.endpoint_data;
					signalData.last_run = new Date().toJSON();

					promise.resolve();
				}
				else {
					_postData(startIndex, eventList, promise);
				}
			}).fail(function(data, xhr, response) {
				console.log('Event post for signal ' + signalToRun.name + ' failed at ' + new Date());
			});
		}

		function _runPermission(index) {
			var eventList, eventSource, permission, permissionName, permissionDeferred, $promise;

			eventList = [];
			$promise = $.Deferred();
			permissionName = Object.keys(signalToRun.permissions)[index];
			permission = signalToRun.permissions[permissionName];
			eventSource = permission.event_source;
			//Each permission will have a promise created for it.  This promise will only be resolved
			//if its event source runs successfully.  If the permission isn't enabled, then that permission
			//will be skipped.
			permissionDeferred = $.Deferred();

			if (permission.enabled) {
				permissionDeferred.promise();
				permissionPromiseList.push(permissionDeferred);

				console.log('Starting to fetch ' + permission.event_source.name + '.');
				_processEventSource(eventList, eventSource, signalToRun, permission, permissionDeferred);
			}

			//When all of a signal's permissions have run successfully, update the signal's lastRun field to the
			//the current datetime.  If any of them fail at any point, lastRun will not be updated so that we
			//do not lose any data.
			$.when(permissionDeferred).done(function(e) {
				$promise.promise();
				_postData(0, eventList, $promise);

				$.when($promise).done(function() {
					if (index < Object.keys(signalToRun.permissions).length - 1) {
						index++;
						_runPermission(index);
					}
					else {
						$.ajax({
							url: '/opi/signal/' + signalToRun.id,
							type: 'PATCH',
							contentType: 'application/json',
							data: JSON.stringify(signalData),
							dataType: 'json',
							headers: {
								'X-CSRFToken': $.cookie('csrftoken')
							}
						}).done(function (data, xhr, response) {
							console.log('Signal ' + signalToRun.name + ' lastRun updated successfully');
							signalPromise.resolve();
						});
					}
				});
			}).fail(function() {
				console.log('Permission ' + permission.name + ' failed.');
			});
		}

		console.log('Starting to run ' + signalToRun.name + ' at ' + new Date());
		signalPromise.promise();
		_runPermission(0);

		return signalPromise;
	}

	/**
	 * Get data from an eventSource
	 *
	 * @param {Object} eventList The list of Events to be sent to OPI
	 * @param {Object} eventSource One of the eventSource
	 * @param {Object} signal The Signal associated with the permission that is calling this eventSource
	 * @param {Object} permission The Permission that is calling this event source
	 * @param {Object} permissionDeferred A promise that the event source will resolve when it is finished gathering data
	 * @returns {Object} The raw data returned from the eventSource
	 */
	function _processEventSource(eventList, eventSource, signal, permission, permissionDeferred) {
		//This is the mapping of fields
		var context = {
			endpoints: _.get(eventSource, 'endpoints'),
			mappings: _.get(eventSource, 'mappings'),
			signal: signal,
			permission: permission
		};

		var endpointAndMappingName = _.get(eventSource, 'initial_mapping');
		var initialMapping = _.get(context.mappings, endpointAndMappingName);
		var eventSourcePromiseList = [];

		//Start the mapping process with the initial endpoint mapping
		_processMapping(initialMapping, endpointAndMappingName, {}, {});

		function _processMapping(mapping, endpointName, parentResponseObject, parentDeferred) {
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

			_processOneEndpointIteration(endpoint, mapping, context, parentDeferred);

			/**
			 * Process one call of an endpoint
			 * At the end, it will check to see if it needs to be called again
			 */
			function _processOneEndpointIteration(endpoint, mapping, context, parentDeferred) {
				//Call the endpoint, and when it is done act on the data that was passed back
				$.when(_callOneEndpoint(endpoint, context)).done(function(data) {
					var returnedDataLocation = _.get(mapping, 'returned_data_location');
					var localDeferredList = [];
					var conditionMapping = _.get(context.mapping, 'conditions');

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
						var localDeferred = $.Deferred();
						localDeferred.promise();
						localDeferredList.push(localDeferred);

						if (Object.keys(parentDeferred).length !== 0) {
							eventSourcePromiseList.push(localDeferred);
						}

						//If this endpoint was called solely to get data for another endpoint, call that endpoint
						if (mapping.hasOwnProperty('submapping')) {
							var endpointAndMappingName = _.get(mapping, 'submapping.endpoint');
							var newMapping = _.get(context.mappings, endpointAndMappingName);
							var skipSubmapping = false;

							responseObject.parentResponseObject = parentResponseObject;
							context.responseObject = responseObject;
							//If there are conditions on the mapping, check to see if this item matches each condition.
							//If any of them do not, then do not perform the child call.
							_.forEach(mapping.conditions, function(condition) {
								var conditionKey = Object.keys(condition)[0];
								var conditionVal = condition[conditionKey].value;
								var conditionField = condition[conditionKey].field;

								if (conditionKey === 'equals') {
									if (_.get(context, conditionField) !== conditionVal) {
										skipSubmapping = true;
									}
								}
								else if (conditionKey === 'notEquals') {
									if (_.get(context, conditionField) === conditionVal) {
										skipSubmapping = true;
									}
								}
							});

							if (!(skipSubmapping)) {
								_processMapping(newMapping, endpointAndMappingName, responseObject, localDeferred);
							}
							else {
								localDeferred.resolve();
							}
						}
						//Otherwise, update the global context and call mapSingleModel
						else {
							var localContext = $.extend({}, context);

							localContext.endpoint = endpoint;
							localContext.mapping = mapping;
							localContext.responseObject = responseObject;
							localContext.parentResponseObject = parentResponseObject;

							mapSingleModel(eventList, localContext, localDeferred);
						}
					});

					$.when.apply($, localDeferredList).then(function() {
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

									//If this endpoint call was a child of another, then parentDeferred will not
									//be an empty object.  In that case, resolve the promise that the parent
									//passed to this child. The parent will update permissionDeferred when it
									//determines that all of its child endpoint calls have finished.
									if (Object.keys(parentDeferred).length !== 0) {
										parentDeferred.resolve();
									}
									//If the endpoint call was not a child of another, then parentDeferred will be empty.
									//In that case, this point is reached only when all of the child endpoint calls
									//have been completed, and thus we have constructed all of the events and
									//are ready to post them, so resolve this permission's promise.
									else {
										permissionDeferred.resolve();
									}
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
										//and need to stop iteration on this event source
										else {
											loopEnd = true;

											//If this endpoint call was a child of another, then parentDeferred will not
											//be an empty object.  In that case, resolve the promise that the parent
											//passed to this child. The parent will update permissionDeferred when it
											//determines that all of its child endpoint calls have finished.
											if (Object.keys(parentDeferred).length !== 0) {
												parentDeferred.resolve();
											}
											//If the endpoint call was not a child of another, then parentDeferred will be empty.
											//In that case, this point is reached only when all of the child endpoint calls
											//have been completed, and thus we have constructed all of the events and
											//are ready to post them, so resolve this permission's promise.
											else {
												permissionDeferred.resolve();
											}
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

									//If this endpoint call was a child of another, then parentDeferred will not
									//be an empty object.  In that case, resolve the promise that the parent
									//passed to this child. The parent will update permissionDeferred when it
									//determines that all of its child endpoint calls have finished.
									if (Object.keys(parentDeferred).length !== 0) {
										parentDeferred.resolve();
									}
									//If the endpoint call was not a child of another, then parentDeferred will be empty.
									//In that case, this point is reached only when all of the child endpoint calls
									//have been completed, and thus we have constructed all of the events and
									//are ready to post them, so resolve this permission's promise.
									else {
										permissionDeferred.resolve();
									}
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

									//If this endpoint call was a child of another, then parentDeferred will not
									//be an empty object.  In that case, resolve the promise that the parent
									//passed to this child. The parent will update permissionDeferred when it
									//determines that all of its child endpoint calls have finished.
									if (Object.keys(parentDeferred).length !== 0) {
										parentDeferred.resolve();
									}
									//If the endpoint call was not a child of another, then parentDeferred will be empty.
									//In that case, this point is reached only when all of the child endpoint calls
									//have been completed, and thus we have constructed all of the events and
									//are ready to post them, so resolve this permission's promise.
									else {
										permissionDeferred.resolve();
									}
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

								//If this endpoint call was a child of another, then parentDeferred will not
								//be an empty object.  In that case, resolve the promise that the parent
								//passed to this child. The parent will update permissionDeferred when it
								//determines that all of its child endpoint calls have finished.
								if (Object.keys(parentDeferred).length !== 0) {
									parentDeferred.resolve();
								}
								//If the endpoint call was not a child of another, then parentDeferred will be empty.
								//In that case, this point is reached only when all of the child endpoint calls
								//have been completed, and thus we have constructed all of the events and
								//are ready to post them, so resolve this permission's promise.
								else {
									permissionDeferred.resolve();
								}
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
										else if (updateLocation === 'epoch_now') {
											updatedValue = new Date().getTime().toString();
										}
										else {
											updatedValue = _.get(responseData, updateLocation);
										}

										_.set(context.signal.endpoint_data[eventSource.name][endpointName], parameter, updatedValue);
									}
								});

								//If this endpoint call was a child of another, then parentDeferred will not
								//be an empty object.  In that case, resolve the promise that the parent
								//passed to this child. The parent will update permissionDeferred when it
								//determines that all of its child endpoint calls have finished.
								if (Object.keys(parentDeferred).length !== 0) {
									parentDeferred.resolve();
								}
								//If the endpoint call was not a child of another, then parentDeferred will be empty.
								//In that case, this point is reached only when all of the child endpoint calls
								//have been completed, and thus we have constructed all of the events and
								//are ready to post them, so resolve this permission's promise.
								else {
									permissionDeferred.resolve();
								}
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
										else if (updateLocation === 'epoch_now') {
											updatedValue = new Date().getTime().toString();
										}
										else {
											updatedValue = _.get(responseData, updateLocation);
										}

										_.set(context.signal.endpoint_data[eventSource.name][endpointName], parameter, updatedValue);
									}
								});

								//If this endpoint call was a child of another, then parentDeferred will not
								//be an empty object.  In that case, resolve the promise that the parent
								//passed to this child. The parent will update permissionDeferred when it
								//determines that all of its child endpoint calls have finished.
								if (Object.keys(parentDeferred).length !== 0) {
									parentDeferred.resolve();
								}
								//If the endpoint call was not a child of another, then parentDeferred will be empty.
								//In that case, this point is reached only when all of the child endpoint calls
								//have been completed, and thus we have constructed all of the events and
								//are ready to post them, so resolve this permission's promise.
								else {
									permissionDeferred.resolve();
								}
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
							parameter_descriptions = _.get(endpoint, 'parameter_descriptions');

							loopEnd = true;

							_.forEach(Object.keys(parameter_descriptions), function(parameter) {
								var thisParameter = parameter_descriptions[parameter];

								if (thisParameter.hasOwnProperty('save_to_signal')) {
									var updatedValue;
									var updateLocation = thisParameter.save_to_signal.location;
									if (updateLocation === 'date_now') {
										updatedValue = new Date().toJSON().split('T')[0].replace(/-/g, '/');
									}
									else if (updateLocation === 'epoch_now') {
										updatedValue = new Date().getTime().toString();
									}
									else {
										updatedValue = _.get(responseData, updateLocation);
									}

									_.set(context.signal.endpoint_data[eventSource.name][endpointName], parameter, updatedValue);
								}
							});

							//If this endpoint call was a child of another, then parentDeferred will not
							//be an empty object.  In that case, resolve the promise that the parent
							//passed to this child. The parent will update permissionDeferred when it
							//determines that all of its child endpoint calls have finished.
							if (Object.keys(parentDeferred).length !== 0) {
								parentDeferred.resolve();
							}
							//If the endpoint call was not a child of another, then parentDeferred will be empty.
							//In that case, this point is reached only when all of the child endpoint calls
							//have been completed, and thus we have constructed all of the events and
							//are ready to post them, so resolve this permission's promise.
							else {
								permissionDeferred.resolve();
							}
						}

						//If this isn't the last iteration through the endpoint
						if (!loopEnd) {
							_processOneEndpointIteration(endpoint, mapping, context, parentDeferred);
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
	 * Transform the raw data returned from the eventSource into BitScoop's format, then post that data to the database.
	 *
	 * @param {Object} eventList A list of Event objects to which the Event created by this call will be added.
	 * @param {Object} context
	 * @param {Object} eventSourceDeferred The deferred object that will be resolved once the item has been fully mapped.
	 */
	//TODO: Abstract posting into a callback passed into mapping a single model or after the mapping function returns the result
	function mapSingleModel(eventList, context, eventSourceDeferred) {
		var canHydrateLocation, organizationsList, conditionMapping, contentList, contactsList, dataList, dbEntryMapping, eventGeolocation, location, locationMapping, mapOrganizationsPromises, mapContactsPromises, mapContentPromises, mapPlacesPromises, mapThingsPromises, placesList, thingsList, totalPromises;

		contentList = [];
		contactsList = [];
		organizationsList = [];
		placesList = [];
		thingsList = [];
		dataList = [];
		dbEntryMapping = _.get(context.mapping, 'db_entry_mapping');
		conditionMapping = _.get(context.mapping, 'conditions');

		//Used in geolocation logic
		locationMapping = _.get(dbEntryMapping, 'location');
		eventGeolocation = _.get(locationMapping, 'geolocation');
		canHydrateLocation = _canHydrateLocation();

		//If there are any conditions
		_.forEach(conditionMapping, function(conditionValue, conditionKey) {
		});

		mapData();
		//Call mapContent, mapContacts, mapOrganizations, and mapLocation.  Each of these can be run independently of the others.
		//The first three return a list of promises.  These promises are resolved only when the mapping or mappings
		//have been completed.  mapContacts, mapContent, and mapOrganizations may create multiple db entries from a single piece of data,
		//so they have a list of promises, one for each item they are creating.
		mapContentPromises = mapContent();
		mapContactsPromises = mapContacts();
		mapOrganizationsPromises = mapOrganizations();
		mapPlacesPromises = mapPlaces();
		mapThingsPromises = mapThings();

		location = mapLocation();
		//Concatenate the list of promises from mapContent, mapContacts, and mapPeople into one list.
		totalPromises = mapContactsPromises.concat(mapContentPromises).concat(mapOrganizationsPromises).concat(mapThingsPromises);

		$.when.apply($, totalPromises).done(function() {
			//On some endpoints, you can get the same contact back multiple times, e.g. if you created the reddit thread
			//and posted in it and replied to your own post.  We don't want the same contact showing up in the
			//list of contacts multiple times, so this wil assemble a list of unique contacts for the event
			//that is about to be posted.
			var uniqueOrganizationsList = [];
			var uniqueOrganizationsMap = [];
			var uniqueContactsList = [];
			var uniqueContactsMap = [];
			var uniquePlacesList = [];
			var uniquePlacesMap = [];

			_.forEach(contactsList, function(contact) {
				if (uniqueContactsMap.indexOf(contact.identifier) === -1) {
					uniqueContactsMap.push(contact.identifier);
					uniqueContactsList.push(contact);
				}
			});

			_.forEach(organizationsList, function(organization) {
				if (uniqueOrganizationsMap.indexOf(organization.identifier) === -1) {
					uniqueOrganizationsMap.push(organization.identifier);
					uniqueOrganizationsList.push(organization);
				}
			});

			_.forEach(placesList, function(place) {
				if (uniquePlacesMap.indexOf(place.identifier) === -1) {
					uniquePlacesMap.push(place.identifier);
					uniquePlacesList.push(place);
				}
			});

			mapEvent(contentList, uniqueContactsList, uniqueOrganizationsList, uniquePlacesList, thingsList, location, eventSourceDeferred);
		}).fail(function() {
			//If something failed, then don't try to map the event, as we don't have the necessary information.
			//Just reject eventSourceDeferred so that this event source's information is not updated, and the next
			//time it runs it will try to map this again.
			eventSourceDeferred.reject();
		});


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
				//The identifier is a way for us to tell this particular item apart from other items of its type.
				//While the item's ID is also unique, we can't reconstruct an ObjectID from the data we receive.
				//Constructing identifier is repeatable.
				var identifier = context.signal.user_id + '_' + context.signal.id + '_';

				//TODO: Hash the unique ID once we're comfortable that this is working properly
				_.forEach(singleDataMapping.unique_identifiers, function(unique_identifier) {
					identifier += _hydrateField(context, unique_identifier) + '_';
				});
				identifier = identifier.substring(0, identifier.length - 1);

				dataObject = {
					data_dict: context.responseObject,
					identifier: identifier,
					user_id: context.signal.user_id
				};

				dataList.push(dataObject);
			});
		}

		//TODO: Make entire parent function more programmatic, better debug success/fail messages with ids?
		function mapEvent(contentList, contactsList, organizationsList, placesList, thingsList, location, eventSourceDeferred) {
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
						//Some endpoints are not returned in normal datetime formats nor epoch time.  Convert these
						//non-standard times.
						if (datetimeMapping.hasOwnProperty('format')) {
							//TODO: Should conversion from unix time and similar conversions be done in hydrateField?
							//Unix time needs to be multiplied by 1000 to get to epoch time.
							if (datetimeMapping.format === 'unix_time') {
								jsonDatetime = new Date(response * 1000).toJSON();
							}
							else if (datetimeMapping.format === 'unix_time_ms') {
								jsonDatetime = new Date(response).toJSON();
							}
						}
						//If the datetime is in a normal, parseable format, just create a new date and convert it to JSON format.
						else {
							jsonDatetime = new Date(response).toJSON();
						}
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
						else if (datetimeMapping.format === 'unix_time_ms') {
							jsonDatetime = new Date(response).toJSON();
						}
					}
					//If the datetime is in a normal, parseable format, just create a new date and convert it to JSON format.
					else {
						jsonDatetime = new Date(jsonDatetime).toJSON();
					}
				}
			}

			//Wait for the datetime to be retrieved from an endpoint if needed.
			//If not, this will be resolved immediately.
			$.when(potentialPromise).done(function() {
				//The identifier is a way for us to tell this particular item apart from other items of its type.
				//While the item's ID is also unique, we can't reconstruct an ObjectID from the data we receive.
				//Constructing identifier is repeatable.
				var identifier = context.signal.user_id + '_' + context.signal.id + '_';

				//TODO: Hash the unique ID once we're comfortable that this is working properly
				_.forEach(eventMapping.unique_identifiers, function(unique_identifier) {
					identifier += _hydrateField(context, unique_identifier) + '_';
				});
				identifier = identifier.substring(0, identifier.length - 1);

				eventObject = {
					organizations: organizationsList,
					contacts: contactsList,
					contact_interaction_type: _hydrateField(context, _.get(eventMapping.mapped_fields, 'contact_interaction_type')),
					content: contentList,
					data: dataList,
					datetime: jsonDatetime,
					location: location,
					identifier: identifier,
					places: placesList,
					provider: context.signal.provider.provider_number,
					provider_name: context.signal.provider.name,
					signal: context.signal.id,
					things: thingsList,
					type: _.get(context.mapping, 'type'),
					user_id: context.signal.user_id
				};

				eventList.push(eventObject);
				eventSourceDeferred.resolve();
			});
		}


		//Create a location if possible
		function mapLocation() {
			//Only try to create a location if it's possible to do so
			if (canHydrateLocation) {
				var locationObject = {};

				//Map the location's fields as specified by the event source's mapping
				_.forEach(locationMapping, function(eventValue, eventKey) {
					if (eventKey === 'datetime') {
						var datetime = _hydrateField(context, eventValue);

						//Do any conversions of the datetime if needed before creating it and converting to JSON format.
						if (eventValue.hasOwnProperty('format')) {
							if (eventValue.format === 'unix_time') {
								locationObject[eventKey] = new Date(datetime * 1000).toJSON();
							}
							else if (datetimeMapping.format === 'unix_time_ms') {
								jsonDatetime = new Date(response).toJSON();
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

				return locationObject;
			}
			//If the location cannot be created, then just set it to undefined and resolve the promise.
			//The server will estimate the location when the event gets posted.
			else {
				return undefined;
			}
		}


		//Create content documents in the DB from this item
		function mapContent() {
			var masterPromiseList = [];
			var subObject;
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
				});

				if (!(skipPost)) {
					if (contentSingleMap.hasOwnProperty('hydrate_list_location')) {
						items = _.get(context, contentSingleMap.hydrate_list_location);
					}
					else {
						items = [context];
					}

					_.forEach(items, function(item) {
						subObject = {};

						//The masterPromiseList holds a deferred for each content item we are trying to map.
						//For this item, push its deferred onto the list and create the promise.
						masterPromiseList.push(masterPromise);
						masterPromise.promise();

						//Map the fields for this content item.
						//As with other mappings like this, a promise is created if the field has to come from another
						//endpoint call, and that promise is resovled when that further endpoint call is finished.
						_.forEach(contentSingleMap.mapped_fields, function(contentValue, contentKey) {
							if (contentValue.hydration_method === 'endpoint' || contentValue.hydration_method === 'concat') {
								var potentialPromise;

								context.subObject = item;
								potentialPromise = _hydrateField(context, contentValue);

								promiseList.push(potentialPromise);
								potentialPromise.done(function(response) {
									subObject[contentKey] = response;
								});
							}
							else {
								subObject[contentKey] = _hydrateField(item, contentValue);
							}
						});

						//This waits for any field mapping promises to be resolved.
						$.when.apply($, promiseList).done(function() {
							var promiseList = [];
							//The identifier is a way for us to tell this particular item apart from other items of its type.
							//While the item's ID is also unique, we can't reconstruct an ObjectID from the data we receive.
							//Constructing identifier is repeatable.
							var identifier = context.signal.user_id + '_' + context.signal.id + '_';

							//TODO: Hash the unique ID once we're comfortable that this is working properly
							_.forEach(contentSingleMap.unique_identifiers, function(unique_identifier) {
								var newField, potentialPromise;

								if (unique_identifier.hydration_method === 'endpoint' || unique_identifier.hydration_method === 'concat') {
									context.subObject = item;

									potentialPromise = _hydrateField(context, unique_identifier);
									promiseList.push(potentialPromise);
									potentialPromise.done(function(response) {
										newField = response;
									});
								}
								else {
									newField = _hydrateField(item, unique_identifier);
								}

								$.when(potentialPromise).done(function() {
									if (newField === undefined || newField === null) {
										skipPost = true;
									}
									else {
										identifier += newField + '_';
									}
								});
							});

							$.when.apply($, promiseList).done(function() {
								identifier = identifier.substring(0, identifier.length - 1);

								subObject.identifier = identifier;

								if (!skipPost) {
									contentList.push(subObject);
								}

								masterPromise.resolve();
							});
						});
					});
				}
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

						contactObject = {};

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
							//The identifier is a way for us to tell this particular item apart from other items of its type.
							//While the item's ID is also unique, we can't reconstruct an ObjectID from the data we receive.
							//Constructing identifier is repeatable.
							var identifier = context.signal.user_id + '_' + context.signal.id + '_';

							//TODO: Hash the unique ID once we're comfortable that this is working properly
							_.forEach(contactMapping.unique_identifiers, function(unique_identifier) {
								var newField, potentialPromise;

								if (unique_identifier.hydration_method === 'endpoint') {
									potentialPromise = _hydrateField(context, unique_identifier);
									promiseList.push(potentialPromise);
									potentialPromise.done(function(response) {
										newField = response;
									});
								}
								else {
									newField = _hydrateField(contact, unique_identifier);
								}

								$.when(potentialPromise).done(function() {
									if (newField === undefined || newField === null) {
										skipPost = true;
									}
									else {
										identifier += newField + '_';
									}
								});
							});

							$.when.apply($, promiseList).done(function() {
								identifier = identifier.substring(0, identifier.length - 1);

								contactObject.identifier = identifier;

								if (!skipPost) {
									contactsList.push(contactObject);
								}
								masterPromise.resolve();
							});
						});
					});
				});
			});

			return masterPromiseList;
		}

		function mapOrganizations() {
			var organizationsMapping = _.get(dbEntryMapping, 'organizations');
			var masterPromiseList = [];

			_.forEach(organizationsMapping, function(organizationMapping) {
				var hydratePromise, contextHydrateList;
				//hydrateList is where potential organizations are listed on the object we are mapping.
				var hydrateList = _.get(organizationMapping, 'hydrate_list_location');
				var deferred = $.Deferred();

				//If we need to call an endpoint to get more information for this organization, do so, and create
				//a promise that is only resolved when the endpoint call has finsihed.
				if (organizationMapping.hasOwnProperty('call_endpoint')) {
					hydratePromise = _hydrateField(context, organizationMapping.call_endpoint);
					hydratePromise.done(function(item) {
						context.childObject = item;
						deferred.resolve();
					});
				}
				else {
					deferred.resolve();
				}

				$.when(deferred).done(function() {
					//Get the list of organizations to be created
					contextHydrateList = _.get(context, hydrateList);

					//The contextHydrateList is supposed to be a list.  If it's a single organization, add them to a list
					//anyway so it can be iterated over.
					if (!(Array.isArray(contextHydrateList))) {
						contextHydrateList = [contextHydrateList];
					}

					_.forEach(contextHydrateList, function(organization) {
						var masterPromise = $.Deferred();
						var organizationObject;
						var promiseList = [];
						var skipPost = false;

						//The masterPromiseList holds a deferred for each organization item we are trying to map.
						//For this item, push its deferred onto the list and create the promise.
						masterPromiseList.push(masterPromise);
						masterPromise.promise();

						organizationObject = {};

						//Map all of the fields shown in the mapping.
						//If a mapping needs to call an endpoint to get more data, create a promise that will be
						//resolved only when the endpoint has been called.
						_.forEach(organizationMapping.mapped_fields, function(organizationValue, organizationKey) {
							if (organizationValue.hydration_method === 'endpoint') {
								var potentialPromise = _hydrateField(context, organizationValue);
								promiseList.push(potentialPromise);
								potentialPromise.done(function(response) {
									organizationObject[organizationKey] = response;
								});
							}
							else {
								organizationObject[organizationKey] = _hydrateField(organization, organizationValue);
							}
						});

						$.when.apply($, promiseList).done(function() {
							var promiseList = [];
							//The identifier is a way for us to tell this particular item apart from other items of its type.
							//While the item's ID is also unique, we can't reconstruct an ObjectID from the data we receive.
							//Constructing identifier is repeatable.
							var identifier = context.signal.user_id + '_' + context.signal.id + '_';

							//TODO: Hash the unique ID once we're comfortable that this is working properly
							_.forEach(organizationMapping.unique_identifiers, function(unique_identifier) {
								var newField, potentialPromise;

								if (unique_identifier.hydration_method === 'endpoint') {
									potentialPromise = _hydrateField(context, unique_identifier);
									promiseList.push(potentialPromise);
									potentialPromise.done(function(response) {
										newField = response;
									});
								}
								else {
									newField = _hydrateField(organization, unique_identifier);
								}

								$.when(potentialPromise).done(function() {
									if (newField === undefined || newField === null) {
										skipPost = true;
									}
									else {
										identifier += newField + '_';
									}
								});
							});

							$.when.apply($, promiseList).done(function() {
								identifier = identifier.substring(0, identifier.length - 1);

								organizationObject.identifier = identifier;

								if (!skipPost) {
									organizationsList.push(organizationObject);
								}
								masterPromise.resolve();
							});
						});
					});
				});
			});

			return masterPromiseList;
		}

		//Create place documents in the DB from this item
		function mapPlaces() {
			var masterPromiseList = [];
			var subObject;
			var placesMasterMapping = _.get(dbEntryMapping, 'places');
			var promiseList = [];

			//Some endpoints may provide multiple types of places, so map each of them as specified in their
			//individual mappings.
			_.forEach(placesMasterMapping, function(placesSingleMap) {
				var skipPost = false;
				var masterPromise = $.Deferred();
				var conditionMapping = _.get(placesSingleMap, 'conditions');
				var items;

				//If there are conditions on the mapping, check to see if this item matches each condition.
				//If any of them do not, then this item will not be posted to the DB.
				_.forEach(conditionMapping, function(condition) {
					var conditionKey = Object.keys(condition)[0];
					var conditionVal = condition[conditionKey].value;
					var conditionField = condition[conditionKey].field;

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
				});

				if (!(skipPost)) {
					if (placesSingleMap.hasOwnProperty('hydrate_list_location')) {
						items = _.get(context, placesSingleMap.hydrate_list_location);
					}
					else {
						items = [context];
					}

					_.forEach(items, function(item) {
						subObject = {};

						//The masterPromiseList holds a deferred for each place item we are trying to map.
						//For this item, push its deferred onto the list and create the promise.
						masterPromiseList.push(masterPromise);
						masterPromise.promise();

						//Map the fields for this place item.
						//As with other mappings like this, a promise is created if the field has to come from another
						//endpoint call, and that promise is resovled when that further endpoint call is finished.
						_.forEach(placesSingleMap.mapped_fields, function(placesValue, placesKey) {
							if (placesValue.constructor === Array) {
								_.forEach(placesValue, function(placeValue, placeKey) {
									if (placeValue.hydration_method === 'endpoint' || placeValue.hydration_method === 'concat') {
										var potentialPromise;

										context.subObject = item;
										potentialPromise = _hydrateField(context, placeValue);

										promiseList.push(potentialPromise);
										potentialPromise.done(function(response) {
											subObject[placeKey].append(response);
										});
									}
									else {
										subObject[placeKey].append(_hydrateField(item, placeValue));
									}
								});
							}
							else if (placesValue.hydration_method === 'endpoint' || placesValue.hydration_method === 'concat') {
								var potentialPromise;

								context.subObject = item;
								potentialPromise = _hydrateField(context, placesValue);

								promiseList.push(potentialPromise);
								potentialPromise.done(function(response) {
									subObject[placesKey] = response;
								});
							}
							else {
								subObject[placesKey] = _hydrateField(item, placesValue);
							}
						});

						//This waits for any field mapping promises to be resolved.
						$.when.apply($, promiseList).done(function() {
							var promiseList = [];
							//The identifier is a way for us to tell this particular item apart from other items of its type.
							//While the item's ID is also unique, we can't reconstruct an ObjectID from the data we receive.
							//Constructing identifier is repeatable.
							var identifier = context.signal.user_id + '_' + context.signal.id + '_';

							//TODO: Hash the unique ID once we're comfortable that this is working properly
							_.forEach(placesSingleMap.unique_identifiers, function(unique_identifier) {
								var newField, potentialPromise;

								if (unique_identifier.hydration_method === 'endpoint' || unique_identifier.hydration_method === 'concat') {
									context.subObject = item;

									potentialPromise = _hydrateField(context, unique_identifier);
									promiseList.push(potentialPromise);
									potentialPromise.done(function(response) {
										newField = response;
									});
								}
								else {
									newField = _hydrateField(item, unique_identifier);
								}

								$.when(potentialPromise).done(function() {
									if (newField === undefined || newField === null) {
										skipPost = true;
									}
									else {
										identifier += newField + '_';
									}
								});
							});

							$.when.apply($, promiseList).done(function() {
								identifier = identifier.substring(0, identifier.length - 1);

								subObject.identifier = identifier;

								if (!skipPost) {
									placesList.push(subObject);
								}

								masterPromise.resolve();
							});
						});
					});
				}
			});

			return masterPromiseList;
		}

		//Create thing documents in the DB from this item
		function mapThings() {
			var masterPromiseList = [];
			var subObject;
			var thingsMasterMapping = _.get(dbEntryMapping, 'things');
			var promiseList = [];

			//Some endpoints may provide multiple types of things, so map each of them as specified in their
			//individual mappings.
			_.forEach(thingsMasterMapping, function(thingsSingleMap) {
				var skipPost = false;
				var masterPromise = $.Deferred();
				var conditionMapping = _.get(thingsSingleMap, 'conditions');
				var items;

				//If there are conditions on the mapping, check to see if this item matches each condition.
				//If any of them do not, then this item will not be posted to the DB.
				_.forEach(conditionMapping, function(condition) {
					var conditionKey = Object.keys(condition)[0];
					var conditionVal = condition[conditionKey].value;
					var conditionField = condition[conditionKey].field;

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
				});

				if (!(skipPost)) {
					if (thingsSingleMap.hasOwnProperty('hydrate_list_location')) {
						items = _.get(context, thingsSingleMap.hydrate_list_location);
					}
					else {
						items = [context];
					}

					_.forEach(items, function(item) {
						subObject = {};

						//The masterPromiseList holds a deferred for each thing item we are trying to map.
						//For this item, push its deferred onto the list and create the promise.
						masterPromiseList.push(masterPromise);
						masterPromise.promise();

						//Map the fields for this thing item.
						//As with other mappings like this, a promise is created if the field has to come from another
						//endpoint call, and that promise is resovled when that further endpoint call is finished.
						_.forEach(thingsSingleMap.mapped_fields, function(thingsValue, thingsKey) {
							if (thingsValue.constructor === Array) {
								subObject[thingsKey] = [];
								_.forEach(thingsValue, function(thingValue) {
									if (thingValue.hydration_method === 'endpoint' || thingValue.hydration_method === 'concat') {
										var potentialPromise;

										context.subObject = item;
										potentialPromise = _hydrateField(context, thingValue);

										promiseList.push(potentialPromise);
										potentialPromise.done(function(response) {
											subObject[thingsKey].push(response);
										});
									}
									else {
										subObject[thingsKey].push(_hydrateField(item, thingValue));
									}
								});
							}
							else if (thingsValue.hydration_method === 'endpoint' || thingsValue.hydration_method === 'concat') {
								var potentialPromise;

								context.subObject = item;
								potentialPromise = _hydrateField(context, thingsValue);

								promiseList.push(potentialPromise);
								potentialPromise.done(function(response) {
									subObject[thingsKey] = response;
								});
							}
							else {
								subObject[thingsKey] = _hydrateField(item, thingsValue);
							}
						});

						//This waits for any field mapping promises to be resolved.
						$.when.apply($, promiseList).done(function() {
							var promiseList = [];
							//The identifier is a way for us to tell this particular item apart from other items of its type.
							//While the item's ID is also unique, we can't reconstruct an ObjectID from the data we receive.
							//Constructing identifier is repeatable.
							var identifier = context.signal.user_id + '_' + context.signal.id + '_';

							//TODO: Hash the unique ID once we're comfortable that this is working properly
							_.forEach(thingsSingleMap.unique_identifiers, function(unique_identifier) {
								var newField, potentialPromise;

								if (unique_identifier.hydration_method === 'endpoint' || unique_identifier.hydration_method === 'concat') {
									context.subObject = item;

									potentialPromise = _hydrateField(context, unique_identifier);
									promiseList.push(potentialPromise);
									potentialPromise.done(function(response) {
										newField = response;
									});
								}
								else {
									newField = _hydrateField(item, unique_identifier);
								}

								$.when(potentialPromise).done(function() {
									if (newField === undefined || newField === null) {
										skipPost = true;
									}
									else {
										identifier += newField + '_';
									}
								});
							});

							$.when.apply($, promiseList).done(function() {
								identifier = identifier.substring(0, identifier.length - 1);

								subObject.identifier = identifier;

								if (!skipPost) {
									thingsList.push(subObject);
								}

								masterPromise.resolve();
							});
						});
					});
				}
			});

			return masterPromiseList;
		}
	}

	return {
		schedule: schedule,
		run: run
	};
});
