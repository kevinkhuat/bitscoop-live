$(document).ready(function() {
	// using jQuery
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	var csrftoken = getCookie('csrftoken');

	var facebook_inbox_data = {};

	$.getJSON(
		'/static/obase/test/facebook/me/mapping/inbox_mapping.json',
		function(schema_mapping) {
			$.getJSON(
				'/static/obase/test/facebook/me/inbox.json',
				function(api_json) {
					facebook_inbox_data = api_json;
					var clean_data_ready_to_send_to_the_server_and_win = smokesignal().map(facebook_inbox_data, schema_mapping);
					$.ajax({
						url: '/obase/event',
						type: 'POST',
						data: JSON.stringify(clean_data_ready_to_send_to_the_server_and_win),
						dataType: 'json',
						headers: {"X-CSRFToken": csrftoken}
					}).done(function(data, xhr, response) {
						$('#result').html(JSON.stringify(data));
					}).fail(function() {
						console.log('FAILED');
					});
				});
		});
});
