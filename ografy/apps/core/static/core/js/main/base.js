function baseView() {
	//Data model
	var baseData = [];

	function mapbox() {
		this.map = 10;
		this.geoJSON = {
			"type": "FeatureCollection",
			"features": []
		};
	}

	var baseMap = new mapbox();
	//Sub Views
	var detailViewInst = detailView();
	var listViewInst = listView();
	var mapViewInst = mapView();
	var utilsViewInst = utils();

	function clearData() {

	}

	function updateData() {

	}

	function search() {

	}

	function loadTestData(completeCallback) {
		var csrftoken = utilsViewInst.session().getCookie('csrftoken');
		$.ajax({
			url: 'static/core/js/test_data/event_test_data.json',
			type: 'GET',
			dataType: 'json',
			headers: {"X-CSRFToken": csrftoken}
		}).done(function(data, xhr, response) {
			baseData = data;
			completeCallback();
		});
	}

	function render() {
		var base_framework = nunjucks.render('static/core/templates/main/base.html');
		$('main').html(base_framework);

		listViewInst.renderBase(baseMap, baseData);
	}

	function bindNavigation() {
		$('.list-view-button').click(function() {
			listViewInst.renderBase(baseMap, baseData);
		});

		$('.timeline-view-button').click(function() {

		});

		$('.map-view-button').click(function() {
			mapViewInst.renderBase(baseMap, baseData, utilsViewInst.mapbox());
		});
	}

	function loadInitialData() {
		$.ajax({
			url: '/opi/event',
			type: 'GET',
			dataType: 'json',
			headers: {"X-CSRFToken": csrftoken}
		}).done(function(data, xhr, response) {
			baseData = data;
			console.log(baseData);
		});
	}

	return {
		render: render,
		bindNavigation: bindNavigation,
		loadInitialData: loadInitialData,
		loadTestData: loadTestData
	}
}