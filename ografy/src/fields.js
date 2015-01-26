var assert = require('./assert');
var oops = require('./oops');
var options = require('./options');
var type = require('./type');


// We need a reference to the returned module so that `getField` will work properly.
var exports;
var settings = {
	breakValidation: true
};
// Built-in synonym alias mapping for field types.
var synonyms = {
	date: 'DateField',
	datetime: 'DateField',

	num: 'NumberField',
	number: 'NumberField',

	int: 'IntegerField',
	integer: 'IntegerField',

	char: 'CharField',
	character: 'CharField',
	str: 'CharField',
	string: 'CharField',

	email: 'EmailField'
};


/**
 * The base functionality and interface for a Field. Not intended to be instantiated directly. However doing so is
 * entirely possible and functional. Establishes a base prototype so that sub-classes have access to the
 * `BaseField$parse` and `BaseField$validate` methods should they not override the functionality in their own
 * prototypes. Additionally establishes default values for common boolean flags `nullable` and `readonly`.
 *
 * @constructor
 * @param {Object} [opts] A configuration object.
 * @config {Boolean} [nullable] A boolean flag indicating whether the field instance is nullable.
 * @config {Boolean} [readonly] A boolean flag indicating whether the field instance is readonly.
 * @config {Array} [validators] An array of custom validator functions that will be run in conjunction with the built-in field validators.
 */
function BaseField(opts) {
	var nullable, readonly, validators;

	opts = options.create(opts);

	if (options.has(opts, 'nullable')) {
		this.nullable = options.pop(opts, 'nullable');
		assert.type(this.nullable, 'boolean');
	}

	if (options.has(opts, 'readonly')) {
		this.readonly = options.pop(opts, 'readonly');
		assert.type(this.readonly, 'boolean');
	}

	if (options.has(opts, 'validators')) {
		this.validators = options.pop(opts, 'validators');
		assert.type(this.validators, 'array');
	}
}

BaseField.prototype = oops.proto(BaseField, {
	nullable: true,
	readonly: false,
	validators: [
		function(val) {
			assert.ok(this.nullable || (val !== null && typeof val !== 'undefined'), 'Value is non-nullable');
		}
	],

	/**
	 * No-op function for interface consistency.
	 */
	hydrate: function BaseField$hydrate() {},

	/**
	 * Parses a provided value. Returns the value verbatim.
	 *
	 * @param {*} val The value that will be parsed.
	 * @returns {*}
	 */
	parse: function BaseField$parse(val) {
		return val;
	},

	/**
	 * Validates a provided value against pre-established rules and the provided list of validators if applicable.
	 *
	 * @param {*} val The value to validate against the field.
	 * @returns {Array} An array of validation errors associated with the field instance.
	 */
	validate: function BaseField$validate(val) {
		var i, assertions, constructor, errors, validators;

		errors = [];
		assertions = this.hasOwnProperty('validators') ? this.validators.slice() : [];

		constructor = oops.constructor(this);

		while (constructor !== Object) {
			if (validators = constructor.prototype.validators) {
				Array.prototype.unshift.apply(assertions, validators);
			}

			constructor = oops.parent(constructor);
		}

		for (i = 0; i < assertions.length; i++) {
			try {
				assertions[i].call(this, val);
			}
			catch(e) {
				errors.push(e.message);

				if (settings.breakValidation) {
					return errors;
				}
			}
		}

		return errors;
	}
});


/**
 * A field type used to specify a number property.
 *
 * @constructor
 * @param {Object} [opts] A configuration object.
 * @config {Boolean} [nullable] A boolean flag indicating whether the field instance is nullable.
 * @config {Boolean} [readonly] A boolean flag indicating whether the field instance is readonly.
 * @config {Array} [validators] An array of custom validator functions that will be run in conjunction with the built-in field validators.
 */
function NumberField(opts) {
	opts = options.create(opts);

	oops.parent(NumberField).call(this, opts);
}

NumberField.prototype = oops.proto(NumberField, BaseField, {
	validators: [
		function(val) {
			assert.type(val, 'number?', 'Value is not a valid number');
			assert.ok(!isNaN(val) && isFinite(val), 'Value is not a valid number');
		}
	],

	/**
	 * Override for `BaseField$parse`. Returns null if the provided value is `null` else attempts to `parseFloat`
	 * the value and returns the result.
	 *
	 * @param {*} val The value that will be parsed.
	 * @returns {Number} The parsed value.
	 */
	parse: function NumberField$parse(val) {
		return (val === null) ? null : parseFloat(val);
	}
});


/**
 * A field type used to specify an integer property, and thus more specific than a number field.
 *
 * @constructor
 * @param {Object} [opts] A configuration object.
 * @config {Boolean} [nullable] A boolean flag indicating whether the field instance is nullable.
 * @config {Boolean} [readonly] A boolean flag indicating whether the field instance is readonly.
 * @config {Array} [validators] An array of custom validator functions that will be run in conjunction with the built-in field validators.
 */
function IntegerField(opts) {
	opts = options.create(opts);

	oops.parent(IntegerField).call(this, opts);
}

