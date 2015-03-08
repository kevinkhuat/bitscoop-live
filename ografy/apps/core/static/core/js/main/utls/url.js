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

	function updateHash() {
		var urlString = 'view=' + currentView + '&zoom=' + currentZoom + '&focus=' + currentFocus[1] + ',' + currentFocus[0];
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
		retrieveHash: retrieveHash,
		updateHash: updateHash
	};
}