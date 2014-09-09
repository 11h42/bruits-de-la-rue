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
                return 'http://localhost:8000/annonces/1/'
            }};
            httpBackend = $httpBackend;
            controller = $controller('bidController', {$scope: scope, $location: fakeLocation});
        }));

        it('should set scope.bid with returned values', function () {
            var bid = {
                'id': 1,
                'title': 'Titre',
                'description': 'Description',
                'type': 'OFFER',
                'quantity': '',
                'begin': '',
                'end': '',
                'category': '1'
            };
            httpBackend.when('GET', '/api/bids/1/').respond(bid);
            httpBackend.flush();
            assert.deepEqual(scope.bid, bid);
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
            var categories = [
                {'id': 1, 'name': 'ALIMENTAIRE'},
                {'id': 2, 'name': 'SERVICE'}
            ];

            bid = {
                'title': '',
                'description': '',
                'type': 'SUPPLY',
                'quantity': '',
                'begin': '',
                'end': '',
                'category': categories,
                'real_author': 'abriand',
                'localization': '',
                'association': '',
                'status_bid': ''
            };
            httpBackend.when('GET', '/api/categories/').respond({"categories": categories});
            httpBackend.when('GET', '/api/users/current/').respond('abriand');
            httpBackend.when('GET', '/api/users/current/address/').respond('');
            httpBackend.when('GET', '/api/users/current/associations/').respond('');
            httpBackend.when('GET', '/api/bids/status/').respond('');
            httpBackend.flush();
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

        it("should return GET if url is /annonces/(id)/", function () {
            assert.equal(scope.get_page_type('http://localhost:8000/annonces/1234/'), 'GET')
        });

        it('should return CREATE if url is /annonces/creer', function () {
            assert.equal(scope.get_page_type('http://localhost:8000/annonces/creer/'), 'CREATE')
        });

    });


});