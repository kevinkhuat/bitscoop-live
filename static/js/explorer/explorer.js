define(['actions', 'bluebird', 'cartano', 'debounce', 'embed', 'favorite', 'history', 'humanize', 'icons', 'jquery', 'leaflet', 'lodash', 'menu', 'moment', 'nunjucks', 'objects', 'search', 'throttle', 'viewstate', 'autoblur', 'jquery-cookie', 'jquery-mixitup', 'templates', 'leaflet-awesome-markers', 'minimodal'], function(externalActions, Promise, cartano, debounce, embedContent, favorite, history, humanize, icons, $, leaflet, _, menu, moment, nunjucks, objects, search, throttle, viewstate) {
	var map;

	// Valid View States: feed, grid, list, map, result
	var container;
	var spinner = viewstate.renderSync('explorer/components/waiting.html');
	var paginationSpinner = viewstate.renderSync('explorer/components/next.html');
	var errorBubble = viewstate.renderSync('explorer/components/error.html');

	//TODO: Explore getting sizes for DOM elements programatically
	var GRID_ITEM_SIZE = 160 + 16; // px
	var MIN_GRID_ITEMS = 4;
	var SCROLL_DEBOUNCE = 500; // ms
	var SCROLL_EMBED_LEAD_AREA = 700; // px
	// Virtual scroll "cursor."
	var cursor = {
		limit: 100,
		offset: 0
	};

	var previewContext = [
		{
			mapping: 'content',
			name: 'Content',
			type: 'content'
		},

		{
			mapping: 'events',
			name: 'History',
			type: 'event'
		},

		{
			mapping: 'contacts',
			name: 'Contacts',
			type: 'contact'
		},

		{
			mapping: 'things',
			name: 'Things',
			type: 'thing'
		},

		{
			mapping: 'places',
			name: 'Places',
			type: 'place'
		},

		{
			mapping: 'locations',
			name: 'Locations',
			type: 'location'
		},

		{
			mapping: 'organizations',
			name: 'Organizations',
			type: 'organization'
		}
	];

	var typeMappings = {};
	var collectionMappings = {};

	_.each(previewContext, function(item) {
		typeMappings[item.mapping] = item.type;
		collectionMappings[item.type] = item.mapping;
	});

	// Valid View States: feed, grid, list, map, result
	// Valid Results Shown: contacts, content, events, locations, people, places, things
	var state = {
		view: null,
		mapping: null,
		object: null
	};

	var views = {
		grid: new viewstate.View('explorer/views/grid.html'),
		list: new viewstate.View('explorer/views/list.html'),
		feed: new viewstate.View('explorer/views/feed.html'),
		map: new viewstate.View('explorer/views/map.html'),
		results: new viewstate.View('explorer/views/results.html')
	};

	function isMobile() {
		if (window.matchMedia) {
			return window.matchMedia('(max-device-width: 1080px) and (min-device-pixel-ratio: 1.5)').matches;
		}
		else {
			return false;
		}
	}

	/**
	 * Renders the Result view. This needs to be separated into a function because we have to recalculate the results
	 * preview on window resize.
	 *
	 * @private
	 * @returns {Promise}
	 */
	function renderPreview() {
		var count, promises;

		// Calculate how many preview items to render based on the window's width, the size of an item,
		// and how large the DOM element for more results is. Minimum is 4.
		count = Math.max(MIN_GRID_ITEMS, Math.floor(window.innerWidth / GRID_ITEM_SIZE));

		promises = _.map(objects.collections, function(results, mapping) {
			var n, humanized;

			n = Math.min(count, results.length);

			// TODO: Put more count for each item type when we can search multiple indices.
			if (mapping === 'events' && objects.cursor.count > n) {
				humanized = humanize.compactInteger(objects.cursor.count - n, 1);
				$('div[data-mapping="' + mapping + '"] .more').text(humanized);
			}

			return objects.render('grid', results.slice(0, n))
				.then(function(fragments) {
					var $el;

					$el = $('div[data-mapping="' + mapping + '"]');

					$el.find('.items').empty().append(fragments);
				});
		});

		return Promise.all(promises);
	}

	/**
	 * Renders the page for a newly-selected view state.
	 *
	 * @returns {Promise} A promise that is resolved when the selected view is rendered.
	 */
	function renderState() {
		var context, html, promise, type, view, $body, $list;

		if (!views.hasOwnProperty(state.view)) {
			return Promise.reject(new Error('Invalid view type.'));
		}

		promise = Promise.resolve();
		type = typeMappings[state.mapping];
		$body = $('body');
		$list = $('#list');

		// MixItUp can run into problems if there are multiple copies active at once, so destroy any active copies.
		if ($list.mixItUp && $list.mixItUp('isLoaded')) {
			$list.mixItUp('destroy', true);
		}

		resetView();

		if (state.view !== 'results') {
			// TODO: Implement promises for prepopulation and autoscrolling.
			//function() {
			//	function inner() {
			//		return search.more();
			//
			//		if (search.results.list[state.type].length < SCROLL_MIN_COUNT && search.results.list.events.length < search.results.count) {
			//			deferred.resolve();
			//		}
			//
			//	}
			//
			//	search.more().then(search.more).then(search.more).then(search.more);
			//
			//	while ()
			//
			//	if (search.results.list[state.type].length < SCROLL_MIN_COUNT && search.results.list.events.length < search.results.count) {
			//		return search.more().then(prepopulate);
			//	}
			//
			//	return deferred.promise;
			//}
		}

		if (state.view === 'results') {
			view = views.results;
			context = {
				types: _.filter(previewContext, function(type) {
					return objects.collections[type.mapping].length > 0;
				})
			};

			$('header > .sort').addClass('hidden');

			promise = promise.then(function() {
				return view.render(context);
			}).then(function() {
				// FIXME: The view is reset too quickly here. Should be waiting until the preview is rendered.
				resetView();
				container.insert(view);

				return renderPreview();
			});
		}
		else if (state.view === 'map') {
			mapView.render().done(function() {
				var $expandDetails;

				$body.addClass('map');
				container.insert(mapView);
				$('#background').append(map.element);
				$list = $('#list');
				addResults(objects.collections[state.mapping]);

				//TODO: Figure out how to bind scroll event delegation instead of binding directly to #background
				$list.on('scroll', throttle(checkScroll, SCROLL_DEBOUNCE));
				renderFeedEmbeddables($list);

				//Prep the expandDetails element for showing the #left panel.
				$expandDetails = $('#expand-details');
				$expandDetails.removeClass('hidden');
				$expandDetails.children('i').removeClass('fa-caret-right').addClass('fa-caret-left');
				$('#details-scroll').addClass('hidden');

				addMapMarkers();

				//If not in mobile, put the controls back in.
				if (!isMobile) {
					addMapControls();
				}

				//Resize the map and fit it so that all markers are visible.
				map.resize();

				if (map.markers.getBounds()._southWest != null) {
					map.object.fitBounds(map.markers.getBounds());
				}

				//Show the #left panel and perform the initial sort.
				$('#left').addClass('expanded');
			});
		}
		else {
			view = views[state.view];

			promise = promise
				.then(function() {
					return view.render();
				})
				.then(function() {
					return objects.render(state.view, objects.collections[state.mapping].slice(0, cursor.limit));
				})
				.tap(function(fragments) {
					var $list;

					resetView();
					container.insert(view);

					$list = $('#list');
					cursor.offset = fragments.length;

					$list.append(fragments);
				});
		}

		if (state.view === 'feed') {
			promise = promise.then(function() {
				$list = $('#list');

				$list.closest('main').on('scroll', debounce(function() {
					renderFeedEmbeddables($list.parent());
				}, SCROLL_DEBOUNCE));

				//render Embeddables the first time
				renderFeedEmbeddables($list.parent());

				return Promise.resolve();
			});
		}

		if (state.view !== 'results') {
			promise.then(function(result) {
				var sortContext,  $selectedSort, $sortFields, $sortArrow;

				$('header > .sort').removeClass('hidden');

				if (type) {
					sortContext = objects[type[0].toUpperCase() + type.slice(1)].sort;
				}
				else {
					sortContext = objects['Event'].sort;
				}

				$sortFields = $('.sort .fields');

				//Generate the sort selectors for the current object type.
				html = nunjucks.render('explorer/components/sort.html', sortContext);
				$sortFields.html(html);

				// Update the sort DOM elements.
				$selectedSort = $sortFields.find('[data-sort="' + objects.cursor.sort.field + '"]');

				$sortArrow = $selectedSort.find('.fa');

				_.forEach($sortFields.children('div'), function(sortItem) {
					var $sortItem = $(sortItem);

					$sortItem.removeClass('active');
					$sortItem.find('.sort-arrow').removeClass('fa-caret-up').removeClass('fa-caret-down');
				});

				$selectedSort.addClass('active');

				if (objects.cursor.sort.order === 'asc') {
					$sortArrow.addClass('fa-caret-up');
				}
				else {
					$sortArrow.addClass('fa-caret-down');
				}

				return Promise.resolve(result);
			});
		}

		return promise.then(function() {
			var scroller, $main;

			$main = $('#list').closest('main');

			scroller = throttle(function(e) {
				var page, promise, scrollBottom, slice, $list;

				scrollBottom = e.target.scrollTop + $(e.target).outerHeight();

				if (scrollBottom > 0.90 * e.target.scrollHeight) {
					$list = $('#list');

					if (objects.cursor.next || cursor.offset < objects.collections[state.mapping].length) {
						$list.addClass('loading');
						$list.append(paginationSpinner);

						if (cursor.offset < objects.collections[state.mapping].length) {
							page = {};
							slice = objects.collections[state.mapping].slice(cursor.offset, cursor.offset + cursor.limit);
							page[state.mapping] = slice;

							cursor.offset += cursor.limit;

							promise = Promise.resolve(page);
						}
						else {
							promise = objects.more()
								.tap(function() {
									cursor.offset = objects.collections[state.mapping].length;
								});
						}

						return promise
							.then(function(data) {
								if (data == null) {
									$main.off('scroll.more', scroller);

									return Promise.resolve();
								}

								$list.removeClass('loading');
								$('#next-icon').remove();

								return objects.render(state.view, data[state.mapping]);
							})
							.tap(function(fragments) {
								$list.append(fragments);
							})
							.catch(function(err) {
								// TODO: Show an error message somehow? Notifications?

								$list.removeClass('loading');
								$('#next-icon').remove();
							});
					}
					else {
						$main.off('scroll.more', scroller);
					}
				}
			});

			$main.off('scroll.more').on('scroll.more', scroller);

			return Promise.resolve(view);
		});
	}

	/**
	 * Resets the viewport so that a different view/facet can be rendered cleanly.
	 */
	function resetView() {
		container.clear();
		search.shrink();
		menu.close();
		$('body')
			.removeClass('feed grid list map results')
			.addClass(state.view);
		$('#menu .views a[data-view="' + state.view + '"]').addClass('active')
			.siblings().removeClass('active');
	}

	/**
	 * Highlights an object that has been selected, usually by rendering its details.
	 * @param {object} object The object that has being selected.
	 */
	function selectObject(object) {
		var params, $details;

		state.object = object;

		if (state.view === 'results') {
			params = $.deparam(location.search.slice(1));
			state.view = params.view || sessionStorage.getItem('explorer.view') || 'feed';
			state.mapping = collectionMappings[objects.type(object)];

			history.param({
				view: state.view,
				type: state.mapping
			});

			renderState()
				.then(function() {
					object._viewFragments[state.view].scrollIntoView(true);
				});
		}
		else if (state.view != 'feed') {
			object._viewFragments[state.view].scrollIntoView(true);

			$details = $('#details');
			$details.modal({
				position: false,
				postOpen: function() {
					var $this = $(this);

					objects.render('details', state.object)
						.then(function(fragment) {
							var $body, $contentEmbedContainers;

							$body = $this.find('.body');
							$body.empty().append(fragment);

							$contentEmbedContainers = $body.find('.content-embed');

							_.forEach($contentEmbedContainers, function(embedContainer) {
								var embedObject, $parentContainer;

								$parentContainer = $(embedContainer).parent('.object');
								embedObject = $parentContainer.data('object');

								embedContent(embedObject, $(embedContainer));
							});

							$this.css('display', 'flex');
						});
				}
			});
		}
	}

	//Bind Results view-specific events.
	views.results.on('click', '.header', throttle(function() {
		var mapping, view, $this = $(this);

		state.view = view = sessionStorage.getItem('explorer.view') || 'feed';
		state.mapping = mapping = $this.parent().data('mapping');

		history.param({
			view: view,
			type: mapping
		});

		return renderState();
	}));

	$(search).on('searching', function(e) {
		state.view = 'results';

		container.clear();
		container.insert(spinner);

		history.replace.delParam(['view', 'type']);
	});

	$(search).on('search', function(e, done) {
		objects.search({
			query: search.query,
			dsl: search.dsl
		})
			.then(renderState)
			.then(done)
			.catch(function(err) {
				container.clear();
				container.insert(errorBubble);
				done();
			});
	});

	$(search).on('update', function(e, search) {
		if (search && search.id) {
			history.replace.param('qid', search.id);
		}
		else {
			history.replace.delParam('qid');
		}
	});

	$(search).on('error', function(err) {
		container.clear();
		container.insert(errorBubble);
	});

	/**
	 * Adds markers to the map. If passed an object, then it just adds a marker for that object. If no object is passed,
	 * then it adds markers for every one of the current object type being displayed.
	 *
	 * @param {object} [object] If present, then only this object's location will be added to the map
	 */
	function addMapMarkers(object) {
		var coordinates, estimated, icon, results;

		//If no object is passed in, then the list of objects to be mapped ('results') should be all of the ones
		//of the current object type shown.
		if (object === null) {
			//Since results are stored in a dictionary, convert the dictionary of the current object type shown
			//into an array.
			results = [];

			_.forEach(Object.keys(searchResults[state.type]), function(val) {
				if (searchResults[explorerState.objectTypeShown][val].location) {
					results.push(searchResults[explorerState.objectTypeShown][val]);
				}
			});
		}
		//If an object is passed in, then the list of objects to be mapped ('results') should be just the object.
		else {
			results = [object];
		}

		//Clear all of the current markers on the map.
		map.clearData();

		//If currently showing events or places:
		if (explorerState.objectTypeShown === 'events' || explorerState.objectTypeShown === 'places') {
			//Add markers to the map using the given callback function on each result item.
			map.addData(results, function(data) {
				var icon;

				//Add the event type's icon to the marker if it's an event.
				if (explorerState.objectTypeShown === 'events') {
					icon = icons.getEventFontIcon(data);
				}
				//Add the place type's icon to the marker if it's a place.
				//TODO: Pick icons for different place types.
				else if (explorerState.objectTypeShown === 'places') {
					icon = icons.getPlaceFontIcon();
				}

				//Get the coordinates and whether or not this location is estimated.
				coordinates = data.location.geolocation;
				estimated = data.location.estimated;

				//Create the icon, with a different color depending on whether the location is estimated.
				icon = leaflet.AwesomeMarkers.icon({
					icon: icon,
					prefix: 'fa',
					markerColor: estimated ? 'green' : 'blue'
				});

				//Return a new leaflet marker with some additional information saved on the options dictionary.
				return leaflet.marker([coordinates[1], coordinates[0]], {
					estimated: estimated,
					objectId: data.id,
					icon: icon
				});
			});
		}
		//If currently showing locations:
		else if (explorerState.objectTypeShown === 'locations') {
			//Add markers to the map using the given callback function on each result item.
			map.addData(results, function(data) {
				//Get the coordinates.
				coordinates = data.geolocation;

				//Create the icon.
				icon = leaflet.AwesomeMarkers.icon({
					icon: icons.getLocationFontIcon(),
					prefix: 'fa',
					markerColor: 'blue'
				});

				//Return a new leaflet marker with some additional information saved on the options dictionary.
				return leaflet.marker([coordinates[1], coordinates[0]], {
					objectId: data.id,
					icon: icon
				});
			});
		}
	}

	/**
	 * Sets the colors of all the markers on the map.
	 * Every marker is set to either green (if the coordinates are estimated) or blue (if not).
	 * If an objectId is passed in, then the marker associated with that objectId will be highlighted orange.
	 * @param {string} [objectIdToHighlight] The objectId of an object whose marker should be highlighted.
	 */
	function setMarkerColors(objectIdToHighlight) {
		//Iterate over each marker.
		map.eachMarker(function(marker) {
			var icon;

			//Get the icon for the marker and un-highlight it by remove the orange class.
			icon = $(marker._icon);
			icon.removeClass('awesome-marker-icon-orange');

			//If the coordinates were estimated, then make the marker green.
			if (marker.options.estimated) {
				icon.addClass('awesome-marker-icon-green');
			}
			//If the coordinates were not estimated, then make the marker blue.
			else {
				icon.addClass('awesome-marker-icon-blue');
			}

			//If the marker's saved objectId matches the input objectId, then center the map on that marker and make the marker orange.
			//If no objectId was passed in, then this will never match.
			if (marker.options.objectId === objectIdToHighlight) {
				map.setCenter(marker._latlng);

				$(marker._icon).removeClass('awesome-marker-icon-blue').removeClass('awesome-marker-icon-green').addClass('awesome-marker-icon-orange');
			}
		});
	}

	function renderFeedEmbeddables($target) {
		var docViewBottom, docViewTop, elemBottom, elemTop, height, object, width, $contentEmbedContainers, $embedContainer, $parentContainer;

		$contentEmbedContainers = $target.find('.content-embed');
		docViewTop = $target.scrollTop();
		docViewBottom = docViewTop + $target.height();

		_.forEach($contentEmbedContainers, function(embedContainer) {
			$embedContainer = $(embedContainer);

			elemTop = $embedContainer.offset().top;
			elemBottom = elemTop + $embedContainer.height();

			$parentContainer = $(embedContainer.parentElement);

			if ((elemBottom <= docViewBottom + SCROLL_EMBED_LEAD_AREA) && (elemTop >= docViewTop - SCROLL_EMBED_LEAD_AREA)) {
				if ($embedContainer.children().length === 0) {
					$embedContainer.css('height', null);
					object = $parentContainer.data('object');

					embedContent(object, $embedContainer)
				}
			}
			else {
				width = $embedContainer.width();
				height = $embedContainer.height();

				if (height > 0) {
					$embedContainer.height(height);
				}

				$embedContainer.empty();
			}
		});
	}

	// Bind Map view-specific events.
	views.map.on('map:zoom', function() {
		// When the user zooms the map, de-select any active objects.
		var $active;

		$active = $('.item.active');
	});

	$(document).ready(function() {
		(function() {
			var params, qid;

			container = new viewstate.Component('main');
			container.clear();
			container.insert(spinner);

			params = $.deparam(location.search.slice(1));
			state.view = params.view || 'results';
			state.mapping = params.type || null;
			qid = params.qid || sessionStorage.getItem('qid');

			sessionStorage.removeItem('qid');

			return search.load(qid);
		})()
			.then(function(saved) {
				if (saved && saved.id) {
					history.replace.param('qid', saved.id);
				}
				else {
					history.replace.delParam('qid');
				}

				return objects.search({
					query: search.query,
					dsl: search.dsl
				});
			})
			.then(renderState)
			.catch(function(err) {
				container.clear();
				container.insert(errorBubble);
			});

		//When explorer is loaded, get the Mapbox token.
		$.ajax({
			url: '/tokens/mapbox',
			type: 'GET',
			dataType: 'json',
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			}
		}).done(function(data) {
			// When the Mapbox token has been retrieved, create a new Cartano map with it.

			map = new cartano.Map(data.MAPBOX_USER_NAME, {
				accessToken: data.MAPBOX_ACCESS_TOKEN,

				className: 'flex-grow',

				zoomControl: true,
				drawControl: true,
				layerControl: true
			});

			//Bind event listeners to the map.
			map.object.on('click', function() {
				//Deselect all events when you click on the map in map view (if you clicked on a marker, that will fire after this occurs).
				if (explorerState.currentViewState === 'map') {
					setMarkerColors();
					$('#details').empty();
					$('#details-scroll').addClass('hidden');
					$('.list-item').removeClass('active');
				}
			}).on('overlayremove', function() {
				//If overlays are removed from the map, then trigger a click so that anything currently selected is deselected.
				$(map.object._container).trigger({
					type: 'click'
				});
			});
		});

		// If the user resizes the window:
		$(window).resize(function() {
			if (state.view === 'results') {
				renderPreview();
			}
		});

		// Select the current item when
		$(document).on('click', '.item', function() {
			var object, $this = $(this);

			object = $this.data('object');

			selectObject(object);
		});

		// When the user clicks on a sort selector, sort on that field.
		$(document).on('click', '.sort .fields > div', throttle(function(e) {
			var sortField, $this = $(this);

			sortField = $this.attr('data-sort');

			// If the new sort type is the same as the previous sort type, then swap to the opposite asc/desc of what
			// was in use before.
			if (objects.cursor.sort.field === sortField) {
				objects.cursor.sort.order = objects.cursor.sort.order === 'asc' ? 'desc' : 'asc';
			}
			// If the new sort type is different from the previous sort type:
			else {
				// Usually, we want the first sort of a field to be asc, so that things are in alphabetical order
				// starting with 'A'. With datetimes, though, we're assuming the user wants the most recent objects
				// first, which is desc order.
				objects.cursor.sort.field = sortField;
				objects.cursor.sort.order = (objects.cursor.sort.field === 'datetime' || objects.cursor.sort.field === '_score') ? 'desc' : 'asc';
			}

			container.clear();
			container.insert(spinner);

			objects.search({
				query: search.query,
				dsl: search.dsl,
				sortField: objects.cursor.sort.field,
				sortOrder: objects.cursor.sort.order
			})
				.then(renderState);
		}));

		// When the user clicks on a marker or markercluster:
		$(document).on('marker:click', function(e) {
			var marker;

			marker = e.marker;

			//If the user clicked on a cluster, then wait until it finishes zooming to fit the clustered markers.
			if (e.clustered) {
				map.object.on('zoomend', function() {
					//If the map is at the maximum zoom level, then what we clicked on couldn't be de-clustered and should be spiderfied.
					//TODO: Get this spiderfication to actually work.
					if (map.object.getZoom() === 18) {
						marker.spiderfy();
					}
				});
			}
		});

		$(document).on('click', '#menu a.explorer', function(e) {
			if (/^\/explore/.test(location.pathname)) {
				e.preventDefault();
			}
		});

		$(document).on('click', '#menu .views a:not(.active)', throttle(function(e) {
			var view, $this = $(this);

			e.preventDefault();

			$this.addClass('active')
				.siblings().removeClass('active');

			state.view = view = $this.data('view');

			if (view === 'results') {
				history.param('view', view);
				history.replace.delParam('type');
			}
			else {
				sessionStorage.setItem('explorer.view', view);
				history.replace.param('view', view);
			}

			return renderState();
		}));

		$(document).on('click', '.share-action', function(e) {
			var object, $actionBar, $shareMenu, $this = $(this);
			$actionBar = $this.parents('.action-bar');
			$shareMenu = $actionBar.find('.share-menu');

			if ($shareMenu.length === 0) {
				$this.hide();

				object = $this.parents('.object').data('object');
				$actionBar.append(externalActions.renderAction(object, 'share'));
			}
			else {
				$this.hide();
				$shareMenu.show();
			}
		});

		$(document).on('click', '.object .contact', function(e) {
			var object, $actionBar, $shareMenu, $this = $(this);
			$actionBar = $this.find('.action-bar');
			$shareMenu = $actionBar.find('.share-menu');

			if ($shareMenu.length === 0) {
				object = $this.data('object');
				$actionBar.append(externalActions.renderAction(object, 'share'));
				$actionBar.find('.close').hide();
			}
			else {
				$actionBar.find('.share-menu').toggle();
			}
		});

		$(document).on('click', '.action-bar .close', function(e) {
			var $actionBar, $this = $(this);
			$actionBar = $this.parents('.action-bar');

			$actionBar.find('.share-menu').hide();
			$actionBar.find('.share-action').show();
		});

		$(document).on('click', '#search-favorited', function(e) {
			var favorited, html, icon, iconColor, name, $colorPreview, $favorite, $iconPreview, $name, $this = $(this);

			$favorite = $('#favorite');

			if (search.current == null) {
				favorited = false;
				icon = null;
				iconColor = null;
				name = '';
			}
			else {
				favorited = search.current.favorited;
				icon = search.current.icon;
				name = search.current.name;
				iconColor = search.current.icon_color;
			}

			html = nunjucks.render('components/favorite.html', {
				hideDelete: !favorited
			});

			$favorite.find('.body').html(html);

			$name = $favorite.find('input[name="search-name"]');
			$name.val(name);

			if (icon == null || icon.length === 0) {
				icon = 'none';
			}

			if (iconColor == null || iconColor.length === 0) {
				iconColor = '#b6bbbf';
			}

			$colorPreview = $favorite.find('.color-picker .preview');
			$iconPreview = $favorite.find('.icon-picker .preview');

			$colorPreview.find('input').val(iconColor);
			$colorPreview.find('label').css('background-color', iconColor);

			$iconPreview.addClass(icon);

			$favorite.find('.data > i').addClass(icon).css('color', iconColor);

			$favorite.modal({
				position: false,
				postOpen: function() {
					$(this).css('display', 'flex');
				}
			});
		});

		$(document).on('click', '#favorite button', function(e) {
			var action, icon, id, paramData, promise, $activeSearch, $favorite, $icon, $target;

			$activeSearch = $('#searches > *.active');
			$target = $(e.target);

			action = $target.closest('[data-action]').data('action');
			id = $activeSearch.data('id');

			promise = new Promise(function(resolve) {
				if (action === 'delete') {
					search.unfavorite(id).then(function() {
						$('#search-favorited').removeClass('filled');

						search.current.favorited = false;

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
						$('#search-favorited').addClass('filled');

						search.current.favorited = paramData.favorited;
						search.current.icon_color = paramData.icon_color;
						search.current.name = paramData.name;

						if (paramData.icon) {
							search.current.icon = paramData.icon;
						}

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

		$(window).on('popstate', function(e) {
			var mapping, params, view;

			// TODO: Cancel existing re-render if it's not done to prevent redundant CPU and pop-in (?).
			// TODO: Actually use history state to cut down on querystring processing.
			// FIXME: When the qid changes you need to rerun the search.

			params = $.deparam(location.search);
			mapping = params.type;

			if (!mapping) {
				view = 'results';
			}
			else {
				view = params.view || sessionStorage.getItem('explorer.view') || 'feed';
			}

			state.mapping = mapping;
			state.view = view;

			renderState();
		});
	});
});
