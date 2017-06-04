'use strict';

const Promise = require('bluebird');
const Validator = require('ajv');
const _ = require('lodash');

const fs = require('./util/fs');


function load(path) {
	let schemaList = [];
	let validator = new Validator({
		coerceTypes: true,
		useDefaults: true
	});

	return fs.find(path)
		.then(function(files) {
			let promises = _.map(files, function(file) {
				return fs.readfile(file)
					.then(function(json) {
						schemaList.push(JSON.parse(json));
					});
			});

			return Promise.all(promises);
		})
		.then(function() {
			validator.addSchema(schemaList);

			function validate(value, schema) {
				validator.validate(schema, value);

				if (validator.errors) {
					let error = new Validator.ValidationError(validator.errors);

					return Promise.reject(error);
				}

				return Promise.resolve(value);
			}

			return Promise.resolve(validate);
		});
}

module.exports = {
	load: load
};
