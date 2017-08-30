// Customer API Controllers
app.controller('customerApiController', function($scope, $http){

    function fetch(){
        // $http.get($location.host() + '/api/customers')
        $http.get('/api/customers')
        .then(function(response){

            data = response.data;
            customers = data.objects;
            total_customers = data.num_results;
            page = data.page;
            total_pages = data.total_pages;

            $scope.details = [total_customers, page, total_pages];

        });
    }

    fetch();

});


// Customer Update Controllers
app.controller('customerUpdateModalWrapperController', function($scope, ModalService) {
    
    $scope.show = function(customer_id_element) {
        ModalService.showModal({
            templateUrl: 'customer-update-modal.html',
            controller: "customerUpdateModalController"
        }).then(function(modal) {
            modal.element.modal();
            modal.close.then(function(result) {
                // $scope.message = "You said " + result;  // <- Placeholder.
                // Need to write code to submit. use 'result' which will come from value attached to ng-close.
            });
            
            $scope.customer_id = customer_id_element.target.attributes.id.value;

        });
    };
});

app.controller('customerUpdateModalController', function($scope, close) {

    customer_id = 'hello world';
    $scope.customer_id = customer_id;

    $scope.close = function(result) {
 	    close(result, 500); // Close, but give 500ms for bootstrap to animate.
 };
});


// Customer Delete Controllers
app.controller('customerDeleteModalWrapperController', function($scope, ModalService) {

    $scope.show = function() {
        ModalService.showModal({
            templateUrl: 'customer-delete-modal.html',
            controller: "customerDeleteModalController"
        }).then(function(modal) {
            modal.element.modal();
            modal.close.then(function(result) {
                // $scope.message = "You said " + result;  // <- Placeholder.
                // Need to write code to submit. use 'result' which will come from value attached to ng-close.
            });
        });
    };

});

app.controller('customerDeleteModalController', function($scope, close) {

    $scope.close = function(result) {
 	    close(result, 500); // Close, but give 500ms for bootstrap to animate.
 };
});
