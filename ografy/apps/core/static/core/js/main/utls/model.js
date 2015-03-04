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
				$('div[data-id=' + id + ']').addClass('active');
			}
			else if (found === false) {
				$('div[data-id=' + id + ']').removeClass('active');
			}
		}
	}

	//Search for items in the database based on the search parameters and filters
	function search(searchString) {
		var cookie = sessionsCookies().getCsrfToken();
		var url = 'opi/event?filter=' + searchString;
		$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			headers: {
				'X-CSRFToken': cookie
			}
		}).done(function(data, xhr, response) {
		for (index in data) {
			data[index].updated = new Date(data[index].updated).toLocaleString();
			data[index].created = new Date(data[index].created).toLocaleString();
			data[index].datetime = new Date(data[index].datetime).toLocaleString();
		}
			resultData = data.sort(function(a, b) {return Date.parse(b.datetime)-Date.parse(a.datetime)});
			updateData();
			currentViewInst.updateContent();
		});
	}

	return {
		getEventData: getEventData,
		getResultData: getResultData,
		setCurrentView: setCurrentView,
		updateData: updateData,
		search: search
	};
}

