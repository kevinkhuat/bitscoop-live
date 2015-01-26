var $ = require('jquery');

var oops = require('./oops');


/**
 * Placeholder.
 *
 * @constructor
 */
function JobQueue() {
	// TODO: Do we care about WeakMap privatization?
	this._library = {};
}

JobQueue.prototype = oops.proto(JobQueue, {
	/**
	 * Placeholder.
	 *
	 * @param type
	 * @param callback
	 */
	enqueue: function JobQueue$enqueue(type, callback) {
		var deferred;

		deferred = _getDeferred(this, type);
		deferred.done(callback);

		return this;
	},

	/**
	 * Placeholder.
	 *
	 * @param type
	 */
	reject: function JobQueue$reject(type) {
		var deferred;

		deferred = _getDeferred(this, type);
		deferred.reject();

		return this;
	},

	/**
	 * Placeholder.
	 *
	 * @param type
	 */
	resolve: function JobQueue$resolve(type) {
		var deferred;

		deferred = _getDeferred(this, type);
		deferred.resolve();

		return this;
	}
});


function _getDeferred(inst, type) {
	var library;

	library = inst._library;

	if (!library.hasOwnProperty(type)) {
		library[type] = $.Deferred();
	}

	return library[type];
}


module.exports = {
	JobQueue: JobQueue
};
