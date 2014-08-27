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

    describe('Bid controller', function () {

        var scope, controller, httpBackend;

        beforeEach(inject(function ($rootScope, $httpBackend, $controller) {
            scope = $rootScope.$new();
            var fakeLocation = {absUrl: function () {
                return 'http://localhost:8000/annonce/1/'
            }};
            httpBackend = $httpBackend;
            controller = $controller('bidController', {$scope: scope, $location: fakeLocation});
        }));

        it("shoud get the bid id in the url", function () {
            var idBid = scope.getidBid('http://localhost:8000/annonce/1/');
            assert.equal(idBid, '1')
        });
        it('should GET bids when controller is instantiated', function () {
            httpBackend.expectGET('/api/bid/1/').respond({});
            httpBackend.flush();
            console.log('toto');
        });

    });
});