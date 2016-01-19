define(['cartano', 'debounce', 'embed-content', 'icons', 'jquery', 'leaflet', 'lodash', 'moment', 'nunjucks', 'object-context', 'search', 'viewstate', 'autoblur', 'jquery-cookie', 'jquery-mixitup', 'templates', 'leaflet-awesome-markers'],
	function(cartano, debounce, embedContent, icons, $, leaflet, _, moment, nunjucks, objectContext, search, viewstate) {
		var DETAILS_ORDERING, EVENT_MAPPED_RELATED_FIELDS, explorerState, feedView, GRID_ITEM_SIZE, gridView, HIDE_FEED_FACETS, HIDE_LIST_FACETS, HIDE_MAP_FACETS, isMobile, listView, map, mapView, MORE_WIDTH, objectTemplateMap, PREVIEW_ORDERING, resultsView, resultsContainerComponent, SCROLL_DEBOUNCE, SCROLL_LOAD_LIMIT, SCROLL_MIN_COUNT, searchResults;

		isMobile = (window.devicePixelRatio >= 1.5 && window.innerWidth <= 768);

		// Valid View States: feed, grid, list, map, result
		resultsContainerComponent = new viewstate.Component('main');
		gridView = new viewstate.View('explorer/views/grid/base.html');
		listView = new viewstate.View('explorer/views/list/base.html');
		feedView = new viewstate.View('explorer/views/feed/base.html');
		mapView = new viewstate.View('explorer/views/map/base.html');
		resultsView = new viewstate.View('explorer/views/results/base.html');

		//TODO: Explore getting sizes for DOM elements programmatically
		GRID_ITEM_SIZE = 276; //px
		MORE_WIDTH = 115; //px
		SCROLL_LOAD_LIMIT = 100; //px
		SCROLL_DEBOUNCE = 250; //ms
		//TODO: Calculate this by screen size
		SCROLL_MIN_COUNT = 50;
		DETAILS_ORDERING = ['events', 'content', 'things', 'contacts', 'places', 'locations', 'organizations'];
		PREVIEW_ORDERING = ['content', 'events', 'contacts', 'things', 'places', 'locations', 'organizations'];
		EVENT_MAPPED_RELATED_FIELDS = ['contacts', 'content', 'organizations', 'places', 'locations', 'things'];
		HIDE_MAP_FACETS = ['contacts', 'content', 'organizations', 'things'];
		HIDE_LIST_FACETS = ['locations'];
		HIDE_FEED_FACETS = ['locations'];

		//	Change to arrays, pass linkages to other objects by references?
		searchResults = {
			contacts: {},
			content: {},
			events: {},
			locations: {},
			people: {},
			places: {},
			organizations: {},
			things: {}
		};

		// Valid View States: feed, grid, list, map, result
		// Valid Results Shown: contacts, content, events, locations, people, places, things
		explorerState = {
			currentViewState: 'results',
			currentSort: null,
			currentSearch: '',
			objectTypeShown: 'events',
			moreLink: '',
			totalResultCount: 0,
			currentResultCount: 0,
			selectedObjectId: null,
			selectedObjectType: null
		};

		objectTemplateMap = {
			contacts: 'explorer/objects/contact.html',
			content: 'explorer/objects/content.html',
			events: 'explorer/objects/event.html',
			locations: 'explorer/objects/location.html',
			organizations: 'explorer/objects/organization.html',
			people: 'explorer/objects/person.html',
			places: 'explorer/objects/place.html',
			things: 'explorer/objects/thing.html'
		};

		/**
		 * Clears data from the map and deletes all stored search results
		 */
		function clearSearchResults() {
			map.clearData();

			searchResults = {
				contacts: {},
				content: {},
				events: {},
				locations: {},
				people: {},
				places: {},
				organizations: {},
				things: {}
			};
		}

		/**
		 * Adds search results to the internal store.
		 * @param {object} resultEvents A list of search result objects
		 */
		function addEventsToSearchResults(resultEvents) {
			//TODO: Change search.js so that this is no longer necessary

			/**
			 * For non-event objects, adds a copy of the event(s) that reference it.
			 * @param {object} object A non-event object
			 * @param {object} event An event
			 */
			function addEventsToSearchResults$addEventReference(object, event) {
				//Either push the new event onto to the list of events, or, if there are no events, set object.events
				//to a list just containing the new event,
				if (object.events) {
					object.events.append(event);
				}
				else {
					object.events = [event];
				}

				//Directly add the event's provider number, provider name, and provider icon to the object
				object.provider = event.provider;
				object.provider_name = event.provider_name;
				//TODO: Make this better, currently here so I don't have to do this over and over in the context generating function.
				object.providerIcon = icons.getProviderFontIcon(event.provider_name.toLowerCase());
			}

			//Iterate through each event.
			_.forEach(resultEvents, function(event) {
				//Try to save the event to searchResults.  If the event has already been saved, then it will just
				//overwrite the event that is present.
				searchResults.events[event.id] = event;

				//If the event has an actual location, then save that location to searchResults and add a reference
				//to that event onto the location.
				if (event.location.id) {
					searchResults.locations[event.location.id] = event.location;
					addEventsToSearchResults$addEventReference(searchResults.locations[event.location.id], event);
				}

				//Iterate through each of the sub-object types.
				_.forEach(EVENT_MAPPED_RELATED_FIELDS, function(renderType) {
					//Iterate through the list of each sub-object type on the event.
					_.forEach(event[renderType], function(singleType) {
						//Save that sub-object to searchResults and add a reference to that event on the sub-object.
						searchResults[renderType][singleType.id] = singleType;
						addEventsToSearchResults$addEventReference(searchResults[renderType][singleType.id], event);
					});
				});
			});
		}

		/**
		 * Adds markers to the map.  If passed an object, then it just adds a marker for that object.  If no object
		 * is passed, then it adds markers for every one of the current object type being displayed.
		 * @param {object} [object] If present, then only this object's location will be added to the map
		 */
		function addMapMarkers(object) {
			var coordinates, estimated, icon, results;

			//If no object is passed in, then the list of objects to be mapped ('results') should be all of the ones
			//of the current object type shown.
			if (object == null) {
				//Since results are stored in a dictionary, convert the dictionary of the current object type shown
				//into an array.
				results = Object.keys(searchResults[explorerState.objectTypeShown]).map(function(val) {
					return searchResults[explorerState.objectTypeShown][val];
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
		 * Render an item for each object passed in using the given template with a context specified by the input context rendering function.
		 * Then add the item to the given list.
		 * @param {object} resultObjects An array of result objects
		 * @param {function} contextFunction The function to be used to generate a context for each result object
		 * @param {string} template The name of the nunjucks template to be used to generate a DOM element for each result object
		 * @param {object} $list A jQuery-selected DOM element where each new element will be inserted
		 */
		function renderResults(resultObjects, contextFunction, template, $list) {
			var context, renderedResult;

			//Each result object has its renderable context generated by the contextFunction passed in.
			//This context is used to render the specified template, and then the resulting DOM element is appended
			//to the specified list.
			_.forEach(resultObjects, function(resultObject) {
				var newObjectId;

				context = contextFunction(resultObject);
				renderedResult = nunjucks.render(template, context);
				newObjectId = $(renderedResult).attr('data-object-id');

				if ($('#list').find('[data-object-id="' + newObjectId + '"]').length === 0) {
					$list.append(renderedResult);
				}
			});
		}

		function addNewResults() {
			var currentContextFunction, currentObjectContext, template, $list;

			currentObjectContext = searchResults[explorerState.objectTypeShown];
			currentContextFunction = objectContext[explorerState.objectTypeShown][explorerState.currentViewState];

			switch(explorerState.currentViewState) {
				case 'grid':
					template = 'explorer/views/grid/item.html';
					break;

				case 'list':
					template = 'explorer/views/list/item.html';
					break;

				case 'map':
					template = 'explorer/views/map/item.html';
					break;
			}

			//Render items for each object and insert the items into the list, then perform the initial sort.
			$list = $('#list');
			renderResults(currentObjectContext, currentContextFunction, template, $list);
			initializeSort($list);
		}

		/**
		 * Performs the initial sort
		 * @param {object} $list A jQuery-selected list of result items
		 */
		function initializeSort($list) {
			var currentViewState, initialSort, onMixStart, sortSplit, $initialSort;

			//TODO: Get from search results if not all results are currently shown
			//Check that there are fields to sort on for this object type, and if so get the initial sort field.
			if (objectContext[explorerState.objectTypeShown].sort.fields.length > 0) {
				initialSort = objectContext[explorerState.objectTypeShown].sort.initial;
			}

			currentViewState = explorerState.currentViewState;

			//Get the function for closing the drawer or details, whichever is currently being shown.
			if (currentViewState === 'grid') {
				onMixStart = closeDrawer;
			}
			else if (currentViewState === 'list') {
				onMixStart = closeDetails;
			}

			//Create a MixItUp instance.
			//Tell it to run the selected close function when it's initialized, and to sort using the specified sort field.
			$list.mixItUp({
				animation: {
					duration: 500
				},
				callbacks: {
					onMixStart: onMixStart
				},
				layout: {
					display: 'flex'
				},
				load: {
					sort: initialSort
				},
				//Normally MixItUp will do a descending sort when you click a sort selector.
				//This can cause visual glitches with our system, as clicking on a sort selector first does that
				//default sort, and then our system tries to do its sort.
				//The workaround was to point MixItUp to a non-existent sort selector so that only our code will run.
				selectors: {
					sort: 'null'
				}
			});

			explorerState.currentSort = initialSort;

			//If there's at least one sortable field, then set the initial sort selector to active and set its
			//ascending/descending arrow appropriately.
			if ($('.sort-selector').length > 0) {
				sortSplit = initialSort.split(':');

				//TODO: Make this keyed of the search engine. Make the selector better.
				$initialSort = $('.sort-selector[data-sort="' + sortSplit[0] + ':none"]');

				$initialSort.attr('data-sort', initialSort).addClass('active');
				$initialSort.find('.sort-arrow').addClass(sortSplit[1] === 'asc' ? 'fa-caret-up' : 'fa-caret-down');
			}
		}

		// Valid Results Shown: contacts, content, events, locations, people, places, things, all (in Results view)
		/**
		 * Renders the page for a newly-selected view state.
		 */
		function renderState() {
			var currentObjectContext, $backToResults, $body, $sortBar, $list, $homeButton, $viewBar;

			/**
			 * Renders the Result view
			 */
			function renderState$renderResultsView() {
				resultsView.render().done(function() {
					var numItems;

					$body.addClass('results');

					//Switch the container to result view
					resultsContainerComponent.insert(resultsView);

					//Calculate how many preview items to render based on the window's width, the size of an item,
					//and how large the DOM element for more results is.
					//A minimum of 4 elements will be shown.
					numItems = Math.max(4, Math.floor((window.innerWidth - MORE_WIDTH) / GRID_ITEM_SIZE));

					//Iterate through each object type in the order specified in PREVIEW_ORDERING
					_.forEach(PREVIEW_ORDERING, function(renderType) {
						var numMoreObjects, resultObjects, $list = $('#' + renderType + '-results');

						//Since searchResults are saved as a dictionary, turn each object's entry into an array.
						//Only use the first n results as calculated in numItems.
						resultObjects = Object.keys(searchResults[renderType]).map(function(val) {
							return searchResults[renderType][val];
						}).slice(0, numItems);

						//If there is at least one result for this object type, render the 'More' element for
						//the current object type and insert it into the DOM.
						//Then render the results for this object type and insert them into the list.
						if (resultObjects.length > 0) {
							if (isMobile) {
								$('.type-header[data-result-type="' + renderType + '"]').append(nunjucks.render('explorer/views/results/more.html', {
									renderType: renderType
								}));
							}
							else {
								$list.after(nunjucks.render('explorer/views/results/more.html', {
									renderType: renderType
								}));
							}

							renderResults(resultObjects, objectContext[renderType].grid, 'explorer/views/grid/item.html', $list);
						}
						//If there aren't any results for this object type, hide its display area.
						else {
							$('[data-result-type=' + renderType + ']').hide();
						}

						//Calculate how many results were not shown.
						numMoreObjects = Math.max(0, explorerState.totalResultCount - numItems);

						//Currently we're only showing how many more Events there are since that is the only
						//object type we're actively searching for in ElasticSearch.
						//If there are more than are being shown, insert that number in the More element.
						//TODO: When we're searching on every object type, show how many more there are for each of them.
						if (renderType === 'events' && numMoreObjects > 0) {
							$('#' + renderType + '-more-count').html('+' + numMoreObjects);
						}
					});
				});
			}

			/**
			 * Some object types should not have access to certain views since they don't have much, or any,
			 * useful information to show in those views.
			 * This disables those views for those types.
			 */
			function renderState$hideInvalidViews() {
				//Only events, locations, and places have coordinates, so all other object types shouldn't have access to map view.
				if (_.indexOf(HIDE_MAP_FACETS, explorerState.objectTypeShown) !== -1) {
					$('.view-selector[data-selector="map"]').addClass('hidden');
				}

				//Locations don't have much to show in feed view, and rendering multiple maps is currently not
				//supported by the explorer.
				if (_.indexOf(HIDE_FEED_FACETS, explorerState.objectTypeShown) !== -1) {
					$('.view-selector[data-selector="feed"]').addClass('hidden');
				}

				//Locations don't have any useful data to show in a list.
				if (_.indexOf(HIDE_LIST_FACETS, explorerState.objectTypeShown) !== -1) {
					$('.view-selector[data-selector="list"]').addClass('hidden');
				}
			}

			//Select useful DOM elements.
			$body = $('body');
			$list = $('#list');
			$homeButton = $('#home');
			$backToResults = $('#back-to-results');
			$sortBar = $('.sort-bar');
			$viewBar = $('.view-bar');

			//MixItUp can run into problems if there are multiple copies active at once, so destroy any active copies.
			if ($list.mixItUp && $list.mixItUp('isLoaded')) {
				$list.mixItUp('destroy', true);
			}

			resultsContainerComponent.clear();
			$body.removeClass('list').removeClass('grid').removeClass('map').removeClass('results').removeClass('feed');

			//If not in Results view:
			if (explorerState.currentViewState !== 'results') {
				//Display the view and sort selectors.
				$viewBar.show();
				$sortBar.show();

				if (isMobile) {
					$homeButton.addClass('hidden');
					$backToResults.removeClass('hidden');
				}

				//Show all the view selectors, then hide the selectors for views that are not applicable to the current object type.
				$('.view-selector').removeClass('hidden');
				renderState$hideInvalidViews();

				//Generate the sort selectors for the current object type.
				$('.sort-fields').html(nunjucks.render('explorer/components/sort.html', objectContext[explorerState.objectTypeShown].sort));

				//On mobile, the header for the sort bar will indicate what object type is being shown
				//and what view it's being shown in.
				$sortBar.find('.title').html('Sorting ' + explorerState.objectTypeShown[0].toUpperCase() + explorerState.objectTypeShown.slice(1) + ' in ' + explorerState.currentViewState[0].toUpperCase() + explorerState.currentViewState.slice(1) + ' View');
			}
			//If in results view, hide the view and sort selectors.
			else {
				$viewBar.hide();
				$sortBar.hide();

				if (isMobile) {
					$homeButton.removeClass('hidden');
					$backToResults.addClass('hidden');
				}
			}

			$('#background').off('scroll');
			$list.off('scroll');

			//Different behavior for each view state.
			switch(explorerState.currentViewState) {
				case 'results':
					if (explorerState.totalResultCount > 0) {
						renderState$renderResultsView();
					}
					else {
						$('main').html(nunjucks.render('explorer/components/no-results.html'));
					}
					break;

				case 'list':
					listView.render().done(function() {
						$body.addClass('list');

						resultsContainerComponent.insert(listView);
						addNewResults();

						//TODO: Figure out how to bind scroll event delegation instead of binding directly to #background
						$('#background').on('scroll', debounce(function(e) {
							checkScrollPagination(e);
						}, SCROLL_DEBOUNCE));
					});
					break;

				case 'map':
					mapView.render().done(function() {
						var $expandDetails;

						$body.addClass('map');

						resultsContainerComponent.insert(mapView);

						//Insert the map into #background
						$('#background').append(map.element);

						//Prep the expandDetails element for showing the #left panel.
						$expandDetails = $('#expand-details');
						$expandDetails.removeClass('hidden');
						$expandDetails.children('i').removeClass('fa-caret-right').addClass('fa-caret-left');
						$('#details-scroll').addClass('hidden');

						addNewResults();

						//We only add markers for every object of the current type when the map view is being rendered.
						//This is so that when the map is shown in the grid drawer or the list details, it will only
						//have a marker for the actively selected result.
						addMapMarkers();

						//If not in mobile, put the controls back in.
						if (!isMobile) {
							addMapControls();
						}

						//Resize the map and fit it so that all markers are visible.
						map.resize();
						map.object.fitBounds(map.markers.getBounds());

						//Show the #left panel and perform the initial sort.
						$('#left').addClass('expanded');

						//TODO: Figure out how to bind scroll event delegation instead of binding directly to #background
						$('#list').on('scroll', debounce(function(e) {
							checkScrollPagination(e);
						}, SCROLL_DEBOUNCE));
					});
					break;

				case 'grid':
					gridView.render().done(function() {
						//TODO: Do these class changes on the template. Possibly do better selectors.
						$body.addClass('grid');

						resultsContainerComponent.insert(gridView);
						addNewResults();

						//TODO: Figure out how to bind scroll event delegation instead of binding directly to #background
						$('#background').on('scroll', debounce(function(e) {
							checkScrollPagination(e);
						}, SCROLL_DEBOUNCE));
					});
					break;

				case 'feed':
					feedView.render().done(function() {
						$body.addClass('feed');

						resultsContainerComponent.insert(feedView);

						$list = $('#list');

						currentObjectContext = searchResults[explorerState.objectTypeShown];

						//Construct a details panel for each object of the current type and insert it into the list.
						_.forEach(currentObjectContext, function(resultObject) {
							var context, newPanel;

							context = objectContext[explorerState.objectTypeShown].details(resultObject);
							newPanel = nunjucks.render(objectTemplateMap[explorerState.objectTypeShown], context);
							$list.append(newPanel);
						});

						//Scale all embeddable objects and perform the initial sort.
						embedContent.loadEmbeddablesAndScale($('.object-details:not(.location)'), 'img');
						initializeSort($list);
					});
					break;

				default :
					renderState$renderResultsView();
					break;
			}
		}

		/**
		 * This adds a when filter to the search.
		 * It runs up to the following day at midnight.
		 * The goal is to provide a breadcrumb for new users to discover the advanced search features by
		 * having this already be present.
		 */
		function addInitialWhenFilter() {
			var currentDate, $filterName, $whenFilter;

			$filterName = $('#filter-name');
			$whenFilter = $('form.when');

			//To cover everything that happened today, have the filter's end date be the following day at midnight.
			//TODO: When we have dateTimePicker implemented, we can probably just use 'up to this very second'.
			currentDate = moment().startOf('day');
			currentDate.add(1, 'd');

			//Create a when filter by triggering a click event on its filter creation button.
			$('#filter-buttons').find('[data-type="when"]').trigger({
				type: 'click'
			});

			//Add a catchy name for the filter, and then trigger a change event so that the name is saved.
			//As the advanced search controls are still display:none, no events are normally fired.
			$filterName.find('input[name="name"]').val('Since the Beginning of Time').trigger({
				type: 'change'
			});

			//Look for estimated events, and set the end date to the one that was generated.
			$whenFilter.find('input[name="estimated"]').prop('checked', true);
			$whenFilter.find('input[type="date"][name="to"]').val(currentDate.format('YYYY-MM-DD'));

			explorerState.currentSort = 'datetime:desc';
		}

		/**
		 * Close the #left panel and empty #details of all DOM elements.
		 */
		function closeDetails() {
			$('#left').removeClass('expanded');
			$('#details').empty();
		}

		/**
		 * Close the drawer
		 */
		function closeDrawer() {
			var $drawer;

			//Hide the map
			$('#map').hide();

			$drawer = $('#drawer');

			//Set all grid items' margin-bottom to 1em, which is the default.
			$('.grid-item').css('margin-bottom', '1em');

			//Keep the map in the drawer, but remove all of the other details panels; then hide and empty the drawer.
			$drawer.children().not('#map').remove();
			$drawer.hide();
			$drawer.empty();
		}

		/**
		 * Add various controls back to the map if they aren't already present.
		 */
		function addMapControls() {
			if (!(map.controls.draw._map)) {
				map.object.addControl(map.controls.draw);
			}

			if (!(map.controls.layer._map)) {
				map.object.addControl(map.controls.layer);
			}
		}

		/**
		 * Remove various controls from the map if they aren't already gone.
		 */
		function removeMapControls() {
			if (map.controls.draw._map) {
				map.object.removeControl(map.controls.draw);
			}

			if (map.controls.layer._map) {
				map.object.removeControl(map.controls.layer);
			}
		}

		/**
		 * Renders the details for a selected object.
		 * @param {object} $target The jQuery-selected DOM element where the rendered detail panels will be inserted.
		 * @private
		 */
		function _renderObjectDetails($target) {
			var detailsContent, detailsObject, newPanel, selectedObjectType;

			selectedObjectType = explorerState.selectedObjectType;
			detailsObject = searchResults[selectedObjectType][explorerState.selectedObjectId];

			//If rendering the details for an event:
			if (selectedObjectType === 'events') {
				//Add details panels in the order specified in DETAILS_ORDERING
				_.forEach(DETAILS_ORDERING, function(objectType) {
					var newPanel;

					//Special case for adding a location
					if (objectType === 'locations') {
						//Don't add the location if currently in map view, as the map makes it redundant
						//(and we don't support multiple maps right now, either).
						if (explorerState.currentViewState !== 'map') {
							//Render a location details panel and append it to the drawer/details window.
							newPanel = nunjucks.render(objectTemplateMap.locations, objectContext.locations.details(detailsObject.location, true));
							$target.append(newPanel);
						}
					}
					//If adding the event details panel, render it and append it to the drawer/details window.
					else if (objectType === 'events') {
						newPanel = nunjucks.render(objectTemplateMap[selectedObjectType], objectContext[selectedObjectType].details(detailsObject));
						$target.append(newPanel);
					}
					//If adding any other type of details panel:
					else {
						//Iterate through each of that object type and add a new panel of that type to the drawer/details window.
						_.forEach(detailsObject[objectType], function(singleObject) {
							newPanel = nunjucks.render(objectTemplateMap[objectType], objectContext[objectType].details(singleObject, true));
							$target.append(newPanel);
						});
					}
				});

				//If not in map view, add the map to $map-container (if no location, this won't occur),
				// add a marker for the selected object, and remove the unnecessary map controls.
				if (explorerState.currentViewState !== 'map') {
					$('#map-container').html(map.element);
					addMapMarkers(detailsObject);
					removeMapControls();
				}
			}
			//If rendering the details for something other than an event:
			else {
				//Render the details panel for that object type and add it to the drawer/details window.
				detailsContent = nunjucks.render(objectTemplateMap[selectedObjectType], objectContext[selectedObjectType].details(detailsObject));
				$target.html(detailsContent);

				//Special cases for locations and places.
				if (selectedObjectType === 'locations' || selectedObjectType === 'places') {
					//If rendering a place, also render a location panel for the place's location and add it to the drawer/details window.
					//TODO: When places have a list of locations, render a bounding box instead of a single marker.
					if (selectedObjectType === 'places' && explorerState.currentViewState !== 'map') {
						newPanel = nunjucks.render(objectTemplateMap.locations, objectContext.locations.details(detailsObject.location));
						$target.append(newPanel);
					}

					//If not in map view, add the map to $map-container (if no location, this won't occur),
					// add a marker for the selected object, and remove the unnecessary map controls.
					if (explorerState.currentViewState !== 'map') {
						$('#map-container').html(map.element);
						addMapMarkers(detailsObject);
						removeMapControls();
					}
				}
			}

			//Re-scale any embeddable content that may have been rendered.
			embedContent.loadEmbeddablesAndScale($('.object-details:not(.location)'), 'img');
		}

		/**
		 * Opens the details window
		 */
		function openDetails() {
			var $details = $('#details');

			//Close the details window to remove any items that may currently be rendered.
			closeDetails();

			$('#details-scroll').removeClass('hidden');

			$details.css('display', 'flex');

			//Open the details window and render the details panel(s) for the selected object.
			$('#left').addClass('expanded');
			_renderObjectDetails($details);
		}

		/**
		 * Opens the drawer
		 */
		function openDrawer() {
			var embeddablesLoaded, $drawer;

			//We want to wait until everything has been loaded before showing and scaling the drawer.
			//embeddablesLoaded will be filled with promises that are fulfilled when the associated content
			//(image, iframe, video, etc.) has been loaded and possibly re-scaled.
			embeddablesLoaded = [];
			$drawer = $('#drawer');

			//Close the drawer to remove any items that may currently be rendered.
			closeDrawer();

			//Make the drawer displayed so that items can scale on their own, but keep it hidden so that rendering
			//objects don't flash on the screen.
			$drawer.css('display', 'flex');
			$drawer.css('visibility', 'hidden');

			//Render the object's detail panels in the drawer.
			_renderObjectDetails($drawer);

			//Scale the embeddable content, and pass the function the embeddablesLoaded array so that the function
			//will insert any promises into it.
			embedContent.loadEmbeddablesAndScale($drawer, '.object-details:not(.location) img', embeddablesLoaded);

			//Wait for all of the embeddables to finish loading and rescaling, then render the drawer and make it visible.
			$.when.apply($, embeddablesLoaded).done(function() {
				renderDrawer();
				$drawer.css('visibility', 'initial');
			});
		}

		/**
		 * Calculates the height of the drawer as well as the margin-bottom of the item being selected.
		 * The drawer sits in an absolutely positioned container, and is inserted below a selected item
		 * by giving the drawer a margin-top equal to the item's position in its containing div plus
		 * the item's height plus the item's vertical margins.
		 */
		function renderDrawer() {
			var heightDistance, item, itemHeight, itemPosition, itemVerticalMargins, $drawer;

			$drawer = $('#drawer');

			//Get the item being selected.
			item = $('.grid-item.active');

			//Reset the item's and the drawer's margins to their default values.
			item.css('margin-bottom', '1em');
			$drawer.css('margin-top', 0);

			//Get the item's position and height.
			itemPosition = item.position();
			itemHeight = item.height();

			//Get the item's vertical margins.
			itemVerticalMargins = parseInt(item.css('margin-top').replace('px', '')) + parseInt(item.css('margin-bottom').replace('px', ''));

			//Give the item a margin-bottom of the drawer's height plus the item's vertical margins.
			item.css('margin-bottom', $drawer.height() + itemVerticalMargins);

			//The drawer's height from the top of the containing div is the item's top plus the item's height plus the item's vertical margins.
			heightDistance = itemPosition.top + itemHeight + itemVerticalMargins;

			//Set the drawer's margin-top to the calculated height.
			$drawer.css('margin-top', heightDistance + 'px');
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

		/**
		 * Handles some of the transition from Results view to Grid view when an object type is selected in Results view.
		 */
		function initializeFacet() {
			//De-select all of the view selectors and then select the grid view selector.
			$('.view-selector').removeClass('active');
			$('[data-selector="grid"]').addClass('active');

			//Set the current view state to Grid view and render it.
			explorerState.currentViewState = 'grid';
			renderState();
			$('.facet').html(explorerState.objectTypeShown !== 'events' ? explorerState.objectTypeShown : 'history');
		}

		/**
		 * Highlights an object that has been selected, usually by rendering its details.
		 * @param {object} $this The object that has being selected.
		 * @param {string} selectionType Where the details will be inserted; either 'drawer' or 'details'.
		 */
		function selectObject($this, selectionType) {
			var dataObjectId, objectId, objectType;

			//Get the objectId of the selected object and split it into its objectType and ID components.
			// (e.g. 'events.8943f9129347' -> 'events', '8943f9129347')
			dataObjectId = $this.attr('data-object-id').split('.');
			objectType = dataObjectId[0];
			objectId = dataObjectId[1];

			//Save the type to the global state.
			explorerState.selectedObjectType = objectType;

			//If the object is currently selected, then de-select it.
			if ($this.hasClass('active')) {
				//Set the global object ID to null since we're de-selecting the active object.
				explorerState.selectedObjectId = null;
				$('.grid-item, .list-item').removeClass('active');

				//If this is targeting the grid view drawer, then close the drawer.
				if (selectionType === 'drawer') {
					closeDrawer();
				}
				//If this is targeting the map or list view details window:
				else if (selectionType === 'details') {
					//Hide the #details-scroll element.  In map view, this is all that needs to be hidden.
					$('#details-scroll').addClass('hidden');

					//If in map view, then remove the contents of #details and trigger a map click.
					//The map click will de-spiderfy any spiderfied clusters.
					if (explorerState.currentViewState === 'map') {
						$('#details').empty();
						$(map.object._container).trigger({
							type: 'click'
						});
					}
					//Otherwise, just close the details window.
					else {
						closeDetails();
					}
				}

				//Reset the marker colors.
				setMarkerColors();
			}
			//If the object is not selected, then select it.
			else {
				//Set the object ID to the global state
				explorerState.selectedObjectId = objectId;
				$('.grid-item, .list-item').removeClass('active');

				$this.addClass('active');

				//If this is targeting the grid view drawer, then open the drawer (that function also renders the drawer contents).
				if (selectionType === 'drawer') {
					openDrawer();
				}
				//If this is targeting the map or list view details window, then open the window
				//(that function also render the window contents).
				else if (selectionType === 'details') {
					openDetails();
				}

				//Set the marker colors; pass the objectId so that the associated marker is colored orange.
				//Also resize the map.
				setMarkerColors(objectId);
				map.resize();

				//Scroll down to the item that was selected.
				//The exception is list view, as this was found to be unpleasant, but could be reversed if further
				//testing determines it's not so unpleasant.
				//Map view should keep this, however, as you could click on a marker for an item not currently in view.
				if (explorerState.currentViewState !== 'list') {
					$this[0].scrollIntoView(true);
				}
			}
		}

		function checkScrollPagination(e) {
			var $lastChild, $list, $target = $(e.target);

			$list = $('#list');

			//Automatically get the next page of results when you reach the last item.
			if (explorerState.currentResultCount < explorerState.totalResultCount) {
				$lastChild = $list.children().last();

				if ($target.scrollTop() + $target.height() > $lastChild.position().top + $lastChild.height() - SCROLL_LOAD_LIMIT) {
					$('#search-bar').trigger({
						type: 'explorer:more',
						more: explorerState.moreLink
					});
				}
			}
		}

		function prepopulateFacet() {
			var objectTypeCount, searchParams;

			objectTypeCount = Object.keys(searchResults[explorerState.objectTypeShown]).length;

			//TODO: Remove this ugly hack when API works better
			if (objectTypeCount < SCROLL_MIN_COUNT && explorerState.currentResultCount < explorerState.totalResultCount) {
				searchParams = {
					filters: explorerState.currentSearch,
					offset: explorerState.currentResultCount,
					sort_field: explorerState.currentSort.split(':')[0],
					sort_desc: explorerState.currentSort.split(':')[1] === 'desc'
				};

				$('#search-bar').trigger({
					type: 'explorer:sort',
					paramData: searchParams
				});
			}
		}

		//When explorer is loaded, get the Mapbox token.
		$.ajax({
			url: '/tokens/mapbox',
			type: 'GET',
			dataType: 'json',
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			}
		}).done(function(data) {
			var searchParams;

			//When the Mapbox token has been retrieved, create a new Cartano map with it.
			map = new cartano.Map(data.MAPBOX_USER_NAME, {
				accessToken: data.MAPBOX_ACCESS_TOKEN,

				className: 'flex-grow',

				zoomControl: true,
				drawControl: true,
				layerControl: true
			});

			//On mobile, the map should not have most of the controls that desktop has, so remove them.
			if (isMobile) {
				removeMapControls();
			}

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

			// TODO: Remove everything below and move to a load function
			//We want to leave a breadcrumb for the users to discover the filters.
			//Generate a when filter that runs up until tomorrow at midnight (once datetimepicker is implemented, merely
			//up until now).
			//Hopefully they will see the when filter, click on it to figure out what it is, and discover all of the filters.
			addInitialWhenFilter();

			//On mobile, the view and sort selectors are in the menu drawer.  On desktop, they are in the header.
			//Both will be rendered, and we then disable the one that will not be used.
			//The disabled class will give that one display: none !important.
			if (!isMobile) {
				$('#menu .view-bar').addClass('disabled');
				$('#menu .sort-bar').addClass('disabled');
			}
			else {
				$('header > nav .view-bar').addClass('disabled');
				$('header > .sort-bar').addClass('disabled');
			}

			searchParams = {
				offset: explorerState.currentResultCount,
				sort_field: explorerState.currentSort.split(':')[0],
				sort_order: explorerState.currentSort.split(':')[1]
			};

			//Perform a query.  By default, it will be with just the initial when filter that was created a few lines back.
			//In the future, we may have loaded the user's last search, or the search that they selected from their saved searches.
			$('#query-form').trigger({
				type: 'submit',
				paramData: searchParams
			});
		});

		//Bind event listeners that are used in multiple views to document.
		$(document).on('submit', '#query-form', function() {
			var $main;

			$main = $('main');

			$main.empty();
			$main.html(nunjucks.render('explorer/components/waiting.html'));
		}).on('search:results', function(e) {
			//When a search is completed:
			explorerState.moreLink = e.results.next;
			explorerState.totalResultCount = e.results.count;
			explorerState.currentSearch = e.searchParams;

			//If this was a new search, as opposed to pagination of an existing search, clear the old search results.
			if (e.clearData) {
				clearSearchResults();
				explorerState.currentResultCount = e.results.results.length;
			}
			else {
				explorerState.currentResultCount += e.results.results.length;
			}

			//Add the new results to the global set of search results.
			addEventsToSearchResults(e.results.results);

			//If this was a new search, then go to Results view and render it.
			if (e.clearData) {
				explorerState.currentViewState = 'results';
				renderState();
			}
		}).on('click', '.view-selector:not(.active)', function() {
			//When the user clicks a view selector for a view other than the one currently being displayed:
			var activeSelector, $this = $(this);

			//If the user clicked on the results view, then just set the current view to that and render it.
			if ($this.attr('data-selector') === 'results') {
				explorerState.currentViewState = 'results';
				renderState();
			}
			//If the user clicked something other than results view:
			else {
				//The active selector is either the active grid item in grid view or the active list item in list or map views.
				if (explorerState.currentViewState === 'grid') {
					activeSelector = $('.grid-item.active');
				}
				else {
					activeSelector = $('.list-item.active');
				}

				//Get the active object's ID.
				explorerState.selectedObjectId = activeSelector.attr('data-object-id');

				//Make all the view selectors inactive and make the selected view selector active.
				$('.view-selector').removeClass('active');
				$this.addClass('active');

				//Set the current view to the one that was selected and render that view.
				explorerState.currentViewState = $this.attr('data-selector');
				renderState();

				//Since feed view doesn't have any clickable object yet, when switching to feed view with something active,
				//just scroll down to that item.
				//Othwerise, trigger a click on the active object's new grid- or list-item, which will open up its details in the new view.
				if (explorerState.currentViewState === 'feed') {
					if (explorerState.selectedObjectId) {
						$('[data-object-id="' + explorerState.selectedObjectId + '"]')[0].scrollIntoView();
					}
				}
				else {
					$('[data-object-id="' + explorerState.selectedObjectId + '"]').trigger('click');
				}
			}
		}).on('click', '.view-selector.active', function() {
			//When the user clicks on a view selector for the current view, this is seen as a 'de-activation' of that
			//view and sends them back to the Results view.
			explorerState.currentViewState = 'results';
			renderState();
		}).on('click', '.sort-selector', function(e) {
			//When the user clicks on a sort selector, sort on that field.
			var activeObjectId, searchParams, sortAttr, $activeObject, $list, $sortArrow, $sortItems, $this = $(this);

			if (explorerState.objectTypeShown == 'events' && explorerState.currentResultCount < explorerState.totalResultCount) {
				searchParams = {
					filters: explorerState.currentSearch,
					offset: explorerState.currentResultCount,
					sort_field: explorerState.currentSort.split(':')[0],
					sort_desc: explorerState.currentSort.split(':')[1] === 'desc'
				};

				$('#search-bar').trigger({
					type: 'explorer:sort',
					paramData: searchParams
				});
			}

			$list = $('#list');

			//In grid view, de-select an active object because, with it open, things get messy.
			//Save the ID of the active object if there is one so that it can be re-opened later.
			if (explorerState.currentViewState === 'grid') {
				$activeObject = $('.grid-item.active');

				if ($activeObject.length > 0) {
					activeObjectId = $activeObject.attr('data-object-id');
					selectObject($activeObject, 'drawer');
				}
			}

			//Save references to DOM elements.
			$sortItems = $('.sort-selector');
			//$sortItems.removeClass('active');
			$sortArrow = $this.find('.fa');

			//sortAttr is [sortType, asc/desc]
			sortAttr = $this.attr('data-sort').split(':');

			//Iterate through each sort selector and reset it to the default state, which is no asc/desc arrow
			//and an asc/desc status of 'none'.
			_.forEach($sortItems, function(sortItem) {
				var sortAttr, $sortArrow, $sortItem;

				//Remove the asc/desc arrows from each sort selector.
				$sortItem = $(sortItem);
				$sortArrow = $sortItem.find('.sort-arrow');
				$sortArrow.removeClass('fa-caret-down').removeClass('fa-caret-up');

				//Set the asc/desc of each sort type to 'none'.
				sortAttr = $sortItem.attr('data-sort').split(':');
				sortAttr[1] = 'none';
				$sortItem.attr('data-sort', sortAttr[0] + ':' + sortAttr[1]);
			});

			//Make the selected sort active.
			//$this.addClass('active');

			//If the new sort type is the same as the previous sort type, then swap to the opposite asc/desc of what was in use before.
			if (explorerState.currentSort.split(':')[0] === sortAttr[0]) {
				//If the old asc/desc was desc, then switch to asc.
				if (sortAttr[1] === 'desc') {
					$sortArrow.addClass('fa-caret-up');
					sortAttr[1] = 'asc';
				}
				//If the old asc/desc was asc, then switch to desc.
				else {
					$sortArrow.addClass('fa-caret-down');
					sortAttr[1] = 'desc';
				}
			}
			//If the new sort type is different from the previous sort type:
			else {
				//Usually, we want the first sort of a field to be asc, so that things are in alphabetical order starting with 'A'.
				//With datetimes, though, we're assuming the user wants the most recent objects first, which is desc order.
				if ($this.attr('data-sort').split(':')[0] === 'datetime') {
					$sortArrow.addClass('fa-caret-down');
					sortAttr[1] = 'desc';
				}
				//In all other cases, make asc be the default asc/desc.
				else {
					$sortArrow.addClass('fa-caret-up');
					sortAttr[1] = 'asc';
				}
			}

			//Save the new sort to the global context.
			$this.attr('data-sort', sortAttr[0] + ':' + sortAttr[1]);
			explorerState.currentSort = sortAttr[0] + ':' + sortAttr[1];

			//Tell MixItUp to perform the sort.
			$list.mixItUp('sort', explorerState.currentSort);

			//Re-open the selected object, if there was one selected.
			if (explorerState.currentViewState === 'grid') {
				$(document).one('mixEnd', function() {
					$('[data-object-id="' + activeObjectId + '"]').trigger('click');
					$(document).off('mixEnd');
				});
			}
		}).on('marker:click', function(e) {
			//When the user clicks on a marker or markercluster:
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
			//If the user clicked on a single marker, then call selectObject on the associated object to either select it
			//if it is open or de-select it if it isn't open.
			else {
				selectObject($('[data-object-id="' + explorerState.objectTypeShown + '.' + marker.options.objectId + '"]'), 'details');
			}
		}).on('click', '.control[data-type="where"]', function() {
			//If the user clicks on the where filter button when not in map view, then go to map view for Events and trigger another
			//click on it so that the draw controls are highlighted in orange.  This hopefully will clue the user to use
			//the draw controls to create where filters.
			//TODO: Instead of going to map view automatically, render some text telling them to go to map view
			//to create where filters and have a link that they can click on to do so.
			if (explorerState.currentViewState !== 'map') {
				explorerState.currentViewState = 'map';
				explorerState.objectTypeShown = 'events';
				renderState();
				$(this).trigger('click');
				$('#expand-details').trigger('click');
			}
		}).on('click', '#map-container', function() {
			//If the user clicks on the location details map:
			var activeSelector;

			//If not in mobile and not on the map, then save the objectId of a potentially selected object,
			//go to map view, and trigger a click on that potentially active object.
			if (!isMobile && explorerState.currentViewState !== 'map') {
				if (explorerState.currentViewState === 'list') {
					activeSelector = $('.list-item.active');
				}
				else {
					activeSelector = $('.grid-item.active');
				}

				explorerState.selectedObjectId = activeSelector.attr('data-object-id');

				//Make all the view buttons inactive, make the selected button active, and get aliases for items that will be referenced.
				$('.view-selector').removeClass('active');
				$('.view-selector[data-selector="map"]').addClass('active');

				explorerState.currentViewState = 'map';
				renderState();

				$('[data-object-id="' + explorerState.selectedObjectId + '"]').trigger('click');
			}
		}).on('click', '#home, #back-to-results', function(e)
		{
			//If not in the Results view, when the user clicks on the home button, they're taken back to the Results view.
			if (explorerState.currentViewState !== 'results') {
				explorerState.currentViewState = 'results';
				renderState();

				return false;
			}
		}).on('click', '.action-bar .share-action', function(e) {
			$(e.target).parents('.action-bar-container').find('.share-menu').toggleClass('hidden');

			if (explorerState.currentViewState === 'grid' && $('.grid-item.active').length > 0) {
				renderDrawer();
			}
		}).on('click', '.action-bar .action-action', function(e) {
			$(e.target).parents('.action-bar-container').find('.action-menu').toggleClass('hidden');

			if (explorerState.currentViewState === 'grid' && $('.grid-item.active').length > 0) {
				renderDrawer();
			}
		}).on('click', '.action-bar .location-action', function(e) {
			$(e.target).parents('.action-bar-container').find('.location-menu').toggleClass('hidden');

			if (explorerState.currentViewState === 'grid' && $('.grid-item.active').length > 0) {
				renderDrawer();
			}
		});

		//Bind Results view-specific events.
		resultsView.on('click', '.grid-item', function() {
			//When the user clicks on the item for an object, save the objectId of that object,
			//go to grid view for that object type and then select that object.
			var gridItem, objectId, $this = $(this);

			objectId = $this.attr('data-object-id');
			explorerState.objectTypeShown = objectId.split('.')[0];

			prepopulateFacet();
			initializeFacet();

			gridItem = $('[data-object-id="' + objectId + '"]');
			selectObject(gridItem, 'drawer');
		}).on('click', '.more-select, .type-header', function() {
			//When the user clicks on the more button or header for an object type, just go to grid view for that object type.
			var $this = $(this);

			explorerState.objectTypeShown = $this.attr('data-result-type');

			prepopulateFacet();
			initializeFacet();
		});

		//Bind Grid view-specific events
		gridView.on('click', '.grid-item', function() {
			//When the user clicks on an object, call selectObject on it.
			var $this = $(this);

			selectObject($this, 'drawer');
		});

		//Bind List view-specific events.
		listView.on('click', '.list-item', function() {
			//When the user clicks on an object, call selectObject on it.
			var $this = $(this);

			selectObject($this, 'details');
		});

		//Bind Map view-specific events.
		mapView.on('click', '.list-item', function() {
			//When the user clicks on an object, call selectObject on it.
			var $this = $(this);

			selectObject($this, 'details');
		}).on('map:zoom', function() {
			//When the user zooms the map, de-select any active objects.
			var $active;

			$active = $('.list-item.active');

			if ($active.length > 0) {
				selectObject($active, 'details');
			}
		}).on('click', '#expand-details', function() {
			//When the user clicks on #expand-details, either close the detail panel and list if they were open
			//(triggering a map click to deselect the active object in the process), or show the list again.
			//TODO: Abstract to call show and hide details.
			var $icon, $this = $(this);

			$icon = $this.find('i');

			//Hiding the detail panel and list
			if ($icon.hasClass('fa-caret-left')) {
				$('#left').removeClass('expanded');
				$icon.removeClass('fa-caret-left').addClass('fa-caret-right');
				$(map.object._container).trigger({
					type: 'click'
				});
			}
			//Showing the detail panel and list
			else {
				$('#left').addClass('expanded');
				$icon.removeClass('fa-caret-right').addClass('fa-caret-left');
			}
		});

		//If the user resizes the window:
		$(window).resize(function() {
			//If in grid view and the drawer is open, re-render the drawer to fit the new window size.
			if (explorerState.currentViewState === 'grid' && $('.grid-item.active').length > 0) {
				renderDrawer();
			}
		});
	});


