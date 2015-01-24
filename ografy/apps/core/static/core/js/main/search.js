function searchView() {
	var utilsInst = utils();

	function addDropdown() {
		var newDropdown = nunjucks.render('static/core/templates/main/filter/initial_filter_dropdown.html');
		$('.filter:last').find('.filter-options').html(newDropdown);

		var initDropdown = $('.filter:last').find('.initial')[0];
		renderDate().dropdown(initDropdown);

		$('.filter:last').find('.initial').change(function () {
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

	function addFilter() {
		createFilterBase();
		addDropdown();
	}

	function createFilterBase() {
		var newFilter = nunjucks.render('static/core/templates/main/filter/filter.html');
		$('.filter-container').append(newFilter);
		$('.filter:last').find('.add-filter-button').on('click', function () {
			addFilter();
		});
		$('.filter:last').find('.remove-filter-button').on('click', function () {
			removeFilter(this);
		});
	}

	function removeFilter(currentButton) {
		$(currentButton).parents('.filter').remove();
	}

	function renderFrom() {
		function dropdown(currentElement) {
			var parent = currentElement.parentElement;
			var newDropdown = nunjucks.render('static/core/templates/main/filter/from_text_field.html');
			$(parent).append(newDropdown);
		}

		return {
			dropdown: dropdown
		}
	}

	function renderDate() {
		function dropdown(currentElement) {
			var parent = currentElement.parentElement;
			var newDropdown = nunjucks.render('static/core/templates/main/filter/date_dropdown.html');
			$(parent).append(newDropdown);

			$(parent).find('.date').change(function () {
				var currentElement = this;
				$(currentElement).siblings().not('.initial').remove();
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

			var initDateDropdown = $(parent).find('.date')[0];
			renderDate().afterField(initDateDropdown);
		}

		function afterField(currentElement) {
			var newDropdown = nunjucks.render('static/core/templates/main/filter/date_after_field.html');
			$(currentElement.parentElement).append(newDropdown);
		}

		function beforeField(currentElement) {
			var newDropdown = nunjucks.render('static/core/templates/main/filter/date_before_field.html');
			$(currentElement.parentElement).append(newDropdown);
		}

		function betweenFields(currentElement) {
			var newDropdown = nunjucks.render('static/core/templates/main/filter/date_between_fields.html');
			$(currentElement.parentElement).append(newDropdown);
		}

		return {
			afterField: afterField,
			beforeField: beforeField,
			betweenFields: betweenFields,
			dropdown: dropdown
		}
	}

	function renderTime() {
		function dropdown(currentElement) {
			var parent = currentElement.parentElement;
			var newDropdown = nunjucks.render('static/core/templates/main/filter/time_dropdown.html');
			$(parent).append(newDropdown);

			$(parent).find('.time').change(function () {
				var currentElement = this;
				$(currentElement).siblings().not('.initial').remove();
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

			var initTimeDropdown = $(parent).find('.time')[0];
			renderTime().afterField(initTimeDropdown);
		}

		function afterField(currentElement) {
			var newDropdown = nunjucks.render('static/core/templates/main/filter/time_after_field.html');
			$(currentElement.parentElement).append(newDropdown);
		}

		function beforeField(currentElement) {
			var newDropdown = nunjucks.render('static/core/templates/main/filter/time_before_field.html');
			$(currentElement.parentElement).append(newDropdown);
		}

		function betweenFields(currentElement) {
			var newDropdown = nunjucks.render('static/core/templates/main/filter/time_between_fields.html');
			$(currentElement.parentElement).append(newDropdown);
		}

		return {
			afterField: afterField,
			beforeField: beforeField,
			betweenFields: betweenFields,
			dropdown: dropdown
		}
	}

	function renderTo() {
		function dropdown(currentElement) {
			var parent = currentElement.parentElement;
			var newField = nunjucks.render('static/core/templates/main/filter/to_text_field.html');
			$(parent).append(newField);
		}

		return {
			dropdown: dropdown
		}
	}

	function dateString(currentFilter) {
		function appendAfter(currentFilter) {
			return 'Date gt ' + $(currentFilter).find('.date-start')[0].value;
		}

		function appendBefore(curretFilter) {
			return 'Date lt ' + $(currentFilter).find('.date-end')[0].value;
		}

		var returnString = '';
		var delimeter = $(currentFilter).children('.date')[0];

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

	function timeString(currentFilter) {
		function appendAfter(currentFilter) {
			return 'Time gt ' + $(currentFilter).find('.time-start')[0].value;
		}

		function appendBefore(currentFilter) {
			return 'Time lt ' + $(currentFilter).find('.time-end')[0].value;
		}

		var returnString = '';
		var delimeter = $(currentFilter).children('.time')[0];

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

	function fromString(currentFilter) {
		return 'From ' + $(currentFilter).find('.from-text')[0].value;
	}

	function toString(currentFilter) {
		return 'To ' + $(currentFilter).find('.to-text')[0].value;
	}

	function bindEvents() {

		$('#search-form').submit(function(event) {
			event.stopPropagation();

			var filterString = "";
			var filtersList = $('.filter-options');

			for (var i = 0; i < filtersList.length; i++) {
				var currentFilter = filtersList[i];
				var type = $(currentFilter).children('.initial')[0].value;
				if (i != 0) {
					filterString += ' AND ';
				}

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

			var encodedSearch = encodeURI($('.search-bar').val());
			var encodedFilters = encodeURI(filterString);

			console.log(filterString);
			console.log(encodedSearch);
			console.log(encodedFilters);

			var token = utilsInst.session().getCsrfToken();
			$.ajax({
				url: '/opi/event',
				type: 'GET',
				dataType: 'json',
				headers: {
					"X-CSRFToken": token
				}
			}).done(function (data, xhr, response) {
				console.log(data)
			});

			return false;
		});

		$('.type-button').on('click', function() {
			$(this).toggleClass('active');
		});

		$('.ui.dropdown .item').not('.add-filter').click(function() {
			$(this).toggleClass('active');
		});

		$('.ui.dropdown .add-filter').click(function() {
			addFilter();
		});

	}
	return {
		addDropdown: addDropdown,
		addFilter: addFilter,
		bindEvents: bindEvents,
		createFilterBase: createFilterBase,
		dateString: dateString,
		fromString: fromString,
		removeFilter: removeFilter,
		renderDate: renderDate,
		renderFrom: renderFrom,
		renderTime: renderTime,
		renderTo: renderTo,
		timeString: timeString,
		toString: toString
	}
}