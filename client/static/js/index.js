/**
 * requirejs define. Start the index app logic.
 * load jquery and rxjs module.
 */
define(["jquery", "rxjs"], function($, Rx){
    // now can use jquery and rxjs now.
    $(document).ready(function() {
        var a = Rx.Observable.interval(1000);
        var b = a.take(3);
        b.subscribe((value) => console.log(value));
    });         // end of document ready.

});
