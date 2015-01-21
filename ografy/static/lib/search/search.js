//Django cookie management
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var testNumFilters = 0;

function addDropdown() {
	var newDropdown = nunjucks.render('static/core/templates/main/filter/initial_filter_dropdown.html');
	$('.filter:last').find('.filter-options').html(newDropdown);

	var initDropdown = $('.filter:last').find('.initial')[0];
	renderDate().dropdown(initDropdown);

	$('.filter:last').find('.initial').change(function() {
		currentElement = this;
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

	var initDateDropdown = $('.filter:last').find('.date')[0];
	renderDate().afterField(initDateDropdown);
}

function addFilter() {

	testNumFilters++;
	addDropdown();
	createRemoveButton();
	createAddButton();
}

function createAddButton() {
	var newFilter = nunjucks.render('static/core/templates/main/filter/filter.html', {num: testNumFilters});
	$('.filter-container').append(newFilter);
	$('.filter:last').find('.add-filter-button').on('click', function() {
		addFilter();
	});
}

function createInitialFilter() {
	createAddButton();
}

function createRemoveButton() {
	var newRemoveButton = nunjucks.render('static/core/templates/main/filter/remove_button.html');
	$('.filter:last').find('.add-remove-buttons').before(newRemoveButton);
	var currentButton = $('.filter:last').find('.remove-filter-button');
	currentButton.on('click', function() {
		removeFilter(currentButton);
	});
}

function removeFilter(currentButton) {
	$(currentButton).parents('.filter').remove();
}

function renderDate() {

	function dropdown(currentElement) {
		var newDropdown = nunjucks.render('static/core/templates/main/filter/date_dropdown.html');
		$(currentElement.parentElement).append(newDropdown);

		$('.filter:last').find('.date').change(function() {
			currentElement = this;
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

		var initDateDropdown = $('.filter:last').find('.date')[0];
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
		var newDropdown = nunjucks.render('static/core/templates/main/filter/time_dropdown.html');
		$(currentElement.parentElement).append(newDropdown);

		$('.filter:last').find('.time').change(function() {
			currentElement = this;
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

		var initTimeDropdown = $('.filter:last').find('.time')[0];
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

$(document).ready(function() {

	createInitialFilter();

	$('.search-bar').keypress(function(event) {
		if (event.keyCode == 13) {
			$.ajax({
				url: '/search/event',
				type: 'POST',
				dataType: 'json',
				data: $('.search-bar').val(),
				headers: {
					"X-CSRFToken": getCookie('csrftoken')
				}
			}).done(function (data, xhr, response) {
				console.log(data)
			});
		}
	});

	$('.type-button').on('click', function() {
		$(this).toggleClass('active');
	});


});