/**
 * Created by Joe Flack on 5/21/2016.
 */

app.controller("GalleryController", function() {
    var app = this;

    app.gallery = [{'class': 'fa fa-android gallery-icon-red', 'description': 'A droid.'},
        {'class': 'fa fa-leaf gallery-icon-green', 'description': 'A leaf.'},
        {'class': 'fa fa-legal gallery-icon-blue', 'description': 'A gavel.'},
        {'class': 'fa fa-trophy gallery-icon-orange', 'description': 'A trophy.'}];
});
