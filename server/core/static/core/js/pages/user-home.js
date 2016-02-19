define(['jquery', 'lodash', 'moment', 'nunjucks', 'jquery-cookie', 'minimodal', 'templates'], function($, _, moment, nunjucks) {
	var eventCount, maxWidth, offset, OVERFLOW_COUNT_WIDTH, paramData, RESULT_PAGE_LIMIT, $document;

	RESULT_PAGE_LIMIT = 20;
	OVERFLOW_COUNT_WIDTH = 30;

	$document = $(document);

	offset = 0;
	paramData = {};

	paramData.offset = offset;
	paramData.limit = RESULT_PAGE_LIMIT;

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
		eventCount = data.count;

		$('.image-and-text[name="events"]').find('.count').html(eventCount + ' Events');

		$('.tab[name="favorited"]').trigger('click');
	});

	$document.on('click', '#delete-save div[name="save"]', function(e) {
		var id, paramData, $activeSearch, $color, $icon, $name;

		$activeSearch = $('.saved-search.active');
		id = $activeSearch.attr('id');
		$color = $('select[name="color"]');
		$icon = $('select[name="icon"]');
		$name = $('#edit-search').find('input[name="search-name"]');

		e.preventDefault();

		paramData = {};

		if ($icon.children(':selected').attr('value') != 'none' || $name.val() != '') {
			if ($icon.children(':selected').attr('value') != 'none') {
				paramData.icon = $icon.children(':selected').attr('value');
				paramData.iconColor = $color.children(':selected').attr('value');
			}
			else {
				paramData.icon = '';
				paramData.iconColor = '';
			}

			paramData.name = $name.val();

			$.ajax({
				url: 'https://p.bitscoop.com/searches/' + id,
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
				if (paramData.name.length > 0) {
					$activeSearch.find('.named-search').html('<div class="name">' + paramData.name + '</div>');
				}
				else {
					$activeSearch.find('.named-search').empty();
				}

				$activeSearch.attr('name', paramData.name);

				if (paramData.icon.length > 0) {
					$activeSearch.attr('icon', paramData.icon);
					$activeSearch.attr('icon-color', paramData.iconColor);
					$activeSearch.find('.icon').html('<i class="' + paramData.icon + '" style="color: ' + paramData.iconColor + '"></i>');
				}
				else {
					$activeSearch.attr('icon', 'none');
					$activeSearch.attr('icon-color', '');
					$activeSearch.find('.icon').empty();
				}
			});
		}

		closeDrawer();
		$activeSearch.removeClass('active');
	});

	$document.on('click', '#delete-save div[name="delete"]', function(e) {
		$('#delete-search-modal').modal();
	});

	$document.on('click', '#delete-save div[name="cancel"]', function(e) {
		closeDrawer();
		$('.saved-search.active').removeClass('active');
	});

	$document.on('click', '#delete-search-modal button', function(e) {
		var action, $target;

		$target = $(e.target);

		$.modal.close();

		if ($target.is('.confirm')) {
			var id;

			id = $('.saved-search.active').attr('id');

			$.ajax({
				url: 'https://p.bitscoop.com/searches/' + id,
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
				closeDrawer();
				$('.saved-search.active').remove();
			});
		}
	});

	$document.on('click', '.saved-search .search', function(e) {
		var id, $this = $(this);

		if (!$(e.target).hasClass('favorite-edit')) {
			id = $this.parents('.saved-search').attr('id');

			location.pathname = 'explore/' + id;
		}
	});

	$document.on('click', '.favorite-edit', function(e) {
		var icon, iconColor, $colorSelect, $iconSelect, $editSearch, $name, $savedSearch, $this = $(this);

		$savedSearch = $this.parents('.saved-search');

		if ($savedSearch.hasClass('active')) {
			closeDrawer();
			$('.saved-search').removeClass('active');
		}
		else {
			closeDrawer();
			$('.saved-search').removeClass('active');
			$savedSearch.addClass('active');
			openDrawer();

			$editSearch = $('#edit-search');

			$name = $editSearch.find('input[name="search-name"]');
			$name.val($savedSearch.attr('name'));

			icon = $savedSearch.attr('icon');

			if (icon) {
				iconColor = $savedSearch.attr('icon-color');

				$colorSelect = $editSearch.find('select[name="color"] option[value="' + iconColor + '"]');
				$iconSelect = $editSearch.find('select[name="icon"] option[value="' + icon + '"]');
			}
			else {
				$colorSelect = $editSearch.find('select[name="color"] option[name="gray"]');
				$iconSelect = $editSearch.find('select[name="icon"] option[value="none"]');
			}

			$iconSelect.prop('selected', true);
			$iconSelect.trigger('change');
			$colorSelect.prop('selected', true);
			$colorSelect.trigger('change');
		}
	});

	$document.on('change', 'select[name="color"]', function(e) {
		var selectedColor, $this = $(this);

		selectedColor = $this.find(':selected').attr('value');
		$this.css('background-color', selectedColor);

		if ($('.icon-preview').children().length > 0) {
			$('.icon-preview i').css('color', selectedColor);
		}
	});

	$document.on('change', 'select[name="icon"]', function(e) {
		var color, $this = $(this);

		color = $('select[name="color"]').find(':selected').attr('value');

		if ($this.children(':selected').attr('value') != 'none') {
			$('.icon-preview').html('<i class="' + $this.find(':selected').attr('value') + '" style="color: ' + color + '"></i>');
		}
		else {
			$('.icon-preview').empty();
		}
	});

	$document.on('click', '#tabs .tab', function(e) {
		var paramData, $this = $(this);

		closeDrawer();

		$('#tabs .tab').removeClass('selected');

		$this.addClass('selected');

		paramData = {};

		paramData.searchTab = $this.attr('name');
		paramData.limit = RESULT_PAGE_LIMIT;
		paramData.offset = offset;

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
			$('#searches .saved-search').remove();

			_.forEach(data.results, function(search) {
				var context, id, namedFilters, savedFilters, source;

				context = {};
				source = search._source;

				if (source.name && source.name.length > 0) {
					context.name = source.name;
				}

				if (source.icon && source.icon.length > 0) {
					context.icon = source.icon;
					context.iconColor = source.icon_color;
				}

				id = search._id;

				context.filters = [];
				context.id = id;
				context.lastRun = moment(new Date(source.last_run)).format('MM-DD-YYYY h:mm:ss a');
				context.count = source.count;
				context.favorited = source.favorited;

				if (source.query && source.query.length > 0) {
					context.query = source.query;
				}

				savedFilters = source.filters;
				namedFilters = source.named_filters;

				_.forEach(savedFilters._must, function(type) {
					_.forEach(type.Or, function(filter) {
						var filterType, zeroElement;

						filterType = '';

						if (filter.Or) {
							zeroElement = filter.Or[0];

							if (zeroElement.search_field && (zeroElement.search_field === 'created' || zeroElement.search_field === 'datetime')) {
								filterType = 'when';
							}
							else if (zeroElement.search_field && (zeroElement.search_field === 'contacts.name' || zeroElement.search_field === 'contacts.handle')) {
								filterType = 'who';
							}
						}
						else if (filter.And) {
							zeroElement = filter.And[0];

							if (zeroElement.Or) {
								if (zeroElement.Or[0].search_field && (zeroElement.Or[0].search_field === 'contacts.name' || zeroElement.Or[0].search_field === 'contacts.handle')) {
									filterType = 'who';
								}
							}
							else {
								if (zeroElement.search_field && (zeroElement.search_field === 'location.geolocation')) {
									filterType = 'where';
								}
								else if (zeroElement.not && zeroElement.not.search_field && zeroElement.not.search_field === 'location.geolocation') {
									filterType = 'where';
								}
							}
						}
						else if (filter.not) {
							if (filter.not.search_field && filter.not.search_field === 'location.geolocation') {
								filterType = 'where';
							}
						}
						else {
							if (filter.search_field && filter.search_field === 'content.type') {
								filterType = 'what';
							}
							else if (filter.search_field && filter.search_field === 'datetime') {
								filterType = 'when';
							}
							else if (filter.search_field && filter.search_field === 'connection') {
								filterType = 'connector';
							}
							else if (filter.search_field && filter.search_field === 'contact_interaction_type') {
								filterType = 'who';
							}
							else if (filter.search_field && filter.search_field === 'location.geolocation') {
								filterType = 'where';
							}
						}

						_renderFilter(filterType, namedFilters, filter, context);
					});
				});

				$('#searches').append(nunjucks.render('core/user/saved-search.html', context));

				if (context.favorited && !context.icon) {
					$('#searches').find('[id="' + context.id + '"] .icon').empty();
				}

				if (context.favorited && !context.name) {
					$('#searches').find('[id="' + context.id + '"] .named-search').empty();
				}

				_compactOverflowFilters(id);
			});
		});
	});

	function _renderFilter(type, namedFilters, filter, context) {
		var matchName;

		_.forEach(namedFilters, function(namedFilter) {
			var matchedKey;

			matchedKey = _.findKey(namedFilter, function(value) {
				return _.isEqual(value, filter);
			});

			if (matchedKey != null) {
				matchName = matchedKey;
			}
		});

		if (matchName != null) {
			context.filters.push(matchName);
		}
		else {
			context.filters.push(type[0].toUpperCase() + type.slice(1));
		}
	}

	function _compactOverflowFilters(id) {
		var hideCount, hideIndex, overflowCounter, width, $filters, $savedSearch;

		maxWidth = $('#searches').find('.saved-search[id="' + id + '"] .search-content').width();
		overflowCounter = $('<div class="overflow">');
		width = 0;
		$savedSearch = $('.saved-search[id="' + id + '"]');
		$filters = $savedSearch.find('.filters > .filter');

		$filters.each(function(i, d) {
			var elemWidth;

			elemWidth = $(d).removeClass('hidden').outerWidth();

			if (elemWidth + width + OVERFLOW_COUNT_WIDTH > maxWidth) {
				hideIndex = i;

				return false;
			}

			width += elemWidth;
		});

		if (typeof hideIndex !== 'undefined') {
			hideCount = $filters.length - hideIndex;

			$filters.slice(hideIndex).addClass('hidden');
			overflowCounter.text('+ ' + hideCount)
				.appendTo($savedSearch.find('.filter-overflow-count'));
		}
		else {
			$savedSearch.find('.filter-overflow-count').empty();
		}
	}

	/**
	 * Close the drawer
	 */
	function closeDrawer() {
		var $drawer;

		$drawer = $('#drawer');

		//Set all grid items' margin-bottom to 1em, which is the default.
		$('.saved-search.active').css('padding-bottom', 0);

		$drawer.hide();
		$drawer.empty();
	}

	/**
	 * Opens the drawer
	 */
	function openDrawer() {
		var $drawer;

		$drawer = $('#drawer');

		closeDrawer();
		$drawer.empty();
		$drawer.html(nunjucks.render('core/user/edit-search.html'));
		renderDrawer();
		$drawer.css('display', 'flex');
		$drawer.css('visibility', 'initial');
	}

	/**
	 * Calculates the height of the drawer as well as the margin-bottom of the item being selected.
	 * The drawer sits in an absolutely positioned container, and is inserted below a selected item
	 * by giving the drawer a margin-top equal to the item's position in its containing div plus
	 * the item's height plus the item's vertical margins.
	 */
	function renderDrawer() {
		var heightDistance, item, itemHeight, itemPosition, itemVerticalPadding, $drawer;

		$drawer = $('#drawer');

		//Get the item being selected.
		item = $('.saved-search.active');

		//Reset the item's and the drawer's margins to their default values.
		item.css('padding-bottom', 0);
		$drawer.css('margin-top', 0);

		//Get the item's position and height.
		itemPosition = item.position();
		itemHeight = item.outerHeight();

		//Get the item's vertical padding.
		itemVerticalPadding = parseInt(item.css('padding-top').replace('px', '')) + parseInt(item.css('padding-bottom').replace('px', ''));

		//Give the item a margin-bottom of the drawer's height plus the item's vertical margins.
		item.css('padding-bottom', $drawer.outerHeight() + itemVerticalPadding);

		//The drawer's height from the top of the containing div is the item's top plus the item's height plus the item's vertical margins.
		heightDistance = itemPosition.top + itemHeight + itemVerticalPadding;

		//Set the drawer's margin-top to the calculated height.
		$drawer.css('margin-top', heightDistance + 'px');
	}
});
