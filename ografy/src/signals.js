var assert = require('./assert');
var fields = require('./fields');
var jobqueue = require('./jobqueue');
var oops = require('./oops');
var options = require('./options');
var querystring = require('./querystring');
var router = require('./router');
var url = require('./url');


var app = new router.Route('^', 'app');
var library = {
	configurations: {},
	models: {},
	routes: {},
	signals: {}
};
var signature = '62ceb9df-77c2-41b2-af2b-ca2167a160db';
var re_valid_model_name = /^[a-z][a-z_]*$/i;

var modelQueue = new jobqueue.JobQueue();


/**
 * The base functionality and interface for a Manager. Not intended to be instantiated directly. Used for instanceof
 * checks on prototype chains to make sure that a Manager instance is actually a BaseManager sub-class.
 *
 * @constructor
 * @param {Object} [opts] An options configuration object.
 * @config {Function} model The model function associated with the manager. Circular reference required in this implementation so new prototype methods need not be recreated for each manager type.
 * @config {Function} [concatenator] A function that describes how to combine several objects into a single request (e.g. multiple IDs into a $set query parameter).
 */
function BaseManager(opts) {
	var concatenator, model;

	opts = options.create(opts);

	model = options.pop(opts, 'model');
	_setModel(this, model);

	if (options.has(opts, 'concatenator')) {
		this.concatenator = options.pop(opts, 'concatenator');
	}

	this._cache = {};
}

BaseManager.prototype = oops.proto(BaseManager, {
	concatenator: null,

	/**
	 * Placeholder.
	 *
	 * @returns {Object} A bundle object containing information to pass-by-reference to the call chain.
	 */
	bundle: function BaseManager$bundle() {
		return {};
	},

	/**
	 * Placeholder.
	 *
	 * @param {BaseFilter|*} [expr] A BaseFilter instance object type congruent with the underlying Model key that can be used to limit the return results of a query.
	 * @returns {*}
	 */
	cache: function(expr) {
		var cache, fn, values;

		cache = this._cache;

		if (arguments.length === 0) {
			return cache;
		}

		if (filters.isFilter(expr)) {
			fn = expr.toFunction(this.model);

			values = Object.keys(cache).map(function(key) {
				return cache[key];
			});

			return values.filter(fn);
		}

		return cache[expr];
	},

	/**
	 * Placeholder.
	 *
	 * @param {Object} bundle
	 */
	exec: function BaseManager$exec(bundle) {
		console.log(bundle);
	},

	/**
	 * Placeholder.
	 *
	 * @param {*} [expr] A value with a type congruent to the underlying Model's key used to qualify the URL requested.
	 * @param {Object} [options] An options configuration object.
	 * @config {Object} [args] Any arguments to override manager defaults in qualifying the URL.
	 * @config {Object} [params] Any parameters to override manager defaults in qualifying the URL.
	 */
	get: function BaseFilter$get(key, options) {
		var bundle;

		bundle = this.bundle();
		bundle.single = true;

		this.preflight(bundle);

		return this.exec(bundle);
	},

	/**
	 * Placeholder.
	 *
	 * @param {Object} bundle
	 * @chainable
	 */
	preflight: function BaseManager$preflight(bundle) {},

	/**
	 * Placeholder
	 *
	 * @param {BaseFilter|*} [expr] A BaseFilter instance that can be used to limit the return results of a query.
	 * @param {Object} [options] An options configuration object.
	 * @config {Object} [args] Any arguments to override manager defaults in qualifying the URL.
	 * @config {Object} [params] Any parameters to override manager defaults in qualifying the URL.
	 */
	query: function BaseManager$query(expr, options) {
		var bundle;

		bundle = this.bundle();
		bundle.single = false;

		this.preflight(bundle);

		return this.exec(bundle);
	}
});


/**
 * Generates a Model constructor which can be used to instantiate Model instances.
 *
 * @param {Object} schema The schema describing the fields and properties of the Model.
 * @param {Object} [options] A configuration object with model creation options.
 * @config {Function} [parser] A schema parser; arguments are the schema, metadata object, and field object all passed by reference. If an object is returned, its iterable properties will be mapped onto the new Model constructor.
 * @config {BaseManager|Function} [manager] A BaseManager instance or constructor function that will be used to set the `objects` property on the model.
 * @config {Object} [managerOpts] Options to pass to the `manager` configuration object IFF it's a constructor function.
 * @returns {Function} A Model constructor created via reflection.
 */
