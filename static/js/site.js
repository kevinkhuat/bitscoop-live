define(['ga', 'jquery', 'jquery-regexp-selector'], function(ga, $) {
	$(document).ready(function() {
		// TODO: Highlight active links?
		//$('a:regex(href,^' + location.pathname + ')').addClass('active');

		$(document).on('click', '.modal .content', function(e) {
			e.stopPropagation();
		});

		$(document).on('modalopen', function() {
			$('body').addClass('modal-open');
		});

		$(document).on('modalclose', function() {
			$('body').removeClass('modal-open');
		});
	});

	ga('create', 'UA-65896068-1', 'auto');
	ga('send', 'pageview');
});
