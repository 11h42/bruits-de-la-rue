var addressModule = angular.module('addressModule', []);

addressModule.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

addressModule.factory('addressService', ['$http', function ($http) {
    return {
        getAddresses: function (callback) {
            $http.get('/api/addresses/').
                success(function (data) {
                    callback(data.addresses);
                }).error(function (data, status, headers, config) {
                    callback({}, 'Une erreur est survenue lors de la récupération des adresses')
                });
        },
        createAddress: function (address, callback) {
            $http.post('/api/addresses/', address).success(function (data) {
                callback(data.address);
            }).error(function (data) {
                callback({}, "Une erreur est survenue lors de la création d'une adresse")
            });
        }
    }
}]);

addressModule.controller('addressController', function ($scope, addressService) {
    $scope.addresses = [];

    addressService.getAddresses(function (addresses, errorMessage) {
        if (errorMessage) {
            $scope.errorMessage = errorMessage
        } else {
            $scope.addresses = addresses;
        }
    });

});
