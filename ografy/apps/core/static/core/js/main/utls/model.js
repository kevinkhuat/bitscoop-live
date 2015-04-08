//View pertaining to obtaining and searching for data
function dataStore() {
	//This is the array of events that is returned from a search
	var resultData = [];

	//This is a dictionary of the IDs of events that have been obtained in previous searches
	var eventIndex = {};

	//This is the master list of events that have been obtained in previous searches
	var eventData = [];

	//This is the list of events in the current search that have not been obtained in previous searches
	var newData = [];

	//This is the collection of HTML elements that are rendered from eventData
	//Most of them will be set to invisible since only ones from the current search
	//should be displayed.
	var eventHTML = '';

	var currentViewInst = '';

	//Data model
	function getEventData() {
		return eventData;
	}

	function getResultData() {
		return resultData;
	}

	function setCurrentView(inst) {
		currentViewInst = inst;
	}

	function getCurrentView() {
		return currentViewInst;
	}

	function updateData() {
		newData = [];
		for (var item in resultData) {
			var currentId = resultData[item].id;

			var removed = false;
			var keys = Object.keys(eventIndex);
			for (var index in keys) {
				if (currentId === keys[index]) {
					removed = true;
				}
			}
			if (removed === false) {
				newData.push(resultData[item]);
				eventIndex[currentId] = true;
				eventData.push(resultData[item]);
			}
		}

		var listItems = nunjucks.render('list/event_list.html',
			{
				eventData: newData
			});
		$('#event-list').append(listItems);

		currentEvents = $('#event-list *');
		for (var index in eventData) {
			var found = false;
			var thisEvent = eventData[index];
			var id = thisEvent.id;
			for (var item in resultData) {
				var thisItem = resultData[item];
				if (id === thisItem.id) {
					found = true;
				}
			}

			if (found === true) {
				$('div[event-id=' + id + ']').addClass('active');
			}
			else if (found === false) {
				$('div[event-id=' + id + ']').removeClass('active');
			}
		}
	}

	//Search for items in the database based on the search parameters and filters
	function search(eventType, searchString, orderString) {
		var cookie = sessionsCookies().getCsrfToken();
		var url = 'opi/' + eventType + '?page=1&ordering='+ orderString + '&filter=' + searchString;
		console.log(url);
		$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			headers: {
				'X-CSRFToken': cookie
			}
		}).done(function(data, xhr, response) {
			if (data.count > 0) {
				results = data.results
				for (var index in results) {
					results[index].updated = new Date(results[index].updated).toLocaleString();
					results[index].created = new Date(results[index].created).toLocaleString();
					results[index].datetime = new Date(results[index].datetime).toLocaleString();
				}
				//resultData = results.sort(function(a, b) {
				//	return Date.parse(b.datetime) - Date.parse(a.datetime);
				//});
				resultData = results;
				updateData();
				currentViewInst.updateContent();
			}
			else if (data.count === 0) {
			}
		});
	}

	return {
		getEventData: getEventData,
		getResultData: getResultData,
		setCurrentView: setCurrentView,
		getCurrentView: getCurrentView,
		updateData: updateData,
		search: search
	};
}