function BaseModel(namespace, schema, options) {
	var name, _fields, _meta, fullName, manager, parsed, parser;

	if (typeof namespace !== 'string') {
		options = schema;
		schema = namespace;
		namespace = void(0);
	}

	schema = schema || {};
	options = options || {};

	_fields = {};
	_meta = {};

	if (name = schema.name) {
		if (!re_valid_model_name.test(name)) {
			throw new Error('Invalid model name: ' + name);
		}

		// Register the model to the internal tracking index.
		// This will serve as a way to dynamically import models (i.e. related fields with deferred model definition).
		if (namespace) {
			_meta.namespace = namespace;
			fullName = namespace + '.' + name;

			library.models[fullName] = Model;
			modelQueue.resolve(fullName);
		}
	}

	// Set properties on the Model constructor.
	parser = options.parser || _schemaParser;
	parsed = parser.call(Model, schema, _meta, _fields);

	if (parsed) {
		oops.extend(Model, parsed);
	}

	// FIXME: Make this work with BaseManager or custom managers.
	if (manager = options.manager) {
		if (typeof manager === 'function') {
			manager = new manager(Model, options.managerOpts);
		}
		else if (!isManager(manager)) {
			throw new Error('Invalid `manager` configuration option');
		}

		Model.objects = manager;
	}

	oops.extend(Model, {
		_meta: _meta,
		_fields: _fields,
		_signature: signature,
		define: function define(name, val) {
			if (_fields.hasOwnProperty(name) || Model.prototype.hasOwnProperty(name)) {
				throw new Error('Conflicting property name "' + name + '"');
			}

			_fields[name] = val;
		}
	});

	function Model(data) {
		var name;

		if (typeof data === 'undefined') {
			data = {};
		}
		else if (typeof data === 'string') {
			data = JSON.parse(data);
		}

		for (name in data) {
			if (!data.hasOwnProperty(name) || !_fields.hasOwnProperty(name)) {
				continue;
			}

			this[name] = _fields[name].parse(data[name]);
		}
	}

	Model.prototype = oops.proto(Model, BaseModel, {
		clean: function Model$clean() {
			var name;

			for (name in this) {
				if (!Object.prototype.hasOwnProperty.call(this, name) || !_fields.hasOwnProperty(name)) {
					continue;
				}

				this[name] = _fields[name].parse(this[name]);
			}

			return this;
		},

		validate: function Model$validate() {
			var name, errors, isValid, messages;

			errors = {};
			isValid = true;

			for (name in _fields) {
				if (!_fields.hasOwnProperty(name)) {
					continue;
				}

				messages = _fields[name].validate(this[name]);

				if (messages.length > 0) {
					errors[name] = messages;
					isValid = false;
				}
			}

			if (!isValid) {
				return errors;
			}

			return this;
		}
	});

	Object.defineProperty(Model.prototype, 'pk', {
		enumerable: true,
		get: function ReflectedModel$pk() {
			return this[_meta.key];
		}
	});

	return Model;
}

BaseModel.prototype = oops.proto(BaseModel);


/**
 * Placeholder.
 *
 * @constructor
 * @param {Object|Options} opts
 * @config model
 */
function HyperlinkRelatedField(opts) {
	// Needs to map to an appropriate route or create a new one so know how to parse the underlying field (which
	// will always be a CharField). The mapping is probably accomplished via pattern matching against a route tree,
	// but how do we anchor it to the root of the tree? Should there be an anchor specified in `models` config, or
	// should the `models` module be kept more independent.

	// Needs the "primary_key" property set so that parsing the underlying CharField string value will yield the
	// primary key that can in turn be used for the related field manager.

	// Qualifying the resource amounts to requesting the URL while supplying any query parameters or performing the
	// necessary auth automatically.
	opts = options.create(opts);

	oops.parent(HyperlinkRelatedField).call(this, opts);
}

HyperlinkRelatedField.prototype = oops.proto(HyperlinkRelatedField, fields.CharField, {

});


/**
 * A field type used to specify a model property.
 *
 * @constructor
 * @param {Object|Options} [opts] A configuration object with model creation options passed directly to the Model constructor if `model` is not a Function.
 * @config {Object|Function} model The model constructor of the related field type or a configuration object used to create a new model type.
 */
