define(['jquery', 'jquery-mixitup'], function($) {
	function flipIcon() {
		if ($('body').hasClass('ctl-expand')) {
			$('.mobile-selector i').removeClass('fa-caret-down').addClass('fa-caret-up');
		}
		else {
			$('.mobile-selector i').removeClass('fa-caret-up').addClass('fa-caret-down');
		}
	}

	$(document).ready(function() {
		$('#provider-grid').mixItUp();

		$(document).on('click', '.mix', function() {
			var $this = $(this);

			window.location = $this.data('link');
		});

		$('#done').on('click', function(e) {
			window.location.href = '/';
		});

		$(document).on('click', '.mobile-selector', function() {
			$('body').toggleClass('ctl-expand');
			flipIcon();
		});

		$(document).on('click', '.filter', function() {
			var $this = $(this);

			$('body').removeClass('ctl-expand');
			$('.mobile-selector').children('.placeholder-text').text($this.text());

			flipIcon();
		});
	});
});
