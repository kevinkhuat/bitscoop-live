//Render the detail panel on the right-hand side of the main page
function detailView(mapboxViewInst, dataInst) {
	//Views
	//Render the detail panel's content
	function renderContent(showMap) {
		//If showMap isn't passed, by default set it to true
		showMap = typeof showMap !== 'undefined' ? showMap : true;

		//Use Nunjucks to render the detail panel from a template and insert it into the page.
		//showMap controls whether or not there will be a map in the lower half of the panel.
		var list_detail = nunjucks.render('detail.html', {
			showMap: showMap
		});

		$('.sidebar').html(list_detail);

		$(window).resize(function() {
			setHeight();
		});

		//If there will be a map, create the map.
		//This needs to be done after the detail panel has been inserted into the DOM
		//since MapBox needs a parent element specified when instantiating a map.
		if (showMap) {
			mapboxViewInst.initializeMap(false);
			map = mapboxViewInst.map;
			geoJSON = mapboxViewInst.geoJSON;
		}

		//Populate content with default data
		hideContent();

		$('.map.drawer-toggle').click(function() {
			$('.map.drawer-toggle').toggleClass('hidden');
			$('.map-half').toggleClass('hidden').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
				function(e) {
					$('.text-half').toggleClass('hidden');
					map.invalidateSize();
					setHeight();
				});
		});
//		return {
//			map: map,
//			geoJSON: geoJSON
//		};
	}

	//Update content
	function updateContent(event) {
		var sidebar = $('.sidebar');
		var dateTimeArray = [];
		var eventSubtypeInstance;

		if ($('.detail-to-from').length !== 0) {
			$('.detail-to-from').remove();
		}
		if ($('.detail-play-title').length !== 0) {
			$('.detail-play-title').remove();
		}
		if ($('.detail-message-body').length !== 0) {
			$('.detail-message-body').remove();
		}
		if (sidebar.hasClass('invisible')) {
			$('.sidebar').removeClass('invisible').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
				function(e) {
					if ($('.sidebar').children('.map-half').length !== 0) {
						map.invalidateSize();
					}
					setHeight();
				});
		}
		dateTimeArray = event.datetime.split(',');
		$('.detail .main-label').html(event.provider_name);
		$('.detail-date .content').html(dateTimeArray[0].trim());
		$('.detail-time .content').html(dateTimeArray[1].trim());
		$('.detail-location .content').html(String(event.location.coordinates));

		if (event['_cls'] === 'Event.Message') {
			var getSingleDocumentPromise = $.Deferred();
			var waitForPromise = false;
			if (!(event['id'] in dataInst.getMessageIndex())) {
				waitForPromise = true;
				dataInst.getSingleDocument('message', event['id'], getSingleDocumentPromise);
			}

			if (!(waitForPromise)) {
				getSingleDocumentPromise.resolve();
			}

			$.when(getSingleDocumentPromise).always(function() {
				event = dataInst.getResultListSingle(event.id);
				var detail_to_from = nunjucks.render('detail/to-from.html', {
					event: {
						message_to: event.message_to.toString().replace(/,/g, ', '),
						message_from: event.message_from
					}
				});
				var detail_message_body = nunjucks.render('detail/message-body.html', {
					event: {
						message_body: event.message_body
					}
				});
				$('.detail-location').before(detail_to_from);
				$('.detail-location').after(detail_message_body)
			});
		}
		else if (event['_cls'] === 'Event.Play') {
			var getSingleDocumentPromise = $.Deferred();
			var waitForPromise = false;
			if (!(event['id'] in dataInst.getPlayIndex())) {
				waitForPromise = true;
				dataInst.getSingleDocument('play', event['id'], getSingleDocumentPromise);
			}

			if (!(waitForPromise)) {
				getSingleDocumentPromise.resolve();
			}

			$.when(getSingleDocumentPromise).always(function() {
				event = dataInst.getResultListSingle(event.id);
				var detail_title = nunjucks.render('detail/title.html', {
					event: {
						title: event.title
					}
				});

				$('.detail-location').before(detail_title);
			});
		}
		else {
			$('.detail-data label').html('');
			$('.detail-data .content').html('');
		}

		if (!$('.detail').hasClass('full')) {
			updateMap(event.provider_name, map, event.location.coordinates);
		}
	}

	//Insert default text into the detail content
	function hideContent() {
		$('.sidebar').addClass('invisible');
	}

	//Update the map with a new event's information
	function updateMap(eventName, map, coordinates) {
		map.removeLayer(map.featureLayer);
		//Create a MapBox GeoJSON element with the new information
		map.featureLayer = L.mapbox.featureLayer({
			// this feature is in the GeoJSON format: see geojson.org
			// for the full specification
			type: 'Feature',
			geometry: {
				type: 'Point',
				// coordinates here are in longitude, latitude order because
				// x, y is the standard for GeoJSON and many formats
				coordinates: coordinates
			},
			properties: {
				title: eventName,
				description: 'event',
				// one can customize markers by adding simplestyle properties
				// https://www.mapbox.com/guides/an-open-platform/#simplestyle
				'marker-size': 'large',
				'marker-color': '#BE9A6B',
				'marker-symbol': 'post'
			}
		}).addTo(map);

		////Add the new element to the map
		//map.featureLayer.setGeoJSON(geoJSON);

		//Center the map on the new element
		map.setView([coordinates[1], coordinates[0]], 13, {
			pan: {
				animate: true
			}
		});
	}

	function setHeight() {
		var detailHeight = $('.detail').height();
		var mainLabelHeight = $('.main-label').height();
		$('.information').height(detailHeight - mainLabelHeight);
	}

	//Remove all markers from the map
	function clearMap(map) {
		map.featureLayer.setGeoJSON([]);
	}

	return {
		renderContent: renderContent,
		updateContent: updateContent,
		hideContent: hideContent,
		updateMap: updateMap,
		clearMap: clearMap
	};
}
