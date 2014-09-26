var assert = chai.assert;


describe('address controller', function () {
    var scope, httpBackend;

    beforeEach(angular.mock.module('addressModule'));

    beforeEach(angular.mock.inject(function ($rootScope, $controller, $httpBackend) {
        scope = $rootScope.$new();
        $controller('addressController', {$scope: scope});
        httpBackend = $httpBackend;
    }));

    it('should have empty address array', function () {
        assert.deepEqual(scope.addresses, []);
    });

    it('should try to get all addresses during initialization', function () {
        var addresses = [
            {"town": "Cestas", "title": "Okiwi", "address1": "3 chemin de marticot", "address2": null, "zipcode": 33610, "recipient_name": "Okiwi", "id": 1}
        ];
        httpBackend.when('GET', '/api/addresses/').respond({"addresses": addresses});
        httpBackend.flush();
        assert.deepEqual(scope.addresses, addresses);
    });

    it('should set errorMessage when we got an error', function () {
        httpBackend.when('GET', '/api/addresses/').respond(400, '');
        httpBackend.flush();
        assert.deepEqual(scope.errorMessage, 'Une erreur est survenue lors de la récupération des addresses');
    })

});