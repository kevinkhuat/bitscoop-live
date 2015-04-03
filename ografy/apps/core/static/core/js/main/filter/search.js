//Construct search filters to send to the database
function searchView(dataInst, cacheInst, mapViewInst, listViewInst, urlParserInst) {
	//Add the intial filter dropdown to a new filter after using Nunjucks to render it
	//from a template.
	//By default the topmost option of the initial dropdown will be selected, so call its
	//render function.
	//Bind an event listener that triggers when the initial dropdown changes.
	//This listener will call the appropriate render function based on which option was selected.
	function addDropdown(inputSelection) {
		var newDropdown = nunjucks.render('search/initial_filter_dropdown.html');
		$(inputSelection).find('.filter.box:last .filter.options').html(newDropdown);

		var initDropdown = $(inputSelection).find('.filter.box:last .initial')[0];
		filters().date().dropdown(initDropdown);

		$(inputSelection).find('.filter.box:last .initial').change(function() {
			var currentElement = this;
			$(currentElement).siblings().remove();
			if (currentElement.value == 'date') {
				filters().date().dropdown(currentElement);
			}
			else if (currentElement.value == 'time') {
				filters().time().dropdown(currentElement);
			}
			else if (currentElement.value == 'provider') {
				filters().provider().dropdown(currentElement);
			}
			else if (currentElement.value == 'to') {
				filters().to().dropdown(currentElement);
			}
			else if (currentElement.value == 'from') {
				filters().from().dropdown(currentElement);
			}
		});
	}

	//Adds a new filter by rendering the base elements and then adding the initial dropdown
	//which will in turn add all of the other dropdowns and elements it needs.
	function addFilter(inputSelection) {
		createFilterBase(inputSelection);
		addDropdown(inputSelection);
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
		$(currentButton).parents('.filter.box').remove();
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
					if (type == 'date') {
						filterString += '(' + filters().date().toString(currentFilter) + ')';
					}
					else if (type == 'time') {
						filterString += '(' + filters().time().toString(currentFilter) + ')';
					}
					else if (type == 'provider') {
						filterString += '(' + filters().provider().toString(currentFilter) + ')';
					}
					else if (type == 'to') {
						filterString += '(' + filters().to().toString(currentFilter) + ')';
					}
					else if (type == 'from') {
						filterString += '(' + filters().from().toString(currentFilter) + ')';
					}
				}

				//Set the Query and Filters in the URL parser
				urlParserInst.setSearchQuery($('.search-bar').val());
				urlParserInst.setSearchFilters(filterString);

				//Perform a search based on the search terms and filters
				dataInst.search(thisType.id, filterString, mapViewInst, listViewInst);
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

		$('.search-button').click(function(event){
			return submitSearch(event);
		});

		//Toggle whether to search for the clicked type of information
		$('.dropdown .item').not('.add-filter').click(function() {
			$(this).toggleClass('active');
		});

		//Create a filter when the "Add a filter" button is selected.
		//By default, there are no filters, and this is the only way to add
		//the first one.  Additional filters can be created from the "+" button
		//on existing filters.
		$('.menu .add-filter').click(function() {
			addFilter($(this).parent().siblings('.filters'));
		});
	}

	function filters() {
		//Render the elements needed to filter on From a given person
		function from() {
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;

				//Render the From field using Nunjucks and add it to the DOM
				var newField = nunjucks.render('search/filters/message_from/from_text_field.html');
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

		function provider() {
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;

				//Render the From field using Nunjucks and add it to the DOM
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

				//When the Date dropdown is first created, set it to the first option
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
		function to(currentElement) {
			function dropdown(currentElement) {
				var parent = currentElement.parentElement;

				//Render the To field using Nunjucks and add it to the DOM
				var newField = nunjucks.render('search/filters/message_to/to_text_field.html');
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
			provider: provider,
			time: time,
			to: to
		};
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
