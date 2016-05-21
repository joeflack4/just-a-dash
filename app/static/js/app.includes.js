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
        // $(".gallery-container span").css('font-size', fontSize);
        $(".gallery-container i").css('font-size', fontSize);
    };

    /////////////
    // Runtime //
    /////////////
    fontIconAutoSizer();

    /////////////////////
    // Event Listeners //
    /////////////////////
    // Gallery Module //
    $(window).resize(fontIconAutoSizer);

    // - Note: The below code is simply reference. I had a bit of a difficult time messing with selectors due to my poor
    // JS syntax understanding at the time.
    // $(window).resize(function(){
    //     fontIconAutoSizer
    // });
    // $(window).resize(function(){alert('hi')});
    // $('#red-icon')[0].onclick = fontIconAutoSizer;
    // $('#red-icon')[0].onclick = function(){alert('hi')};

})();
