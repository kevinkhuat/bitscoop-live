define(['jquery', 'jquery-mixitup'], function($) {
	$(document).ready(function() {
		$('#provider-grid').mixItUp();
	});

	$(document).on('click', '.mix', function() {
		var $this = $(this);

		window.location = $this.data('link');
	});

	$('#done').on('click', function(e) {
		window.location.href = '/explore';
	});

	$('main')
		.on('click', '.mobile-placeholder', function() {
			var $this = $(this);

			$('.filter').toggleClass('visible');

			flipIcon($this.find('i'));
		})
		.on('click', '.filter', function() {
			var dataFilter, $placeholder, $this = $(this);
			$placeholder = $('.mobile-placeholder');
			dataFilter = $this.data('filter');
			if (dataFilter.charAt(0) === '.') {
				dataFilter = dataFilter.slice(1);
			}
			window.location.hash = dataFilter;
			if ($placeholder.css('display') !== 'none') {
				$placeholder.children('.placeholder-text').html($this.html());
				$('.filter').toggleClass('visible');
				$('#filters').toggleClass('open');
			}

			flipIcon($placeholder.find('i'));
		});

	function flipIcon($icon) {
		if ($icon.hasClass('fa-caret-down')) {
			$icon.removeClass('fa-caret-down').addClass('fa-caret-up');
		}
		else {
			$icon.removeClass('fa-caret-up').addClass('fa-caret-down');
		}
	}
});
