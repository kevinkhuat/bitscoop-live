$(document).ready(function () {
	$('a.options').bind('click', function (e) {
		e.preventDefault();
		$('#request_wrapper_method').val('OPTIONS');
		$('#request_wrapper').submit();
	});
	
	$('a.delete').bind('click', function (e) {
		e.preventDefault();
		$('#request_wrapper_method').val('DELETE');
		$('#request_wrapper').submit();
	});
});


$.GET = function (url, data, callback, type) {
	if ($.isFunction(data)) {
		callback = data;
		type = callback;
		data = null;
	}
	
	if (!type) {
		type = 'json';
	}

	return $.ajax({
		type: 'GET',
		url: url,
		data: data,
		success: callback,
		dataType: type,
		async: true
	});
};