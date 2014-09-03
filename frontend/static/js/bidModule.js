var bidsModule = angular.module('bidsModule', ['ui.bootstrap.datetimepicker']);

bidsModule.filter('startFrom', function () {
    return function (input, start) {
        start = +start;
        return input.slice(start);
    }
});

bidsModule.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

bidsModule.controller('bidsController', function ($scope, $http) {

    $scope.pageSize = 10;
    $scope.searchText = "";
    $scope.hasError = false;
    $scope.bids = [];
    $scope.currentPage = 0;
    $scope.getBids = function () {
        $http.get('/api/bids/').
            success(function (data) {
                $scope.bids = data.bids;
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site rencontre des difficultés techniques. Nous vous invitions à réessayer dans quelques minutes.";
            });
    };
    $scope.getBids();

    $scope.numberOfPages = function () {
        return Math.ceil($scope.bids.length / $scope.pageSize);
    };

    $scope.showBid = function (element) {
        window.location = '/annonces/' + element.bid.id + '/';
    };
});


bidsModule.controller('bidController', function ($scope, $http, $location) {
    function isInt(n) {
        var intRegex = /^\d+$/;
        return intRegex.test(n);
    }

    $scope.form_title = "Création d'une annonce";
    $scope.createBid = function () {
        if ($scope.bid.title.length == 0 || $scope.bid.description.length == 0) {
            $scope.errorMessage = "Le titre et la description d'une annonce doivent être renseignés";
        } else {
            $http.post('/api/bids/', $scope.bid).
                success(function (data, status, headers, config) {
                    window.location = '/annonces/' + data['bid_id'] + '/';
                }).error(function (data, status, headers, config) {
                    $scope.errorMessage = "Veuillez nous excuser, notre site rencontre des difficultés techniques. Nous vous invitions à réessayer dans quelques minutes.";
                });
        }
    };

    $scope.getBidId = function (url) {
        var url_split = url.split('/');
        var indexOfId = url_split.indexOf('annonces') + 1;
        return url_split[indexOfId];
    };

    $scope.updateCategories = function () {
        $http.get('/api/categories/').
            success(function (data) {
                $scope.categories = data.categories;
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site rencontre des difficultés techniques. Nous vous invitions à réessayer dans quelques minutes.";
            });
    };


    $scope.getBid = function () {
        $http.get('/api/bids/' + $scope.bidId + '/').
            success(function (data) {
                $scope.bid = data;
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site rencontre des difficultés techniques. Nous vous invitions à réessayer dans quelques minutes.";
            });
    };
    $scope.bid = {
        'title': '',
        'description': '',
        'type': 'OFFER',
        'quantity': '',
        'begin': '',
        'end': '',
        'category': ''
    };

    $scope.get_page_type = function (url) {
        if (isInt($scope.getBidId(url))) {
            $scope.bidId = $scope.getBidId(url);
            return "GET OR UPDATE"
        } else {
            return "CREATE"
        }
    };

    $scope.init = function () {
        var url = $location.absUrl();

        if ($scope.get_page_type(url) == "GET OR UPDATE") {
            $scope.getBid();
        } else {
            $scope.updateCategories();
        }

    };

    $scope.init();

    $scope.hasError = false;
    $scope.user_id = "";
    $scope.bid_id = "";

    // TODO : TEST ME !
    $scope.acceptBid = function () {
        $http.put('/api/bids/' + $scope.bidId + '/').
            success(function (data, status, headers, config) {
                $scope.successMessage = "Vous avez accepté cette annonce";
            }).error(function (data, status, headers, config) {
                if (status == 403) {
                    $scope.errorMessage = "Vous ne pouvez pas accepter une annonce que vous avez créée."
                } else {
                    $scope.errorMessage = "Veuillez nous excuser, notre site rencontre des difficultés techniques. Nous vous invitions à réessayer dans quelques minutes.";
                }
            });
    };

    // TODO : TEST ME !
    $scope.deleteBid = function () {
        if (confirm("Vous allez supprimer cette annonce. Cette action est irréversible. Continuer ?")) {
            $http.delete('/api/bids/' + $scope.bidId + '/').
                success(function (data, status, headers, config) {
                    window.location = '/annonces/'
                }).error(function (data, status, headers, config) {
                    if (status == 403) {
                        $scope.errorMessage = "Vous n'avez pas le droit de supprimer cette annonce"
                    } else {
                        $scope.errorMessage = "Veuillez nous excuser, notre site rencontre des difficultés techniques. Nous vous invitions à réessayer dans quelques minutes.";
                    }
                });
        }
    }

});