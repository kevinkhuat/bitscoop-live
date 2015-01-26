// Keep a reference to the last checked query and found variables.
// This improves performance on repeated calls to the same URL string.
// If the query string changes, simply re-run the logic to generate the new cached map.
var cachedSrc;
var cachedVars;
var re_parse_args = /[&;]?([^=]*)=([^&;]*)/g;


/**
 * Placeholder.
 * @param {String} [qs]
 */
function _getQuerystring(qs) {
	if (typeof qs === 'undefined') {
		if (window && window.location) {
			qs = window.location.search;
		}
	}

	if (typeof qs === 'string' && qs) {
		return (qs[0] === '?') ? qs.slice(1) : qs;
	}
}


/**
 * Returns a string representation of a querystring object.
 *
 * @param {Object} obj An object whose key/value pairs will be used to generate a querystring.
 * @returns {string} The string representation of the querystring object.
 */
function format(obj) {
	var key, str;

	str = '';

	for (key in obj) {
		if (!Object.prototype.hasOwnProperty.call(obj, key)) {
			break;
		}

		str += encodeURIComponent(key) + '=' + encodeURIComponent(obj[key]) + '&';
	}

	return str.slice(0, -1);
}


/**
 * Returns the value of a specific query variable from a valid querystring.
 *
 * @param {string} name The query variable name to retrieve.
 * @param {string} [qs=location.search] A valid URL querystring.
 * @returns {string} The decoded query variable value from the provided querystring.
 */
function get(name, qs) {
	var vars;

	qs = _getQuerystring(qs);

	if (qs === cachedSrc) {
		vars = cachedVars;
	}
	else {
		cachedSrc = qs;
		vars = cachedVars = parse(qs);
	}

	if (vars) {
		return vars[name];
	}
}


/**
 * Parses a query string from a querystring and returns a plain object hashmap of key/value pairs.
 * The query variable values are automatically decoded before they are stored.
 *
 * @param {string} [qs=location.search] The URL to scan for a query string.
 * @returns {Object} A plain object hashmap of query variable key/value pairs.
 */
function parse(qs) {
	var match, vars;

	qs = _getQuerystring(qs);
	vars = {};

	while (match = re_parse_args.exec(qs)) {
		vars[decodeURIComponent(match[1])] = decodeURIComponent(match[2]);
	}

	return vars;
}


module.exports = {
	format: format,
	get: get,
	parse: parse
};
