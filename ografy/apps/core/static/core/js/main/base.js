//Render the base elements of the main page and bind the navigation event listeners
//Also call for rendering of the default page view
function baseView() {
	var renderDark = false;

	//Instantiate instances of the views that the main page uses

	//Cache Instance
	var cacheInst = cacheManager();

	//URL Parser Instance
	var urlParserInst = urlParser();

	//Mapbox handler
	var mapboxViewInst = mapboxManager();

	//Cookie/Session Handler
	var sessionInst = sessionsCookies();

	//View components
	var detailViewInst = detailView(mapboxViewInst);

	//Data Instance
	var dataInst = dataStore(urlParserInst, detailViewInst);

	//Views
	var listViewInst = listView(detailViewInst, dataInst, cacheInst, mapboxViewInst, sessionInst, urlParserInst);
	var mapViewInst = mapView(detailViewInst, dataInst, cacheInst, mapboxViewInst,  sessionInst, urlParserInst);

	//Search components
	var searchViewInst = searchView(dataInst, cacheInst, mapboxViewInst, mapViewInst, listViewInst, urlParserInst);
	searchViewInst.bindEvents();

	//Bind event listeners for switching between the different page views
	function bindNavigation() {
		var sidebar = $('.sidebar');

		$('.list-view-button').click(function() {
			urlParserInst.setView('list');
			dataInst.setCurrentView(listViewInst);
			if (!sidebar.hasClass('invisible')) {
				detailViewInst.hideContent();
				sidebar.one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
					function (e) {
						listViewInst.renderBase(function () {
							listViewInst.updateContent();
						});
					});
			}
			else {
				listViewInst.renderBase(function () {
					listViewInst.updateContent();
				});
			}
		});

		//$('.timeline-view-button').click(function() {
		//});

		$('.map-view-button').click(function() {
			urlParserInst.setView('map');
			dataInst.setCurrentView(mapViewInst);
			if (!sidebar.hasClass('invisible')) {
				detailViewInst.hideContent();
				sidebar.one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
				function(e) {
					mapViewInst.renderBase(function () {
						mapViewInst.updateContent();
					});
				});
			}
			else {
				mapViewInst.renderBase(function () {
					mapViewInst.updateContent();
				});
			}

		});
	}

	function bindFilterCommands() {
		$('.filter-button').click(function() {
			$('.menu.filter').toggleClass('hidden');
		});

		$(document.body).click(function(e) {
			if (!e.target.classList.contains('filter-button') &&
				!e.target.classList.contains('item') &&
				!e.target.closest('.filter')) {
				$('.menu.filter').addClass('hidden');
			}
		});
	}

	function setColorScheme(scheme) {
		var renderStyle = (scheme === 'light') ? ('light') : 'dark';
		var mainLink  = document.createElement('link');
		var siteLink  = document.createElement('link');
		mainLink.rel = "stylesheet";
		siteLink.rel  = "stylesheet";
		mainLink.type = "text/css";
		siteLink.type = "text/css";
		mainLink.href = "/static/core/css/main/main-" + renderStyle + ".css";
		siteLink.href = "/static/shared/css/site-" + renderStyle + ".css";

		document.head.appendChild(mainLink);
		document.head.appendChild(siteLink);
	}
	//Render the base page, which consists of the header bar and the content area
	function render() {
		if (renderDark) {
			setColorScheme ('dark');
		}
		else {
			setColorScheme ('light');
		}
		//Use Nunjucks to render the base page from a template and insert it into the page
		var base_framework = nunjucks.render('base.html');
		$('main').html(base_framework);

		//Have the URL parser retreieve and parse the URL hash
		urlParserInst.retrieveHash();

		//Get the intial search
		var searchString = getInitialSearchString();

		var sort = getInitialSort();

		//Set the initial view
		setInitialView();

		//Call the renderBase function for the current view with a callback to perform a search on the search string
		var cookie = sessionsCookies().getCsrfToken();
		var url = 'app/keys/mapbox';
		$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			headers: {
				'X-CSRFToken': cookie
			}
		}).done(function(data, xhr, response) {
			L.mapbox.accessToken = data.OGRAFY_MAPBOX_ACCESS_TOKEN;
			dataInst.getCurrentView().renderBase(function() {
				console.log(searchString);
				urlParserInst.setSearchFilters(searchString);
				dataInst.search('event', searchString, sort);
			});
		});

		//Render the default page view

		//Bind event listeners for switching between different page views
		bindNavigation();
		bindFilterCommands();
	}

	function getInitialSearchString() {
		//Get filters from the URL parser
		var searchString = urlParserInst.getSearchFilters();

		//If no search string was provided in the URL, use a default
		if (searchString.length === 0) {
			//The default search, if none is provided in the URL, is to get everything from the past week
			var oneWeekAgo = new Date();
			oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

			//This will be the default search string if none is provided, but as of now that functionality isn't working on the backend.
//		    searchString = '(datetime gt ' + oneWeekAgo.toJSON() + ')';

			//This is a temporary default search string, as searching by providers does work
			searchString = '(provider_name contains twitter) or (provider_name contains facebook) or (provider_name contains github) or (provider_name contains instagram) or (provider_name contains steam) or (provider_name contains spotify)';
		}

		return searchString;
	}

	function getInitialSort() {
		var sort = urlParserInst.getSort();

		if (sort.length === 0) {
			sort = '-datetime';
			urlParserInst.setSort(sort);
		}

		return sort;
	}

	function setInitialView() {
		//Get the current view from the URL parser
		var currentView = urlParserInst.getView();

		//When the page is first loaded, if a view is specified in the URL hash, set the page to that view
		if (currentView === 'map') {
			dataInst.setCurrentView(mapViewInst);
		}
		else if (currentView === 'list') {
			dataInst.setCurrentView(listViewInst);
		}
		//If no view is specified, default to map view and set the URL parser to that view
		else {
			urlParserInst.setView('map');
			dataInst.setCurrentView(mapViewInst);
		}
	}

	return {
		render: render,
		getInitialSearchString: getInitialSearchString,
		setInitialView: setInitialView
	};
}
