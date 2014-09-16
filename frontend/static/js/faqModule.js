var faqsModule = angular.module('faqsModule', []);

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
    $scope.faqs = [];
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

    $scope.deleteFaq = function (faq_id) {
        if (confirm("Vous allez supprimer cette annonce. Cette action est irréversible. Continuer ?")) {
            $http.delete('/api/faq/' + faq_id + '/').success(function () {
                $scope.successMessage = "La FAQ à bien été supprimée";
                $scope.getFaqs();
            }).error(function (data) {
                if (data.message) {
                    $scope.errorMessage = data.message
                } else {
                    $scope.errorMessage = "Veuillez nous excuser, notre site rencontre des difficultés techniques. Nous vous invitions à réessayer dans quelques minutes.";
                }
            })
        }
    }
})
;

faqsModule.controller('createFaqController', function ($scope, $http) {
    $scope.faq = {
        'question': '',
        'answer': ''
    };
    $scope.postFaq = function () {
        if (!$scope.faq.question || !$scope.faq.answer) {
            $scope.errorMessage = "Vous devez renseigner la question et la réponse.";
        } else {
            $http.post('/api/faq/', $scope.faq).
                success(function (data) {
                    window.location = '/faq/'
                }).error(function (data, status, headers, config) {
                    $scope.errorMessage = "Veuillez nous excuser, notre site rencontre des difficultés techniques. Nous vous invitions à réessayer dans quelques minutes.";
                });
        }
    };
});