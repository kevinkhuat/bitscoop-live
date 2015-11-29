define(['jquery'], function($) {
	var $menu;

	$(document).on('click', ':not(#menu)', function(e) {
		$menu = $('#menu');

		if ($menu.hasClass('open')) {
			$menu.removeClass('open');
		}
	});

	$(document).on('click', '#menu-button', function(e) {
		e.stopPropagation();
		$('#menu').addClass('open');
	});
});