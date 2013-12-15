$(document).ready(function() {
	$('.waypoint').waypoint(function(e) {
		var sectionId, $active, $link, $this = $(this);
		
		sectionId = $this.attr('id');
		$link = $('a[href="#' + sectionId + '"]');
		$active = $('.steps > a.active').first();
		
		if ($active[0] !== $link[0]) {
			$active.removeClass('active');
			$link.addClass('active');
		}
	});
	
	$(document).delegate('.steps > a', 'click', function(e) {
		var $this = $(this);
		
		e.preventDefault();
		
		$('.steps > a.active').removeClass('active');
		$this.addClass('active');
		
		$(document.body).waypointScroll($this.attr('href'));
	});
	
	
	$(document).delegate('input[name="password"]', 'change', function(e) {
		var value = $(this).val();
		
		$('input[name="password"]').each(function(i, el) {
			$(el).val(value);
		});
	});
	
	
	$('#sign-up').bind('submit', function(e) {
		var identifier, $username, $email;
		
		e.preventDefault();
		
		$username = $('input[name="username"]');
		$email = $('input[name="email"]');
		identifier = $('input[name="identifier"]').val();
		
		$username.val('');
		$email.val('');
		$('.signup').show();
		
		if (/^\w+@\w+\.\w+$/.test(identifier)) {
			$email.val(identifier);
			$username.focus();
		}
		else {
			$username.val(identifier);
			$email.focus();
		}
		
		$(document.body).waypointScroll('#welcome');
	});
});


$.fn.extend({
	waypointScroll: (function() {
		var options = {
			offset: -65,
			duration: 150,
			onAfter: function() {
				$.waypoints('enable');
			}
		};
		
		return function waypointScroll(target) {
			$.waypoints('disable');
			$(this).scrollTo(target, options);
		};
	})()
});