function ModelField(opts) {
	var model;

	opts = options.create(opts);

	model = options.pop(opts, 'model');
	_setModel(this, model);

	oops.parent(ModelField).call(this, opts);
}

ModelField.prototype = oops.proto(ModelField, fields.BaseField, {
	validators: [
		function(val) {
			assert.ok(val instanceof this.model, 'Field is not an instance of the bound model');
		}
	],

	/**
	 * Override for `BaseField$parse`. Returns null if the provided value is `null` else a new model instance
	 * constructed from the provided value object.
	 *
	 * @param {*} val The value that will be parsed.
	 * @returns {Model} The parsed value.
	 */
	parse: function ModelField$parse(val) {
		return (val === null) ? null : new this.model(val);
	},

	/**
	 * Override for `BaseField$validate`. Runs base validation explicitly and additionally checks to make sure the
	 * provided value is a valid model instance. Additionally validates the underlying model instance and propagates
	 * sub-errors if applicable.
	 *
	 * @param {*} val The value to validate against the field.
	 * @returns {Array} An array of validation errors associated with the field instance.
	 */
	validate: function ModelField$validate(val) {
		var errors, modelErrors;

		errors = oops.parentProto(ModelField).validate.call(this, val);

		if (modelErrors = this.model.prototype.validate.call(val)) {
			errors.push(modelErrors);
		}

		return errors;
	}
});


/**
 * ModelRoute Placeholder.
 *
 * @param opts
 * @config {Model|String}
 * @constructor
 */
function ModelRoute(opts) {
	var actual, model;

	opts = options.create(opts);

	if (options.has(opts, 'responsePath')) {
		this.responsePath = actual = options.pop(opts, 'responsePath');
		assert.type(actual, 'string', 'The `responsePath` property should be a string.');
	}

	if (options.has(opts, 'many')) {
		this.many = actual = options.pop(opts, 'many');
		assert.type(actual, 'boolean', 'The `many` property should be a boolean.');
	}

	model = options.pop(opts, 'model');
	_setModel(this, model);

	oops.parent(ModelRoute).call(this, opts);
}

ModelRoute.prototype = oops.proto(ModelRoute, router.Route, {
	many: false,
	responsePath: null,

	parse: function ModelRoute$parse(data) {
		var i, model, parsed, raw;

		model = this.model;
		raw = oops.locate(data, this.responsePath);

		if (!this.many) {
			return new model(data);
		}
		else {
			parsed = raw.slice();

			for (i = 0; i < parsed.length; i++) {
				parsed[i] = new model(parsed[i]);
			}

			return parsed;
		}
	}
});


/**
 * Placeholder.
 *
 * @constructor
 * @param opts
 * @config model
 */
function RelatedField(opts) {
	// Needs a way to map to an appropriate route. This will probably be accomplished by a "single_uri" and/or
	// "group_uri" property required on any model that is used as a related field, so the model that's passed in can
	// be referenced for these properties.

	// Need a way to reverse a "primary_key" or the value of the underlying field. But where should the rest of the
	// params and args necessary for URL reversing come from? Pulled from config? How do we reference the config?

	// Probably need to specify which URL param the "primary_key" corresponds to, but can default to the name of the
	// field.
	opts = options.create(opts);

	oops.parent(RelatedField).call(this, opts);
}

RelatedField.prototype = oops.proto(RelatedField, fields.BaseField, {

});


/**
 * Placeholder.
 *
 * @param root
 * @param options
 * @returns {Signal}
 * @constructor
 */
function Signal(root, options) {
	if (!(this instanceof Signal)) {
		return new Signal(root, options);
	}

	options = Object(options);

	this._root = root;
	this._freq = options.frequency;
	this._last = null;
}

Signal.prototype = {
	/**
	 * Placeholder.
	 */
	auth: function Signal$auth() {
	},

	/**
	 * Placeholder.
	 */
	condition: function Signal$condition() {
	},

	/**
	 * Placeholder.
	 */
	execute: function Signal$execute() {
		// TODO: Implement old code, this left in for reference.
		/*
		var data, headers, reversed;

		data = {};
		headers = {};

		signal.preflight(data, headers);

		reversed = '';

		ajax.send(reversed, data, headers)
			.done(function(data) {
				signal.condition(data);
			})

		// Send request based on reversed Signal URL

		signal.condition()
		*/
	},

	/**
	 * Placeholder.
	 */
	preflight: function Signal$preflight() {},

	/**
	 * Placeholder.
	 */
	submit: function Signal$submit() {}
};


