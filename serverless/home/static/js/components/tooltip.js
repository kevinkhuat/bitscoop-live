define('tooltip', ['jquery', 'lodash'], function($, _) {
	function _toggleOneTooltip(event) {
		event.stopPropagation();
		var $triggerElement = $(this);
		var $tooltipElement = $triggerElement.parents().hasClass('.tooltip') ? $triggerElement.parents('.tooltip') : $triggerElement.siblings('.tooltip');
		if (!($tooltipElement.hasClass('visible'))) {
			$('body').find('.tooltip').removeClass('visible');
			$tooltipElement.toggleClass('visible');
		}
		else {
			$('body').find('.tooltip').removeClass('visible');
		}
	}

	function bindTooltip(triggerClass, closeClass) {
		$('body').on('click', triggerClass, _toggleOneTooltip);
		$('body').on('click', closeClass, _toggleOneTooltip);
	}

	return {
		bindTooltip: bindTooltip
	};
});
