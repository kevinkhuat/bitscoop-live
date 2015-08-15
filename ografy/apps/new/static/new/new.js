//require(['jquery', 'jutsu'], function($, jutsu) {
//	$(document).ready(function() {
//		window.$a = $('#a');
//		window.$b = $('#b');
//		window.$box = $('<div>').addClass('foo bar');
//
//		window.a = jutsu.viewstate.Component('#a');
//		window.v = jutsu.viewstate.View($box);
//
//		window.logger = function(e) {
//			console.log(e);
//		};
//	});
//});


require(['jquery'], function($) {
	// When certain "important" elements are clicked, fire the "autoblur" event on detail panes.
	// Individual autoblur compatible elements handle the event in certain ways, e.g. the list pane shrinks to an icon and the detail pane scoots away.

	$(document).on('click tap', '.autoblur', function(e) {
		var $filtered, $set;

		$set = $(e.target).parents('.autohide');
		$filtered = $('.autohide').not($set);

		$filtered.trigger('autohide');
	});

	/*
	$('#panel').on('autohide', function(e) {
		var $this = $(this);

		e.stopPropagation();

		$this.children().not(':first-child').hide();

		$('#panel-search').addClass('hidden');
	});

	$('#panel-filter').on('autohide', function(e) {
		e.stopPropagation();

		$('#filter-toggle').removeClass('icon-triangle-up').addClass('icon-triangle-down');
		$(this).hide();
	});
	*/

	$('#panel-search div.input-group:first').on('click', function(e) {
		if (e.target === this) {
			$('#panel-search').toggleClass('hidden');
		}
	});

	//
	//$(document).on('click', '.filter > .close', function(e) {
	//	var $this = $(this);
	//
	//	$this.closest('.filter').remove();
	//});

	//$('#search-form').on('submit', function(e) {
	//	e.preventDefault();
	//
	//	// TODO: Implement search.
	//	console.log('search submit!');
	//});

	$('#filter-toggle').on('click', function(e) {
		var $this = $(this);

		e.stopPropagation();

		if ($this.is('.icon-triangle-up')) {
			$this.removeClass('icon-triangle-up').addClass('icon-triangle-down');
			$('#panel-filter').hide();
		}
		else {
			$this.removeClass('icon-triangle-down').addClass('icon-triangle-up');
			$('#panel-filter').show();
		}
	});
});

require.config({
	paths: {
		location: 'static/core/js/search/location',
		scheduleMapper: 'static/core/js/search/scheduleMapper',
		search: 'static/new/search'
	}
});

