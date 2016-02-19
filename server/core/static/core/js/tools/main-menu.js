define(['jquery', 'minimodal'], function($) {
	$(document).on('click', function(e) {
		var $menu, $target;

		$target = $(e.target);
		$menu = $('#menu');

		if ($menu.hasClass('open') && ($target.parents('#menu').length === 0)) {
			$menu.removeClass('open');
		}
	});

	$(document).on('click', '#close-menu', function(e) {
		var $menu;
		$menu = $('#menu');

		if ($menu.hasClass('open')) {
			$menu.removeClass('open');
		}
	});

	$(document).on('click', '#menu-button, #search-favorited', function(e) {
		e.stopPropagation();
		$('#menu').addClass('open');
	});

	$('select[name="color"]').on('change', function(e) {
		var selectedColor, $this = $(this);

		selectedColor = $this.find(':selected').attr('value');
		$this.css('background-color', selectedColor);

		if ($('.icon-preview').children().length > 0) {
			$('.icon-preview i').css('color', selectedColor);
		}
	});

	$('select[name="icon"]').on('change', function(e) {
		var color, $this = $(this);

		color = $('select[name="color"]').find(':selected').attr('value');

		if ($this.children(':selected').attr('value') != 'none') {
			$('.icon-preview').html('<i class="' + $this.find(':selected').attr('value') + '" style="color: ' + color + '"></i>');
		}
		else {
			$('.icon-preview').empty();
		}
	});

	$('#delete-save').on('click', 'div[name="save"]', function(e) {
		$('#search-bar').trigger('search:save');
	});

	$('#delete-save').on('click', 'div[name="delete"]', function(e) {
		$('#delete-search-modal').modal();
	});

	$('#delete-search-modal').on('click', 'button', function(e) {
		var action, $target;

		$target = $(e.target);

		$.modal.close();

		if ($target.is('.confirm')) {
			$('#search-bar').trigger('search:delete');
		}
	});

	$(document).on('filter:change', function(e) {
		var $colorSelect, $iconSelect, $menuSearch, $name;


		$menuSearch = $('.menu-searches');

		$colorSelect = $menuSearch.find('select[name="color"] option[name="gray"]');
		$iconSelect = $menuSearch.find('select[name="icon"] option[value="none"]');

		$iconSelect.prop('selected', true);
		$iconSelect.trigger('change');
		$colorSelect.prop('selected', true);
		$colorSelect.trigger('change');

		$name = $menuSearch.find('input[name="search-name"]');

		$name.val('');
		$name.trigger('change');
	});
});
