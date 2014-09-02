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
                return 'http://localhost:8000/annonces/creer/'
            }};
            httpBackend = $httpBackend;
            controller = $controller('bidController', {$scope: scope, $location: fakeLocation});
        }));


        it('should have an empty bid', function () {
            var categories = [{'id': 1, 'name': 'ALIMENTAIRE'}, {'id': 2, 'name': 'SERVICE'}];
            var bid = {
                id: null,
                'title': '',
                'description': '',
                'type': 'OFFER',
                'quantity': '',
                'begin': '',
                'end': '',
                'categories': categories
            };
            httpBackend.when('GET', '/api/categories/').respond({"categories": categories});
            httpBackend.flush();

            assert.deepEqual(scope.bid, bid)
        });

    });

    describe('Bid controller', function () {

        var scope, controller, httpBackend;

        beforeEach(inject(function ($rootScope, $httpBackend, $controller) {
            scope = $rootScope.$new();
            httpBackend = $httpBackend;
            var fakeLocation = {absUrl: function () {
                return 'http://localhost:8000/annonces/creer/'
            }};
            controller = $controller('bidController', {$scope: scope, $location: fakeLocation});
        }));

        it("should get bid id", function () {
            assert.equal(scope.getBidId('http://localhost:8000/annonces/creer/'), 'creer');
            assert.equal(scope.getBidId('http://localhost:8000/annonces/1234/'), '1234');
        });

    });


});