require(['cartano', 'jquery', 'nunjucks', 'search', 'jquery-cookie'], function(cartano, $, nunjucks, search) {
	var searchResults, searchDSL, paramDSL, stringDSL, searchCallback, markerCallback, mainMap, callData, clearResults, getLeafletId, renderDetailPanel, highlightEvent, deselectEvents;
	var eventCache = {};

	//Get the mapbox API key
	$.ajax({
		url: '/app/keys/mapbox',
		type: 'GET',
		dataType: 'json',
		headers: {
			'X-CSRFToken': $.cookie('csrftoken')
		}
	}).done(function(data) {
		//Create an instance of a Mapbox map using Cartano
		mainMap = new cartano.Map('liambroza.hl4bi8d0', {
			accessToken: data.OGRAFY_MAPBOX_ACCESS_TOKEN,

			className: 'grow',

			zoomControl: true,
			drawControl: true,
			layerControl: true
		});

		$('#background').append(mainMap.element);
		mainMap.resize();
		$.when(search.init(window.location.hash, '#panel', mainMap)).done(function() {
			searchCallback();
		});

		//Highlight an event in the list panel when you click on its associated marker (also change the icon
		//to a highlighted image)
		mainMap.markers.on('click', function(e) {
			var layer = e.layer;
			var eventId = layer.options['event-id'];

			highlightEvent(eventId);
		});

		//Deselect all events when you click on a marker cluster
		mainMap.markers.on('clusterclick', function(e) {
			deselectEvents();
			$('.list-element').removeClass('active');
		});

		//Deselect all events when you click on the map (if you clicked on a marker, that will fire after this occurs)
		mainMap.object.on('click', function() {
			deselectEvents();
			$('.list-element').removeClass('active');
		});
	});


	//Clear saved data from the cache, list panel, and map
	clearResults = function() {
		eventCache = {};
		mainMap.clearData();
		$('#panel-list').html('');
	};

	//Create a marker from the coordinates provided on the data input
	markerCallback = function(data, index) {
		var coordinates = data._source.location.geolocation;
		return L.marker([coordinates[1], coordinates[0]], { 'event-id': data._source._id });
	};

	//Return the leaflet ID of a marker if its event ID matches the ID of the input result
	getLeafletId = function(marker, result) {
		if (result._id === marker.options['event-id']) {
			return marker._leaflet_id;
		}
	};

	//Un-highlight all events in the list and hide the detail panel
	deselectEvents = function() {
		$('.list-element').removeClass('active');
		$('#panel-detail').html('').addClass('hidden');
	};


	//The steps for highlighting an event that has been selected.
	highlightEvent = function(eventId) {
		//Un-highlight all of the events in the list, then highlight the one that was selected.
		$('.list-element').removeClass('active');
		$('.list-element[data-event-id=' + eventId + ']').addClass('active');

		//Populate the detail panel.
		renderDetailPanel(eventId);

		//Iterate through each marker.  If it's the marker that corresponds to the select event,
		//Center the map on that marker, spiderfy the parent clustergroup if the marker is in a clustergroup,
		//Set all the non-selected markers to the default icon, and change the icon of the selected marker to the
		//"selected" image.
		mainMap.eachMarker(function(marker) {
			if (marker.options['event-id'] === eventId) {
				mainMap.setCenter(marker._latlng);
				if (marker.__parent._childCount > 1) {
					marker.__parent.spiderfy();
				}
				_.forEach(marker.__parent._markers, function(childMarker) {
					childMarker._icon.src = 'https://api.tiles.mapbox.com/mapbox.js/v2.2.1/images/marker-icon.png';
				});
				marker._icon.src = '/static/assets/img/marker-red.png';
			}
		});
	};

	//Render the detail panel based on the event type and remove the 'hidden' class so it's rendered and visible.
	renderDetailPanel = function(eventId) {
		var event = eventCache[eventId];
		var datetime = new Date(event.datetime);

		var panelDetail = nunjucks.render('templates/detail.html', {
			event: event,
			datetime: datetime.toDateString() + ' ' + datetime.toLocaleTimeString()
		});

		$('#panel-detail').html(panelDetail).removeClass('hidden');
	};

	//The callback for a search.
	searchCallback = function() {
		//Get the DSL query for the current set of filters and query text.
		searchDSL = search.getQuery();

		//Parameterize the DSL query and put it in the URL hash
		paramDSL = $.param(searchDSL);
		window.location.hash = paramDSL;

		//Stringify the DSL query
		stringDSL = JSON.stringify(searchDSL);

		//Construct the callData dictionary
		callData = {
			dsl: stringDSL
		};

		//Call the Tornado endpoint for ElasticSearch.
		$.ajax({
			url: 'https://p.ografy.io/search',
			type: 'GET',
			dataType: 'text',
			data: callData,
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			xhrFields: {
				withCredentials: true
			}
		}).done(function(data, xhr, response) {
			//Remove the results of the previous search
			clearResults();

			//Save the search results
			searchResults = JSON.parse(data).hits.hits;

			//Add all of the search results to the map
			mainMap.addData(searchResults, markerCallback);

			//Iterate through each event
			_.forEach(searchResults, function(result) {
				var datetime, date, contacts_list, hours, minutes, ampm;
				var listElement, leafletId;
				var $panelList = $('#panel-list');

				//Get the actual data from the search result; at this point, 'result' contains ES-specific metadata,
				//while the actual data we're interested in is at result._source
				result = result._source;

				date = new Date(result.datetime);
				contacts_list = result.contacts_list;

				//Turn the datetime into a form we want to use (built-in date formats have unnecessary data or
				//are too verbose)
				datetime = search.stringifyDate(date);

				//Cache the result
				eventCache[result._id] = result;

				//Save the leaflet ID corresponding to the event's marker
				mainMap.eachMarker(function(marker) {
					var match = getLeafletId(marker, result);
					if (match !== undefined) {
						leafletId = match;
					}
				});

				//Render the list element for this event
				listElement = nunjucks.render('templates/list_element.html', {
					id: result._id,
					leaflet_id: leafletId,
					provider_name: result.provider_name,
					event_type: result.event_type,
					datetime: datetime
				});

				//Insert the event into the list.
				//If it's the first event to be inserted, just set #panel-list to it; otherwise append each
				//successive event to the last one present.
				if ($panelList.children().length === 0) {
					$panelList.html(listElement);
				}
				else {
					$panelList.last().append(listElement);
				}
			});
		}).fail(function(data, xhr, response) {
			console.log('ES search failed');
		});
	};

	//When the search form is submitted, prevent the submission from bubbling up any further and call searchCallback
	//to perform the search.
	$('#search-form').on('submit', function(e) {
		e.preventDefault();

		searchCallback();
	});

	//When an event in the list is clicked, call highlightEvent
	$('#panel-list').on('click', '.list-element', function(e) {
		var $this = $(e.target);
		var $listElement = $this.closest('.list-element');
		var eventId = $listElement.data('event-id');

		highlightEvent(eventId);
	});
});

//require(['scheduleMapper'], function(scheduleMapper) {
//	var user_id = 1;
//	scheduleMapper.schedule(10000000, user_id);
//});
