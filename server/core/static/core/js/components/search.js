define(['debounce', 'filters', 'jquery', 'moment', 'jquery-cookie', 'jquery-deserialize'], function(debounce, filters, $, moment) {
	var activeFilter;
	var overflowCounter = $('<div>');
	var MAX_FILTER_WIDTH_FRACTION = 0.3;
	var RESIZE_DEBOUNCE = 250;  // ms
	var ACTIVE_GEO_FILL_COLOR = '#ff9933';
	var PASSIVE_GEO_FILL_COLOR = '#f06eaa';
	var RESULT_PAGE_LIMIT = 100;
	var isMobile = (devicePixelRatio >= 1.25 && innerWidth < 1080) || (devicePixelRatio >= 3);


	$.get('/opi/connections').done(function(data) {
		var $select;

		$select = $('form.connector select[name="connection"]');

		$.each(data, function(i, d) {
			if (d.auth_status.connected) {
				$('<option>')
					.attr('value', d.id)
					.text(d.name)
					.appendTo($select);
			}
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

	$('#query-form').on('keypress', function(e) {
		if (e.which === 13) {
			e.preventDefault();
		}
	}).on('keyup', function(e) {
		if (e.which === 13) {
			e.preventDefault();

			$('#query-form').trigger({
				type: 'submit',
				paramData: {
					offset: 0
				}
			});
		}
	});

	$('#search-button').on('click press', function(e) {
		$('#query-form').trigger({
			type: 'submit',
			paramData: {
				offset: 0
			}
		});
	});

	$('#search-bar').on('click', '.filter > .fa-close', function(e) {
		var $filter, layer, map, paramData, type, $this = $(this);

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

		$(document).trigger({
			type: 'filter:change'
		});

		_checkNewQuery();
	});

	$('#search-bar').on('click', '#filter-overflow-count', function(e) {
		e.stopPropagation();
		expand();
	});

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

		//Deserialize can't handle unchecked checkboxes, as they are not serialized in the first place.
		//Uncheck any that are present so that filters where they weren't checked aren't checked by mistake.
		//If you don't, then if the checkbox on the form was checked from a previous filter, it will remain so
		//on the newly-selected one.
		$('#filter-values input[type="checkbox"]').prop('checked', false);

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

	$('#search-bar').on('search:save', function(e) {
		var paramData, searchQuery, serializedFilters, $color, $icon, $name;

		$color = $('select[name="color"]');
		$icon = $('select[name="icon"]');
		$name = $('.menu-searches').find('input[name="search-name"]');

		e.preventDefault();

		serializedFilters = _getSerializedFilters();
		paramData = {};

		searchQuery = $('#search-query').val();

		if (searchQuery !== '') {
			paramData.query = searchQuery;
		}

		paramData.filters = serializedFilters.bool;

		if (serializedFilters.namedFilters.length > 0) {
			paramData.namedFilters = serializedFilters.namedFilters;
		}

		if ($icon.children(':selected').attr('value') != 'none' || $name.val() !== '') {
			if ($icon.children(':selected').attr('value') != 'none') {
				paramData.icon = $icon.children(':selected').attr('value');
				paramData.iconColor = $color.children(':selected').attr('value');
			}

			if ($name.val() !== '') {
				paramData.name = $name.val();
			}
		}

		if (/\/explore\/\w+/g.test(location.pathname)) {
			$.ajax({
				url: 'https://p.bitscoop.com/searches/' + location.pathname.split('/explore/')[1],
				type: 'PUT',
				dataType: 'json',
				contentType: 'json',
				data: JSON.stringify(paramData),
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				},
				xhrFields: {
					withCredentials: true
				}
			}).done(function(data, xhr, response) {
				history.pushState({}, '', '/explore/' + data.searchID);
				$('#search-favorited').find('i').attr('class', 'fa fa-star');
			});
		}
		else {
			$.ajax({
				url: 'https://p.bitscoop.com/searches',
				type: 'PUT',
				dataType: 'json',
				contentType: 'json',
				data: JSON.stringify(paramData),
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				},
				xhrFields: {
					withCredentials: true
				}
			}).done(function(data, xhr, response) {
				history.pushState({}, '', '/explore/' + data.searchID);
				$('#search-favorited').find('i').attr('class', 'fa fa-star');
			});
		}
	});

	$('#search-bar').on('search:delete', function(e) {
		if (/\/explore\/\w+/g.test(location.pathname)) {
			$.ajax({
				url: 'https://p.bitscoop.com/searches/' + location.pathname.split('/explore/')[1],
				type: 'DELETE',
				dataType: 'json',
				contentType: 'json',
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				},
				xhrFields: {
					withCredentials: true
				}
			}).done(function(data, xhr, response) {
				var $colorSelect, $iconSelect, $menuSearch, $name;

				history.pushState({}, '', '/explore/' + data.searchID);
				$('#search-favorited').find('i').attr('class', 'fa fa-star-o');

				$menuSearch = $('.menu-searches');

				$colorSelect = $menuSearch.find('select[name="color"] option[name="gray"]');
				$iconSelect = $menuSearch.find('select[name="icon"] option[value="none"]');

				$iconSelect.prop('selected', true);
				$iconSelect.trigger('change');
				$colorSelect.prop('selected', true);
				$colorSelect.trigger('change');

				$name = $menuSearch.find('input[name="search-name"]');

				$name.val('');
				$name.trigger('change');
			});
		}
	});

	$('#search-bar').on('submit', '#filter-values form', function(e) {
		e.preventDefault();

		return false;
	});

	$('.control[data-type="where"]').on('click', function(e) {
		var listener, $set;

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

	$('#filter-name input').on('keydown keyup paste change', function(e) {
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

		$(geofilter.element).data('filter', $filter.get(0));

		if (!e.preventClick) {
			$filter.trigger('click');
		}
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

		$(document).trigger({
			type: 'filter:change'
		});

		_checkNewQuery();
		_compactOverflowFilters();
	});

	$(document).on('drawstart', function(e) {
		if ($('#search-bar').hasClass('expanded')) {
			shrink();

			$(this).one('drawend', expand);
		}
	});

	$(document).on('explorer:more', function(e) {
		$.ajax({
			url: e.more,
			type: 'GET',
			dataType: 'json',
			contentType: 'json',
			data: [],
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			xhrFields: {
				withCredentials: true
			}
		}).done(function(data, xhr, response) {
			$('#search-bar').trigger({
				type: 'search:results',
				results: data,
				clearData: false
			});
		});
	});

	$(document).on('explorer:sort', function(e) {
		e.paramData.limit = RESULT_PAGE_LIMIT;

		$.ajax({
			url: 'https://p.bitscoop.com/events',
			type: 'GET',
			dataType: 'json',
			contentType: 'json',
			data: e.paramData,
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			xhrFields: {
				withCredentials: true
			}
		}).done(function(data, xhr, response) {
			$('#search-bar').trigger({
				type: 'search:results',
				results: data,
				clearData: false
			});
		});
	});

	$(document).on('change', '#filter-values:visible input, #filter-values:visible select', function(e) {
		_saveFilter();

		$(document).trigger({
			type: 'filter:change'
		});

		_checkNewQuery();
	});

	$(document).on('click', '#filter-controls', function(e) {
		var thisId, $this = $(e.target);

		thisId = $this.attr('id');

		if (thisId !== '#filter-editor' && thisId !== 'filter-list' && $this.parents('#filter-editor').length === 0 && $this.parents('#filter-list').length === 0) {
			shrink();
		}
	});

	$(document).on('click', function(e) {
		var $this = $(e.target);

		if ($this.parents('#search-bar').length === 0 && $this.attr('id') !== '#search-bar') {
			shrink();
		}
	});

	$('#query-form').on('submit', function(e) {
		var paramData, searchQuery, serializedFilters;

		e.preventDefault();

		shrink(true);

		serializedFilters = _getSerializedFilters();
		paramData = {};

		searchQuery = $('#search-query').val();

		if (searchQuery !== '') {
			paramData.query = searchQuery;
		}

		paramData.filters = serializedFilters.bool;

		if (serializedFilters.namedFilters.length > 0) {
			paramData.namedFilters = serializedFilters.namedFilters;
		}

		$.ajax({
			url: 'https://p.bitscoop.com/search',
			type: 'PUT',
			dataType: 'json',
			contentType: 'json',
			data: JSON.stringify(paramData),
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			xhrFields: {
				withCredentials: true
			}
		}).done(function(data, xhr, response) {
			var filterDSL, paramData, searchID;

			searchID = data.searchID;

			filterDSL = serializedFilters.bool.toDSL();

			e.paramData.limit = RESULT_PAGE_LIMIT;
			e.paramData.filters = JSON.stringify(filterDSL);

			paramData = e.paramData;

			if (searchQuery !== '') {
				paramData.q = searchQuery;
			}

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
				//When the search is done, trigger a search:results event.
				//This can be caught by any other libraries and used to initiate post-search behavior, such as
				//the map view adding marker at the coordinates of each result and adding the results to a list.
				//Set clearData to true to indicate that this is a new search, not a pagination of a current search.
				$('#search-bar').trigger({
					type: 'search:results',
					results: data,
					searchParams: paramData,
					clearData: true,
					searchID: searchID
				});
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


	function _checkNewQuery() {
		var paramData, searchQuery, serializedFilters;

		paramData = {};

		searchQuery = $('#search-query').val();

		if (searchQuery !== '') {
			paramData.query = searchQuery;
		}

		serializedFilters = _getSerializedFilters();
		paramData.filters = JSON.stringify(serializedFilters.bool);

		if (serializedFilters.namedFilters.length > 0) {
			paramData.namedFilters = JSON.stringify(serializedFilters.namedFilters);
		}

		$.ajax({
			url: 'https://p.bitscoop.com/searches',
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
			var $activeFilter, $colorSelect, $filters, $iconSelect, $menuSearch, $name;

			if (data.favorited) {
				$menuSearch = $('.menu-searches');

				if (data.icon && data.icon != null && data.icon !== '') {
					$colorSelect = $menuSearch.find('select[name="color"] option[value="' + data.iconColor + '"]');
					$iconSelect = $menuSearch.find('select[name="icon"] option[value="' + data.icon + '"]');

					$iconSelect.prop('selected', true);
					$iconSelect.trigger('change');
					$colorSelect.prop('selected', true);
					$colorSelect.trigger('change');
				}

				if (data.name && data.name != null && data.name !== '') {
					$name = $menuSearch.find('input[name="search-name"]');

					$name.val(data.name);
				}

				$('#search-favorited').find('i').attr('class', 'fa fa-star');
			}
			else {
				$('#search-favorited').find('i').attr('class', 'fa fa-star-o');
			}

			if (data.searchID) {
				history.pushState({}, '', location.pathname + '/' + data.searchID);
			}
			else {
				history.pushState({}, '', '/explore');
			}

			$filters = $('#filter-list, #filters').find('.filter');

			_.forEach($filters, function(filter) {
				var serializedFilter;

				serializedFilter = _getSerializedFilter(filter);

				_.forEach(data.named_filters, function(namedFilter) {
					var matchedKey, serialized, $filter;

					matchedKey = _.findKey(namedFilter, function(value) {
						return _.isEqual(value, JSON.parse(JSON.stringify(serializedFilter)));
					});

					if (matchedKey != null) {
						$filter = $(filter);

						serialized = $filter.data('serialized');
						serialized.name = matchedKey;
						$filter.data('serialized', serialized);
						$filter.find('span')
							.text(_capitalize(matchedKey));
					}
				});
			});

			$activeFilter = $('.filter.active');

			if ($activeFilter.length > 0) {
				$('#filter-name').find('input[type="text"]').val($activeFilter.data('serialized').name);
			}
		});
	}


	function _getSerializedFilters() {
		var bool, connectorFilters, name, namedFilters, whatFilters, whenFilters, whereFilters, whoFilters;

		bool = new filters.BoolFilter();
		namedFilters = [];

		$('.filter').each(function(i, d) {
			var i, coordinates, data, filter, geofilter, namedFilter, operand, radius, serialized, type, $d;

			$d = $(d);
			type = $d.data('type');
			serialized = $d.data('serialized');
			name = serialized.name;
			data = serialized.data;

			if (type === 'who') {
				if (data.contact) {
					filter = new filters.MatchFilter('contacts.name', data.contact);
					filter = filter.or(new filters.MatchFilter('contacts.handle', data.contact));
				}

				if (data.interaction) {
					operand = new filters.TermFilter('contact_interaction_type', data.interaction);
					filter = filter ? filter.and(operand) : operand;
				}

				if (filter != null) {
					if (whoFilters) {
						whoFilters.or(filter);
					}
					else {
						whoFilters = new filters.OrFilter(filter);
					}

					if (name) {
						namedFilter = {};
						namedFilter[name] = filter;

						namedFilters.push(namedFilter);
					}
				}
			}
			else if (type === 'what') {
				if (data.type) {
					filter = new filters.TermFilter('content.type', data.type);
				}

				if (filter != null) {
					if (whatFilters) {
						whatFilters.or(filter);
					}
					else {
						whatFilters = new filters.OrFilter(filter);
					}

					if (name) {
						namedFilter = {};
						namedFilter[name] = filter;

						namedFilters.push(namedFilter);
					}
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

				if (filter != null) {
					if (data.estimated) {
						operand = new filters.RangeFilter('created');

						if (data.from) {
							operand.gte(new Date(data.from));
						}

						if (data.to) {
							operand.lte(new Date(data.to));
						}

						filter = filter.or(operand);
					}

					if (whenFilters) {
						whenFilters.or(filter);
					}
					else {
						whenFilters = new filters.OrFilter(filter);
					}

					if (name) {
						namedFilter = {};
						namedFilter[name] = filter;

						namedFilters.push(namedFilter);
					}
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

				if (!data.estimated) {
					operand = new filters.TermFilter('location.estimated', false);
					filter = filter.and(operand);
				}

				if (filter != null) {
					if (whereFilters) {
						whereFilters.or(filter);
					}
					else {
						whereFilters = new filters.OrFilter(filter);
					}

					if (name) {
						namedFilter = {};
						namedFilter[name] = filter;

						namedFilters.push(namedFilter);
					}
				}
			}
			else if (type === 'connector') {
				if (data.connection) {
					filter = new filters.TermFilter('connection', data.connection);
				}

				if (filter != null) {
					if (connectorFilters) {
						connectorFilters.or(filter);
					}
					else {
						connectorFilters = new filters.OrFilter(filter);
					}

					if (name) {
						namedFilter = {};
						namedFilter[name] = filter;

						namedFilters.push(namedFilter);
					}
				}
			}
		});

		if (connectorFilters != null) {
			bool.must(connectorFilters);
		}

		if (whoFilters != null) {
			bool.must(whoFilters);
		}

		if (whatFilters != null) {
			bool.must(whatFilters);
		}

		if (whenFilters != null) {
			bool.must(whenFilters);
		}

		if (whereFilters != null) {
			bool.must(whereFilters);
		}

		return {
			bool: bool,
			namedFilters: namedFilters
		};
	}


	function _getSerializedFilter(inputFilter) {
		var coordinates, data, filter, geofilter, i, name, operand, radius, serialized, type, $filter;

		$filter = $(inputFilter);
		type = $filter.data('type');
		serialized = $filter.data('serialized');
		name = serialized.name;
		data = serialized.data;

		if (type === 'who') {
			if (data.contact) {
				filter = new filters.MatchFilter('contacts.name', data.contact);
				filter = filter.or(new filters.MatchFilter('contacts.handle', data.contact));
			}

			if (data.interaction) {
				operand = new filters.TermFilter('contact_interaction_type', data.interaction);
				filter = filter ? filter.and(operand) : operand;
			}
		}
		else if (type === 'what') {
			if (data.type) {
				filter = new filters.TermFilter('content.type', data.type);
			}

			if (filter != null) {
				returnFilter = new filters.OrFilter(filter);
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

			if (filter != null) {
				if (data.estimated) {
					operand = new filters.RangeFilter('created');

					if (data.from) {
						operand.gte(new Date(data.from));
					}

					if (data.to) {
						operand.lte(new Date(data.to));
					}

					filter = filter.or(operand);
				}
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

			if (!data.estimated) {
				operand = new filters.TermFilter('location.estimated', false);
				filter = filter.and(operand);
			}
		}
		else if (type === 'connector') {
			if (data.connection) {
				filter = new filters.TermFilter('connection', data.connection);
			}
		}

		return filter;
	}


	function _saveFilter() {
		var data, name, serialized, type;

		serialized = {};

		serialized.data = data = {};

		if (type = $('#filter-values').attr('class')) {
			serialized.type = type;

			if (name = $('#filter-name input').val()) {
				serialized.name = name;
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


	function generateFilters(filters, namedFilters) {
		var must;

		must = filters._must;

		_.forEach(must, function(type) {
			_.forEach(type.Or, function(filter) {
				var zeroElement;

				if (filter.Or) {
					zeroElement = filter.Or[0];

					if (zeroElement.search_field && (zeroElement.search_field === 'created' || zeroElement.search_field === 'datetime')) {
						_createWhenFilter(filter, zeroElement, namedFilters, true, namedFilters);
					}
					else if (zeroElement.search_field && (zeroElement.search_field === 'contacts.name' || zeroElement.search_field === 'contacts.handle')) {
						_createWhoFilter(filter, zeroElement, namedFilters);
					}
				}
				else if (filter.And) {
					zeroElement = filter.And[0];

					if (zeroElement.Or) {
						if (zeroElement.Or[0].search_field && (zeroElement.Or[0].search_field === 'contacts.name' || zeroElement.Or[0].search_field === 'contacts.handle')) {
							_createWhoFilter(filter, zeroElement.Or[0], namedFilters, filter.And[1].value);
						}
					}
					else {
						if (zeroElement.search_field && (zeroElement.search_field === 'location.geolocation')) {
							_createWhereFilter(filter, zeroElement, namedFilters, filter.And[1].value, 'inside');
						}
						else if (zeroElement.not && zeroElement.not.search_field && zeroElement.not.search_field === 'location.geolocation') {
							_createWhereFilter(filter, zeroElement.not, namedFilters, filter.And[1].value, 'outside');
						}
					}
				}
				else if (filter.not) {
					if (filter.not.search_field && filter.not.search_field === 'location.geolocation') {
						_createWhereFilter(filter, filter.not, namedFilters, true, 'outside');
					}
				}
				else {
					if (filter.search_field && filter.search_field === 'content.type') {
						_createWhatFilter(filter, namedFilters);
					}
					else if (filter.search_field && filter.search_field === 'datetime') {
						_createWhenFilter(filter, filter, namedFilters, false);
					}
					else if (filter.search_field && filter.search_field === 'connection') {
						_createConnectorFilter(filter, namedFilters);
					}
					else if (filter.search_field && filter.search_field === 'contact_interaction_type') {
						_createWhoFilter(filter, '', namedFilters, filter.value);
					}
					else if (filter.search_field && filter.search_field === 'location.geolocation') {
						_createWhereFilter(filter, filter, namedFilters, true, 'inside');
					}
				}
			});
		});
	}


	function _createWhoFilter(filter, values, namedFilters, contact_interaction_type) {
		var $whoFilter;

		$whoFilter = $('form.who');
		//Create a who filter by triggering a click event on its filter creation button.
		$('#filter-buttons').find('[data-type="who"]').trigger({
			type: 'click'
		});

		if (typeof values === 'object') {
			$whoFilter.find('input[name="contact"]').val(values.value);
		}
		else {
			$whoFilter.find('input[name="contact"]').val('');
		}

		if (contact_interaction_type) {
			$whoFilter.find('input[value="' + contact_interaction_type + '"]').prop('checked', true);
		}
		else {
			$whoFilter.find('input[value=""]').prop('checked', true);
		}

		_.forEach(namedFilters, function(namedFilter) {
			var matchedKey;

			matchedKey = _.findKey(namedFilter, function(value) {
				return _.isEqual(value, filter);
			});

			if (matchedKey != null) {
				$('#filter-name').find('input[name="name"]').val(matchedKey).trigger('change');
			}
		});
	}

	function _createWhatFilter(filter, namedFilters) {
		var $whatFilter;

		$whatFilter = $('form.what');
		//Create a what filter by triggering a click event on its filter creation button.
		$('#filter-buttons').find('[data-type="what"]').trigger({
			type: 'click'
		});

		//Set the select to the type specified.
		$whatFilter.find('select[name="type"]').val(filter.value);

		_.forEach(namedFilters, function(namedFilter) {
			var matchedKey;

			matchedKey = _.findKey(namedFilter, function(value) {
				return _.isEqual(value, filter);
			});

			if (matchedKey != null) {
				$('#filter-name').find('input[name="name"]').val(matchedKey).trigger('change');
			}
		});
	}

	function _createWhenFilter(filter, values, namedFilters, estimated) {
		var date, $whenFilter;

		$whenFilter = $('form.when');

		//Create a when filter by triggering a click event on its filter creation button.
		$('#filter-buttons').find('[data-type="when"]').trigger({
			type: 'click'
		});

		$whenFilter.find('input[name="estimated"]').prop('checked', estimated);

		//TODO: Get rid of formatting the dates to be date-only once we implement datetimepicker
		if (values.lte) {
			date = moment(new Date(values.lte)).utc().format('YYYY-MM-DD');
			$whenFilter.find('input[name="to"]').val(date);
		}
		else {
			$whenFilter.find('input[name="to"]').val('');
		}

		if (values.gte) {
			date = moment(new Date(values.gte)).utc().format('YYYY-MM-DD');
			$whenFilter.find('input[name="from"]').val(date);
		}
		else {
			$whenFilter.find('input[name="from"]').val('');
		}

		_.forEach(namedFilters, function(namedFilter) {
			var matchedKey;

			matchedKey = _.findKey(namedFilter, function(value) {
				return _.isEqual(value, filter);
			});

			if (matchedKey != null) {
				$('#filter-name').find('input[name="name"]').val(matchedKey).trigger('change');
			}
		});
	}

	function _createWhereFilter(filter, values, namedFilters, estimated, insideOutside) {
		var coordinates, distance, newFilter, latlng, layerKeys, layer, layers, response, type, $whereFilter;

		coordinates = [];
		latlng = [];
		$whereFilter = $('form.where');

		if (Array.isArray(values.points)) {
			type = 'polygon';

			_.forEach(values.points, function(coords) {
				coordinates.push([coords.lat, coords.lon]);
				latlng.push({
					lat: coords.lat,
					lng: coords.lon
				});
			});

			response = leaflet.polygon(coordinates).addTo(map.layers.draw);
		}
		else {
			type = 'circle';

			coordinates = [values.points.lat, values.points.lon];
			distance = parseFloat(values.distance.replace('km', '')) * 1000;
			response = leaflet.circle(coordinates, distance).addTo(map.layers.draw);
			latlng = [{
				lat: values.points.lat,
				lng: values.points.lon
			}];
		}

		newFilter = {
			id: response._leaflet_id,
			type: type,
			layer: response,
			element: response._path,
			coordinates: latlng
		};

		map.geofilters[response._leaflet_id] = newFilter;

		$(document).trigger({
			type: 'geofilter:create',
			filter: newFilter,
			map: map,
			preventClick: true
		});

		//Create a what filter by triggering a click event on its filter creation button.
		$('#filter-buttons').find('[data-type="where"]').addClass('active');

		$whereFilter.find('input[name="estimated"]').prop('checked', estimated);
		$whereFilter.find('input[value="' + insideOutside + '"]').prop('checked', true);

		_.forEach(namedFilters, function(namedFilter) {
			var matchedKey;

			matchedKey = _.findKey(namedFilter, function(value) {
				return _.isEqual(value, filter);
			});

			if (matchedKey != null) {
				$('#filter-name').find('input[name="name"]').val(matchedKey).trigger('change');
			}
		});
	}

	function _createConnectorFilter(filter, namedFilters) {
		var $connectorFilter;

		$connectorFilter = $('form.connector');
		//Create a connector filter by triggering a click event on its filter creation button.
		$('#filter-buttons').find('[data-type="connector"]').trigger({
			type: 'click'
		});

		//Set the select to the connection specified.
		$connectorFilter.find('select[name="connection"]').val(filter.value);

		_.forEach(namedFilters, function(namedFilter) {
			var matchedKey;

			matchedKey = _.findKey(namedFilter, function(value) {
				return _.isEqual(value, filter);
			});

			if (matchedKey != null) {
				$('#filter-name').find('input[name="name"]').val(matchedKey).trigger('change');
			}
		});
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

		if (isMobile) {
			$('#content').hide();
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

		if (isMobile) {
			$('#content').show();
		}
	}


	return {
		expand: expand,
		generateFilters: generateFilters,
		shrink: shrink
	};
});
