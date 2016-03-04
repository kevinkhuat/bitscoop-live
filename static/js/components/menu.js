define(['jquery', 'minimodal', 'templates'], function($) {
	var exports;

	function open() {
		$('#menu').addClass('open');
	}

	function close() {
		$('#menu').removeClass('open');
	}

	$(document).on('click', function(e) {
		var $menu, $target;

		$target = $(e.target);
		$menu = $('#menu');

		if ($menu.hasClass('open') && ($target.closest('#menu').length === 0)) {
			close();
		}
	});

	$(document).on('click', '#menu .menu header', close);

	$(document).on('click', '#menu-button', function(e) {
		e.stopPropagation();
		open();
	});

	$('#menu').on('click', '.menu .views > div:first-child, .menu .sort > div:first-child', function(e) {
		var $siblings, $this = $(this);

		$siblings = $this.parent().siblings();

		$siblings.children('div:first-child').removeClass('active');
		$this.toggleClass('active');
	});

	exports = {
		close: close,
		open: open
	};

	return exports;
});
