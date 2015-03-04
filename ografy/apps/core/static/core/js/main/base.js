//Render the base elements of the main page and bind the navigation event listeners
//Also call for rendering of the default page view
function baseView() {
	//Instantiate instances of the views that the main page uses

	// Geocoder Instance

	//TODO: Ugly - fix in a big way so it is done better. On server?
	var geocoder = new google.maps.Geocoder();

	//Cache Instance
	var cacheInst = cacheManager();

	//Data Instance
	var dataInst = dataStore();

	//Cookie/Session Handler
	var sessionInst = sessionsCookies();

	//Mapbox handler
	var mapboxViewInst = mapboxManager();

	//View components
	var detailViewInst = detailView(mapboxViewInst);

	//Views
	var listViewInst = listView(detailViewInst, dataInst, cacheInst, mapboxViewInst, sessionInst);
	var mapViewInst = mapView(detailViewInst, dataInst, cacheInst, mapboxViewInst,  sessionInst);

	//Search components
	var searchViewInst = searchView(dataInst, cacheInst, mapViewInst, listViewInst);
	searchViewInst.bindEvents();

	//Bind event listeners for switching between the different page views
	function bindNavigation() {
		$('.list-view-button').click(function() {
			dataInst.setCurrentView(listViewInst);
			listViewInst.renderBase();
		});

		//$('.timeline-view-button').click(function() {
		//});

		$('.map-view-button').click(function() {
			dataInst.setCurrentView(mapViewInst);
			mapViewInst.renderBase(function() {
				mapViewInst.updateContent();

			});
		});
	}

	//Render the base page, which consists of the header bar and the content area
	function render() {
		//Use Nunjucks to render the base page from a template and insert it into the page
		var base_framework = nunjucks.render('base.html');
		$('main').html(base_framework);

		//Load data from the database
		dataInst.setCurrentView(mapViewInst);
		mapViewInst.renderBase(function() {
			var oneWeekAgo = new Date();
			oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

//			var searchString = '(datetime gt ' + oneWeekAgo.toJSON() + ')';
			var searchString = '(provider_name contains twitter) or (provider_name contains facebook) or (provider_name contains github) or (provider_name contains instagram) or (provider_name contains steam)';
			console.log(searchString);
			dataInst.search(searchString);
		});

		//Render the default page view

		//Bind event listeners for switching between different page views
		bindNavigation();
	}

	return {
		render: render
	};
}
