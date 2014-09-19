var associationsModule = angular.module('associationsModule', ['ui.bootstrap.datetimepicker']);

associationsModule.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

associationsModule.filter('startFrom', function () {
    return function (input, start) {
        start = +start;
        return input.slice(start);
    }
});

associationsModule.factory('AssociationService', ['$http', function ($http) {
    return {
        getAssociation: function (association_id, callback) {
            $http.get('/api/associations/' + association_id + '/').
                success(function (data) {
                    callback(data);
                }).error(function (data, status, headers, config) {
                    callback({}, 'Une erreur est survenue lors de la récupération de l\'annonce')
                });
        },
        getAssociations: function (callback) {
            $http.get('/api/associations/').
                success(function (data) {
                    callback(data.associations);
                }).error(function (data, status, headers, config) {
                    callback({}, 'Une erreur est survenue lors de la récupération des annonces')
                });
        }
    }
}]);
associationsModule.controller('associationsController', function ($scope, $http, $location, AssociationService) {

    $scope.pageSize = 10;
    $scope.searchText = "";
    $scope.hasError = false;
    $scope.associations = [];
    $scope.currentPage = 0;
    $scope.users = [];

    $scope.numberOfPages = function () {
        return Math.ceil($scope.associations.length / $scope.pageSize);
    };

    var url = $location.absUrl();
    var url_split = url.split('/');
    var indexOfId = url_split.indexOf('associations') + 1;
    var associationId = url_split[indexOfId];
    var isInt = /^\d+$/;

    if (isInt.test(associationId)) {
        AssociationService.getAssociation(associationId, function (data, errorMessage) {
            if (errorMessage) {
                $scope.errorMessage = errorMessage;
            }
            $scope.association = data.association;
            $scope.members = data.members;

        });
        $http.get('/api/users/').success(function (data) {
            $scope.users = data.users;
        }).error(function (data) {
            $scope.errorMessage = "Veuillez nous excuser, notre site rencontre des difficultés techniques. Nous vous invitions à réessayer dans quelques minutes.";
        })
    } else {
        AssociationService.getAssociations(function (associations, errorMessage) {
            if (errorMessage) {
                $scope.errorMessage = errorMessage;
            }
            $scope.associations = associations;
        });
    }

    $scope.showAssociation = function (association_id) {
        window.location = '/associations/' + association_id + '/';
    };
});