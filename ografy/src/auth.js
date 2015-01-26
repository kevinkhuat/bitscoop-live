var $ = require('jquery');
var oops = require('./oops');


var defaultOptions = {
	baseURL: 'dev.ografy.io:8000',
	associateURL: '/associate/',
	signalsURL: '/signals/',
	callURL: '/call/',
	proxyURL: '/proxy/'
};


/**
 * The base functionality and interface for an authentication method. Not intended to be instantiated directly.Used
 * for instanceof checks on prototype chains to make sure that an Auth instance is actually a BaseAuth sub-class.
 *
 * @constructor
 */
function BaseAuth() {}

BaseAuth.prototype = oops.proto(BaseAuth, {
	/**
	 * Placeholder.
	 */
	preflight: function BaseAuth$preflight() {
		console.log(this);
	}
});


/**
 * Auth object to be used for making authorized API calls and Proxy calls for a single signal.
 * Auth object is configured using a JSON object config.
 * config has five properties:
 *
 * @constructor
 * @param {Object} [config]  A configuration object.
 * @config {String} [baseURL] root directory of the server domain
 * @config {String} [associateURL] authorization endpoint for logging in
 * @config {String} [signalsURL] returns a list of all logged in backends
 * @config {String} [callURL] endpoint for making API calls where the server wraps the AJAX calls in authorization headers such as OAuth
 * @config {String} [proxyURL] endpoint for making API calls where the server acts as a call proxy
 */
function Auth(config, backend, backend_id) {
	this.backend = backend;
	this.backend_id = backend_id;
	this.config = Object.create(config || defaultOptions);
}

Auth.prototype = oops.extend(BaseAuth, {
	/**
	 * Login to a backend using stored access and secret tokens
	 *
	 * @param {String} access_token
	 * @param {String} access_token_secret
	 * @returns {$.promise}
	 */
	associate: function Auth$associate(access_token, access_token_secret) {
		var options;

		options = {
			access_token: access_token,
			access_token_secret: access_token_secret
		};

		return $.get(this.config.baseURL + this.config.associateURL + '/' + this.backend + '/', options);
	},

	/**
	 * Send an API call.  The backend and backend_id are present to verify
	 * that calls are being sent to the correct service.
	 *
	 * @param {String} api_call_url
	 * @returns {$.promise}
	 */
	call: function Auth$call(api_call_url) {
		var options;

		options = {
			backend_id: this.backend_id,
			api_call_url: api_call_url
		};

		return $.get(this.config.baseURL + this.config.call + '/' + this.backend + '/', options);
	},

	/**
	 * Send a proxy API call
	 *
	 * @param {String} api_call_url
	 * @returns {$.promise}
	 */
	proxy: function Auth$proxy(api_call_url) {
		var options = {
				api_call_url: api_call_url
			};
		return $.get(this.config.baseURL + this.config.proxyURL, options);
	}
});


/**
 * Get the list of signal backends into which you're already logged in
 *
 * @returns {$.promise}
 */
function signals() {
	var options;

	options = {};

	return $.get(defaultOptions.baseUrl + defaultOptions.signalsURL, options);
}


module.exports = {
	BaseAuth: BaseAuth,
	Auth: Auth,
	signals: signals
};
