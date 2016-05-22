/**
 * Created by Joe Flack on 5/21/2016.
 */

// (function(){
$(document).ready(function() {

    /////////////////
    // Definitions //
    /////////////////
    // Gallery Module //
    var fontIconAutoSizer = function(){
        var fontSize = parseInt($(".gallery-container").width())+"px";
        $(".gallery-container i").css('font-size', fontSize);
        // $(".gallery-container span").css('font-size', fontSize);
    };

    /////////////
    // Runtime //
    /////////////
    fontIconAutoSizer();

    /////////////////////
    // Event Listeners //
    /////////////////////
    // Gallery Module //
    $(window).on('resize', fontIconAutoSizer);

    // - Note: The below code is simply reference. I had a bit of a difficult time messing with selectors due to my poor
    // JS syntax understanding at the time.
    // 1: $(window).resize(fontIconAutoSizer);
    // 2: $(window).resize(function(){
    //     fontIconAutoSizer
    // });
    // 3: $(window).resize(function(){alert('hi')});
    // 4: $('#red-icon')[0].onclick = fontIconAutoSizer;
    // 5: $('#red-icon')[0].onclick = function(){alert('hi')};

})();
