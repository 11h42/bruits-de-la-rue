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

associationsModule.controller('associationsController', function ($scope, $http) {

    $scope.pageSize = 10;
    $scope.searchText = "";
    $scope.hasError = false;
    $scope.associations = [];
    $scope.currentPage = 0;
    $scope.getAssociations = function () {
        $http.get('/api/associations/').
            success(function (data) {
                $scope.associations = data.associations;
            }).error(function (data, status, headers, config) {
                $scope.errorMessage = "Veuillez nous excuser, notre site rencontre des difficultés techniques. Nous vous invitions à réessayer dans quelques minutes.";
            });
    };
    $scope.getAssociations();

    $scope.numberOfPages = function () {
        return Math.ceil($scope.associations.length / $scope.pageSize);
    };
});