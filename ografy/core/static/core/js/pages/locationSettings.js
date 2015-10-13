define(['jutsu', 'location', 'jquery-cookie'], function(jutsu, location) {
	$(document).ready(function() {
		$('body').autoform('.autoformEnabled', {
			'X-CSRFToken': $.cookie('csrftoken')
		});

		$('.estimate').not('disabled').click(function() {
			location.estimate(1);
		});
	});
});
