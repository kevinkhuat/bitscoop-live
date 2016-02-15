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
	EMAIL_IFRAME_TEMPLATE = '<iframe src="" class="email-iframe" data-iframe-type="email" data-content-id="___content_id___" frameBorder="0" width="100%" height="400px"></iframe>';
	IFRAME_TEMPLATE = '<iframe src="___embed_content___" width="100%" height="400px"></iframe>';
	IMAGE_TEMPLATE = '<img src="___embed_content___" alt="___title___"/>';
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

	function _formatIframe(iframeString) {
		var scaleRatio, $iframeString;

		$iframeString = $(iframeString);

		scaleRatio = $iframeString.attr('height') / $iframeString.attr('width');

		if (!isMobile && $iframeString.width > MAX_EMBED_WIDTH) {
			$iframeString.attr('width', MAX_EMBED_WIDTH);
			$iframeString.attr('height', MAX_EMBED_WIDTH * scaleRatio);
		}
		else {
			$iframeString.attr('width', '100%');
		}

		return $iframeString.wrap('<div/>').parent().html();
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
	 * Adds email content to enmpty iframes
	 * @param {object} $container The container whose descendants will be searched for embeddables.
	 * @param {object} contentResults The dictionary of content obtained from searching.
	 */
	function insertEmailContent($container, contentResults) {
		var $iframes;

		$iframes = $container.find('iframe');

		_.forEach($iframes, function(iframe) {
			var contentId, $iframe;
			$iframe = $(iframe);

			if ($iframe.attr('data-iframe-type') === 'email') {
				contentId = $iframe.attr('data-content-id');

				$iframe[0].contentDocument.body.innerHTML = contentResults[contentId].embed_content;

				if (isMobile) {
					$iframe.width($iframe.width() * 2);
					//$iframe.height($iframe.height() * 2);
				}
			}
		});
	}

	renderEmbedContent.handleSpecialCase = handleSpecialCase;
	renderEmbedContent.insertEmailContent = insertEmailContent;

	return renderEmbedContent;
});
