var assert = chai.assert;

describe('Bids Application', function () {
    beforeEach(module('bidsModule'));

    describe('Bids controller', function () {

        var scope, controller;
        beforeEach(inject(function ($rootScope, $httpBackend, $controller) {
            scope = $rootScope.$new();
            controller = $controller('bidsController', {$scope: scope});
        }));

        it('should be instanciate with default values', function () {
            assert.isFalse(scope.hasError);
            assert.deepEqual(scope.bids, [])
        })
    });
});