var assert = chai.assert;

describe('Bid Application', function () {
    beforeEach(module('bidsModule'));

    describe('Bid controller', function () {

        var scope, httpBackend, controller;
        beforeEach(inject(function ($rootScope, $httpBackend, $controller) {
            scope = $rootScope.$new();
            httpBackend = $httpBackend;
            controller = $controller('bidsController', {$scope: scope});
        }));

        it('should have no error', function () {
            assert.isFalse(scope.hasError);
        });

    });
});