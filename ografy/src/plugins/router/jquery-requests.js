var $ = require('jquery');
var router = require('../../router');


function makeRequest(url, opts) {
	var deferred, id, that = this;

	// if cached, just return cached data instead of AJAX.
	//that.getData(getId.call(this,url));

	deferred = $.Deferred();

	$.ajax(url, opts)
		.done(function(data, event, req) {
			var args;

			args = Array.prototype.slice.call(arguments);
			args.push(that.parseData(data));

			deferred.resolveWith(this, args);
		})
		.fail(function() {
			// FIXME: Can rejectWith map arguments?
			deferred.rejectWith(this, arguments);
		});

	return deferred.promise();
}

router.settings.makeRequest = makeRequest;
