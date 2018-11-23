
$(document).ready(function() {	
	
	// COUNTER ANIMATION
	if ( $( ".numbers" ).length ) {
		$('.numbers').each(function () {
		    $(this).prop('Counter',0).animate({
		        Counter: $(this).text()
		    }, {
		        duration: 5000,
		        easing: 'swing',
		        step: function (now) {
		            $(this).text(Math.ceil(now));
		        }
		    });
		});
	}

	// STICKY MENU
	// $(window).scroll(function () {
	//       //if you hard code, then use console
	//       //.log to determine when you want the 
	//       //nav bar to stick.  
	//       //console.log($(window).scrollTop())
	//     if ($(window).scrollTop() > 120) {
	//       $('#t3-mainnav').addClass('navbar-fixed-top');
	//       $("#content").css("padding-top","60px");
	//       $(".homepage").css("padding-top","60px");
	      
	//     }
	//     if ($(window).scrollTop() < 121) {
	//       $('#t3-mainnav').removeClass('navbar-fixed-top');
	//       $("#content").css("padding-top","10px");
	//       // $(".homepage").css("padding-top","10px");
	//     }
	//   });

});