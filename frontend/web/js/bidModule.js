var bidsModule = angular.module('bidsModule', []);

bidsModule.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

bidsModule.controller('bidsController', function ($scope) {
    $scope.hasError = false;
});

