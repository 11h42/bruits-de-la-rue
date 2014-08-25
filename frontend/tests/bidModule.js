var assert = chai.assert;

describe('Bids Application', function () {
    beforeEach(module('bidsModule'));

    describe('Bids controller', function () {

        var scope, controller, httpBackend;
        beforeEach(inject(function ($rootScope, $httpBackend, $controller) {
            scope = $rootScope.$new();
            httpBackend = $httpBackend;
            controller = $controller('bidsController', {$scope: scope});
        }));

        it('should be instanciate with default values', function () {
            assert.isFalse(scope.hasError);
            assert.deepEqual(scope.bids, []);
        });

        it('should GET bids when controller is instantiated', function () {
            httpBackend.expectGET('/api/bids/').respond({});
            httpBackend.flush();
        });

        it('should update bids from values get from API', function () {
            var bids = [
                {id: 1, name: 'name test'}
            ];
            httpBackend.when('GET', '/api/bids/').respond({"bids": bids});
            httpBackend.flush();
            assert.deepEqual(scope.bids, bids);
        });
    });
});