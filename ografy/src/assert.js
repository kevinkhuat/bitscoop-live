/**
 * Subscribes to interface standard available at:
 *     http://wiki.commonjs.org/wiki/Unit_Testing/1.0
 *
 * Based on the NodeJS implementation found at:
 *     https://github.com/joyent/node/blob/master/lib/assert.js
 */
var type = require('./type');


var native_slice = Array.prototype.slice;
if (typeof Buffer === 'undefined') {
	var Buffer = function() {};
}


/**
 * Placeholder.
 *
 * @param options
 * @constructor
 */
function AssertionError(message, options) {
	var lhs, rhs;

	if (type(message) === 'object' && arguments.length === 1) {
		options = message;
		message = void(0);
	}

	if (type(options) !== 'object') {
		options = {};
	}

	this.name = 'AssertionError';
	this.actual = options.actual;
	this.expected = options.expected;
	this.operator = options.operator;

	if (message) {
		// TODO: Harden this for `undefined` and `null`?
		this.message = message.toString();
		this.generatedMessage = false;
	}
	else {
		lhs = JSON.stringify(this.actual, _replacer);
		lhs = _truncate(lhs, 128);

		rhs = JSON.stringify(this.expected, _replacer);
		rhs = _truncate(rhs, 128);

		this.message = lhs + ' ' + this.operator + ' ' + rhs;
		this.generatedMessage = true;
	}

	Error.captureStackTrace(this, options.stackStartFunction || _fail);
}

AssertionError.prototype = new Error();


/**
 * Placeholder.
 *
 * @param actual
 * @param expected
 * @returns {*}
 * @private
 */
function _deepEqual(a, b) {
	var i;

	if (a === b) {
		return true;
	}

	if (a instanceof Buffer && b instanceof Buffer) {
		if (a.length != b.length) {
			return false;
		}

		for (i = 0; i < a.length; i++) {
			if (a[i] !== b[i]) {
				return false;
			}
		}

		return true;
	}

	if (a instanceof Date && b instanceof Date) {
		return a.getTime() === b.getTime();
	}

	if (a instanceof RegExp && b instanceof RegExp) {
		return a.source === b.source &&
			a.global === b.global &&
			a.multiline === b.multiline &&
			a.lastIndex === b.lastIndex &&
			a.ignoreCase === b.ignoreCase;
	}

	if (typeof a !== 'object' && typeof b !== 'object') {
		return a == b;
	}

	return _objEquiv(a, b);
}


/**
 * Placeholder.
 *
 * @private
 * @param message
 * @param actual
 * @param expected
 * @param operator
 * @param stackStartFunction
 */
function _fail(message, actual, expected, operator, stackStartFunction) {
	throw new AssertionError(message, {
		actual: actual,
		expected: expected,
		operator: operator,
		stackStartFunction: stackStartFunction
	});
}


/**
 * Placeholder.
 *
 * @param a
 * @param b
 * @returns {*}
 * @private
 */
function _objEquiv(a, b) {
	var i, key, aIsArgs, aKeys, bIsArgs, bKeys;

	if ((typeof a === 'undefined' || a === null) || (typeof b === 'undefined' || b === null)) {
		return false;
	}

	if (a.prototype !== b.prototype) {
		return false;
	}

	aIsArgs = type(a) === 'arguments';
	bIsArgs = type(b) === 'arguments';

	if ((aIsArgs && !bIsArgs) || (!aIsArgs && bIsArgs)) {
		return false;
	}

	if (aIsArgs) {
		a = native_slice.call(a);
		b = native_slice.call(b);

		return _deepEqual(a, b);
	}

	try {
		aKeys = Object.keys(a);
		bKeys = Object.keys(b);
	}
	catch(err) {
		return false;
	}

	if (aKeys.length !== bKeys.length) {
		return false;
	}

	aKeys.sort();
	bKeys.sort();

	for (i = 0; i < aKeys.length; i++) {
		if (aKeys[i] !== bKeys[i]) {
			return false;
		}
	}

	for (i = 0; i < aKeys.length; i++) {
		key = aKeys[i];

		if (!_deepEqual(a[key], b[key])) {
			return false;
		}
	}

	return true;
}


/**
 * Placeholder.
 *
 * @private
 * @param key
 * @param value
 * @returns {*}
 */
function _replacer(key, value) {
	if (typeof value === 'undefined') {
		return '' + value;
	}

	if (typeof value === 'number' && !isFinite(value)) {
		return value.toString();
	}

	if (value instanceof Function || value instanceof RegExp) {
		return value.toString();
	}

	return value;
}


