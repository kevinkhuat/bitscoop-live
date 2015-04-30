//Construct search filters to send to the database
function searchView(dataInst, mapboxViewInst, urlParserInst) {
	//Add the intial filter dropdown to a new filter after using Nunjucks to render it
	//from a template.
	//By default the topmost option of the initial dropdown will be selected, so call its
	//render function.
	//Bind an event listener that triggers when the initial dropdown changes.
	//This listener will call the appropriate render function based on which option was selected.
	function addDropdown(inputSelection) {
		var newDropdown = nunjucks.render('search/initial_filter_dropdown.html', {
			eventType: inputSelection.parent().attr('id')
		});
		$(inputSelection).find('.filter.box:last .filter.options').html(newDropdown);

		var initDropdown = $(inputSelection).find('.filter.box:last .initial')[0];
		filters().provider().dropdown(initDropdown);

		$(inputSelection).find('.filter.box:last .initial').change(function() {
			var currentElement = this;

			$(currentElement).siblings().remove();
			if (currentElement.value == 'area') {
				filters().area().dropdown(currentElement);
			}
			else if (currentElement.value == 'created') {
				filters().date().dropdown(currentElement);
			}
			else if (currentElement.value == 'datetime') {
				filters().date().dropdown(currentElement);
			}
			//else if (currentElement.value == 'time') {
			//	filters().time().dropdown(currentElement);
			//}
			else if (currentElement.value == 'from') {
				filters().from().dropdown(currentElement);
			}
			else if (currentElement.value == 'near') {
				filters().near().dropdown(currentElement);
			}
			else if (currentElement.value == 'provider') {
				filters().provider().dropdown(currentElement);
			}
			else if (currentElement.value == 'signal') {
				filters().signal().dropdown(currentElement);
			}
			else if (currentElement.value == 'to') {
				filters().to().dropdown(currentElement);
			}
			else if (currentElement.value == 'updated') {
				filters().date().dropdown(currentElement);
			}

			checkDrawDisplay();
		});
	}

	//Adds a new filter by rendering the base elements and then adding the initial dropdown
	//which will in turn add all of the other dropdowns and elements it needs.
	function addFilter(inputSelection) {
		createFilterBase(inputSelection);
		addDropdown(inputSelection);
		eventType = inputSelection.parents().attr('id');
		eventType = eventType.charAt(0).toUpperCase() + eventType.slice(1) + 's';
		inputSelection.siblings().find('.item').html(eventType);
	}

	//Create the base elements of a filter
	function createFilterBase(inputSelection) {
		//Render the base framework of a filter from a template using Nunjucks.
		var newFilter = nunjucks.render('search/filter.html');
		$(inputSelection).append(newFilter);

		//Bind event listeners to the add filter and remove filter buttons.
		//These will call the add and remove filter functions on click.
		$(inputSelection).find('.filter.box:last .filter.button.add').on('click', function() {
			addFilter($(this).closest('.filters'));
		});

		$(inputSelection).find('.filter.box:last .filter.button.add')
			.add('.filter.box:last .filter.button.remove')
			.mouseenter(function() {
				$(this).addClass('hover');
			})
			.mouseleave(function() {
				$(this).removeClass('hover');
			})
			.click(function() {
				$(this).removeClass('hover');
			});

		$(inputSelection).find('.filter.box:last .filter.button.remove').on('click', function() {
			var customFilter = false;
			var filterList = $('.filters');
			removeFilter(this);
			for (var i = 0; i < filterList.length; i++) {
				if ($(filterList[i]).children().length > 0) {
					customFilter = true;
				}
			}

			if (customFilter === true) {
				$('.filter-button').addClass('active');
			}
			else {
				if ($('.selector').not('.active').length > 0) {
					$('.filter-button').addClass('active');
				}
				else {
					$('.filter-button').removeClass('active');
				}
			}
		});
	}

	//Remove the filter that the selected remove button is part of.
	function removeFilter(currentButton) {
		if ($(currentButton).parents('.filters').children().length === 1 && $(currentButton).parents('.filters').siblings().find('.active').length !== 0) {
			eventType = $(currentButton).parents('.type-grouping').attr('id');
			eventType = eventType.charAt(0).toUpperCase() + eventType.slice(1) + 's';
			$(currentButton).parents('.filters').siblings().find('.item').html('All ' + eventType)
		}
		$(currentButton).parents('.filter.box').remove();
		checkDrawDisplay();
	}

	function submitSearch(event) {
		//Prevent normal form submission from bubbling any further up.
		event.stopPropagation();

		var typeList = $('.type-grouping');

		for (var k = 0; k < typeList.length; k++) {
			var thisType = typeList[k];
			if ($(thisType).find('.selector.active').length > 0) {
				var filterString = '';

				//Get a list of the filters that are being used
				var filtersList = $(thisType).find('.filter.options');

				var sort;
				//For each filter, construct the appropriate filter string and add it to the
				//full filter string that will be submitted to the database.
				for (var i = 0; i < filtersList.length; i++) {
					var currentFilter = filtersList[i];

					//Determine what type of filter this is
					var type = $(currentFilter).children('.initial')[0].value;

					//If this isn't the first filter, append an AND to the top-level filter string.
					if (i !== 0) {
						filterString += ' or ';
					}

					//Construct the filter string based on the filter type
					if (type == 'area') {
						filterString += '(' + filters().area().toString(currentFilter) + ')';
					}
					else if (type == 'created') {
						filterString += '(' + filters().date().toString(currentFilter, 'created') + ')';
					}
					else if (type == 'datetime') {
						filterString += '(' + filters().date().toString(currentFilter, 'datetime') + ')';
					}
					else if (type == 'from') {
						filterString += '(' + filters().from().toString(currentFilter) + ')';
					}
					//else if (type == 'time') {
					//	filterString += '(' + filters().time().toString(currentFilter) + ')';
					//}
					else if (type == 'near') {
						filterString += '(' + filters().near().toString(currentFilter) + ')';
					}
					else if (type == 'provider') {
						filterString += '(' + filters().provider().toString(currentFilter) + ')';
					}
					else if (type == 'signal') {
						filterString += '(' + filters().signal().toString(currentFilter) + ')';
					}
					else if (type == 'to') {
						filterString += '(' + filters().to().toString(currentFilter) + ')';
					}
					else if (type == 'updated') {
						filterString += '(' + filters().date().toString(currentFilter, 'updated') + ')';
					}
				}

				//Set the Query and Filters in the URL parser
				urlParserInst.setSearchQuery($('.search-bar').val());
				urlParserInst.setSearchFilters(filterString);

				sort = urlParserInst.getSort();
				//Perform a search based on the search terms and filters
				dataInst.search(thisType.id, filterString, sort);
			}
		}

		return false;
	}
	//Create event listeners for actions related to searching
	function bindEvents() {
		//Perform the search when the form that contains the search bar is submitted.
		$('#search-form').submit(function(event) {
			return submitSearch(event);
		});

		$('.search-button').click(function(event) {
			return submitSearch(event);
		});

		//Toggle whether to search for the clicked type of information
		$('.dropdown .item').not('.add-filter').click(function() {
			$(this).toggleClass('active');
			if ($(this).hasClass('active') && $(this).closest('.flex').siblings().children().length === 0) {
				eventType = $(this).parents('.type-groping').attr('id');
				eventType = eventType.charAt(0).toUpperCase() + eventType.slice(1) + 's';
				$(this).siblings('.item').html('All ' + eventType);
			}
			else {
				eventType = $(this).parents('.type-groping').attr('id');
				eventType = eventType.charAt(0).toUpperCase() + eventType.slice(1) + 's';
				$(this).siblings('.item').html(eventType);
			}
		});

		//Create a filter when the "Add a filter" button is selected.
		//By default, there are no filters, and this is the only way to add
		//the first one.  Additional filters can be created from the "+" button
		//on existing filters.
		$('.menu .add-filter').click(function() {
			addFilter($(this).parent().siblings('.filters'));
		});
	}

	function checkDrawDisplay() {
		var initialSet = $('.initial');
		var len = initialSet.length;
		var showMarkerDraw = false;
		var showPolygonDraw = false;
		var map = mapboxViewInst.map;

		for (var i = 0; i < len; i++) {
			if (initialSet[i].value === 'area') {
				showPolygonDraw = true;
			}
			if (initialSet[i].value === 'near') {
				showMarkerDraw = true;
			}
		}

		if (showPolygonDraw && (map.polygonDrawControl._map === null || map.polygonDrawControl._map === undefined)) {
			map.polygonDrawControl.addTo(map);
		}
		else {
			if (!showPolygonDraw && map.polygonDrawControl._map !== null && map.polygonDrawControl._map !== undefined) {
				map.polygonDrawControl.removeFrom(map);
			}
		}

		if (showMarkerDraw && (map.markerDrawControl._map === null || map.markerDrawControl._map === undefined)) {
			map.markerDrawControl.addTo(map);
		}
		else {
			if (!showMarkerDraw && map.markerDrawControl._map !== null && map.markerDrawControl._map !== undefined) {
				map.markerDrawControl.removeFrom(map);
			}
		}
	}

	function filters() {
		//Render the elements needed to filter on From a given person
		function area() {
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;

				//Render the From field using Nunjucks and add it to the DOM
				var newField = nunjucks.render('search/filters/area/area.html');
				$(parent).append(newField);
			}

			function toString(currentFilter) {
				currentValue = $(currentFilter).find('.area')[0].value;
				if (currentValue === 'within') {
					var returnString = 'location geo_within_polygon \'[';
				}
				else if (currentValue === 'without') {
					var returnString = 'not (location geo_within_polygon \'[';
				}
				var loopEnd = mapboxViewInst.map.polySelect.length;
				for (var i = 0; i < loopEnd; i++) {
					var thisLatLng = mapboxViewInst.map.polySelect[i];
					returnString += '[' + [thisLatLng.lng, thisLatLng.lat] + '], ';
				}
				var thisLatLng = mapboxViewInst.map.polySelect[0];
				returnString += '[' + [thisLatLng.lng, thisLatLng.lat] + ']]\'';
				if (currentValue === 'without') {
					returnString += ')';
				}
				console.log(returnString);
				return returnString;
			}

			return {
				dropdown: dropdown,
				toString: toString
			};
		}

		function from() {
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;

				//Render the From field using Nunjucks and add it to the DOM
				var newField = nunjucks.render('search/filters/message_from/from_text_field.html');
				$(parent).append(newField);
			}

			//Consruct a filter string from an inputted From
			function toString(currentFilter) {
				return 'message_from contains ' + $(currentFilter).find('.from-text')[0].value;
			}

			return {
				dropdown: dropdown,
				toString: toString
			};
		}

		//Render the elements needed to filter on Dates
		function date() {
			//Create the Date dropdown
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;
				//Render the Date dropdown from a template using Nunjucks and add it to the DOM
				var newDropdown = nunjucks.render('search/filters/date/date_dropdown.html');
				$(parent).append(newDropdown);

				//Bind an event listener to the new dropdown.
				//When the dropdown is changed, the listener will add the appropriate fields
				//based on which option was selected.
				$(parent).find('.date').change(function() {
					var currentElement = this;

					//Remove the existing filter elements from this filter
					//except for the initial dropdown.
					$(currentElement).siblings().not('.initial').remove();

					//Call the appropriate function to render additional fields based
					//on which option was selected.
					if (currentElement.value == 'after') {
						afterField(currentElement);
					}
					else if (currentElement.value == 'before') {
						beforeField(currentElement);
					}
					else if (currentElement.value == 'between') {
						betweenFields(currentElement);
					}
				});

				//When the Date dropdown is first created, set it to the first option
				//in the dropdown and render the associated fields.
				var initDateDropdown = $(parent).find('.date')[0];
				filters().date().afterField(initDateDropdown);
			}

			//Render the After field with Nunjucks and add it to the DOM.
			function afterField(currentElement) {
				var newDropdown = nunjucks.render('search/filters/date/date_after_field.html');
				$(currentElement.parentElement).append(newDropdown);
			}

			//Render the Before field with Nunjucks and add it to the DOM.
			function beforeField(currentElement) {
				var newDropdown = nunjucks.render('search/filters/date/date_before_field.html');
				$(currentElement.parentElement).append(newDropdown);
			}

			//Render the Between fields with Nunjucks and add them to the DOM.
			function betweenFields(currentElement) {
				var newDropdown = nunjucks.render('search/filters/date/date_between_fields.html');
				$(currentElement.parentElement).append(newDropdown);
			}


			//Construct a filter string from an inputted Date
			function toString(currentFilter, dateField) {
				//Add the text for "date after XXX"
				function appendAfter(currentFilter) {
					return dateField + ' gt \'' + $(currentFilter).find('.date-start')[0].value + '\'';
				}

				//Add the text for "date before XXX"
				function appendBefore(curretFilter) {
					return dateField + ' lt \'' + $(currentFilter).find('.date-end')[0].value + '\'';
				}

				var returnString = '';

				//By default set the delimeter to the first dropdown option since
				//that is selected on filter creation.
				var delimeter = $(currentFilter).children('.date')[0];

				//Add the filter string depending on which option is currently selected.
				if (delimeter.value == 'after') {
					returnString += appendAfter(currentFilter);
				}
				else if (delimeter.value == 'before') {
					returnString += appendBefore(currentFilter);
				}
				else if (delimeter.value == 'between') {
					returnString += appendBefore(currentFilter) + ' and ' + appendAfter(currentFilter);
				}

				return returnString;
			}

			return {
				afterField: afterField,
				beforeField: beforeField,
				betweenFields: betweenFields,
				dropdown: dropdown,
				toString: toString
			};
		}

		function near() {
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;

				//Render the near dropdown using Nunjucks and add it to the DOM
				var newField = nunjucks.render('search/filters/near/near.html');
				$(parent).append(newField);
				radiusField(currentElement);

				$(parent).find('.near').change(function() {
					var currentElement = this;

					//Remove the existing filter elements from this filter
					//except for the initial dropdown.
					$(currentElement).siblings().not('.initial').remove();

					//Call the appropriate function to render additional fields based
					//on which option was selected.
					if (currentElement.value == 'coordinates') {
						coordinateField(currentElement);
					}

					radiusField(currentElement);
				});
			}

			//Render the coordinate fields with Nunjucks and add them to the DOM.
			function coordinateField(currentElement) {
				var newDropdown = nunjucks.render('search/filters/near/near_coordinate_field.html');
				$(currentElement.parentElement).append(newDropdown);
			}

			function radiusField(currentElement) {
				var newField = nunjucks.render('search/filters/near/near_radius_field.html');
				$(currentElement.parentElement).append(newField);
			}

			function toString(currentFilter) {
				currentValue = $(currentFilter).find('.near')[0].value;
				var returnString = 'location near \'';
				if (currentValue === 'selection') {
					var thisLatLng = mapboxViewInst.map.markerSelect;
					returnString += '[' + [thisLatLng.lng, thisLatLng.lat] + ']\'';
				}
				else {
					returnString += '[' + [$('.near.longitude')[0].value, $('.near.latitude')[0].value] + ']\'';
				}
				//max_distance is in meters, and we're getting the input in miles, so we need to convert
				returnString += ' and location max_distance ' + ($('.near.radius')[0].value * 1609.34);
				return returnString;
			}

			return {
				coordinateField: coordinateField,
				dropdown: dropdown,
				toString: toString
			};
		}

		function provider() {
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;

				//Render the provider list using Nunjucks and add it to the DOM
				var newField = nunjucks.render('search/filters/provider/provider_dropdown.html');
				$(parent).append(newField);
			}

			//Consruct a filter string from an inputted From
			function toString(currentFilter) {
				return 'provider_name contains ' + $(currentFilter).find('.provider')[0].value;
			}

			return {
				dropdown: dropdown,
				toString: toString
			};
		}

		function signal() {
			function dropdown(currentElement) {
				var cookie = sessionsCookies().getCsrfToken();
				var parent = currentElement.parentElement;
				$.ajax({
					url: '/opi/signal',
					type: 'GET',
					dataType: 'json',
					headers: {
						'X-CSRFToken': cookie
					}
				}).done(function(data, xhr, response) {
					var signals = data;

					//Render the signal list using Nunjucks and add it to the DOM
					var newField = nunjucks.render('search/filters/signal/signal_dropdown.html', {
						signals: signals
					});
					$(parent).append(newField);
				});
			}

			//Consruct a filter string from an inputted From
			function toString(currentFilter) {
				return 'signal_id exact ' + $(currentFilter).find('.signal')[0].value;
			}

			return {
				dropdown: dropdown,
				toString: toString
			};
		}

		//Render the elements needed to filter on Times
		function time() {
			//Create the Time dropdown
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;
				//Render the Time dropdown from a template using Nunjucks and add it to the DOM
				var newDropdown = nunjucks.render('search/filters/time/time_dropdown.html');
				$(parent).append(newDropdown);

				//Bind an event listener to the new dropdown.
				//When the dropdown is changed, the listener will add the appropriate fields
				//based on which option was selected.
				$(parent).find('.time').change(function() {
					var currentElement = this;

					//Remove the existing filter elements from this filter
					//except for the initial dropdown.
					$(currentElement).siblings().not('.initial').remove();

					//Call the appropriate function to render additional fields based
					//on which option was selected.
					if (currentElement.value == 'after') {
						afterField(currentElement);
					}
					else if (currentElement.value == 'before') {
						beforeField(currentElement);
					}
					else if (currentElement.value == 'between') {
						betweenFields(currentElement);
					}
				});

				//When the Time dropdown is first created, set it to the first option
				//in the dropdown and render the associated fields.
				var initTimeDropdown = $(parent).find('.time')[0];
				filters().time().afterField(initTimeDropdown);
			}

			//Render the After field with Nunjucks and add it to the DOM.
			function afterField(currentElement) {
				var newDropdown = nunjucks.render('search/filters/time/time_after_field.html');
				$(currentElement.parentElement).append(newDropdown);
			}

			//Render the Before field with Nunjucks and add it to the DOM.
			function beforeField(currentElement) {
				var newDropdown = nunjucks.render('search/filters/time/time_before_field.html');
				$(currentElement.parentElement).append(newDropdown);
			}

			//Render the Between fields with Nunjucks and add them to the DOM.
			function betweenFields(currentElement) {
				var newDropdown = nunjucks.render('search/filters/time/time_between_fields.html');
				$(currentElement.parentElement).append(newDropdown);
			}

			//Consruct a filter string from an inputted Time
			function toString(currentFilter) {
				//Add the text for "time after XXX"
				function appendAfter(currentFilter) {
					return 'datetime gt ' + $(currentFilter).find('.time-start')[0].value;
				}

				//Add the text for "time before XXX"
				function appendBefore(currentFilter) {
					return 'datetime lt ' + $(currentFilter).find('.time-end')[0].value;
				}

				function appendBetween(currentFilter) {
					return 'datetime range ' + $(currentFilter).find('.time-start')[0].value + ', ' + $(currentFilter).find('.time-end')[0].value;
				}

				var returnString = '';

				//By default set the delimeter to the first dropdown option since
				//that is selected on filter creation.
				var delimeter = $(currentFilter).children('.time')[0];

				//Add the filter string depending on which option is currently selected.
				if (delimeter.value == 'after') {
					returnString += appendAfter(currentFilter);
				}
				else if (delimeter.value == 'before') {
					returnString += appendBefore(currentFilter);
				}
				else if (delimeter.value == 'between') {
					returnString += (appendBetween(currentFilter));
				}

				return returnString;
			}

			return {
				afterField: afterField,
				beforeField: beforeField,
				betweenFields: betweenFields,
				dropdown: dropdown,
				toString: toString
			};
		}

		//Render the elements needed to filter on To a given person
		function to(currentElement) {
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;

				//Render the To field using Nunjucks and add it to the DOM
				var newField = nunjucks.render('search/filters/message_to/to_text_field.html');
				$(parent).append(newField);
			}


			//Consruct a filter string from an inputted To
			function toString(currentFilter) {
				return 'message_to contains ' + $(currentFilter).find('.to-text')[0].value;
			}

			return {
				dropdown: dropdown,
				toString: toString
			};
		}

		return {
			area: area,
			from: from,
			date: date,
			near: near,
			provider: provider,
			signal: signal,
			time: time,
			to: to
		};
	}

	return {
		addDropdown: addDropdown,
		addFilter: addFilter,
		bindEvents: bindEvents,
		checkDrawDisplay: checkDrawDisplay,
		createFilterBase: createFilterBase,
		removeFilter: removeFilter,
		filters: filters
	};
}
