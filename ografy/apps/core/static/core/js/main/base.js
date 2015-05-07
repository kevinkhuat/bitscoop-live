//Render the base elements of the main page and bind the navigation event listeners
//Also call for rendering of the default page view
function baseView() {
	//Instantiate instances of the views that the main page uses

	//Data Instance
	var dataInst = dataStore();

	//URL Parser Instance
	var urlParserInst = urlParser(dataInst);

	//Mapbox handler
	var mapboxViewInst = mapboxManager();

	//View components
	var detailViewInst = detailView(mapboxViewInst, dataInst);

	//Views
	var listViewInst = listView(detailViewInst, dataInst, urlParserInst);
	var mapViewInst = mapView(detailViewInst, dataInst, mapboxViewInst, urlParserInst);

	dataInst.state.view.instances.list = listViewInst;
	dataInst.state.view.instances.map = mapViewInst;

	//Search components
	var searchViewInst = searchView(dataInst, urlParserInst);
	searchViewInst.bindEvents();

	//Bind event listeners for switching between the different page views
	function bindNavigation() {
		var sidebar = $('.sidebar');

		$('.view-button').click(function() {
			var viewType = $(this).attr('id').slice(12);
			if (dataInst.state.view.active[viewType] === true) {
				if (dataInst.state.view.active.count > 1) {
					$(this).removeClass('active').removeClass('hover');
					$('.' + viewType + '-view').addClass('hidden');
					dataInst.state.view.active[viewType] = false;
					dataInst.state.view.active.count-=1;
				}
			}
			else {
				$(this).addClass('active').removeClass('hover');
				$('.' + viewType + '-view').removeClass('hidden');
				dataInst.state.view.active[viewType] = true;
				dataInst.state.view.active.count+=1;
			}
			mapboxViewInst.map.invalidateSize();
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

	//Render the base page, which consists of the header bar and the content area
	function render() {
		//Use Nunjucks to render the base page from a template and insert it into the page
		var base_framework = nunjucks.render('base.html');
		$('main').html(base_framework);

		//Have the URL parser retreieve and parse the URL hash
		urlParserInst.retrieveHash();

		//Get the intial search
		var searchString = getInitialSearchString();

		if (dataInst.state.view.sort.length === 0) {
			dataInst.state.view.sort = '-datetime';
		}

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
			var mapPromise = $.Deferred();
			var listPromise = $.Deferred();
			L.mapbox.accessToken = data.OGRAFY_MAPBOX_ACCESS_TOKEN;
			mapViewInst.renderContent(mapPromise);
			listViewInst.renderContent(listPromise);
			detailViewInst.renderContent(false);
			$.when(mapPromise && listPromise).always(function() {
				dataInst.search('event', searchString);
			});
		});

		//Render the default page view

		//Bind event listeners for switching between different page views
		bindNavigation();
		bindFilterCommands();
	}

	function getInitialSearchString() {
		//Get filters from the URL parser
		var searchString = dataInst.state.query.event.searchString;

		//If no search string was provided in the URL, use a default
		if (searchString.length === 0) {
			//The default search, if none is provided in the URL, is to get everything from the past week
			var oneWeekAgo = new Date();
			oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

			//This will be the default search string if none is provided, but as of now that functionality isn't working on the backend.
//		    searchString = '(datetime gt ' + oneWeekAgo.toJSON() + ')';

			//This is a temporary default search string, as searching by providers does work
			searchString = '(provider_name contains twitter) or (provider_name contains facebook) or (provider_name contains github) or (provider_name contains instagram) or (provider_name contains steam) or (provider_name contains spotify)';
			dataInst.state.query.event.searchString = searchString;
		}

		return searchString;
	}

	function setInitialView() {
		//Get the current view from the URL parser
		var views = dataInst.state.view.active;

		urlParserInst.updateHash();
	}

	return {
		render: render,
		getInitialSearchString: getInitialSearchString,
		setInitialView: setInitialView
	};
}
