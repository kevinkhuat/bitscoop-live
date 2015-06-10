//require(['jquery', 'jutsu'], function($, jutsu) {
//	$(document).ready(function() {
//		window.$a = $('#a');
//		window.$b = $('#b');
//		window.$box = $('<div>').addClass('foo bar');
//
//		window.a = jutsu.viewstate.Component('#a');
//		window.v = jutsu.viewstate.View($box);
//
//		window.logger = function(e) {
//			console.log(e);
//		};
//	});
//});


require(['jquery'], function($) {
	// When certain "important" elements are clicked, fire the "autoblur" event on detail panes.
	// Individual autoblur compatible elements handle the event in certain ways, e.g. the list pane shrinks to an icon and the detail pane scoots away.

	$(document).on('click tap', '.autoblur', function(e) {
		var $filtered, $set;

		$set = $(e.target).parents('.autohide');
		$filtered = $('.autohide').not($set);

		$filtered.trigger('autohide');
	});

	/*
	$('#panel').on('autohide', function(e) {
		var $this = $(this);

		e.stopPropagation();

		$this.children().not(':first-child').hide();

		$('#panel-search').addClass('hidden');
	});

	$('#panel-filter').on('autohide', function(e) {
		e.stopPropagation();

		$('#filter-toggle').removeClass('icon-triangle-up').addClass('icon-triangle-down');
		$(this).hide();
	});
	*/

	$('#panel-search div.input-group:first').on('click', function(e) {
		if (e.target === this) {
			$('#panel-search').toggleClass('hidden');
		}
	});

	$(document).on('click', '.filter', function(e) {
		var $this = $(this);

		$this.addClass('active');
		$this.siblings('.filter').removeClass('active');

		// TODO: Insert code to open filter editor.
	});

	$(document).on('click', '.filter > .close', function(e) {
		var $this = $(this);

		$this.closest('.filter').remove();
	});

	$('#search-form').on('submit', function(e) {
		e.preventDefault();

		// TODO: Implement search.
		console.log('search submit!');
	});

	$('#filter-toggle').on('click', function(e) {
		var $this = $(this);

		e.stopPropagation();

		if ($this.is('.icon-triangle-up')) {
			$this.removeClass('icon-triangle-up').addClass('icon-triangle-down');
			$('#panel-filter').hide();
		}
		else {
			$this.removeClass('icon-triangle-down').addClass('icon-triangle-up');
			$('#panel-filter').show();
		}
	});

	$(document).bind('geofilter', function(e) {
		console.log(e);
		// TODO: Perhaps create a geofilter filter (or at least start one) automatically.
	});
});


require(['cartano', 'jquery', 'jquery-cookie'], function(cartano, $) {
	var mainMap;

	$.ajax({
		url: '/app/keys/mapbox',
		type: 'GET',
		dataType: 'json',
		headers: {
			'X-CSRFToken': $.cookie('csrftoken')
		}
	}).done(function(data) {
		mainMap = new cartano.Map('liambroza.hl4bi8d0', {
			accessToken: data.OGRAFY_MAPBOX_ACCESS_TOKEN,

			className: 'grow',

			zoomControl: true,
			drawControl: true,
			layerControl: true
		});

		$('#background').append(mainMap.element);
		mainMap.resize();
	});
});
