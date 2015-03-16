//Render the base elements of the main page and bind the navigation event listeners
//Also call for rendering of the default page view
function baseView() {
	//Instantiate instances of the views that the main page uses

	//TODO: Ugly - fix in a big way so it is done better. On server?
	var geocoder = new google.maps.Geocoder();

	//Cache Instance
	var cacheInst = cacheManager();

	//Data Instance
	var dataInst = dataStore();

	//URL Parser Instance
	var urlParserInst = urlParser();

	//Cookie/Session Handler
	var sessionInst = sessionsCookies();

	//Mapbox handler
	var mapboxViewInst = mapboxManager();

	//View components
	var detailViewInst = detailView(mapboxViewInst);

	//Views
	var listViewInst = listView(detailViewInst, dataInst, cacheInst, mapboxViewInst, sessionInst, urlParserInst);
	var mapViewInst = mapView(detailViewInst, dataInst, cacheInst, mapboxViewInst,  sessionInst, urlParserInst);

	//Search components
	var searchViewInst = searchView(dataInst, cacheInst, mapViewInst, listViewInst, urlParserInst);
	searchViewInst.bindEvents();

	//Bind event listeners for switching between the different page views
	function bindNavigation() {
		$('.list-view-button').click(function() {
			dataInst.setCurrentView(listViewInst);
			listViewInst.renderBase(function() {
				listViewInst.updateContent();
			});
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

		urlParserInst.retrieveHash();

		var currentView = urlParserInst.getView();
		var oneWeekAgo = new Date();
		oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

		//Load data from the database
		if (currentView === 'map') {
			dataInst.setCurrentView(mapViewInst);
			mapViewInst.renderBase(function() {
//			var searchString = '(datetime gt ' + oneWeekAgo.toJSON() + ')';
//				var searchString = '(provider_name%20contains%20twitter)%20or%20(provider_name%20contains%20facebook)%20or%20(provider_name%20contains%20github)%20or%20(provider_name%20contains%20instagram)%20or%20(provider_name%20contains%20steam)%20or%20(provider_name%20contains%20spotify)';
				var searchString = urlParserInst.getSearchFilters();
				console.log(searchString);
				dataInst.search(searchString);
			});
		}
		else if (currentView === 'list') {
			dataInst.setCurrentView(listViewInst);
			listViewInst.renderBase(function() {
//			var searchString = '(datetime gt ' + oneWeekAgo.toJSON() + ')';
				var searchString = urlParserInst.getSearchFilters();
				console.log(searchString);
				dataInst.search(searchString);
			});
		}
		else {
			currentView = 'map';
			dataInst.setCurrentView(mapViewInst);
			mapViewInst.renderBase(function() {
//			var searchString = '(datetime gt ' + oneWeekAgo.toJSON() + ')';
				var searchString = urlParserInst.getSearchFilters();
				console.log(searchString);
				dataInst.search(searchString);
			});
		}

		$(window).resize(function() {
			if (window.outerHeight >= window.outerWidth) {
				$('body').addClass('mobile').addClass;
			}
			else if (window.outerHeight < window.outerWidth) {
				$('body').removeClass('mobile');
			}
		});
		//Render the default page view

		//Bind event listeners for switching between different page views
		bindNavigation();
	}

	return {
		render: render
	};
}
