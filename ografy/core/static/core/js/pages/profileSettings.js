define(['jutsu', 'jquery-cookie'], function(jutsu) {
	$(document).ready(function() {
		$('body').autoform('.autoformEnabled', {
			'X-CSRFToken': $.cookie('csrftoken')
		});
	});
});
