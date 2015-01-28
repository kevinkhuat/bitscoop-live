function baseView() {

	//Utils Instance
	var utilsInst = utils();

	//Local Storage Data Handler
	var dataInst = utilsInst.dataStore();

	//Cookie/Session Handler
	var sessionInst = utilsInst.sessionsCookies();

	//View components
	var detailViewInst = detailView(utilsInst);

	//Views
	var listViewInst = listView(detailViewInst, dataInst, utilsInst, sessionInst);
	var mapViewInst = mapView(detailViewInst, dataInst, utilsInst, sessionInst);

	function bindNavigation() {
		$('.list-view-button').click(function() {
			listViewInst.renderBase();
		});

		$('.timeline-view-button').click(function() {
		});

		$('.map-view-button').click(function() {
			mapViewInst.renderBase();
		});
	}

	function render() {
		var base_framework = nunjucks.render('base.html');
		$('main').html(base_framework);

		mapViewInst.renderBase();

		bindNavigation();
	}

	return {
		render: render
	};
}
