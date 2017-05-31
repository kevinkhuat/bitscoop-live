const config = require('config');

/**
 * Concatenate the protocol, subdomain, and base url to return a complete base url
 * @param subdomainOverride - allow subdomain overrides
 * @returns {string}
 */
function getBaseUrl(subdomainOverride) {
    // NODE_ENV determines what config file to choose from. By default,
    // default.json will always get used if there are no NODE_ENV that
    // matches a files in the config folder
    let baseUrl = config.get('domainInfo.baseUrl');
    let protocol = config.get('domainInfo.protocol');
    let subdomain = config.get('domainInfo.subdomain');

    // We need to allow an override for home.js. We can keep the subdomain to local
    // if we are in a development environment
    if (typeof(subdomainOverride) != 'undefined' && subdomain != 'local') {
        subdomain = subdomainOverride;
    }
    return protocol + "://" + subdomain + "." + baseUrl;
}

module.exports = getBaseUrl;
