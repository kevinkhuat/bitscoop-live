var querystring = require('./querystring');


var re_parse_url = /^((?:([^:\/?#]+):\/\/)?([^\/?#]*)?(\/[^?#]*)?)(\?[^#]*)?(#.*)?$/;


/**
 * Placeholder.
 * @param {String} [url]
 */
function _getUrl(url) {
	if (typeof url === 'undefined') {
		if (window && window.location) {
			url = window.location.href;
		}
	}

	if (typeof url === 'string' && url) {
		return url;
	}
}


/**
 * Returns a string representation of a parsed URL.
 *
 * @returns {string} The string representation of a parsed URL.
 */
function format(obj) {
	var fragment, host, path, port, protocol, query, str;

	host = obj.host || obj.hostname;

	if (!host) {
		throw new SyntaxError('URL invalid without a host');
	}

	str = '';
	fragment = obj.fragment || obj.hash;
	path = obj.path || obj.pathname;
	port = obj.port;
	protocol = obj.protocol;
	query = obj.query || obj.search || obj.vars;

	if (typeof query === 'object') {
		query = querystring.format(query);
	}

	if (protocol) {
		str += protocol + '://';
	}

	str += host;

	if (port) {
		str += (~host.indexOf(':') ? ':' : '') + port;
	}

	if (path) {
		if (path[0] !== '/') {
			str += '/';
		}

		str += path;
	}

	if (query) {
		if (query[0] !== '?') {
			str += '?';
		}

		str += query;
	}

	if (fragment) {
		if (fragment[0] !== '#') {
			str += '#';
		}

		str += fragment;
	}

	return str;
}


/**
 * Returns a Java convention formatted namespace for a URL.
 *
 * @param {String} str The URL string to be parsed into a namespace.
 * @param {String}xN Extra namespace qualifiers to add to the end of the derived namespace
 * @returns {String} The namespace of the URL.
 */
function namespace(str) {
	var i, authority, match, name;

	str = _getUrl(str);

	match = re_parse_url.exec(str);
	if (match === null || !match[3]) {
		throw new SyntaxError('Invalid url `' + str + '`');
	}

	authority = match[3];
	if (~(i = authority.indexOf(':'))) {
		authority = authority.slice(0, i);
	}

	name = authority.split('.').reverse().join('.');

	for (i = 1; i < arguments.length; i++) {
		name += ':' + arguments[i];
	}

	return name;
}


/**
 * Parses a URL string into components:
 *   fragment - The fragment of the URL.
 *   hash - The fragment of the URL preceded with the hash (#) character.
 *   host - The domain name including any subdomain components and port information.
 *   hostname - The domain name including any subdomain components and excluding the port information.
 *   location - The protocol, domain (including subdomains), port, and path as a single string.
 *   path - The path of the URL preceded with a leading slash (/).
 *   port - The port of the URL.
 *   protocol - The protocol of the URL (e.g. https, ftp, git).
 *   query - The querystring of the URL.
 *   search - The querystring of the URL with a preceding question mark (?).
 *
 * @param {String} [str=window.location.href] The URL string to be parsed into components.
 * @param {Boolean} [full] A Boolean flag to indicate whether the querystring should be parsed into individually accessible variables.
 */
function parse(str, full) {
	var i, hash, host, match, obj, query, search;

	str = _getUrl(str);

	obj = {};
	match = re_parse_url.exec(str);

	if (match === null) {
		throw new SyntaxError('Invalid url: ' + str);
	}

	obj.fragment = null;
	obj.hash = hash = match[6] || null;
	obj.host = host = match[3] || null;
	obj.hostname = host || null;
	obj.location = match[1] || null;
	obj.path = match[4] || null;
	obj.port = null;
	obj.protocol = match[2] || null;
	obj.query = null;
	obj.search = search = match[5] || null;

	if (~(i = host.indexOf(':'))) {
		obj.hostname = host.slice(0, i);
		obj.port = host.slice(i + 1);
	}

	if (hash) {
		obj.fragment = hash.slice(1);
	}

	if (search) {
		obj.query = query = search.slice(1);
	}

	if (full === true && query) {
		obj.vars = querystring.parse(query);
	}

	return obj;
}


module.exports = {
	format: format,
	namespace: namespace,
	parse: parse
};
