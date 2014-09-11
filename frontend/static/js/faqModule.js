var faqsModule = angular.module('faqsModule', ['ui.bootstrap.datetimepicker']);

faqsModule.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

faqsModule.filter('startFrom', function () {
    return function (input, start) {
        start = +start;
        return input.slice(start);
    }
});

faqsModule.controller('faqsController', function ($scope, $http) {

    $scope.pageSize = 10;
    $scope.searchText = "";
    $scope.hasError = false;
    $scope.currentPage = 0;
    $scope.getFaqs = function () {
        $http.get('/api/faq/').
            success(function (data) {
                $scope.faqs = data.faqs;
            }).error(function (data, status, headers, config) {
                $scope.errorMessage = "Veuillez nous excuser, notre site rencontre des difficultés techniques. Nous vous invitions à réessayer dans quelques minutes.";
            });
    };
    $scope.getFaqs();

    $scope.numberOfPages = function () {
        return Math.ceil($scope.faqs.length / $scope.pageSize);
    };
});