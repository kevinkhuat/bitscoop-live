//Render the Map View on the main page
function mapView(detailViewInst, dataInst, cacheInst, mapboxViewInst, sessionInst, urlParserInst) {
	var mapInst;
	var map = 'pants';
	var geoJSON = 'shorts';

	//Render the base framework of the Map View
	function renderBase(callback) {
		//Render the map content
		renderContent();

		//Render the detail panel content without a map
		detailViewInst.renderContent(false);

		callback();
	}

	//Render the map content
	function renderContent() {
		//Render the container for the map using Nunjucks and insert it into the DOM
		var map_framework = nunjucks.render('map/map.html');
		$('.data-view').html(map_framework);

		//Create a MapBox map.
		//This needs to be done after the map container has been inserted into the DOM
		//since MapBox needs a parent element specified when instantiating a map.
		mapboxViewInst.initializeMap();
		map = mapboxViewInst.map;
		geoJSON = mapboxViewInst.geoJSON;
	}

	function updateContent() {
		var line = [];
		if (map.hasLayer(map.clusterGroup)) {
			map.removeLayer(map.clusterGroup);
			map.removeLayer(map.polyline);
			map.removeControl(map.layerControl);
		}
		//map.featureLayer.eachLayer(function(marker) {
		//	map.clusterGroup.removeLayer(marker);
		//});

		map.removeLayer(map.featureLayer);
		//map.removeLayer(map.clusterGroup);
		geoJSON.features = [];

		var newData = dataInst.getResultData().reverse();

		//Create a MapBox GeoJSON element with the new information
		for (var index in newData) {
			geoJSON.features.push({
				// this feature is in the GeoJSON format: see geojson.org
				// for the full specification
				type: 'Feature',
				geometry: {
					type: 'Point',
					// coordinates here are in longitude, latitude order because
					// x, y is the standard for GeoJSON and many formats
					coordinates: newData[index].location.coordinates
				},
				properties: {
					title: newData[index].name,
					description: newData[index].provider_name,
					// one can customize markers by adding simplestyle properties
					// https://www.mapbox.com/guides/an-open-platform/#simplestyle
					'marker-size': 'large',
					'marker-color': '#BE9A6B',
					'marker-symbol': 'post',
					datetime: newData[index].datetime,
					data: newData[index].data,
					id: newData[index].id
				}
			});
		}

		//Add the new element to the map
		map.featureLayer = L.mapbox.featureLayer(geoJSON);

		map.clusterGroup = new L.MarkerClusterGroup();

		var currentFocus = urlParserInst.getFocus().slice();
		var currentZoom = urlParserInst.getZoom();

		if (currentFocus !== '' || currentZoom !== 0) {
			if (currentFocus !== '' && currentZoom !== 0) {
				map.setView(currentFocus.reverse(), currentZoom);
			}
			else if (currentFocus !== '') {
				urlParserInst.setZoom(12);
				currentZoom = urlParserInst.getZoom();
				map.setView(currentFocus.reverse(), 12);
			}
			else {
				urlParserInst.setFocus([parseFloat(geoplugin_longitude()), parseFloat(geoplugin_latitude())]);
				currentFocus = urlParserInst.getFocus();
				map.setView(currentFocus.reverse(), currentZoom);
			}
		}
		else {
			//Fit the map's view so that all of the items are visible
			map.fitBounds(map.featureLayer.getBounds());
			urlParserInst.setZoom(map.getZoom());
			urlParserInst.setFocus([map.getCenter().lng, map.getCenter().lat]);
			currentZoom = urlParserInst.getZoom();
			currentFocus = urlParserInst.getFocus();
		}

		urlParserInst.updateHash();

		map.featureLayer.eachLayer(function(marker) {
			map.clusterGroup.addLayer(marker);
			line.push(marker.getLatLng());
		});

		map.addLayer(map.clusterGroup);

		var polyline_options = {
			color: '#000'
		};

		map.polyline = L.polyline(line, polyline_options).addTo(map);


		map.layerControl = L.control.layers({ 'Street View': map.featureLayer }, { Directions: map.polyline }).addTo(map);
		//FIXME: This is most of what's needed to generate walking directions once the API is working
//		var directions = L.mapbox.directions({
//			profile: 'mapbox.driving'
//		});
//
//		for (var index in geoJSON.features) {
//			if (index == 0) {
//				directions.setOrigin(geoJSON.features[index]);
//			}
//			else if (index == geoJSON.features.length-1){
//				directions.setDestination(geoJSON.features[index]);
//			}
//			else {
//				directions.addWaypoint(index-1, geoJSON.features[index]);
//			}
//		}
//
//		directions.query();
//		map.directionsLayer = L.mapbox.directions.layer(directions).addTo(map);

		map.on('zoomend', function() {
			urlParserInst.setZoom(map.getZoom());
			currentZoom = urlParserInst.getZoom();
			urlParserInst.updateHash();
		});

		map.on('moveend', function() {
			urlParserInst.setFocus([map.getCenter().lng, map.getCenter().lat]);
			currentFocus = urlParserInst.getFocus();
			urlParserInst.updateHash();
		});

		map.on('click', function(e) {
			resetColors(map);
			//Populate the detail panel content with information from the selected item.
			detailViewInst.clearContent();
		});

		//Bind an event listener that triggers when an item on the map is selected.
		//This listener will populate the detail content with the selected item's information.
		map.clusterGroup.on('click', function(e) {
			//Save which item was selected
			var feature = e.layer.feature;

			resetColors(map);
			feature.properties['old-color'] = feature.properties['marker-color'];
			feature.properties['marker-color'] = '#ff8888';
			e.layer.setIcon(L.mapbox.marker.icon(feature.properties));

			//Populate the detail panel content with information from the selected item.
			detailViewInst.updateContent(feature.properties.description, feature.properties.datetime, String(feature.geometry.coordinates), String(feature.properties.data))
		});
	}

	function resetColors(map) {
		var clusterMarkers = map.clusterGroup.getLayers();
		for (var index in clusterMarkers) {
			var thisMarker = clusterMarkers[index];

			thisMarker.feature.properties['marker-color'] = thisMarker.feature.properties['old-color'] || thisMarker.feature.properties['marker-color'];
			thisMarker.setIcon(L.mapbox.marker.icon(thisMarker.feature.properties));
		}
	}


	return {
		renderBase: renderBase,
		renderContent: renderContent,
		updateContent: updateContent
	};
}
