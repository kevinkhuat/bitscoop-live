//FIXME: This was an attempt at dynamically resizing the information boxes on the front page ("Bring your services together", etc.)
//so that each pair of boxes has the same height.
//It wasn't working as intended, but I didn't want to delete it entirely in case I come back to it.

//$(document).ready(function() {
//	sizeWindows();
//
//	$(window).resize(function() {
//		sizeWindows();
//	});
//});
//
//function sizeWindows() {
//	var flexInfos = $('.flex.wrap.info');
//	for (var i = 0; i < flexInfos.length; i++) {
//		var descendants = $(flexInfos[i]).find('.square-set');
//		var maxHeight = 0;
//		for (var j = 0; j < descendants.length; j++) {
//			var thisDesc = $(descendants[j]);
//			if (thisDesc.height() > maxHeight) {
//				maxHeight = thisDesc.height();
//			}
//		}
//		for (var k = 0; k < descendants.length; k++) {
//			$(descendants[k]).height(maxHeight);
//		}
//	}
//}
$(document).ready(function() {
	var renderDark = true;

	if (renderDark) {
		setColorScheme ('dark');
	}
	else {
		setColorScheme ('light');
	}
	$('.user-button').click(function() {
		$('.menu.main').toggleClass('hidden');
	});

	$(document.body).click(function(e) {
		if (!e.target.classList.contains('item')) {
			$('.menu.main').addClass('hidden');
		}
	});

	$('.drawer-toggle').click(function() {
		$('.left.drawer').toggleClass('hidden');
		$('.drawer-toggle').toggleClass('hidden');
	});

	$(document.body).click(function(e) {
		if (!e.target.classList.contains('drawer-toggle') &&
			!e.target.classList.contains('link')) {
			$('.left.drawer').addClass('hidden');
			$('.drawer-toggle').addClass('hidden');
		}
	});

	$('.fullscreen').click(function() {
		if (document.webkitFullscreenEnabled) {
			if (document.webkitIsFullScreen) {
				document.webkitCancelFullScreen();
			}
			else {
				document.documentElement.webkitRequestFullscreen();
			}
		}
		else if (document.mozFullScreenEnabled) {
			if (document.mozFullScreen) {
				document.mozCancelFullScreen();
			}
			else {
				document.documentElement.mozRequestFullScreen();
			}
		}
		else if (document.msFullscreenEnabled) {
			if (document.msIsFullScreen) {
				document.msCancelFullScreen();
			}
			else {
				document.documentElement.msRequestFullscreen();
			}
		}
		else {
			if (document.isFullScreen) {
				document.cancelFullScreen();
			}
			else {
				document.documentElement.requestFullscreen();
			}
		}
	});

	$('header nav .item')
		.add('.menu .add-filter')
		.add('.signal-button')
		.add('ul.links > li > *')
		.add('.filter-button')
		.add('.dropdown span')
		.add('.list.item')
		.add('.selector')
		.mouseenter(function() {
			$(this).addClass('hover');
		})
		.mouseleave(function() {
			$(this).removeClass('hover');
		})
		.click(function() {
			if (window.window.devicePixelRatio > 1.5) {
				$(this).removeClass('hover');
			}
		});

	$('.menu .add-filter').click(function() {
		$('.filter-button').addClass('active');
	});

	$('.selector').click(function() {
		$(this).toggleClass('active');
		if ($('.selector').not('.active').length > 0) {
			$('.filter-button').addClass('active');
		}
		else {
			$('.filter-button').removeClass('active');
		}
	});
});

function setColorScheme(scheme) {
		var renderStyle = (scheme === 'light') ? ('light') : 'dark';
		var mainLink  = document.createElement('link');
		var siteLink  = document.createElement('link');
		mainLink.rel = "stylesheet";
		siteLink.rel  = "stylesheet";
		mainLink.type = "text/css";
		siteLink.type = "text/css";
		mainLink.href = "/static/core/css/main/main-" + renderStyle + ".css";
		siteLink.href = "/static/shared/css/site-" + renderStyle + ".css";

		document.head.appendChild(mainLink);
		document.head.appendChild(siteLink);
	}