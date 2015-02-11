//Render the Map View on the main page
function mapView(detailViewInst, dataInst, cacheInst, mapboxViewInst, sessionInst) {
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
		map.removeLayer(map.featureLayer);

		geoJSON.features = [];

		var newData = dataInst.getResultData();

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
		map.featureLayer = L.mapbox.featureLayer(geoJSON).addTo(map);

		//Fit the map's view so that all of the items are visible
		map.fitBounds(map.featureLayer.getBounds());

		//Bind an event listener that triggers when an item on the map is selected.
		//This listener will populate the detail content with the selected item's information.
		map.featureLayer.on('click', function(e) {
			//Save which item was selected
			var feature = e.layer.feature;

			//Populate the detail panel content with information from the selected item.
			$('.detail.main-label').html(feature.properties.description);
			$('.detail.time-content').html(feature.properties.datetime);
			$('.detail.location-content').html(String(feature.geometry.coordinates));
			$('.detail.body-content').html(String(feature.properties.data));
		});
	}

	return {
		renderBase: renderBase,
		renderContent: renderContent,
		updateContent: updateContent
	};
}
