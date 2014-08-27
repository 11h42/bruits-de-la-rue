var bidsModule = angular.module('bidsModule', []);

bidsModule.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

bidsModule.controller('bidsController', function ($scope, $http) {
    $scope.hasError = false;
    $scope.bids = [];
    $scope.getBids = function () {
        $http.get('/api/bids/').
            success(function (data, status, headers, config) {
                $scope.bids = data.bids;
            }).error(function (data, status, headers, config) {
                $scope.errorMessage = "L'accès au serveur n'est pas possible, retentez dans quelques instants";
            });
    };
    $scope.getBids();
});

bidsModule.controller('bidController', function ($scope, $http) {
    $scope.getBid = function () {
        $http.get('/api/bid/' + $scope.idBid).
            success(function (data, status, headers, config) {

            }).error(function (data, status, headers, config) {
                $scope.messageDErreur = "L'accès au serveur n'est pas possible, retentez dans quelques instants";
            });
    }
});