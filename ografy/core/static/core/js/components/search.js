define(['debounce', 'filters', 'jquery', 'jquery-cookie', 'jquery-deserialize'], function(debounce, filters, $) {
	var activeFilter;
	var overflowCounter = $('<div>');
	var MAX_FILTER_WIDTH_FRACTION = 0.3;
	var RESIZE_DEBOUNCE = 250;  // ms
	var ACTIVE_GEO_FILL_COLOR = '#ff9933';
	var PASSIVE_GEO_FILL_COLOR = '#f06eaa';
	var limit = 10;
	var offset = 0;


	$.get('/opi/signal').done(function(data) {
		var $select;

		$select = $('form.connector select[name="connection"]');

		$.each(data, function(i, d) {
			$('<option>')
				.attr('value', d.id)
				.text(d.name)
				.appendTo($select);
		});

		$('#advanced').on('click press', function(e) {
			var $icon, $this = $(this);

			$icon = $this.find('i');

			if ($icon.hasClass('fa-caret-down')) {
				expand();
			}
			else {
				shrink();
			}
		});
	});

	$(window).on('resize', debounce(function(e) {
		if ($('#search-bar').hasClass('expanded')) {
			return false;
		}

		_compactOverflowFilters();
	}, RESIZE_DEBOUNCE));

	$('#search-button').on('click press', function(e) {
		$('#query-form').submit();
	});

	$('#search-bar').on('click', '.filter > .fa-close', function(e) {
		var $filter, layer, map, type, $this = $(this);

		e.stopPropagation();

		$filter = $this.closest('div');
		type = $filter.data('type');

		if (activeFilter && $filter.get(0) === activeFilter.get(0)) {
			_resetFilterEditor();
		}

		if (type === 'where') {
			layer = $filter.data('geofilter').layer;
			map = $filter.data('map');
			map.object.removeLayer(layer);
		}

		$filter.remove();
	});

	$('#search-bar').on('click', '#filter-overflow-count div', expand);

	$('#search-bar').on('click', '#filters .filter', function(e) {
		expand();

		$(this).trigger('click');
	});

	$('#search-bar').on('click', '#filter-list .filter', function(e) {
		var serialized, type, $this = $(this);

		if (activeFilter && activeFilter.get(0) === $this.get(0)) {
			return false;
		}

		if (activeFilter && activeFilter.data('type') === 'where') {
			$(activeFilter.data('geofilter').element).attr('fill', PASSIVE_GEO_FILL_COLOR);
		}

		_saveFilter();

		activeFilter = $this;
		serialized = $this.data('serialized');
		type = $this.data('type');

		if (type === 'where') {
			$(activeFilter.data('geofilter').element).attr('fill', ACTIVE_GEO_FILL_COLOR);
		}

		$('#filter-editor .control[data-type="' + type + '"]').addClass('active')
			.siblings('.active')
			.removeClass('active');

		activeFilter.addClass('active')
			.siblings('.filter').removeClass('active');

		$('form.' + type).deserialize(serialized.data);

		$('#filter-values').attr('class', type);

		$('#filter-name').removeClass('hidden')
			.find('input')
			.attr('placeholder', type.toUpperCase())
			.val(serialized.name || '');
	});

	// Event listener for clicking on one of the five new filter buttons.
	$('#search-bar').on('click', '.control:not(.disabled)', function(e) {
		var type, $this = $(this);

		type = $this.data('type');

		_addFilter(type);
	});

	$('#search-bar').on('submit', '#filter-values form', function(e) {
		e.preventDefault();

		return false;
	});

	$('.control[data-type="where"]').on('click', function(e) {
		var listener, $set;

		e.stopPropagation();

		_saveFilter();
		activeFilter = void(0);
		$('.filter.active').removeClass('active');
		_resetFilterEditor();

		$set = $('.leaflet-draw-draw-polygon, .leaflet-draw-draw-circle');

		$set.addClass('highlight');

		listener = function(e) {
			$set.removeClass('highlight');
		};

		setTimeout(listener, 3000);

		$(document).one('drawstart', listener);
	});

	$('#filter-name input').on('keydown keyup', function(e) {
		var name, type, $this = $(this);

		name = $this.val();
		type = activeFilter.data('type');

		activeFilter.find('span').text(name || _capitalize(type));
	});

	$(document).on('geofilter:create', function(e) {
		var geofilter, map, $filter;

		geofilter = e.filter;
		map = e.map;
		$filter = _addFilter('where');

		$filter.data('geofilter', geofilter);
		$filter.data('map', map);

		$(geofilter.element).data('filter', $filter.get(0))
	});

	$(document).on('geofilter:update', function(e) {
		var element, filter;

		element = e.target;
		filter = $(element).data('filter');

		$(filter).data('geofilter', e.filter);
	});

	$(document).on('geofilter:delete', function(e) {
		var filter, geofilter;

		geofilter = e.filter;
		filter = $(geofilter.element).data('filter');

		if (activeFilter && filter === activeFilter.get(0)) {
			_resetFilterEditor();
		}

		$(filter).remove();
		_compactOverflowFilters();
	});

	$(document).on('drawstart', function(e) {
		if ($('#search-bar').hasClass('expanded')) {
			shrink();

			$(this).one('drawend', expand);
		}
	});

	$('#query-form').on('submit', function(e) {
		var paramData, filterDSL, searchQuery;

		e.preventDefault();

		shrink();

		searchQuery = $('#search-query').val();
		filterDSL = _getFilterDSL();

		paramData = {
			filters: JSON.stringify(filterDSL),
			q: searchQuery,
			offset: offset,
			limit: limit
		};

		console.log(filterDSL);
		console.log(JSON.stringify(filterDSL));

		$.ajax({
			url: 'https://p.bitscoop.com/events',
			type: 'GET',
			dataType: 'json',
			contentType: 'json',
			data: paramData,
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			xhrFields: {
				withCredentials: true
			}
		}).done(function(data, xhr, response) {
			var results;

			results = data.results;

			//When the search is done, trigger a search:results event.
			//This can be caught by any other libraries and used to initiate post-search behavior, such as
			//the map view adding marker at the coordinates of each result and adding the results to a list.
			//Set clearData to true to indicate that this is a new search, not a pagination of a current search.
			$('#search-bar').trigger({
				type: 'search:results',
				results: results,
				clearData: true
			});
		});
	});


	function _addFilter(type) {
		if (activeFilter && activeFilter.data('type') === 'where') {
			$(activeFilter.data('geofilter').element).attr('fill', PASSIVE_GEO_FILL_COLOR);
		}

		// Save the active filter (if there is one).
		_saveFilter();
		// Clear out the filter editor (hide the form inputs and the independent name input).
		_resetFilterEditor();

		// Create a new filter DOM element and assign it to active filter.
		// Initialize the type as a data attribute right away. This data attribute is used in various places and never
		// needs to change again.
		activeFilter = $('<div><span></span><i class="fa fa-close"></i></div>').addClass('filter')
			.data('type', type);

		// Set the default name of the filter. This "name" isn't saved because it can be reconstructed from the type,
		// however it is used to distinguish the filter from others.
		activeFilter.find('span')
			.text(_capitalize(type));

		// Append the new filter DOM element to the list pane.
		if ($('#search-bar').hasClass('expanded')) {
			$('#filter-list').append(activeFilter);
		}
		else {
			$('#filters').append(activeFilter);
			_compactOverflowFilters();
		}

		activeFilter.addClass('active')
			.siblings('.filter').removeClass('active');

		// Mark the clicked control as active and deactivate any other active control buttons.
		$('.control[data-type="' + type + '"]').addClass('active')
			.siblings('.active').removeClass('active');

		// Control what form is visible by adjusting the class name on this element.
		$('#filter-values').attr('class', type);

		// Adjust the visibility of the reused name input. Set the placeholder to the type of the active filter.
		$('#filter-name').removeClass('hidden')
			.find('input')
			.attr('placeholder', type.toUpperCase())
			.val('');

		return activeFilter;
	}


	function _capitalize(s) {
		return s[0].toUpperCase() + s.slice(1);
	}


	function _getFilterDSL() {
		var bool;

		bool = new filters.BoolFilter();

		$('.filter').each(function(i, d) {
			var i, coordinates, data, filter, geofilter, operand, radius, serialized, type, $d;

			$d = $(d);
			type = $d.data('type');
			serialized = $d.data('serialized');
			data = serialized.data;

			console.log(data);

			if (type === 'who') {
				if (data.contact) {
					filter = new filters.TermFilter('contacts_list.name', data.contact);
					filter = filter.or(new filters.TermFilter('contacts_list.handle', data.contact));
				}

				if (data.interaction) {
					operand = new filters.TermFilter('contact_interaction_type', data.interaction);
					filter = filter ? filter.and(operand) : operand;
				}
			}
			else if (type === 'what') {
				if (data.type) {
					filter = new filters.TermFilter('content_list.content_type', data.type);
				}
			}
			else if (type === 'when') {
				if (data.from || data.to) {
					filter = new filters.RangeFilter('datetime');
				}

				if (data.from) {
					filter.gte(new Date(data.from));
				}

				if (data.to) {
					filter.lte(new Date(data.to));
				}
			}
			else if (type === 'where') {
				geofilter = $d.data('geofilter');

				if (geofilter.type === 'circle') {
					coordinates = geofilter.coordinates[0];
					radius = (geofilter.layer.getRadius() / 1000).toFixed(3) + 'km';

					filter = new filters.GeoFilter('location.geolocation', radius, new filters.Geolocation(coordinates.lat, coordinates.lng));
				}
				else {
					coordinates = geofilter.coordinates;
					filter = new filters.GeoFilter('location.geolocation');

					for (i = 0; i < coordinates.length; i++) {
						filter.addPoint(new filters.Geolocation(coordinates[i].lat, coordinates[i].lng));
					}
				}

				if (data.geometry === 'outside') {
					filter = filter.not();
				}
			}
			else if (type === 'connector') {
				if (data.connection) {
					filter = new filters.TermFilter('signal', data.connection);
				}
			}

			if (filter) {
				bool.should(filter);
			}
		});

		return bool.toDSL();
	}


	function _saveFilter() {
		var data, name, serialized, type;

		serialized = {};

		serialized['data'] = data = {};

		if (type = $('#filter-values').attr('class')) {
			serialized['type'] = type;

			if (name = $('#filter-name input').val()) {
				serialized['name'] = name;
			}

			$('form.' + type).serializeArray().map(function(d) {
				data[d.name] = d.value;
			});
		}

		if (activeFilter) {
			activeFilter.data('serialized', serialized);
		}
	}


	function _resetFilterEditor() {
		$('#filter-values form:visible').trigger('reset');
		$('#filter-values').removeAttr('class');

		$('#filter-name').addClass('hidden')
			.find('input').val('');

		$('.control.active').removeClass('active');
	}


	function _compactOverflowFilters() {
		var hideCount, hideIndex, maxWidth, width, $filters;

		if ($('#search-bar').hasClass('expanded')) {
			return;
		}

		maxWidth = MAX_FILTER_WIDTH_FRACTION * $('#search-bar').width();
		width = 0;
		$filters = $('#filters > .filter');

		$filters.each(function(i, d) {
			var elemWidth;

			elemWidth = $(d).removeClass('hidden').width();

			if (elemWidth + width > maxWidth) {
				hideIndex = i;

				return false;
			}

			width += elemWidth;
		});

		if (typeof hideIndex !== 'undefined') {
			hideCount = $filters.length - hideIndex;

			$filters.slice(hideIndex).addClass('hidden');
			overflowCounter.text('+ ' + hideCount)
				.appendTo('#filter-overflow-count');
		}
		else {
			$('#filter-overflow-count').empty();
		}
	}


	function expand() {
		$('#filters > .filter').appendTo('#filter-list')
			.removeClass('hidden');

		$('#advanced i').removeClass('fa-caret-down').addClass('fa-caret-up');
		$('#search-bar').addClass('expanded');
		$('#filter-overflow-count').empty();

		if (activeFilter && activeFilter.data('type') === 'where') {
			$(activeFilter.data('geofilter').element).attr('fill', ACTIVE_GEO_FILL_COLOR);
		}
	}


	function shrink() {
		_saveFilter();

		$('#advanced i').removeClass('fa-caret-up').addClass('fa-caret-down');
		$('#search-bar').removeClass('expanded');
		$('#filter-list > .filter').appendTo('#filters');

		_compactOverflowFilters();

		if (activeFilter && activeFilter.data('type') === 'where') {
			$(activeFilter.data('geofilter').element).attr('fill', PASSIVE_GEO_FILL_COLOR);
		}
	}


	return {
		expand: expand,
		shrink: shrink
	};
});
