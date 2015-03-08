function urlParser() {
	var urlHash = '';

	var viewPattern = /view=\S*?(&|$)/;
	var viewRegexResult = '';
	var currentView = '';

	var zoomPattern = /zoom=\S*?(&|$)/;
	var zoomRegexResult = '';
	var currentZoom = 0;

	var focusPattern = /focus=\S*?(&|$)/;
	var focusRegexResult = '';
	var currentFocus = [];
	var currentFocusString = '';

	var sortPattern = /sort=\S*?(&|$)/;
	var sortRegexResult = '';
	var currentSort = '';

	var filtersPattern = /filters=\S*?(&|$)/;
	var filtersRegexResult = '';
	var currentFilters = '';

	var queryPattern = /query=\S*?(&|$)/;
	var queryRegexResult = '';
	var currentQuery = '';

	function retrieveHash() {
		urlHash = window.location.hash;

		if (focusPattern.test(urlHash)) {
			focusRegexResult = focusPattern.exec(urlHash)[0];
			currentFocusString = focusRegexResult.replace('focus=', '').replace('&', '');
			currentFocus = currentFocusString.split(',');
			for (var index in currentFocus) {
				currentFocus[index] = parseFloat(currentFocus[index]);
			}
		}
		else {
			focusRegexResult = '';
			currentFocus = '';
		}

		if (sortPattern.test(urlHash)) {
			sortRegexResult = sortPattern.exec(urlHash)[0];
			currentSort = sortRegexResult.replace('sort=', '').replace('&', '');
		}
		else {
			sortRegexResult = '';
			currentSort = '';
		}

		if (viewPattern.test(urlHash)) {
			viewRegexResult = viewPattern.exec(urlHash)[0];
			currentView = viewRegexResult.replace('view=', '').replace('&', '');
		}
		else {
			viewRegexResult = '';
			currentView = '';
		}

		if (zoomPattern.test(urlHash)) {
			zoomRegexResult = zoomPattern.exec(urlHash)[0];
			currentZoom = parseInt(zoomRegexResult.replace('zoom=', '').replace('&', ''));
		}
		else {
			zoomRegexResult = '';
			currentZoom = 0;
		}

		if (filtersPattern.test(urlHash)) {
			filtersRegexResult = filtersPattern.exec(urlHash)[0];
			currentFilters = filtersRegexResult.replace('filters=', '').replace('&20', ' ').replace('&', '');
		}
		else {
			filtersRegexResult = '';
			currentFilters = '';
		}

		if (queryPattern.test(urlHash)) {
			queryRegexResult = queryPattern.exec(urlHash)[0];
			currentQuery = queryRegexResult.replace('query=', '').replace('&20', ' ').replace('&', '');
		}
		else {
			queryRegexResult = '';
			currentQuery = '';
		}
	}

	function getFocus() {
		return currentFocus;
	}

	function getSort() {
		return currentSort;
	}

	function getView() {
		return currentView;
	}

	function getZoom() {
		return currentZoom;
	}

	function setFocus(input) {
		currentFocus = input;
	}

	function setSort(input) {
		currentSort = input;
	}

	function setView(input) {
		currentView = input;
	}

	function setZoom(input) {
		currentZoom = input;
	}

	function getSearchFilters() {
		return currentFilters;
	}

	function getSearchQuery() {
		return currentQuery;
	}

	function setSearchFilters(input) {
		currentFilters = input;
	}

	function setSearchQuery(input) {
		currentQuery = input;
	}

	function updateHash() {
		var urlString = 'view=' + currentView + '&zoom=' + currentZoom + '&focus=' + currentFocus[1] + ',' + currentFocus[0] + '&filters=' + currentFilters;
		window.location.hash = urlString;
	}

	return {
		getFocus: getFocus,
		getSort: getSort,
		getView: getView,
		getZoom: getZoom,
		setFocus: setFocus,
		setSort: setSort,
		setView: setView,
		setZoom: setZoom,
		getSearchFilters: getSearchFilters,
		getSearchQuery: getSearchQuery,
		setSearchFilters: setSearchFilters,
		setSearchQuery: setSearchQuery,
		retrieveHash: retrieveHash,
		updateHash: updateHash
	};
}