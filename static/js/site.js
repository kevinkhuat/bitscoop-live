define(['ga', 'jquery', 'nunjucks', 'jquery-cookie', 'jquery-regexp-selector'], function(ga, $, nunjucks) {
	$(document).ready(function() {
		var cookieConsent, html;

		cookieConsent = $.cookie('cookieconsent');

		if (!cookieConsent) {
			html = nunjucks.render('components/cookie-consent.html');
			$('body').append(html);
		}

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

		$(document).on('click', '.cookie-consent button', function() {
			$.cookie('cookieconsent', true, {
				expires: 365,
				path: '/'
			});

			$('.cookie-consent').remove();
		});
	});

	// Google Analytics dependency may be undefined if the user is running ad blockers or ghostery.
	if (ga) {
		ga('create', 'UA-65896068-1', 'auto');
		ga('send', 'pageview');
	}
});
