$(document).ready(function() {
//	function getCookie(name) {
//	    var cookieValue = null;
//	    if (document.cookie && document.cookie != '') {
//	        var cookies = document.cookie.split(';');
//	        for (var i = 0; i < cookies.length; i++) {
//	            var cookie = jQuery.trim(cookies[i]);
//	            // Does this cookie string begin with the name we want?
//	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
//	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//	                break;
//	            }
//	        }
//	    }
//	    return cookieValue;
//	}
//
//	var csrftoken = getCookie('csrftoken');
//
//	$.ajax({
//		url: '/opi/provider',
//		type: 'GET',
//		headers: {"X-CSRFToken": csrftoken}
//	}).done(function(data, xhr, response){
//		console.log(data);
////		if
////		$('');
//	}).fail(function(){
//		console.log('FAILED');
//	});

//	$.ajax({
//		url: '/auth/signals',
//		type: method.toUpperCase(),
//		data: formData,
//		dataType: 'json',
//		headers: {"X-CSRFToken": csrftoken}
//	}).done(function(data, xhr, response) {
//		$('#event-result').html(JSON.stringify(data));
//	}).fail(function() {
//		console.log('FAILED');
//	});

//	$('.signal-button').on('click', function(e) {
//		service = e.target.name;
//		window.location="http://dev.ografy.io:8000/signals/1";
////		$.ajax({
////			url: '/opi/signal',
////			type: 'POST',
////			headers: {'X-CSRFToken': csrftoken},
////			data: false
////		})
//	});

	function getFilter() {
		var filters = [];
		$('#filters .active').each(function(i, el) {
			filters.push($(el).data('filter'));
		})

		return filters.join(',');
	}


	var $container = $('#isotope-container').isotope({
	  // options
	});


	// filter items on button click
	$('#filters').on( 'click', 'span', function() {
		$(this).toggleClass('active');
		var filterValue = getFilter();

		$container.isotope({ filter: filterValue });
	});
});
