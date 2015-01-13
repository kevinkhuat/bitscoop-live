function mapView(mapUtil) {
	//Views
	function renderContent() {
		var map_framework = nunjucks.render('static/core/templates/main/map/map.html');
		$('#content').html(map_framework);

		map = new mapboxgl.Map({
			container: 'map',
			style: style
		});

		mapUtil.calculateFitBounds(DANGEROUS_TEST_DATA);
		mapUtil.placeMapPoints(DANGEROUS_TEST_DATA);
	}

	return {
		renderContent: renderContent
	}
}
