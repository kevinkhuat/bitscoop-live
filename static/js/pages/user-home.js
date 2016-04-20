define(['bluebird', 'favorite', 'humanize', 'jquery', 'lodash', 'moment', 'nunjucks', 'rgb-to-hex', 'search', 'throttle', 'jquery-cookie', 'minimodal', 'templates'], function(Promise, favorite, humanize, $, _, moment, nunjucks, rgbToHex, search, throttle) {
	var currentResultCount, cursor, OVERFLOW_COUNT_WIDTH, RESULT_OFFSET, RESULT_PAGE_LIMIT, SCROLL_DEBOUNCE, SCROLL_LOAD_LIMIT, totalResultCount, $document;

	RESULT_PAGE_LIMIT = 10;
	RESULT_OFFSET = 0;
	OVERFLOW_COUNT_WIDTH = 30;
	SCROLL_DEBOUNCE = 1000; //ms
	SCROLL_LOAD_LIMIT = 200; //px

	$document = $(document);

	currentResultCount = 0;
	totalResultCount = 0;
	cursor = {};

	function getSearches(tab) {
		var paramData;

		paramData = {};

		paramData.type = tab;
		paramData.limit = RESULT_PAGE_LIMIT;
		paramData.offset = RESULT_OFFSET;

		return new Promise(function(resolve, reject) {
			$.ajax({
				url: 'https://api.bitscoop.com/v2/searches',
				type: 'GET',
				dataType: 'json',
				contentType: 'application/json',
				data: paramData,
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				},
				xhrFields: {
					withCredentials: true
				}
			}).done(function(data) {
				var i, response;

				totalResultCount = data.count;
				currentResultCount = data.results.length;
				cursor.next = data.next;

				for (i = 0; i < data.results.length; i++) {
					renderSearch(data.results[i]);
				}

				if ($('#searches').height() < $('#searches-container').height() && currentResultCount < totalResultCount) {
					response = moreSearches();
				}
				else {
					response = Promise.resolve(null);
				}

				response.then(function() {
					resolve(null);
				});
			}).fail(function(req) {
				var error;

				error = new Error(req.statusText);
				error.code = req.status;

				reject(error);
			});
		});
	}

	function moreSearches() {
		return new Promise(function(resolve, reject) {
			$.ajax({
				url: cursor.next.url,
				type: cursor.next.method,
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				},
				xhrFields: {
					withCredentials: true
				}
			}).done(function(data, status, req) {
				var i;

				currentResultCount += data.results.length;
				cursor.next = data.next;

				for (i = 0; i < data.results.length; i++) {
					renderSearch(data.results[i]);
				}

				resolve(null);
			}).fail(function(req) {
				var error;

				error = new Error(req.statusText);
				error.code = req.status;

				reject(error);
			});
		});
	}

	function renderSearch(search) {
		var context, id, lastRun;

		id = search.id;
		lastRun = moment(new Date(search.last_run));

		context = {
			id: id,
			filters: search.filters,
			lastRunRelative: lastRun.fromNow(),
			favorited: search.favorited,
			name: search.name,
			icon: search.icon,
			iconColor: search.icon_color,
			count: search.count,
			query: search.query
		};

		$('#searches').append(nunjucks.render('components/saved-search.html', context));

		compactOverflowFilters(id);
	}

	function compactOverflowFilters(id) {
		var hideCount, hideIndex, margin, maxWidth, overflowCounter, queryWidth, searchWidth, width, $filters, $overflowCount, $search;

		$search = $('#searches').find('*[data-id="' + id + '"] .search');

		searchWidth = $search.width();
		queryWidth = $search.find('.query').outerWidth();
		maxWidth = searchWidth - queryWidth;

		overflowCounter = $('<div class="overflow">');
		width = 0;
		$filters = $search.find('.filters > .filter');

		$filters.each(function(i, d) {
			var elemWidth;

			elemWidth = $(d).removeClass('hidden').outerWidth();
			margin = Math.ceil(parseFloat($(d).css('margin-right').replace('px', '')));

			if (elemWidth + width + 4 * margin + OVERFLOW_COUNT_WIDTH > maxWidth) {
				hideIndex = i;

				return false;
			}

			width += elemWidth;
		});

		if (typeof hideIndex !== 'undefined') {
			hideCount = $filters.length - hideIndex;

			$filters.slice(hideIndex).addClass('hidden');
			$overflowCount = $search.find('.filter-overflow-count');
			$overflowCount.empty();

			overflowCounter.text('+ ' + hideCount)
				.appendTo($overflowCount);
		}
		else {
			$search.find('.filter-overflow-count').empty();
		}
	}

	function checkScrollPagination(e) {
		var deferred, $lastChild, $target = $(e.target);

		//Automatically get the next page of results when you reach the last item.
		if (currentResultCount < totalResultCount) {
			$lastChild = $('#searches').children().last();

			if ($target.scrollTop() + $target.height() > $lastChild.position().top + $lastChild.height() - SCROLL_LOAD_LIMIT) {
				deferred = new $.Deferred();

				return new Promise(function(resolve, reject) {
					moreSearches($('.tab.selected').attr('name')).then(function() {
						resolve(null);
					});
				});
			}
		}
	}

	$document.ready(function() {
		$.ajax({
			url: 'https://api.bitscoop.com/v2/events',
			type: 'SEARCH',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				offset: 0,
				limit: 1
			}),
			xhrFields: {
				withCredentials: true
			}
		}).done(function(data) {
			var count;

			count = humanize.compactInteger(data.count, 1).toUpperCase();

			$('.stats .events .count')
				.text(count)
				.removeClass('transparent');

			$('.tab[name="favorites"]').trigger('click');
		});

		$.ajax({
			url: 'https://api.bitscoop.com/v2/searches',
			type: 'GET',
			contentType: 'application/json',
			data: {
				type: 'recent',
				offset: 0,
				limit: 1
			},
			xhrFields: {
				withCredentials: true
			}
		}).done(function(data) {
			var count;

			count = humanize.compactInteger(data.count, 1).toUpperCase();

			$('.stats .searches .count')
				.text(count)
				.removeClass('transparent');
		});

		$document.on('click', '#favorite button', function(e) {
			var action, icon, id, paramData, promise, $activeSearch, $favorite, $icon, $target;

			$activeSearch = $('#searches > *.active');
			$target = $(e.target);

			action = $target.closest('[data-action]').data('action');
			id = $activeSearch.data('id');

			promise = new Promise(function(resolve) {
				if (action === 'unfavorite') {
					search.unfavorite(id).then(function() {
						if ($('.tab.selected').attr('name') === 'favorites') {
							$activeSearch.remove();
						}
						else {
							$activeSearch.attr('data-favorited', false);
							$activeSearch.find('i.favorite-edit').removeClass('favorite-edit').addClass('favorite-create').removeClass('fa-star').addClass('fa-star-o');
							$activeSearch.find('.icon').replaceWith('<i class="icon fa fa-circle-o subdue" style="color: #b6bbbf"></i>');
							$activeSearch.find('.name').empty();
							$activeSearch.removeClass('active');
						}

						resolve(null);
					});
				}
				else if (action === 'save') {
					$favorite = $('#favorite');
					$icon = $favorite.find('.data > i');

					paramData = {
						id: id,
						favorited: true,
						icon_color: $('#color-edit').val(),
						name: $favorite.find('input[name="search-name"]').val()
					};

					icon = $icon.attr('class');

					if (!icon || $icon.hasClass('transparent')) {
						paramData.icon = 'none';
					}
					else {
						paramData.icon = icon;
					}

					search.favorite(paramData).then(function() {
						$activeSearch.attr('data-favorited', true);
						$activeSearch.find('i.favorite-create').removeClass('favorite-create').addClass('favorite-edit').removeClass('fa-star-o').addClass('fa-star');

						$activeSearch.attr('data-name', paramData.name);
						$activeSearch.find('.name').html(paramData.name);

						if (paramData.icon && paramData.icon !== 'none') {
							$activeSearch.attr('data-icon', paramData.icon);
							$activeSearch.attr('data-icon-color', paramData.icon_color);
							$activeSearch.find('i.icon').removeClass('fa subdue').removeClass(function(index, css) {
								return (css.match (/fa-[\S-]+/g) || []).join(' ');
							}).addClass(paramData.icon).css('color', paramData.icon_color);
						}
						else {
							$activeSearch.attr('data-icon', 'none');
							$activeSearch.attr('data-icon-color', '');
							$activeSearch.find('i.icon').removeClass('fa').removeClass(function(index, css) {
								return (css.match (/fa-[\S-]+/g) || []).join(' ');
							}).addClass('fa fa-circle-o').css('color', '#b6bbbf');
						}

						$activeSearch.removeClass('active');

						resolve(null);
					});
				}
				else if (action === 'delete') {
					search.del(id).then(function() {
						$activeSearch.remove();

						resolve(null);
					});
				}
				else {
					$activeSearch.removeClass('active');

					resolve(null);
				}
			});

			promise.then(function() {
				$.modal.close();
			});
		});

		$document.on('click', '#searches > *', function(e) {
			var id, $this = $(this);

			if ($(e.target).is('.favorite-edit, .favorite-create')) {
				e.preventDefault();

				return false;
			}

			id = $this.attr('data-id');

			sessionStorage.setItem('qid', id);
		});

		$document.on('click', '.favorite-edit, .favorite-create', function(e) {
			var html, icon, iconColor, $colorPreview, $favorite, $iconPreview, $name, $search, $this = $(this);

			$favorite = $('#favorite');
			$search = $this.parents('[data-id]');

			$search.addClass('active');

			html = nunjucks.render('components/favorite.html', {
				hideUnfavorite: ($search.attr('data-favorited') === 'false' || $search.attr('data-favorited') == null)
			});

			$favorite.find('.body').html(html);

			$name = $favorite.find('input[name="search-name"]');
			$name.val($search.attr('data-name'));

			icon = $search.attr('data-icon');

			if (icon == null || icon.length === 0 || icon === 'none') {
				icon = 'fa fa-times transparent';
			}

			iconColor = $search.attr('data-icon-color');

			if (iconColor == null || iconColor.length === 0) {
				iconColor = '#b6bbbf';
			}

			$colorPreview = $favorite.find('.color-picker .preview');
			$iconPreview = $favorite.find('.icon-picker .preview');

			$colorPreview.find('input').val(iconColor);
			$colorPreview.find('label').css('background-color', iconColor);

			$iconPreview.addClass(icon);

			$favorite.find('.data > i').attr('class', icon).css('color', iconColor);

			$favorite.modal({
				position: false,
				postOpen: function() {
					$(this).css('display', 'flex');
				}
			});
		});

		$document.on('click', '#tabs .tab', function(e) {
			var $searchContainer, $this = $(this);

			$searchContainer = $('#search-container');

			$('#tabs .tab').removeClass('selected');

			$this.addClass('selected');

			totalResultCount = 0;
			currentResultCount = 0;

			$('#searches').empty();

			$searchContainer.off('scroll');
			getSearches($this.attr('name'));
			$searchContainer.on('scroll', throttle(checkScrollPagination, SCROLL_DEBOUNCE));
		});

		$(window).resize(function() {
			var $searches;

			$searches = $('#searches > *');

			_.forEach($searches, function(search) {
				var $filters, $search;

				compactOverflowFilters($(search).attr('data-id'));
			});
		});
	});

	$(search).on('search', function(e, done) {
		location.pathname = '/explore';
		done();
	});

	$(search).on('update', function(e, search) {
		if (search && search.id) {
			sessionStorage.setItem('qid', search.id);
		}
		else {
			sessionStorage.removeItem('qid');
		}
	});
});
