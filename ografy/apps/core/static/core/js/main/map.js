//Views
function renderMapContent() {
	var map_framework = nunjucks.render('static/core/templates/main/map/map.html');
	$('#content').html(map_framework);

	map = new mapboxgl.Map({
		container: 'map',
		style: style
	});

	calculateFitBounds(DANGEROUS_TEST_DATA);
	placeMapPoints(DANGEROUS_TEST_DATA);
}