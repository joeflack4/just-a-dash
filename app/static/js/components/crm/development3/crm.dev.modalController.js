app.controller('customerUpdateModalWrapperController', function($scope, ModalService) {

    $scope.show = function() {
        ModalService.showModal({
            templateUrl: 'customer-update-modal.html',
            controller: "customerUpdateModalController"
        }).then(function(modal) {
            modal.element.modal();
            modal.close.then(function(result) {
                // $scope.message = "You said " + result;  <- Placeholder.
                // Need to write code to submit. use 'result' which will come from value attached to ng-close.
            });
        });
    };

});

app.controller('customerUpdateModalController', function($scope, close) {

 $scope.close = function(result) {
 	close(result, 500); // Close, but give 500ms for bootstrap to animate.
 };

});
