define(['jquery'], function($) {
	var EMBED_FORMAT_TEMPLATE_CONTEXTS, AUDIO_TEMPLATE, EMAIL_IFRAME_TEMPLATE, IFRAME_TEMPLATE, IMAGE_TEMPLATE, isMobile, MAX_EMBED_WIDTH, VIDEO_TEMPLATE;

	isMobile = (window.devicePixelRatio >= 1.5 && window.innerWidth <= 1080);
	MAX_EMBED_WIDTH = 475; //px

	EMBED_FORMAT_TEMPLATE_CONTEXTS = {
		mp4: {
			tag: 'video',
			type: 'video/mp4'
		},
		oggv: {
			tag: 'video',
			type: 'video/ogg'
		},
		webm: {
			tag: 'video',
			type: 'video/webm'
		},
		mp3: {
			tag: 'audio',
			type: 'audio/mp3'
		},
		ogga: {
			tag: 'audio',
			type: 'audio/audio'
		},
		wav: {
			tag: 'audio',
			type: 'audio/wav'
		},
		png: {
			tag: 'image'
		},
		jpg: {
			tag: 'image'
		},
		jpeg: {
			tag: 'image'
		},
		svg: {
			tag: 'image'
		},
		tiff: {
			tag: 'image'
		},
		bmp: {
			tag: 'image'
		},
		webp: {
			tag: 'image'
		},
		email: {
			tag: 'iframe'
		},
		iframe: {
			tag: 'iframe'
		},
		link: {
			tag: 'iframe'
		}
	};

	AUDIO_TEMPLATE = '<audio controls style="width:100%"><source src="___embed_content___" type="___type___"></audio>';
	EMAIL_IFRAME_TEMPLATE = '<iframe src="" data-iframe-type="email" data-content-id="___content_id___" frameBorder="0" width="100%" height="400px"/>';
	IFRAME_TEMPLATE = '<iframe src="___embed_content___" width="100%" height="400px"/>';
	IMAGE_TEMPLATE = '<img src="___embed_content___" alt="___title___">';
	VIDEO_TEMPLATE = '<video width="100%" height="100%" controls><source src="___embed_content___" type="___type___"></video>';

	/**
	 * Creates a string containing the HTML tag of the embeded content out of the content object.
	 *
	 * TODO: Handle PROXY and API Calls to get protected content
	 *
	 * @param {Object} content A single piece of content
	 * @param {Boolean} iframeContent Whether the provided content needs to be inserted into an iframe
	 * @returns {String} A template string of the content
	 */
	function renderEmbedContent(content) {
		var context = EMBED_FORMAT_TEMPLATE_CONTEXTS[content.embed_format.toLowerCase()];

		if (content.embed_format.toLowerCase() == 'email') {
			return _generateEmailIframe(content.id);
		}

		if (content.embed_format.toLowerCase() == 'link') {
			return _generateIframe(content.embed_content);
		}

		if (context.tag == 'iframe') {
			return _formatIframe(content.embed_content);
		}

		if (context.tag == 'audio') {
			return _generateAudioTag(content.embed_content, context.type);
		}

		if (context.tag == 'image') {
			return _generateImgTag(content.embed_content);
		}

		if (context.tag == 'video') {
			return _generateVideoTag(content.embed_content, context.type);
		}
	}

	function _generateAudioTag(URL, type) {
		return AUDIO_TEMPLATE.replace('___embed_content___', URL).replace('___type___', type);
	}

	function _generateEmailIframe(contentId) {
		return EMAIL_IFRAME_TEMPLATE.replace('___content_id___', contentId);
	}

	function _generateIframe(URL) {
		return IFRAME_TEMPLATE.replace('___embed_content___', URL);
	}

	function _generateImgTag(URL) {
		return IMAGE_TEMPLATE.replace('___embed_content___', URL);
	}

	function _generateVideoTag(URL, type) {
		return VIDEO_TEMPLATE.replace('___embed_content___', URL).replace('___type___', type);
	}

	//TODO: Fix, broken replace.
	function _formatIframe(iframeString) {
		var newHeight, scaleRatio, $iframeString;

		//$iframeString = $(iframeString)[0];
		//scaleRatio = $iframeString.height / $iframeString.width;
		//
		//newHeight = $iframeString.width * scaleRatio;

		//return iframeString.replace(/(width=')\d+'/, '$1100%\'').replace(/(height=')\d+'/, '');
		return iframeString;
	}


	function handleSpecialCase(provider, args) {
		if (provider === 'Instagram' && window.instgrm) {
			window.instgrm.Embeds.process();
		}
	}

	//TODO: FIX
	function _proxyCall(URL, providerName) {
		var promise;

		promise = $.Deferred();

		function callback(data) {
			promise.resolveWith([data]);
		}

		$.ajax({
			url: 'https://p.bitscoop.com/proxy',
			type: 'GET',
			dataType: 'json',
			data: {
				provider_name: providerName,
				url: URL
			},
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			xhrFields: {
				withCredentials: true
			}
		})
		.done(callback)
		.fail(function() {
			promise.resolve();
		});

		return promise;
	}

	//TODO: FIX
	function _APICall(URL, providerName) {
		var promise;

		promise = $.Deferred();

		function callback(data) {
			promise.resolveWith([data]);
		}

		$.ajax({
			url: 'https://p.bitscoop.com/preview',
			type: 'GET',
			dataType: 'json',
			data: {
				provider_name: providerName,
				url: URL
			},
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			xhrFields: {
				withCredentials: true
			}
		})
		.done(callback)
		.fail(function() {
			promise.resolve();
		});

		return promise;
	}

	/**
	 * Re-scales embeddable content (images, iframes, videos, etc.) to fit their containing element.
	 * If provided with a deferredArray, this will create a promise for each item that is only resolved when that item
	 * finishes loading. (This is not done for iframes because they usually already have a fixed size)
	 * @param {object} $container The container whose descendants will be searched for embeddables.
	 * @param {string} selector A selector to narrow down the descendants of $container.
	 * @param {list} [deferredArray] An optional list into which to insert promises for non-iframe embeddables
	 *                              that will be resolved when those embeddables finish loading.
	 * @param {object} contentResults The dictionary of content obtained from searching.
	 */
	function loadEmbeddablesAndScale($container, selector, deferredArray, contentResults) {
		var $iframes, $images, $videos;

		$images = $container.find(selector);
		$iframes = $container.find('iframe');
		$videos = $container.find('video');

		_.forEach($images, function(image) {
			var deferred, $image;

			$image = $(image);
			deferred = $.Deferred();
			deferred.promise();

			if (deferredArray) {
				deferredArray.push(deferred);
			}

			$image.on('load', function() {
				deferred.resolve();
			});
		});

		_.forEach($iframes, function(iframe) {
			var contentId, newWidth, oldHeight, oldWidth, scaleRatio, $iframe;

			$iframe = $(iframe);

			oldHeight = $iframe.height();
			oldWidth = $iframe.width();
			scaleRatio = oldHeight / oldWidth;

			if (!isMobile && iframe.width > MAX_EMBED_WIDTH) {
				$iframe.width(MAX_EMBED_WIDTH);
				$iframe.height(MAX_EMBED_WIDTH * scaleRatio);
			}
			else {
				$iframe.width('100%');
				newWidth = $iframe.width();
				$iframe.height(newWidth * scaleRatio);
			}

			if ($iframe.attr('data-iframe-type')) {
				contentId = $iframe.attr('data-content-id');

				$iframe[0].contentDocument.body.innerHTML = contentResults[contentId].embed_content;
			}
		});

		_.forEach($videos, function(video) {
			var deferred, $video;

			$video = $(video);
			deferred = $.Deferred();
			deferred.promise();

			$video.on('canplay', function() {
				$video.css('width', '100%');

				deferred.resolve();
			});
		});
	}

	renderEmbedContent.handleSpecialCase = handleSpecialCase;
	renderEmbedContent.loadEmbeddablesAndScale = loadEmbeddablesAndScale;

	return renderEmbedContent;
});