/**
 * Parses a schema in the default expected format into meta and field information.
 *
 * @private
 * @param {Object} schema The schema of the model to be created.
 * @param {Object} _meta The metadata of the model to be created (passed and modified by reference).
 * @param {Object} _fields The field map of the model to be created (passed and modified by reference).
 */
function _schemaParser(schema, _meta, _fields) {
	var name, fieldFn, property, properties;

	_meta.key = schema.key || 'id';
	_meta.name = schema.name;

	// Build out the _fields object as a list of fields associated with the model.
	properties = schema.properties;
	for (name in properties) {
		if (!properties.hasOwnProperty(name)) {
			continue;
		}

		property = properties[name];
		fieldFn = fields.get(property.type);
		_fields[name] = new fieldFn(property);
	}
}


/**
 * Placeholder.
 *
 * @param inst
 * @param model
 * @private
 */
function _setModel(inst, model) {
	if (typeof model === 'string') {
		modelQueue.enqueue(model, function() {
			inst.model = getModel(model);
		});
	}
	else if (!isModelFn(model)) {
		inst.model = new BaseModel(model.namespace, model.schema, model.options);
	}

	throw new Error('Unsupported definition format.');
}



/**
 * Returns a model from the registry by name.
 *
 * @param {String} name The name of the model constructor to retrieve.
 * @returns {Function} The Model constructor matching the provided name.
 */
function getModel(name) {
	var model;

	model = library.models[name];

	if (typeof model === 'undefined') {
		throw new Error('Model "' + name + '" not found');
	}

	if (!isModelFn(model)) {
		throw new Error('Object "' + name + '" is not a valid Model constructor');
	}

	return model;
}


/**
 * Determines whether a test object is an instance of `BaseManager` or any sub-class.
 *
 * @param {Object} obj The object whose type to check.
 * @returns {Boolean} True if `obj` is an instance of `BaseManager` or any sub-class thereof else false.
 */
function isManager(obj) {
	return obj instanceof BaseManager;
}


/**
 * Determines whether a test object is an instance of `BaseModel` or any sub-class.
 *
 * @param {Object} obj The object whose type to check.
 * @returns {Boolean} True if `obj` is an instance of `BaseModel` or any sub-class thereof else false.
 */
function isModel(obj) {
	return obj instanceof BaseModel;
}


/**
 * Determines whether a constructor function has been created via reflection with the Model constructor.
 *
 * @param {*} obj The object to test for a creation signature.
 * @returns {Boolean} True if the object is a Model function created with the Model constructor, else False.
 */
function isModelFn(obj) {
	return typeof obj === 'function' && obj._signature === signature;
}


/**
 * A proxy function for the 'match' instance method on the internal `app` route tree.
 *
 * @URLparam {String} url The
 * @returns {Object}
 */
function match(url) {
	return app.match(url);
}


/**
 * Registers a signal plugin by including the plugin's route tree in the app tree and creating a new
 * Signal instance to manage authentication, poll frequency, etc.
 *
 * @URLparam {String} name The name for the Signal in the internal Signal library.
 * @URLparam {Route} root The Route
 * @URLparam {Object} options A plain JavaScript object passed directly to the signal constructor.
 * @returns {Signal}
 */
function register(name, root, options) {
	app.include(root);

	return library[name] = new Signal(root, options);
}


// Extend `fields` module with `models` functionality.
oops.extend(fields, {
	HyperlinkedRelatedField: HyperlinkRelatedField,
	ModelField: ModelField,
	RelatedField: RelatedField
});

// Extend `router` module with `models` functionality.
oops.extend(router, {
	ModelRoute: ModelRoute
});

module.exports = {
	BaseManager: BaseManager,
	BaseModel: BaseModel,
	HyperlinkedRelatedField: HyperlinkRelatedField,
	Model: BaseModel,
	ModelField: ModelField,
	ModelRoute: ModelRoute,
	RelatedField: RelatedField,
	Signal: Signal,

	getModel: getModel,
	isManager: isManager,
	isModel: isModel,
	isModelFn: isModelFn,
	match: match,
	register: register,
	url: url,

	app: app
};
