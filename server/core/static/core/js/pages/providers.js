define(['jquery', 'jquery-mixitup'], function($) {
	$(document).ready(function() {
		$('#provider-grid').mixItUp();
	});

	$(document).on('click', '.mix', function() {
		var $this = $(this);

		if (!($this.hasClass('associated'))) {
			window.location = $this.data('link');
		}
		else {
			window.location = '/settings/connections?provider=' + $this.data('id');
		}
	});

	$('#done').on('click', function(e) {
		window.location.href = '/explore';
	});
});
