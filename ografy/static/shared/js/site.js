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
			$('.drawer-toggle').not('.map').addClass('hidden');
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
		$(this).siblings('.item').toggleClass('active');
		if ($(this).hasClass('active') && $(this).closest('.flex').siblings().children().length === 0) {
			var eventType = $(this).parents('.type-grouping').attr('id');
			eventType = eventType.charAt(0).toUpperCase() + eventType.slice(1) + 's';
			$(this).siblings('.item').html('All ' + eventType);
		}
		else {
			var  eventType = $(this).parents('.type-grouping').attr('id');
			eventType = eventType.charAt(0).toUpperCase() + eventType.slice(1) + 's';
			$(this).siblings('.item').html(eventType);
		}
		if ($('#event .selector').not('.active').length === 1 || $('.selector.active').length > 1) {
			$('.filter-button').addClass('active');
		}
		else {
			$('.filter-button').removeClass('active');
		}
	});
});

function verifiedSignal(signal_id) {
	var data = {};
	data.updateFrequency = $('input:radio:checked').attr('updateFrequency');
	data.permissions = [];
	data.name = $('input[name=signal-name]')[0].value;

	$('input:checkbox').each(function() {
		data.permissions.push($(this).prop('checked'));
	});

	data.permissions = JSON.stringify(data.permissions);
	$.ajax({
		url: '/verify/' + signal_id,
		type: 'POST',
		dataType: 'json',
		data: data,
		headers: {
			'X-CSRFToken': getCookie('csrftoken')
		}
	}).done(function(data, xhr, response) {
		console.log('pants');
		window.location.pathname = data;
	}).fail(function(data, xhr, response) {
		console.log('fail');
	});
}
