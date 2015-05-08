//Render the detail panel on the right-hand side of the main page (bottom of the page in mobile)
function detailView(mapboxViewInst, dataInst) {
	//Views
	//Render the detail panel's content
	function renderContent() {
		//Use Nunjucks to render the detail panel from a template and insert it into the page.
		//showMap controls whether or not there will be a map in the lower half of the panel.
		var list_detail = nunjucks.render('detail.html');

		$('.sidebar').html(list_detail);

		$(window).resize(function() {
			setHeight();
		});

		//Create the map.
		//This needs to be done after the detail panel has been inserted into the DOM
		//since MapBox needs a parent element specified when instantiating a map.
		mapboxViewInst.initializeDetailMap();
		map = mapboxViewInst.map.detail;
		geoJSON = mapboxViewInst.geoJSON;

		//Populate content with default data and make sure the sidebar is hidden on page load.
		hideContent();

		//When the map drawer toggle is clicked, open or close the map drawer.
		//If it's being opened, close the data drawer.
		$('.map.drawer-toggle').click(function() {
			//Close the data half if it's open.
			if ($('.data-half').not('.hidden').length > 0) {
				$('.data.drawer-toggle').toggleClass('hidden');
				//Wait until the data drawer is closed before setting the height of the text half
				$('.data-half').toggleClass('hidden').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
					function(e) {
						setHeight();
					});
			}
			//Open/close the map drawer
			$('.map.drawer-toggle').toggleClass('hidden');
			//Wait until the map drawer is opened or closed before refreshing the map and setting the height of the text half.
			$('.map-half').toggleClass('hidden').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
				function(e) {
					$('.text-half').toggleClass('hidden');
					map.invalidateSize();
					setHeight();
				});
		});

		//When the data drawer toggle is clicked, open or close the data drawer.
		//If it's being opened, close the map drawer.
		$('.data.drawer-toggle').click(function() {
			//Close the map half if it's open.
			if ($('.map-half').not('.hidden').length > 0) {
				$('.map.drawer-toggle').toggleClass('hidden');
				//Wait until the map drawer is closed before setting the height of the text half
				$('.map-half').toggleClass('hidden').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
					function(e) {
						setHeight();
					});
			}
			//Open/close the data drawer
			$('.data.drawer-toggle').toggleClass('hidden');
			//Wait until the data drawer is opened or closed before setting the height of the text half.
			$('.data-half').toggleClass('hidden').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
				function(e) {
					$('.text-half').toggleClass('hidden');
					setHeight();
				});
		});
	}

	//Update sidebar content
	function updateContent(event) {
		var sidebar = $('.sidebar');
		var dateTimeArray = [];
		var data_blob = event.data.data_blob.d;

		//Remove any fields that aren't always present.
		if ($('.detail-to-from').length !== 0) {
			$('.detail-to-from').remove();
		}
		if ($('.detail-play-title').length !== 0) {
			$('.detail-play-title').remove();
		}
		if ($('.detail-message-body').length !== 0) {
			$('.detail-message-body').remove();
		}
		//Wait for the sidebar to fully expand before setting the text-half height.
		if (sidebar.hasClass('invisible')) {
			$('.sidebar').removeClass('invisible').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
				function(e) {
					setHeight();
				});
		}

		//Fill in information in the sidebar.
		dateTimeArray = event.datetime.split(',');
		$('.detail .main-label').html(event.provider_name);
		$('.detail-date .content').html(dateTimeArray[0].trim());
		$('.detail-time .content').html(dateTimeArray[1].trim());
		$('.detail-location .content').html(String(event.location.coordinates));


		//Populate the data drawer.
		$('.data-entries').html('Event Extra Data');
		for (var key in data_blob) {
			var value = data_blob[key];
			var formattedValue = '';

			//If a data entry is an array, format it to look like an array in string form.
			if (value instanceof Array) {
				formattedValue = '[' + value + ']';
			}
			//If a data entry is an object, format it to look like a dictionary in string form.
			else if (value instanceof Object) {
				formattedValue = '{';
				for (var innerKey in value) {
					formattedValue += innerKey + ': ' + value[innerKey] + ', ';
				}
				formattedValue = formattedValue.trim();
				formattedValue = formattedValue.substring(0, formattedValue.length - 1) +  '}';
			}
			//All other types should be automatically stringified with no formatting necessary.
			else {
				formattedValue = value;
			}

			//Create a new entry in the data drawer from a template.
			var newEntry = nunjucks.render('detail/data-entry.html', {
				key: key,
				value: formattedValue
			});
			$('.data-entries').append(newEntry);
		}

		//If the event is a Message, render Message-specific fields in the sidebar.
		if (event._cls === 'Event.Message') {
			//These variables are used to wait for a Message to be retrieved from the database before continuing on.
			var getSingleDocumentPromise = $.Deferred();
			var waitForPromise = false;

			//Check if this Message has been retrieved as a Message before, not just as an Event.
			//The Event API only returns fields that all Events have, but not the Message-specific fields.
			//If it hasn't been retrieved as a Message, then retrieve it using the Message API.
			if (dataInst.eventCache.subtypes.messages.indexOf(event.id) < 0) {
				waitForPromise = true;
				dataInst.getSingleDocument('message', event.id, getSingleDocumentPromise);
			}

			//waitForPromise is only set to true if the Message needs to be retrieved through the Message API.
			//If it's still false, then it's already been retrieved and the promise can be resolved immediately.
			//If it's true, then the promise will be resolved once the API call has been returned and the cache updated.
			if (!(waitForPromise)) {
				getSingleDocumentPromise.resolve();
			}

			//When the promise has been resolved, render Message-specific information in the sidebar.
			$.when(getSingleDocumentPromise).always(function() {
				event = dataInst.eventCache.events[event.id];
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
				$('.detail-location').after(detail_message_body);
			});
		}
		//If the event is a Play, render Play-specific fields in the sidebar.
		else if (event._cls === 'Event.Play') {
			//These variables are used to wait for a Message to be retrieved from the database before continuing on.
			var getSingleDocumentPromise = $.Deferred();
			var waitForPromise = false;

			//Check if this Play has been retrieved as a Play before, not just as an Event.
			//The Event API only returns fields that all Events have, but not the Play-specific fields.
			//If it hasn't been retrieved as a Play, then retrieve it using the Play API.
			if (dataInst.eventCache.subtypes.plays.indexOf(event.id) < 0) {
				waitForPromise = true;
				dataInst.getSingleDocument('play', event.id, getSingleDocumentPromise);
			}

			//waitForPromise is only set to true if the Play needs to be retrieved through the Play API.
			//If it's still false, then it's already been retrieved and the promise can be resolved immediately.
			//If it's true, then the promise will be resolved once the API call has been returned and the cache updated.
			if (!(waitForPromise)) {
				getSingleDocumentPromise.resolve();
			}

			//When the promise has been resolved, render Play-specific information in the sidebar.
			$.when(getSingleDocumentPromise).always(function() {
				event = dataInst.eventCache.events[event.id];
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

		//Update the detail map
		updateMap(event, map);

		//Move the sort bar so that it isn't covering any portion of the detail sidebar.
		if (!(($('.sort')).hasClass('moved'))) {
			$('.sort').toggleClass('moved');
		}
	}

	//Hide the detail sidebar and move the sort bar to its original position.
	function hideContent() {
		$('.sidebar').addClass('invisible');
		if (($('.sort')).hasClass('moved')) {
			$('.sort').removeClass('moved');
		}
	}

	//Update the detail map with a new event's information
	function updateMap(event, map) {
		var coordinates = event.location.coordinates;
		var markerColor, markerSymbol;

		map.removeLayer(map.featureLayer);

		//Each event type has a different marker color and symbol
		if (event._cls === 'Event') {
			markerColor = '#0052CE';
			markerSymbol = 'star-stroked';
		}
		else if (event._cls === 'Event.Message') {
			markerColor = '#E6B800';
			markerSymbol = 'post';
		}
		else if (event._cls === 'Event.Play') {
			markerColor = '#33CC33';
			markerSymbol = 'music';
		}

		//Create a MapBox GeoJSON element with the new information and add it to the detail map.
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
				title: event.provider_name,
				description: 'event',
				'marker-size': 'large',
				'marker-color': markerColor,
				'marker-symbol': markerSymbol
			}
		}).addTo(map);

		//Center the map on the new element
		map.setView([coordinates[1], coordinates[0]], 13, {
			pan: {
				animate: true
			}
		});
	}

	//Set the height of the text half so that it's always taking up as much space as it should
	//(half the sidebar if a drawer is open, or the entire sidebar if no drawers are open).
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
