function urlParser(dataInst) {
	var urlHash = '';

	//Variables for parsing the state
	var statePattern = /s=\S*?(&|$)/;
	var stateRegexResult = '';
	var currentStateEncoded = '';

	//Variables for parsing the query
	var queryPattern = /q=\S*?(&|$)/;
	var queryRegexResult = '';
	var currentQuery= '';

	function retrieveHash() {
		//Get the hash from the URL
		urlHash = window.location.hash;

		if (statePattern.test(urlHash)) {
			stateRegexResult = statePattern.exec(urlHash)[0];
			currentStateEncoded = stateRegexResult.replace('s=', '').replace('&', '');
		}
		dataInst.state = window.atob(currentStateEncoded);

		if (queryPattern.test(urlHash)) {
			queryRegexResult = queryPattern.exec(urlHash)[0];
			currentQuery = queryRegexResult.replace('q=', '').replace('&', '');
		}
		dataInst.resultCache.query_id = currentQuery;

	}

	//Update the URL hash with whatever the current properties are.  E.g. as the user moves the map around, the URL
	//has its focus coordinates updated as well, or a new search puts that search's filters and query into the URL
	function updateHash() {
		urlHash = 's=' + window.btoa(dataInst.state)+
			'&q=' + dataInst.resultCache.query_id;
		
		window.location.hash = urlHash;
	}

	return {
		retrieveHash: retrieveHash,
		updateHash: updateHash
	};
}
