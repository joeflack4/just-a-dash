/**
 * Created by Joe Flack on 5/21/2016.
 */
// app.controller("CrmController", function($http) {
app.controller('CrmController', ['$scope', function($scope) {
    var app = this;



    //EXPERIMENT
    $scope.tabz = 1;

    $scope.setTab = function(newTabz){
      $scope.tabz = newTabz;
    };

    $scope.isSet = function(tabzNum){
      return $scope.tabz === tabzNum;
    };
    //EXPERIMENT



    $http.get("/api/customers").success(function (data) {
        app.customers = data.objects;
    });

    app.message = 'hello';

    // Tabular Logic
    app.tabs = {};


    // Tabular Logic: Tab Selection
    app.selected_tab = '';

    // - Note: The following code is currently broken.
    //     var set_selected_tab = function(tab){
    //         selected_tab = tab;
    //     };
    //     $('.crm-tab').on('click', '', set_selected_tab(tab));


    // Tabular Logic: Tab Models
    app.criticalValues = {
        tableHeaders: ['#', 'Last Name', 'First Name', 'Type'],
        fields: [
            {db_key: 'id', label: 'ID'},
            {db_key: 'name_last', label: 'Last Name'},
            {db_key: 'name_first', label: 'First Name'},
            {db_key: 'customer_type', label: 'Customer Type'}
        ]
    };

    app.criticalValues.inactiveValues = {
        tableHeaders: ['Customer Type ID #1', 'Customer Type ID #2', 'Customer Type ID #3'],
        fields: [
            {db_key: 'customer_type_id1', label: 'Customer Type ID #1'},
            {db_key: 'customer_type_id2', label: 'Customer Type ID #2'},
            {db_key: 'customer_type_id3', label: 'Customer Type ID #3'}
        ]
    };

    app.tabs.contactInfo = {
        label: 'Contact Info',
        tableHeaders: ['Phone #', 'Address'],
        fields: [
            {db_key: 'phone1', label: 'Phone #'},
            {db_key: 'address_street', label: 'Street Address'},
            {db_key: 'address_suite', label: 'Suite #'},
            {db_key: 'address_city', label: 'City'},
            {db_key: 'address_state', label: 'State'},
            {db_key: 'address_county', label: 'County'},
            {db_key: 'address_zip', label: 'Zip'},
            {db_key: 'address_zip_extension', label: 'Zip Extension'}
        ]
    };

    app.tabs.contactInfo.inactiveValues = {
        label: 'Contact Info',
        tableHeaders: ['Name Prefix', 'Name Suffix', 'Middle Name', 'Phone #2', 'Phone #3', 'Phone #4', 'Phone #5',
            'E-mail', 'E-mail #2'],
        fields: [
            {db_key: 'name_prefix', label: 'Name Prefix'},
            {db_key: 'name_suffix', label: 'Name Suffix'},
            {db_key: 'name_middle', label: 'Middle Name'},
            {db_key: 'phone2', label: 'Phone #2'},
            {db_key: 'phone3', label: 'Phone #3'},
            {db_key: 'phone4', label: 'Phone #4'},
            {db_key: 'phone5', label: 'Phone #5'},
            {db_key: 'email1', label: 'E-mail'},
            {db_key: 'email2', label: 'E-mail #2'}
        ]
    };


    app.tabs.identifiers = {
        label: 'Identifiers',
        tableHeaders: ['DOB', 'SSN', 'Health Information', 'Other'],
        fields: [
            {db_key: 'pii_dob', label: 'DOB'},
            {db_key: 'pii_id', label: 'SSN'},
            {db_key: 'phi', label: 'PHI'},
            {db_key: 'pii_other', label: 'Other PII'}
        ]
    };

    app.tabs.inactiveIdentifiers = {
        label: 'Identifiers',
        tableHeaders: ['PFI'],
        fields: [
            {db_key: 'pfi', label: 'Personal Financial Information'}
        ]
    };

    app.tabs.servicesAndAuthorizations = {
        label: 'Services & Authorizations',
        tableHeaders: ['Service 1', 'Service 2', 'Service 3', 'Service 4', 'Service 5', 'Service 6'],
        fields: [
            {db_key: 'service_1_id', label: 'Service 1 ID'},
            {db_key: 'service_1_day', label: 'Service 1 Day'},
            {db_key: 'service_1_hours', label: 'Service 1 Hours'},
            {db_key: 'service_1_type', label: 'Service 1 Type'},
            {db_key: 'service_1_rate', label: 'Service 1 Rate'},
            {db_key: 'service_2_id', label: 'Service 2 ID'},
            {db_key: 'service_2_day', label: 'Service 2 Day'},
            {db_key: 'service_2_hours', label: 'Service 2 Hours'},
            {db_key: 'service_2_type', label: 'Service 2 Type'},
            {db_key: 'service_2_rate', label: 'Service 2 Rate'},
            {db_key: 'service_3_id', label: 'Service 3 ID'},
            {db_key: 'service_3_day', label: 'Service 3 Day'},
            {db_key: 'service_3_hours', label: 'Service 3 Hours'},
            {db_key: 'service_3_type', label: 'Service 3 Type'},
            {db_key: 'service_3_rate', label: 'Service 3 Rate'},
            {db_key: 'service_4_id', label: 'Service 4 ID'},
            {db_key: 'service_4_day', label: 'Service 4 Day'},
            {db_key: 'service_4_hours', label: 'Service 4 Hours'},
            {db_key: 'service_4_type', label: 'Service 4 Type'},
            {db_key: 'service_4_rate', label: 'Service 4 Rate'},
            {db_key: 'service_5_id', label: 'Service 5 ID'},
            {db_key: 'service_5_day', label: 'Service 5 Day'},
            {db_key: 'service_5_hours', label: 'Service 5 Hours'},
            {db_key: 'service_5_type', label: 'Service 5 Type'},
            {db_key: 'service_5_rate', label: 'Service 5 Rate'},
            {db_key: 'service_6_id', label: 'Service 6 ID'},
            {db_key: 'service_6_day', label: 'Service 6 Day'},
            {db_key: 'service_6_hours', label: 'Service 6 Hours'},
            {db_key: 'service_6_type', label: 'Service 6 Type'},
            {db_key: 'service_6_rate', label: 'Service 6 Rate'}
        ]
    };

    app.tabs.billingInfo = {
        label: 'Billing Info',
        tableHeaders: ['Billing Method', 'Billing Frequency', 'Billing Relationship Name', 'Billing E-mail', 'Billing Address', 'Billing Notes'],
        fields: [
            {db_key: 'billing_method', label: 'Billing Method'},
            {db_key: 'billing_frequency', label: 'Billing Frequency'},
            {db_key: 'billing_relation_name', label: 'Billing Relationship Name'},
            {db_key: 'billing_email', label: 'Billing E-mail'},
            {db_key: 'billing_address_street', label: 'Billing Street Address'},
            {db_key: 'billing_address_suite', label: 'Billing Suite #'},
            {db_key: 'billing_address_city', label: 'Billing City'},
            {db_key: 'billing_address_state', label: 'Billing State'},
            {db_key: 'billing_address_county', label: 'Billing County'},
            {db_key: 'billing_address_zip', label: 'Billing Zip'},
            {db_key: 'billing_address_zip_extension', label: 'Billing Zip Extension'},
            {db_key: 'billing_notes', label: 'Billing Notes'}
        ]
    };

    app.tabs.caseNotes = {
        label: ' Case Notes',
        tableHeaders: ['Case Notes'],
        fields: [
            {db_key: 'notes_case', label: 'Case Notes'}
        ]
    };

    app.tabs.relationships = {
        label: 'Relationships',
        tableHeaders: ['Relationship #1: Name', 'Relationship #1: Type', 'Relationship #2: Name', 'Relationship #2: Type', 'Relationship #3: Name', 'Relationship #3: Type', 'Relationship #4: Name', 'Relationship #4: Type', 'Relationship #5: Name', 'Relationship #5: Type'],
        fields: [
            {db_key: 'relation_1_name', label: 'Relationship #1: Name'},
            {db_key: 'relation_1_role', label: 'Relationship #1: Type'},
            {db_key: 'relation_2_name', label: 'Relationship #2: Name'},
            {db_key: 'relation_2_role', label: 'Relationship #2: Type'},
            {db_key: 'relation_3_name', label: 'Relationship #3: Name'},
            {db_key: 'relation_3_role', label: 'Relationship #3: Type'},
            {db_key: 'relation_4_name', label: 'Relationship #4: Name'},
            {db_key: 'relation_4_role', label: 'Relationship #4: Type'},
            {db_key: 'relation_5_name', label: 'Relationship #5: Name'},
            {db_key: 'relation_5_role', label: 'Relationship #5: Type'}
        ]
    };

    app.tabs.other = {
        label: 'Other',
        tableHeaders: ['Other Notes'],
        fields: [
            {db_key: 'notes_other', label: 'Other Notes'}
        ]
    };

}]);
// });
