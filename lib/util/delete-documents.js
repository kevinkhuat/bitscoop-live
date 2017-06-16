'use strict';


function deleteDocuments(index, type, terms) {
	let elastic = env.databases.elastic;
	let mongo = env.databases.mongo;

	let mongoDelete = mongo.db('live').collection(type).remove(terms);

	let esDelete = new Promise(function(resolve, reject) {
		let from = 0;
		let size = 1000;
		let matchingDocuments = [];

		let query = {
			query: {
				bool: {
					filter: {
						bool: {
							must: []
						}
					}
				}
			}
		};

		for (let key in terms) {
			if (!terms.hasOwnProperty(key)) {
				break;
			}

			let newTerm;

			if (key === 'connection' || key === 'user_id') {
				newTerm = {
					term: {
						[key]: terms[key].toString('hex')
					}
				};
			}
			else {
				newTerm = {
					term: {
						[key]: terms[key]
					}
				};
			}

			query.query.bool.filter.bool.must.push(newTerm);
		}

		let searchBody = {
			from: from,
			size: size,
			query: query
		};

		function performSearch(type, index, body) {
			elastic.search({
				type: type,
				index: index,
				body: body
			})
				.then(function(data) {
					let hits = data.hits.hits;

					Array.prototype.push.apply(matchingDocuments, hits);

					if (hits.length < size) {
						resolve(matchingDocuments);
					}
					else {
						body.from = body.from + size;

						performSearch(type, index, body);
					}
				})
				.catch(function(err) {
					reject(err);
				});
		}

		performSearch(type, index, searchBody);
	})
		.then(function(matchingDocuments) {
			if (matchingDocuments.length > 0) {
				let bulkDeleteBody = [];

				for (let i = 0; i < matchingDocuments.length; i++) {
					let document = matchingDocuments[i];

					bulkDeleteBody.push({
						'delete': {
							_index: index,
							_type: type,
							_id: document._id
						}
					});
				}

				return elastic.bulk({
					body: bulkDeleteBody
				});
			}
			else {
				return Promise.resolve(null);
			}
		});

	return Promise.all([mongoDelete, esDelete]);
}


module.exports = deleteDocuments;
