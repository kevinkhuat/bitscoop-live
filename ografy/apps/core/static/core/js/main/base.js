//Render the base elements of the main page and bind the navigation event listeners
//Also call for rendering of the default page view
function baseView() {
	//Instantiate instances of the views that the main page uses

	// Geocoder Instance
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


	//Bind event listeners for switching between the different page views
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

	//Render the base page, which consists of the header bar and the content area
	function render() {
		//Use Nunjucks to render the base page from a template and insert it into the page
		var base_framework = nunjucks.render('base.html');
		$('main').html(base_framework);

		//Render the default page view
		mapViewInst.renderBase();

		//Bind event listeners for switching between different page views
		bindNavigation();
	}

	return {
		render: render
	};
}
