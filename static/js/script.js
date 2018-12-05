$(document).ready(function() {
	$('.step-btn').click(function() {
		$('.step-active').removeClass('step-active');
		$(this).addClass('step-active');
		const id = $(this).data('step');
		
		$('.active').fadeOut('slow', function() {
			$(this).removeClass('active');
			$('.step-' + id).fadeIn('slow', function() {
				$(this).addClass('active');
			});			
		});
	});
});
