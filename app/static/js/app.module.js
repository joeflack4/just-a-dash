/**
 * Created by Joe Flack on 5/21/2016.
 */
var app = angular.module("app", []);

// - Note: These config options are used to make Angular bracket notation compatible with Jinja2.
app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);
