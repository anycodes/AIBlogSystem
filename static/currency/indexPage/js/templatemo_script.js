

var menuDisabled = false;

jQuery(function($) {
    
    $(window).load(function() { // makes sure the whole site is loaded
            $('#status').fadeOut(); // will first fade out the loading animation
            $('#preloader').delay(350).fadeOut('slow'); // will fade out the white DIV that covers the website.
            $('#main-wrapper').delay(350).css({'overflow':'visible'});
    });
    
    $(document).ready( function() {

        //loadGoogleMap();
        
        // backstretch for background image
        var defaultImgSrc = $('img.main-img').attr('src');
        $.backstretch(defaultImgSrc, {speed: 400});

	//for image slide on menu item click(normal) and responsive
	$(".change-section").on('click',function(e){
            e.preventDefault();
            if (menuDisabled == false) // check the menu has disabled?
            {
                menuDisabled = true; // disable to menu
                
                var name = $(this).attr('href');
                console.log(name);
                // get image url and assign to backstretch for background
                var imgSrc = $("img"+name+"-img").attr('src');
                $.backstretch(imgSrc, {speed: 400}); //backstretch for background fade in/out
                
                // content zoom in/out
                $("section.active").hide('size',{easing: 'easeInQuart', duration: 400},function(){
                    $(this).removeClass("active");
                    $(name+"-section").show('size',{easing: 'easeOutQuart', duration: 400},function(){
                        $(this).addClass("active");
                        
                        // google map need to resize for animate contents
                        google.maps.event.trigger(map, 'resize'); // resize map
                        $.backstretch("resize"); // resize the background image
                        menuDisabled = false;
                     });
                });                
            }
            return;
	});
        
    });

});

var map = '';

function initialize() {
    var mapOptions = {
      zoom: 14,
      center: new google.maps.LatLng(16.8496189,96.1288854)
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),  mapOptions);
}

function loadGoogleMap(){
    // load google map
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&' +
        'callback=initialize';
    document.body.appendChild(script);
}