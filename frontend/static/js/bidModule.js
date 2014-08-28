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

    $scope.showBid = function (element) {

        window.location = '/annonces/' + element.bid.id + '/';

    };
});

bidsModule.controller('createBidController', function ($scope, $http) {

    $scope.bid = {};
    $scope.createBid = function () {
        if ($scope.bid.title.length == 0 || $scope.bid.description.length == 0) {
            $scope.errorMessage = "Le titre et la description d'une annonce doivent être renseignés";
        } else {
            $http.post('/api/bids/', $scope.bid).
                success(function (data, status, headers, config) {
                    window.location = '/annonces/' + data['bid_id'] + '/';
                }).error(function (data, status, headers, config) {
                    $scope.errorMessage = "L'accès au serveur n'est pas possible, retentez dans quelques instants";
                });
        }
    };
});

bidsModule.controller('bidController', function ($scope, $http, $location) {
    $scope.hasError = false;
    $scope.bid = [];

    $scope.getidBid = function (url) {
        var url_split = url.split('/');
        var indexOfId = url_split.indexOf('annonces') + 1;
        return url_split[indexOfId];
    };

    $scope.idBid = $scope.getidBid($location.absUrl());

    $scope.getBid = function () {
        $http.get('/api/bids/' + $scope.idBid + '/').
            success(function (data) {
                $scope.bid = data.bids;
            }).error(function () {
                $scope.errorMessage = "L'accès au serveur n'est pas possible, retentez dans quelques instants";
            });
    };
    $scope.getBid();
});