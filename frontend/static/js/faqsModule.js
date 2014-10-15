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

    $scope.faqs = [];

    $scope.getFaqs = function () {
        $http.get('/api/faqs/').
            success(function (data) {
                $scope.faqs = data.faqs;
            }).error(function (data, status, headers, config) {
                $scope.errorMessage = "Nous ne pouvons pas récupérer les questions pour l'instant, retentez plus tard";
            });
    };
    $scope.getFaqs();

    $scope.deleteFaq = function (faq_id) {
        if (confirm("Vous allez supprimer cette FAQ. Cette action est irréversible. Continuer ?")) {
            $http.delete('/api/faqs/' + faq_id + '/').success(function () {
                $scope.successMessage = "La FAQ à bien été supprimée";
                $scope.getFaqs();
            }).error(function (data) {
                $scope.errorMessage = "Nous ne pouvons pas supprimer cette question, retentez plus tard";
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
    $scope.createFAQ = function () {
        if (!$scope.faq.question || !$scope.faq.answer) {
            $scope.errorMessage = "Vous devez renseigner une question et une réponse";
        } else {
            $http.post('/api/faqs/', $scope.faq).
                success(function (data) {
                    window.location = '/faqs/'
                }).error(function (data, status, headers, config) {
                    $scope.errorMessage = "Nous ne pouvons pas créer cette question, retentez plus tard";
                });
        }
    };
});