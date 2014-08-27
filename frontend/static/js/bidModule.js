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
            success(function (data) {
                $scope.bids = data.bids;
            }).error(function () {
                $scope.errorMessage = "L'accès au serveur n'est pas possible, retentez dans quelques instants";
            });
    };
    $scope.getBids();
});

bidsModule.controller('bidController', function ($scope, $http, $location) {
    $scope.hasError = false;
    $scope.bid = [];

    $scope.getidBid = function (url) {
        var url_split = url.split('/');
        var indexOfId = url_split.indexOf('annonce') + 1;
        return url_split[indexOfId];
    };

    $scope.idBid = $scope.getidBid($location.absUrl());

    $scope.getBid = function () {
        $http.get('/api/bid/' + $scope.idBid + '/').
            success(function (data) {
                $scope.bid = data.bids;
            }).error(function () {
                $scope.errorMessage = "L'accès au serveur n'est pas possible, retentez dans quelques instants";
            });
    };
    $scope.getBid();
});