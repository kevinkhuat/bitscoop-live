//Construct search filters to send to the database
function searchView(dataInst, mapViewInst, listViewInst) {
	//Utils instance
	var utilsInst = utils();

	//Add the intial filter dropdown to a new filter after using Nunjucks to render it
	//from a template.
	//By default the topmost option of the initial dropdown will be selected, so call its
	//render function.
	//Bind an event listener that triggers when the initial dropdown changes.
	//This listener will call the appropriate render function based on which option was selected.
	function addDropdown() {
		var newDropdown = nunjucks.render('filter/initial_filter_dropdown.html');
		$('.filter.box:last').find('.filter.options').html(newDropdown);

		var initDropdown = $('.filter.box:last').find('.initial')[0];
		renderDate().dropdown(initDropdown);

		$('.filter.box:last').find('.initial').change(function() {
			var currentElement = this;
			$(currentElement).siblings().remove();
			if (currentElement.value == 'date') {
				renderDate().dropdown(currentElement);
			}
			else if (currentElement.value == 'time') {
				renderTime().dropdown(currentElement);
			}
			else if (currentElement.value == 'to') {
				renderTo().dropdown(currentElement);
			}
			else if (currentElement.value == 'from') {
				renderFrom().dropdown(currentElement);
			}
		});
	}

	//Adds a new filter by rendering the base elements and then adding the initial dropdown
	//which will in turn add all of the other dropdowns and elements it needs.
	function addFilter() {
		createFilterBase();
		addDropdown();
	}

	//Create the base elements of a filter
	function createFilterBase() {
		//Render the base framework of a filter from a template using Nunjucks.
		var newFilter = nunjucks.render('filter/filter.html');
		$('.filter.container').append(newFilter);

		//Bind event listeners to the add filter and remove filter buttons.
		//These will call the add and remove filter functions on click.
		$('.filter.box:last').find('.filter.button.add').on('click', function() {
			addFilter();
		});
		$('.filter.box:last').find('.filter.button.remove').on('click', function() {
			removeFilter(this);
		});
	}

	//Remove the filter that the selected remove button is part of.
	function removeFilter(currentButton) {
		$(currentButton).parents('.filter.box').remove();
	}

	//Create event listeners for actions related to searching
	function bindEvents() {
		//Perform the search when the form that contains the search bar is submitted.
		$('#search-form').submit(function(event) {
			//Prevent normal form submission from bubbling any further up.
			event.stopPropagation();

			var filterString = '';

			//Get a list of the filters that are being used
			var filtersList = $('.filter.options');

			//For each filter, construct the appropriate filter string and add it to the
			//full filter string that will be submitted to the database.
			for (var i = 0; i < filtersList.length; i++) {
				var currentFilter = filtersList[i];

				//Determine what type of filter this is
				var type = $(currentFilter).children('.initial')[0].value;

				//If this isn't the first filter, append an AND to the top-level filter string.
				if (i !== 0) {
					filterString += ' AND ';
				}

				//Construct the filter string based on the filter type
				if (type == 'date') {
					filterString += '(' + dateString(currentFilter) + ')';
				}
				else if (type == 'time') {
					filterString += '(' + timeString(currentFilter) + ')';
				}
				else if (type == 'to') {
					filterString += '(' + toString(currentFilter) + ')';
				}
				else if (type == 'from') {
					filterString += '(' + fromString(currentFilter) + ')';
				}
			}

			//Encode both the search terms and the filter string
			var encodedSearch = encodeURI($('.search-bar').val());
			var encodedFilters = encodeURI(filterString);

			//Perform a search based on the search terms and filters
			dataInst.search(encodedFilters, mapViewInst, listViewInst);

			return false;
		});

		//Toggle whether to search for the clicked type of information
		$('.ui.dropdown .item').not('.add-filter').click(function() {
			$(this).toggleClass('active');
		});

		//Create a filter when the "Add a filter" button is selected.
		//By default, there are no filters, and this is the only way to add
		//the first one.  Additional filters can be created from the "+" button
		//on existing filters.
		$('.ui.dropdown .add-filter').click(function() {
			addFilter();
		});
	}

	function filters() {
		//Render the elements needed to filter on From a given person
		function from() {
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;

				//Render the From field using Nunjucks and add it to the DOM
				var newField = nunjucks.render('filter/from_text_field.html');
				$(parent).append(newField);
			}

			//Consruct a filter string from an inputted From
			function toString(currentFilter) {
				return 'name contains ' + $(currentFilter).find('.from-text')[0].value;
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
				var newDropdown = nunjucks.render('filter/date_dropdown.html');
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
				renderDate().afterField(initDateDropdown);
			}

			//Render the After field with Nunjucks and add it to the DOM.
			function afterField(currentElement) {
				var newDropdown = nunjucks.render('filter/date_after_field.html');
				$(currentElement.parentElement).append(newDropdown);
			}

			//Render the Before field with Nunjucks and add it to the DOM.
			function beforeField(currentElement) {
				var newDropdown = nunjucks.render('filter/date_before_field.html');
				$(currentElement.parentElement).append(newDropdown);
			}

			//Render the Between fields with Nunjucks and add them to the DOM.
			function betweenFields(currentElement) {
				var newDropdown = nunjucks.render('filter/date_between_fields.html');
				$(currentElement.parentElement).append(newDropdown);
			}


			//Construct a filter string from an inputted Date
			function toString(currentFilter) {

				//Add the text for "date after XXX"
				function appendAfter(currentFilter) {
					return 'Date gt ' + $(currentFilter).find('.date-start')[0].value;
				}

				//Add the text for "date before XXX"
				function appendBefore(curretFilter) {
					return 'Date lt ' + $(currentFilter).find('.date-end')[0].value;
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
					returnString += (appendBefore(currentFilter) + ' AND ' + appendAfter(currentFilter));
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

		//Render the elements needed to filter on Times
		function time() {
			//Create the Time dropdown
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;
				//Render the Time dropdown from a template using Nunjucks and add it to the DOM
				var newDropdown = nunjucks.render('filter/time_dropdown.html');
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

				//When the Date dropdown is first created, set it to the first option
				//in the dropdown and render the associated fields.
				var initTimeDropdown = $(parent).find('.time')[0];
				renderTime().afterField(initTimeDropdown);
			}

			//Render the After field with Nunjucks and add it to the DOM.
			function afterField(currentElement) {
				var newDropdown = nunjucks.render('filter/time_after_field.html');
				$(currentElement.parentElement).append(newDropdown);
			}

			//Render the Before field with Nunjucks and add it to the DOM.
			function beforeField(currentElement) {
				var newDropdown = nunjucks.render('filter/time_before_field.html');
				$(currentElement.parentElement).append(newDropdown);
			}

			//Render the Between fields with Nunjucks and add them to the DOM.
			function betweenFields(currentElement) {
				var newDropdown = nunjucks.render('filter/time_between_fields.html');
				$(currentElement.parentElement).append(newDropdown);
			}

			//Consruct a filter string from an inputted Time
			function toString(currentFilter) {

				//Add the text for "time after XXX"
				function appendAfter(currentFilter) {
					return 'Time gt ' + $(currentFilter).find('.time-start')[0].value;
				}

				//Add the text for "time before XXX"
				function appendBefore(currentFilter) {
					return 'Time lt ' + $(currentFilter).find('.time-end')[0].value;
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
					returnString += (appendBefore(currentFilter) + ' AND ' + appendAfter(currentFilter));
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
		function to() {
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;

				//Render the To field using Nunjucks and add it to the DOM
				var newField = nunjucks.render('filter/to_text_field.html');
				$(parent).append(newField);
			}


			//Consruct a filter string from an inputted To
			function toString(currentFilter) {
				return 'name contains ' + $(currentFilter).find('.to-text')[0].value;
			}

			return {
				dropdown: dropdown,
				toString: toString
			};
		}

		return {
			from: from,
			date: date,
			time: time,
			to: to
		}
	}

	return {
		addDropdown: addDropdown,
		addFilter: addFilter,
		bindEvents: bindEvents,
		createFilterBase: createFilterBase,
		removeFilter: removeFilter,
		filters: filters
	};
}
