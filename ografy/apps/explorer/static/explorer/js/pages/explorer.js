define(['cartano', 'jquery', 'leaflet', 'lodash', 'nunjucks', 'scheduleMapper', 'search', 'autoblur', 'jquery-cookie', 'templates', 'leaflet-awesome-markers'], function(cartano, $, leaflet, _, nunjucks, scheduleMapper, search) {
	var map;
	var eventCache = {};

	var content_type_translation = {
		game: 'gamepad',
		text: 'comment',
		video: 'video-camera'
	};


	function getContentFontIcon(content) {
		var content_type;

		if (content.length === 0) {
			return 'map-marker';
		}

		// TODO: Make this a little more robust, how do we determine the content type if there is more than one.
		content_type = content[0].content_type;

		return content_type_translation[content_type] || 'map-marker';
	}

	/**
	 * Un-highlight all events in the list and hide the detail panel.
	 *
	 */
	function deselectEvents() {
		$('.list-element').removeClass('active');
		$('#detail').empty();
	}

	/**
	 * Return the leaflet ID of a marker if its event ID matches the ID of the input result.
	 *
	 * @param marker A mapbox marker
	 * @param id An ID of an event returned from ElasticSearch
	 */
	function getLeafletId(marker, id) {
		if (id === marker.options['event-id']) {
			return marker._leaflet_id;
		}
	}

	/**
	 * The steps for highlighting an event that has been selected.
	 *
	 * @param eventId The ID of an event to be highlighted.
	 */
	function highlightEvent(eventId) {
		var event;

		event = eventCache[eventId];

		//Un-highlight all of the events in the list, then highlight the one that was selected.
		$('.list-element').removeClass('active');
		$('.list-element[data-event-id=' + eventId + ']').addClass('active');

		//Populate the detail panel.
		renderDetailPanel(event);

		//Iterate through each marker.  If it's the marker that corresponds to the select event,
		//Center the map on that marker, spiderfy the parent clustergroup if the marker is in a clustergroup,
		//Set all the non-selected markers to the default icon, and change the icon of the selected marker to the
		//"selected" image.
		map.eachMarker(function(marker) {
			if (marker.options['event-id'] === eventId) {
				map.setCenter(marker._latlng);

				if (marker.__parent._childCount > 1) {
					marker.__parent.spiderfy();
				}

				_.forEach(marker.__parent._markers, function(childMarker) {
					$(childMarker._icon).removeClass('awesome-marker-icon-orange').addClass('awesome-marker-icon-blue');
				});

				$(marker._icon).removeClass('awesome-marker-icon-blue').addClass('awesome-marker-icon-orange');
			}
		});
	}

	/**
	 * Render the detail panel based on the event type.
	 *
	 * @param event An event whose details are to be rendered
	 */
	function renderDetailPanel(event) {
		var datetime = new Date(event.datetime);

		var panelDetail = nunjucks.render('explorer/detail.html', {
			event: event,
			datetime: datetime.toDateString() + ' ' + datetime.toLocaleTimeString()
		});

		$('#detail').html(panelDetail);
	}

	/**
	 * This converts datetimes into a stringified form that we like.  All of the built-in functions are too verbose
	 * or don't look the way we want.
	 *
	 * @param datetime A datetime object
	 */
	function stringifyDatetime(datetime) {
		var hours, minutes, ampm, return_datetime;

		hours = datetime.getHours()%12;
		hours = hours ? hours : 12;
		minutes = datetime.getMinutes();
		minutes = minutes < 10 ? '0' + minutes : minutes;
		ampm = datetime.getHours() >= 12 ? 'PM' : 'AM';

		return_datetime = datetime.toLocaleDateString() + ' ' + hours + ':' + minutes + ' ' + ampm;

		return return_datetime;
	}


	$.ajax({
		url: '/tokens/mapbox',
		type: 'GET',
		dataType: 'json',
		headers: {
			'X-CSRFToken': $.cookie('csrftoken')
		}
	}).done(function(data) {
		map = new cartano.Map('liambroza.hl4bi8d0', {
			accessToken: data.MAPBOX_ACCESS_TOKEN,

			className: 'flex-grow',

			zoomControl: true,
			drawControl: true,
			layerControl: true
		});

		$('#background').append(map.element);
		map.resize();

		//Deselect all events when you click on the map (if you clicked on a marker, that will fire after this occurs)
		map.object.on('click', function() {
			deselectEvents();
			$('.list-element').removeClass('active');
		});
	});

	$('#left').on('autoblur:hide', function(e) {
		e.stopPropagation();

		$(this).removeClass('expanded');
		$('#expand-details i').removeClass('fa-caret-left').addClass('fa-caret-right');
	});

	$('#search-bar').addClass('autoblur').on('autoblur:hide', function(e) {
		e.stopPropagation();

		search.shrink();
	});

	$(document).on('geofilter', function(e) {
		var filters, id, map;

		map = e.map;
		filters = e.filters;

		if (e.action === 'create') {

		}
		else if (e.action === 'update') {

		}
		else if (e.action === 'delete') {

		}
	});

	$(document).on('map:move', function(e) {
		var map;

		map = e.map;

		// Perhaps update the inherent geofilter.
	});

	$(document).on('map:zoom', function(e) {
		var map;

		map = e.map;

		//When the map zooms in or out, any spiderfied clustergroup de-spiderfies.  If a marker in a spiderfied
		//clustergroup was selected, it is now no longer visible, so deselect it.  If it wasn't in a spiderfied
		//clustergroup, then there is no problem, but I'm not sure how to handle this case, and if the user is
		//zooming, they're probably moving to look at different events anyway.
		deselectEvents();
		$('.list-element').removeClass('active');
		// Perhaps update the inherent geofilter.
	});

	$(document).on('marker:click', function(e) {
		var marker, eventId;

		marker = e.marker;

		if (e.clustered) {
			// You're clicking on a map cluster.

			if (e.action === 'zoom') {
				// You may update the inherent where filter (i.e. map bounds).
				// Or do other things associated with map zoom (like update the state if we still use it).
			}
			else if (e.action === 'spiderfy') {
				// Do anything you want when the marker "de-spiderfys" (handled automatically).
			}
		}
		else {
			// We're dealing with a single (unspiderfied) "event" click.
			//In this case, highlight the associated event.
			eventId = marker.options['event-id'];
			highlightEvent(eventId);

			$('#left').addClass('expanded');
			$('#expand-details i').removeClass('fa-caret-right').addClass('fa-caret-left');
		}
	});

	$('#expand-details').on('click', function(e) {
		var $icon, $this = $(this);

		$icon = $this.find('i');

		if ($icon.hasClass('fa-caret-left')) {
			$('#left').removeClass('expanded');
			$icon.removeClass('fa-caret-left').addClass('fa-caret-right');
		}
		else {
			$('#left').addClass('expanded');
			$icon.removeClass('fa-caret-right').addClass('fa-caret-left');
		}
	});

	$(document).on('search:results', function(e) {
		var coordinates, results, $list;

		$list = $('#list');

		//If this was a new search, it will indicate that the old results should be cleared by having clearData be set to True.
		//Searches for additional pages of results should have clearData set to False so that the current results
		//are left alone.
		//If we're clearing data, then call clearData on the cartano map, remove the contents of the list, and empty the event cache.
		if (e.clearData) {
			map.clearData();
			$list.empty();
			eventCache = {};
		}

		results = e.results;

		$('#detail').empty();

		if (results.length > 0) {
			$('#left').addClass('expanded');
			$('#expand-details').removeClass('hidden')
				.find('i').removeClass('fa-caret-right').addClass('fa-caret-left');
		}
		else {
			$('#left').removeClass('expanded');
			$('#expand-details').addClass('hidden');
		}

		//Add all of the search results to the map
		map.addData(results, function(data) {
			var coordinates, icon;

			coordinates = data.result.location.geolocation;
			icon = leaflet.AwesomeMarkers.icon({
				icon: 'circle',
				prefix: 'fa',
				markerColor: 'blue'
			});

			return leaflet.marker([coordinates[1], coordinates[0]], {
				'event-id': data.id,
				icon: icon
			});
		});

		//Iterate through each event
		_.forEach(results, function(event) {
			var date, datetime, id, leafletId, listElement, result;

			id = event.id;
			result = event.result;

			date = new Date(result.datetime);

			//Turn the datetime into a form we want to use (built-in date formats have unnecessary data or
			//are too verbose)
			datetime = stringifyDatetime(date);

			//Cache the event
			eventCache[id] = result;

			//Save the leaflet ID corresponding to the event's marker
			map.eachMarker(function(marker) {
				var match = getLeafletId(marker, id);
				if (match !== undefined) {
					leafletId = match;
				}
			});

			//Render the list element for this event
			listElement = nunjucks.render('explorer/list_element.html', {
				datetime: datetime,
				event_type: result.event_type,
				content_type: getContentFontIcon(result.content_list),
				id: id,
				leaflet_id: leafletId,
				provider_name: result.provider_name
			});

			//Insert the event into the list.
			//If it's the first event to be inserted, just set #list to it; otherwise append each successive event to the last one present.
			if ($list.children().length === 0) {
				$list.html(listElement);
			}
			else {
				$list.last().append(listElement);
			}
		});
	});

	//When an event in the list is clicked, call highlightEvent on it.
	$(document).on('click', '.list-element', function(e) {
		var eventId, $listElement, $this = $(e.target);

		$listElement = $this.closest('.list-element');
		eventId = $listElement.data('event-id');

		highlightEvent(eventId);
	});

	scheduleMapper.schedule(600000);
});