/**
 * Placeholder.
 *
 * @param s
 * @param n
 * @returns {*}
 * @private
 */
function _truncate(s, n) {
	if (typeof s === 'string') {
		return s.length < n ? s : s.slice(0, n);
	}

	return s;
}


/**
 * Placeholder.
 *
 * @param actual
 * @param expected
 * @param message
 */
function deepEqual(actual, expected, message) {
	if (!_deepEqual(actual, expected)) {
		_fail(message, actual, expected, 'deepEqual', deepEqual);
	}
}


/**
 * Placeholder.
 *
 * @param block
 * @param message
 */
function doesNotThrow(block, message) {
	var actual;

	try {
		block();
	}
	catch(err) {
		actual = err;
	}

	message = message ? ' ' + message : '.';

	if (actual) {
		_fail('Got unwanted exception' + message);
	}
}


/***
 * Placeholder.
 *
 * @param actual
 * @param expected
 * @param message
 */
function equal(actual, expected, message) {
	if (actual != expected) {
		_fail(message, actual, expected, '==', equal);
	}
}


/**
 * Placeholder.
 *
 * @param value
 * @param message
 */
function $isFinite(value, message) {
	message = message || 'Expected finite number';

	if (!isFinite(value)) {
		_fail(message, value, 'finite number', 'isFinite', $isFinite);
	}
}


/**
 * Placeholder.
 *
 * @param value
 * @param message
 */
function $isNaN(value, message) {
	message = message || 'Expected NaN';

	if (!isNaN(value)) {
		_fail(message, value, NaN, 'isNaN', $isNaN);
	}
}


/**
 * Placeholder.
 *
 * @param actual
 * @param expected
 * @param message
 */
function notEqual(actual, expected, message) {
	if (actual == expected) {
		_fail(message, actual, expected, '!=', notEqual);
	}
}


/**
 * Placeholder.
 *
 * @param actual
 * @param expected
 * @param message
 */
function notDeepEqual(actual, expected, message) {
	if (_deepEqual(actual, expected)) {
		_fail(message, actual, expected, 'notDeepEqual', notDeepEqual);
	}
}


/**
 * Placeholder.
 *
 * @param actual
 * @param expected
 * @param {String} [message]
 */
function notStrictEqual(actual, expected, message) {
	if (actual === expected) {
		_fail(message, actual, expected, '!==', notStrictEqual);
	}
}


/**
 * Placeholder.
 *
 * @param value
 * @param message
 */
function ok(value, message) {
	if (!value) {
		_fail(message, value, true, '==', ok);
	}
}


/**
 * Placeholder.
 *
 * @param actual
 * @param expected
 * @param message
 */
function strictEqual(actual, expected, message) {
	if (actual !== expected) {
		_fail(message, actual, expected, '===', strictEqual);
	}
}


/**
 * Placeholder.
 *
 * @param block
 * @param error
 * @param message
 */
function throws(block, expected, message) {
	var actual, typ;

	typ = type(expected);

	try {
		block();
	}
	catch(err) {
		actual = err;
	}

	message = (expected && expected.name ? ' (' + expected.name + ').' : '.') + (message ? ' ' + message : '.');

	if (!actual) {
		_fail('Missing expected exception' + message);
	}

	if (typ === 'function' && !(actual instanceof expected) ||
		typ === 'string' && expected !== actual.message ||
		typ === 'regexp' && !expected.test(actual.message)) {
		_fail('Got unwanted exception');
	}
}


/**
 * Placeholder.
 *
 * @param value
 * @param expected
 * @param message
 */
function $type(value, expected, message) {
	var actual, terminator;

	actual = type(value);
	terminator = expected.charAt(expected.length - 1);

	if (terminator === '?') {
		if (value === void(0) || value === null) {
			return;
		}

		expected = expected.slice(0, -1);
	}

	if (actual !== expected) {
		_fail(message, actual, expected, 'typeof', type);
	}
}


module.exports = {
	AssertionError: AssertionError,

	deepEqual: deepEqual,
	doesNotThrow: doesNotThrow,
	equal: equal,
	isFinite: $isFinite,
	isNaN: $isNaN,
	notEqual: notEqual,
	notDeepEqual: notDeepEqual,
	notStrictEqual: notStrictEqual,
	ok: ok,
	strictEqual: strictEqual,
	throws: throws,
	type: $type
};
