'use strict';

const callEndpoint = require('../util/call-endpoint');


class Source {
	constructor(schema, connection) {
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
	}

	call(connectionId) {
		let self = this;

		let body = {
			options: {
				populate: self.population
			}
		};

		return callEndpoint(self.connection.provider.remote_provider_id.toString('hex'), connectionId, self.mapping, 'POST', body)
			.catch(function(err) {
				if (!err.data) {
					err.data = {};
				}

				err.data.connection = self.connection;
				err.data.source = self.name;
				err.data.endpoint = self.mapping;

				return Promise.reject(err);
			});
	}
}


module.exports = {
	Source: Source
};
