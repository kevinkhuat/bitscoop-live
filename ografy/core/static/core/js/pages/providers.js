define(['jquery', 'jquery-mixitup'], function($) {
	$(document).ready(function() {
		$('#provider-grid').mixItUp();
	});

	$(document).on('click', '.mix', function() {
		$this = $(this);
		if (!($this.hasClass('associated'))) {
			window.location = $this.data('link');
		}
	});
});
