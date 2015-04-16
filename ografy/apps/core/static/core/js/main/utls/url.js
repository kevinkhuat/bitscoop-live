function urlParser() {
	var urlHash = '';

	//Variables for parsing the map's focus
	var focusPattern = /focus=\S*?(&|$)/;
	var focusRegexResult = '';
	var currentFocus = [];
	var currentFocusString = '';

	//Variables for parsing the map's zoom
	var zoomPattern = /zoom=\S*?(&|$)/;
	var zoomRegexResult = '';
	var currentZoom = 0;

	//Variables for parsing the list's sorting
	var sortPattern = /sort=\S*?(&|$)/;
	var sortRegexResult = '';
	var currentSort = '';

	//Variables for parsing the current view
	var viewPattern = /view=\S*?(&|$)/;
	var viewRegexResult = '';
	var currentView = '';

	//Variables for parsing the current filters
	var filtersPattern = /filters=\S*?(&|$)/;
	var filtersRegexResult = '';
	var currentFilters = '';

	//Variables for parsing the current query
	var queryPattern = /query=\S*?(&|$)/;
	var queryRegexResult = '';
	var currentQuery = '';

	var encodedFilters = '';

	function retrieveHash() {
		//Get the hash from the URL
		urlHash = window.location.hash;

		//Test if the map focus pattern returns any results.  If yes, then parse out the relevant data.
		//If no, then set the focus to a blank array.
		if (focusPattern.test(urlHash)) {
			//Since a regex execution returns an array, pull out the first entry in the result set
			focusRegexResult = focusPattern.exec(urlHash)[0];
			//Replace URL-specific portions of the URL hash with nothing
			currentFocusString = focusRegexResult.replace('focus=', '').replace('&', '');
			//Turn the lat/lng from the URL string into an array
			currentFocus = currentFocusString.split(',');
			//Parse the lat/lng array, which still contains strings, into floats
			for (var index in currentFocus) {
				currentFocus[index] = parseFloat(currentFocus[index]);
			}
		}
		else {
			focusRegexResult = '';
			currentFocus = [];
		}

		//Test if the map zoom pattern returns any results.  If yes, then parse out the relevant data.
		//If no, then set the zoom to a blank string.
		if (zoomPattern.test(urlHash)) {
			//Since a regex execution returns an array, pull out the first entry in the result set
			zoomRegexResult = zoomPattern.exec(urlHash)[0];
			//Replace URL-specific portions of the URL hash with nothing
			currentZoom = parseInt(zoomRegexResult.replace('zoom=', '').replace('&', ''));
		}
		else {
			zoomRegexResult = '';
			currentZoom = 0;
		}

		//Test if the list sort pattern returns any results.  If yes, then parse out the relevant data.
		//If no, then set the sort to a blank string.
		if (sortPattern.test(urlHash)) {
			sortRegexResult = sortPattern.exec(urlHash)[0];
			//Replace URL-specific portions of the URL hash with nothing
			currentSort = sortRegexResult.replace('sort=', '').replace('&', '');
		}
		else {
			sortRegexResult = '';
			currentSort = '';
		}

		//Test if the current view pattern returns any results.  If yes, then parse out the relevant data.
		//If no, then set the view to a blank string.
		if (viewPattern.test(urlHash)) {
			//Since a regex execution returns an array, pull out the first entry in the result set
			viewRegexResult = viewPattern.exec(urlHash)[0];
			//Replace URL-specific portions of the URL hash with nothing
			currentView = viewRegexResult.replace('view=', '').replace('&', '');
		}
		else {
			viewRegexResult = '';
			currentView = '';
		}

		//Test if the current filters pattern returns any results.  If yes, then parse out the relevant data.
		//If no, then set the filters to a blank string.
		if (filtersPattern.test(urlHash)) {
			//Since a regex execution returns an array, pull out the first entry in the result set
			filtersRegexResult = filtersPattern.exec(urlHash)[0];
			//Replace URL-specific portions of the URL hash with nothing
			currentFilters = filtersRegexResult.replace('filters=', '').replace(/%20/g, ' ').replace(/&/g, '');
		}
		else {
			filtersRegexResult = '';
			currentFilters = '';
		}

		//Test if the current query pattern returns any results.  If yes, then parse out the relevant data.
		//If no, then set the query to a blank string.
		if (queryPattern.test(urlHash)) {
			//Since a regex execution returns an array, pull out the first entry in the result set
			queryRegexResult = queryPattern.exec(urlHash)[0];
			//Replace URL-specific portions of the URL hash with nothing
			currentQuery = queryRegexResult.replace('query=', '').replace(/%20/g, ' ').replace(/&/g, '');
		}
		else {
			queryRegexResult = '';
			currentQuery = '';
		}
	}

	//Functions to get and set the specified variables
	function getFocus() {
		return currentFocus;
	}

	function getZoom() {
		return currentZoom;
	}

	function getSort() {
		return currentSort;
	}

	function getView() {
		return currentView;
	}

	function getSearchFilters() {
		return currentFilters;
	}

	function getSearchQuery() {
		return currentQuery;
	}

	function setFocus(input) {
		currentFocus = input;
	}

	function setZoom(input) {
		currentZoom = input;
	}

	function setSort(input) {
		currentSort = input;
	}

	function setView(input) {
		currentView = input;
		updateHash();
	}

	function setSearchFilters(input) {
		currentFilters = input;
	}

	function setSearchQuery(input) {
		currentQuery = input;
	}

	//Update the URL hash with whatever the current properties are.  E.g. as the user moves the map around, the URL
	//has its focus coordinates updated as well, or a new search puts that search's filters and query into the URL
	function updateHash() {
		encodedFilters = encodeURI(getSearchFilters());
		var urlString = 'view=' + currentView + '&sort=' + currentSort + '&zoom=' + currentZoom + '&focus=' + currentFocus[0] + ',' + currentFocus[1] + '&filters=' + encodedFilters;
		window.location.hash = urlString;
	}

	return {
		getFocus: getFocus,
		getZoom: getZoom,
		getSort: getSort,
		getView: getView,
		getSearchFilters: getSearchFilters,
		getSearchQuery: getSearchQuery,
		setFocus: setFocus,
		setZoom: setZoom,
		setSort: setSort,
		setView: setView,
		setSearchFilters: setSearchFilters,
		setSearchQuery: setSearchQuery,
		retrieveHash: retrieveHash,
		updateHash: updateHash
	};
}