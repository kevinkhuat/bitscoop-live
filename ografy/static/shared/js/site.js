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
	$('.user-button').click(function () {
		$('.menu.main').toggleClass('hidden');
	});

	$(document.body).click(function (e) {
		if (e.target.className !== ('user-button item') &&
			e.target.className !== ('item')) {
			$('.menu.main').addClass('hidden');
		}
	});

	$('.drawer-toggle').click(function() {
		$('.left.drawer').toggleClass('hidden');
		$('.drawer-toggle').toggleClass('hidden');
	});

	$(document.body).click(function (e) {
		if (e.target.className !== ('drawer-toggle icon-paragraph-justify') &&
			e.target.className !== ('link')) {
			$('.left.drawer').addClass('hidden');
			$('.drawer-toggle').addClass('hidden');
		}
	});

	$('.menu .item')
		.add('header nav .item')
		.add('.signal-button')
		.add('ul.links > li > *')
		.add('.filter-button')
		.add('.dropdown span')
		.add('.filter.button')
		.add('.list.item')
		.mouseenter(function() {
			$(this).addClass('hover');
		});

	$('.menu .item')
		.add('header nav .item')
		.add('.signal-button')
		.add('ul.links > li > *')
		.add('.filter-button')
		.add('.dropdown span')
		.add('.filter.button')
		.add('.list.item')
		.mouseleave(function() {
			$(this).removeClass('hover');
		});

	$('.menu .item')
		.add('header nav .item')
		.add('.signal-button')
		.add('ul.links > li > *')
		.add('.filter-button')
		.add('.dropdown span')
		.add('.filter.button')
		.add('.list.item')
		.click(function() {
			$(this).removeClass('hover');
		});
});