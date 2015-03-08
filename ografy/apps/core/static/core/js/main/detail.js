//Render the detail panel on the right-hand side of the main page
function detailView(mapboxViewInst) {
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
		$('.detail.sidebar').html(list_detail);

		//If there will be a map, create the map.
		//This needs to be done after the detail panel has been inserted into the DOM
		//since MapBox needs a parent element specified when instantiating a map.
		if (showMap) {
			mapboxViewInst.initializeMap();
			map = mapboxViewInst.map;
			geoJSON = mapboxViewInst.geoJSON;
//			mapboxViewInst.renderDetailMap();
		}

		//Populate content with default data
		clearContent();

//		return {
//			map: map,
//			geoJSON: geoJSON
//		};
	}

	//Update content
	function updateContent(eventName, eventDate, eventLocation, eventData) {
		$('.detail.main-label').html(eventName);
		$('.detail.time-content').html(eventDate);
		$('.detail.location-content').html(eventLocation);
		$('.detail.body-content').html(eventData);
	}

	//Insert default text into the detail content
	function clearContent() {
		$('.detail.main-label').html('Select an Event at left to see its details.');
		$('.detail.time-content').html('Select an Event at left to see its details.');
		$('.detail.location-content').html('Select an Event at left to see its details.');
		$('.detail.body-content').html('Select an Event at left to see its details.');
	}

	//Update the map with a new event's information
	function updateMap(eventName, map, coordinates) {
		//Create a MapBox GeoJSON element with the new information
		var geoJSON = {
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
		};

		//Add the new element to the map
		map.featureLayer.setGeoJSON(geoJSON);

		//Center the map on the new element
		map.setView([coordinates[1], coordinates[0]], 13, {
			pan: {
				animate: true
			}
		});
	}

	//Remove all markers from the map
	function clearMap(map) {
		map.featureLayer.setGeoJSON([]);
	}

	return {
		renderContent: renderContent,
		updateContent: updateContent,
		clearContent: clearContent,
		updateMap: updateMap,
		clearMap: clearMap
	};
}
