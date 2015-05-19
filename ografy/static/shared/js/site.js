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
		.add('.delete-signal')
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

	$('.delete-signal').click(function() {
		$(this).parent().siblings('.delete-check').toggleClass('hidden');
	});

	$('.delete-cancel').click(function() {
		$(this).parents('.delete-check').addClass('hidden');
	});
});

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function verifiedSignal(signal_id) {
	var data = {};
	data.updateFrequency = $('input:radio:checked').attr('updateFrequency');
	data.authorizedEndpointsEnabledList = {};
	data.name = $('input[name=signal-name]')[0].value;

	$('input:checkbox').each(function() {
		var parent = $(this).parent();
		var def_id = parent.attr('data-endpoint-definition-id');
		var auth_id = parent.attr('data-authorized-endpoint-id');
		data.authorizedEndpointsEnabledList[def_id] = {};
		data.authorizedEndpointsEnabledList[def_id][auth_id] = $(this).prop('checked')
	});

	data.authorizedEndpointsEnabledList = JSON.stringify(data.authorizedEndpointsEnabledList);
	$.ajax({
		url: '/verify/' + signal_id,
		type: 'POST',
		'content-type': 'application/json',
		dataType: 'text',
		data: data,
		headers: {
			'X-CSRFToken': getCookie('csrftoken')
		}
	}).done(function(data, xhr, response) {
		window.location.pathname = data;
	}).fail(function(data, xhr, response) {
		console.log('fail');
	});
}

function updateName(user_id) {
	var data = {};
	data.first_name = $('input[name="first_name"]')[0].value;
	data.last_name = $('input[name="last_name"]')[0].value;
	$.ajax({
		url: '/opi/user/' + user_id,
		type: 'PATCH',
		dataType: 'json',
		data: data,
		headers: {
			'X-CSRFToken': getCookie('csrftoken')
		}
	}).done(function(data, xhr, response) {
		console.log('succeeded');
	}).fail(function(data, xhr, response) {
		console.log('failed');
	});
}

function updateEmail(user_id) {
	var data = {};
	data.email = $('input[name="email"]')[0].value;
	$.ajax({
		url: '/opi/user/' + user_id,
		type: 'PATCH',
		dataType: 'json',
		data: data,
		headers: {
			'X-CSRFToken': getCookie('csrftoken')
		}
	}).done(function(data, xhr, response) {
		console.log('succeeded');
	}).fail(function(data, xhr, response) {
		console.log('failed');
	});
}

// TODO: Fix, not working with hashing.
function updatePassword(user_id) {
	var data = {};
	data.password = $('input[name="new_password"]')[0].value;
	$.ajax({
		url: '/opi/user/' + user_id,
		type: 'PATCH',
		dataType: 'json',
		data: data,
		headers: {
			'X-CSRFToken': getCookie('csrftoken')
		}
	}).done(function(data, xhr, response) {
		console.log('succeeded');
	}).fail(function(data, xhr, response) {
		console.log('failed');
	});
}

function updateHandle(user_id) {
	var data = {};
	data.handle = $('input[name="handle"]')[0].value;
	$.ajax({
		url: '/opi/user/' + user_id,
		type: 'PATCH',
		dataType: 'json',
		data: data,
		headers: {
			'X-CSRFToken': getCookie('csrftoken')
		}
	}).done(function(data, xhr, response) {
		console.log('succeeded');
	}).fail(function(data, xhr, response) {
		console.log('failed');
	});
}

function toggleSignal(signal_id) {
	var data = {};
	data.enabled = !($('#onoffswitch-' + signal_id)[0].checked);
	$.ajax({
		url: '/opi/signal/' + signal_id,
		type: 'PATCH',
		dataType: 'json',
		data: data,
		headers: {
			'X-CSRFToken': getCookie('csrftoken')
		}
	}).done(function(data, xhr, response) {
		console.log('succeeded');
	}).fail(function(data, xhr, response) {
		console.log('failed');
	});
}

function deleteSignal(signal_id) {
	$.ajax({
		url: '/opi/signal/' + signal_id,
		type: 'DELETE',
		dataType: 'json',
		data: data,
		headers: {
			'X-CSRFToken': getCookie('csrftoken')
		}
	}).done(function(data, xhr, response) {
		console.log('succeeded');
	}).fail(function(data, xhr, response) {
		console.log('failed');
	});
}
