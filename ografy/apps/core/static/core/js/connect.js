function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
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

var signalTemplate = {
	'user': null,
	'provider': null,
	'name': null,
	'verified': false,
	'complete': false
};

function postNewSignal(signalData) {
	var csrftoken = getCookie('csrftoken');
	$.ajax({
		url: '/opi/signal',
		type: 'POST',
		data: signalData,
		dataType: 'json',
		headers: {"X-CSRFToken": csrftoken}
	}).done(function(data, xhr, response) {
		window.location = reverse('core_authorize');
	}).fail(function() {
		console.log('FAILED');
	});
}


function createConnectSignal(providerId, defaultName, userId/*, psaUrl*/) {
	//First, create a signal from signalTemplate
	var newSignal = signalTemplate;
	newSignal.user = userId;
	newSignal.provider = providerId;
	newSignal.name = defaultName;
	//Second, post new signal with given provider (goes to OPI)
	postNewSignal(newSignal);
	//When done, navigate to psaURL
}
