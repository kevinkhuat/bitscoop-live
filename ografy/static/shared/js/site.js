//This was an attempt at dynamically resizing the information boxes on the front page ("Bring your services together", etc.)
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