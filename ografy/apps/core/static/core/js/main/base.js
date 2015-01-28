function baseView() {

	//Utils Instance
	var utilsInst = utils();

	//Map Handler
	var mapInst = utilsInst.mapboxManager();

	//Local Storage Data Handler
	var dataInst = utilsInst.dataStore();

	//Cookie/Session Handler
	var sessionInst = utilsInst.sessionsCookies();

	//View components
	var detailViewInst = detailView();

	//Views
	var listViewInst = listView(detailViewInst, dataInst, mapInst, sessionInst);
	var mapViewInst = mapView(detailViewInst, dataInst, mapInst, sessionInst);

	function bindNavigation() {
		$('.list-view-button').click(function() {
			listViewInst.renderBase(baseMap, baseData);
		});

		$('.timeline-view-button').click(function() {

		});

		$('.map-view-button').click(function() {
			mapViewInst.renderBase(baseMap, baseData, mapInst);
		});
	}

	function render() {
		var base_framework = nunjucks.render('static/core/templates/main/base.html');
		$('main').html(base_framework);

		mapViewInst.renderBase(baseMap, baseData, mapInst);

		bindNavigation();
	}

	return {
		render: render
	};
}
