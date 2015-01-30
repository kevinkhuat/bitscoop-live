function baseView() {
	var geocoder = new google.maps.Geocoder();

	//Utils Instance
	var utilsInst = utils();

	//Local Storage Data Handler
	var dataInst = utilsInst.dataStore();

	//Cookie/Session Handler
	var sessionInst = utilsInst.sessionsCookies();

	//View components
	var detailViewInst = detailView(utilsInst, geocoder);

	//Search components
	var searchViewInst = searchView(dataInst);
	searchViewInst.bindEvents();

	//Views
	var listViewInst = listView(detailViewInst, dataInst, utilsInst, sessionInst, geocoder);
	var mapViewInst = mapView(detailViewInst, dataInst, utilsInst, sessionInst, geocoder);


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