IntegerField.prototype = oops.proto(IntegerField, NumberField, {
	validators: [
		function(val) {
			assert.ok(val === (val|0), 'Value is not an integer');
		}
	],

	/**
	 * Override for `NumberField$parse`. Returns null if the provided value is `null` else attempts to `parseInt`
	 * the value and returns the result.
	 *
	 * @param {*} val The value that will be parsed.
	 * @returns {Number} The parsed value.
	 */
	parse: function IntegerField$parse(val) {
		return (val === null) ? null : parseInt(val);
	}
});


/**
 * A field type used to specify a date property.
 *
 * @constructor
 * @param {Object} [opts] A configuration object.
 * @config {Boolean} [nullable] A boolean flag indicating whether the field instance is nullable.
 * @config {Boolean} [readonly] A boolean flag indicating whether the field instance is readonly.
 * @config {Array} [validators] An array of custom validator functions that will be run in conjunction with the built-in field validators.
 */
function DateField(opts) {
	opts = options.create(opts);

	oops.parent(DateField).call(this, opts);
}

DateField.prototype = oops.proto(DateField, BaseField, {
	validators: [
		function(val) {
			assert.type(val, 'date?', 'Value is not a valid date');

			// Need to cover `Invalid Date` cases.
			// http://stackoverflow.com/questions/1353684/detecting-an-invalid-date-date-instance-in-javascript/1353711#1353711
			if (type(val) === 'date') {
				assert.ok(!isNaN(val), 'Value is not a valid date');
			}
		}
	],

	/**
	 * Override for `BaseField$parse`. Returns null if the provided value is `null` else attempts to instantiate a
	 * new `Date` object with the value and returns the result.
	 *
	 * @param {*} val The value that will be parsed.
	 * @returns {Date} The parsed value.
	 */
	parse: function DateField$parse(val) {
		return (val === null) ? null : new Date(val);
	}
});


/**
 * A field type used to specify a string property.
 *
 * @constructor
 * @param {Object} [opts] A configuration object.
 * @config {Boolean} [nullable] A boolean flag indicating whether the field instance is nullable.
 * @config {Boolean} [readonly] A boolean flag indicating whether the field instance is readonly.
 * @config {Array} [validators] An array of custom validator functions that will be run in conjunction with the built-in field validators.
 * @config {Number} [maxlength] The maximum allowable length for the `CharField` value.
 */
function CharField(opts) {
	opts = options.create(opts);

	if (options.has(opts, 'maxlength')) {
		this.maxlength = options.pop(opts, 'maxlength');
		assert.type(this.maxlength, 'number');
	}

	oops.parent(CharField).call(this, opts);
}

CharField.prototype = oops.proto(CharField, BaseField, {
	maxlength: null,
	validators: [
		function(val) {
			assert.type(val, 'string?', 'Value is not a valid string');

			if (typeof val === 'string' && this.maxlength !== null) {
				assert.ok(val.length <= this.maxlength, 'Value exceeds maximum allowable length');
			}
		}
	],

	/**
	 * Override for `BaseField$parse`. Returns null if the provided value is `null` else the `toString` result of
	 * the passed value.
	 *
	 * @param {*} val The value that will be parsed.
	 * @returns {String} The parsed value.
	 */
	parse: function CharField$parse(val) {
		return (val === null) ? null : val.toString();
	}
});


function EmailField(opts) {
	opts = options.create(opts);

	oops.parent(EmailField).call(this, opts);
}

EmailField.prototype = oops.proto(EmailField, CharField, {
	validators: [
		function(val) {
			assert.ok(/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/.test(val), 'Email address invalid');
		}
	]
});


/**
 * Placeholder.
 *
 * @param type
 * @param fn
 * @returns {*}
 */
function define(type, name) {
	if (synonyms.hasOwnProperty(type)) {
		throw new Error('Synonym already defined');
	}

	return synonyms[String(type)] = String(name);
}


/**
 * Returns the appropriate field type constructor corresponding to the provided name. Raises an error if no field
 * matches the provided type.
 *
 * @param {String} type The type of field to return; checked against synonym aliases.
 * @param {Object}xN otherSynonyms Plain objects containing custom key/value type aliases (in case modifying the built-in module `synonyms` is not desired).
 * @returns {Function} The field function constructor matching the provided `type`.
 */
function get(type) {
	var alias, field, synonymArgs, synonymObj;

	alias = type;

	if (typeof exports[type] === 'undefined') {
		if (arguments.length > 1) {
			synonymArgs = Array.prototype.slice.call(arguments, 1);
			synonymArgs.unshift(synonyms);
			synonymObj = oops.merge.apply(null, synonymArgs);
		}
		else {
			synonymObj = synonyms;
		}

		alias = synonymObj[type];
	}

	field = exports[alias];

	if (typeof field === 'undefined') {
		throw new Error('Invalid field type "' + type + '"');
	}

	return field;
}


module.exports = exports = {
	BaseField: BaseField,
	CharField: CharField,
	DateField: DateField,
	EmailField: EmailField,
	IntegerField: IntegerField,
	NumberField: NumberField,

	define: define,
	get: get
};
