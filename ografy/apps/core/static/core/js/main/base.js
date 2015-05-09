//Render the base elements of the main page and bind the navigation event listeners.
//Get search parameters from the URL or insert a default search if none is present.
//Also call for rendering of the default page view.
function baseView() {
	//Instantiate instances of the views that the main page uses

	//Data Instance
	var dataInst = dataStore();

	//URL Parser Instance
	var urlParserInst = urlParser(dataInst);

	//Mapbox handler
	var mapboxViewInst = mapboxManager(dataInst);

	//Detail sidebar
	var detailViewInst = detailView(mapboxViewInst, dataInst);

	//Views
	var listViewInst = listView(dataInst, urlParserInst);
	var mapViewInst = mapView(dataInst, mapboxViewInst, urlParserInst);

	//Search components
	var searchViewInst = searchView(dataInst, mapboxViewInst, urlParserInst);
	searchViewInst.bindEvents();

	//The data model needs references to the views and the detail sidebar, so save references to them.
	dataInst.state.view.instances.list = listViewInst;
	dataInst.state.view.instances.map = mapViewInst;
	dataInst.state.view.detail = detailViewInst;

	//Bind event listeners for switching between the different page views.
	function bindNavigation() {
		var sidebar = $('.sidebar');

		$('.view-button').click(function() {
			//Each view has an ID with the form 'view-model-<type>'
			//This gets the type from the ID.
			var viewType = $(this).attr('id').slice(12);

			//If the clicked view is active, then it needs to be deactivated and hidden
			//unless it's the only one active, in which case do nothing.
			//There must be at least one view active at all times .
			if (dataInst.state.view.active[viewType] === true) {
				//If more than one view is active, hide the current one.
				if (dataInst.state.view.active.count > 1) {
					$(this).removeClass('active').removeClass('hover');
					$('.' + viewType + '-view').addClass('hidden');
					dataInst.state.view.active[viewType] = false;
					dataInst.state.view.active.count-=1;
				}
				//Don't do anything if the clicked view is the only one active.
			}
			//If the clicked view is not active, then activate it.
			else {
				$(this).addClass('active').removeClass('hover');
				$('.' + viewType + '-view').removeClass('hidden');
				dataInst.state.view.active[viewType] = true;
				dataInst.state.view.active.count+=1;
				//If this is a mobile device, then hide the detail sidebar.
				//Mobile view can't have more than two views, including the sidebar, open
				//at the same time or else things get too crowded.
				if (dataInst.isMobile) {
					detailViewInst.hideContent();
				}
			}
			//This makes sure that the list view's height is properly restored after switching views.
			if (dataInst.state.view.active.list && dataInst.isMobile) {
				if ($('.sidebar').hasClass('invisible')) {
					$('.sidebar').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
						function(e) {
							listViewInst.setHeight();
						});
				}
				else {
					listViewInst.setHeight();
				}
			}
			//Re-render the map tiles after everything is done.
			//If this isn't done, the map often tries to render tiles in the middle of expanding
			//or contracting its size and ends up with missing tiles.
			mapboxViewInst.map.main.invalidateSize();
		});
	}

	//Create an event listener on the filter menu button to hide and show the filter menu.
	//Also create an event listener that hides the filter menu if the user clicks anywhere outside the menu.
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

		//If there isn't an initial sort for the search, set it to datetime starting from the most recent events.
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
			//These promises ensure that the search isn't started until all the views have been rendered
			//and are thus ready to be fed data.
			var mapPromise = $.Deferred();
			var listPromise = $.Deferred();
			L.mapbox.accessToken = data.OGRAFY_MAPBOX_ACCESS_TOKEN;
			mapViewInst.renderContent(mapPromise);
			listViewInst.renderContent(listPromise);
			detailViewInst.renderContent();
			//Wait for the view promises to be resolved, at which point the views have been instantiated.
			$.when(mapPromise && listPromise).always(function() {
				dataInst.search('event', searchString);
			});
		});

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
			var now = new Date();
			var oneWeekAgo = new Date();
			oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

			//This will be the default search string if none is provided, but as of now that functionality isn't working on the backend.
//		    searchString = '(datetime gt ' + oneWeekAgo.toJSON() + ')';

			//The below line is the actual default search to be used - anything in the last week
			//searchString = '(datetime lt \'' + now.toJSON().slice(0, 16) + '\') and (datetime gt \'' + oneWeekAgo.toJSON().slice(0, 16) + '\')';

			searchString = '';
			console.log(searchString);
			dataInst.state.query.event.searchString = searchString;
		}

		return searchString;
	}

	function setInitialView() {
		//Get the current view from the data model
		var views = dataInst.state.view.active;

		urlParserInst.updateHash();
	}

	return {
		render: render,
		getInitialSearchString: getInitialSearchString,
		setInitialView: setInitialView
	};
}
