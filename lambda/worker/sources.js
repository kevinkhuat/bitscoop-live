'use strict';


class Source {
	constructor(schema, connection, api) {
		if (schema.hasOwnProperty('enabled')) {
			this.enabled = schema.enabled === true;
		}

		if (schema.hasOwnProperty('frequency')) {
			this.frequency = schema.frequency;
		}

		if (schema.hasOwnProperty('updated')) {
			this.updated = schema.updated;
		}

		this.connection = connection;
		this.name = schema.name || null;
		this.internalName = schema.internalName || null;
		this.population = schema.population || null;
		this.enabled = schema.enabled_by_default === true;
		this.frequency = 1;
		this.mapping = schema.mapping || null;
		this.api = api;
	}

	call() {
		return this.api.endpoint(this.mapping)({
			headers: {
				'X-Populate': this.population
			}
		});
	}
}


module.exports = {
	Source: Source
};
