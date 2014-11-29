$(document).ready(function() {

	$.ajax({
			url: '/auth/signals',
			type: method.toUpperCase(),
			data: formData,
			dataType: 'json',
			headers: {"X-CSRFToken": csrftoken}
		}).done(function(data, xhr, response) {
			$('#event-result').html(JSON.stringify(data));
		}).fail(function() {
			console.log('FAILED');
		});


	$('.slide-grid').on('click', 'a', function(e) {
		service = e.target.name;
	});
});
