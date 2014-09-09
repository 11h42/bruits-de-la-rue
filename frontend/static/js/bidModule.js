var bidsModule = angular.module('bidsModule', ['ui.bootstrap.datetimepicker']);

bidsModule.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

bidsModule.filter('startFrom', function () {
    return function (input, start) {
        start = +start;
        return input.slice(start);
    }
});

bidsModule.controller('bidsController', function ($scope, $http) {

    $scope.pageSize = 10;
    $scope.searchText = "";
    $scope.bids = [];
    $scope.currentPage = 0;
    $scope.getBids = function () {
        $http.get('/api/bids/').
            success(function (data) {
                $scope.bids = data.bids;
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser," +
                    " notre site rencontre des difficultés techniques." +
                    " Nous vous invitons à réessayer dans quelques minutes.";
            });
    };
    $scope.getBids();

    $scope.numberOfPages = function () {
        return Math.ceil($scope.bids.length / $scope.pageSize);
    };

    $scope.showBid = function (element) {
        window.location = '/annonces/' + element.bid.id + '/';
    };
});
bidsModule.controller('bidUser', function ($scope, $http) {
    $scope.address = {
        'title': '',
        'recipient_name': '',
        'address1': '',
        'address2': '',
        'zipcode': '',
        'town': ''
    };
    $scope.createUserAddress = function () {
        if ($scope.address.title.length == 0
            || $scope.address.recipient_name.length == 0
            || $scope.address.address1.length == 0
            || $scope.address.zipcode.length == 0
            || $scope.address.town.length == 0) {
            $scope.errorMessage = "Les champs suivants sont requis : Titre, Destinataire, Adresse, Code Postal, Ville";
        } else {
            $http.post('/api/users/current/address/', $scope.address).
                success(function () {
                    $scope.errorMessage = '';
                    $scope.successMessage = 'Votre adresse à bien été ajoutée.';
                    $scope.updateAddress();
                }).error(function () {

                    $scope.errorMessage = "Veuillez nous excuser, notre site " +
                        "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";

                });
        }
    };
});

bidsModule.controller('bidController', function ($scope, $http, $location) {
    function isInt(n) {
        var intRegex = /^\d+$/;
        return intRegex.test(n);
    }

    $scope.bid = {
        'title': '',
        'description': '',
        'type': 'SUPPLY',
        'quantity': '',
        'begin': '',
        'end': '',
        'category': '',
        'real_author': '',
        'localization': '',
        'association': '',
        'status_bid': ''
    };

    $scope.createBid = function () {
        if ($scope.bid.title.length == 0 || $scope.bid.description.length == 0) {
            $scope.errorMessage = "Le titre et la description d'une annonce doivent être renseignés";
        } else {
            $http.post('/api/bids/', $scope.bid).
                success(function (data) {
                    window.location = '/annonces/' + data['bid_id'] + '/';
                }).error(function (data) {
                    if (data.code == '10215') {
                        $scope.errorMessage = data.message;
                    } else {
                        $scope.errorMessage = "Veuillez nous excuser, notre site" +
                            " rencontre des difficultés techniques. Nous vous invitons " +
                            "à réessayer dans quelques minutes.";
                    }

                });
        }
    };

    $scope.getBidId = function (url) {
        var url_split = url.split('/');
        var indexOfId = url_split.indexOf('annonces') + 1;

        if (url_split[url_split.indexOf('annonces') + 2] == 'modifier') {
            $scope.bidId = url_split[url_split.indexOf('annonces') + 1];
            return 'modifier';
        }

        return url_split[indexOfId];
    };

    $scope.updateCategories = function () {
        $http.get('/api/categories/').
            success(function (data) {
                $scope.categories = data.categories;
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site" +
                    " rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
            });
    };


    $scope.getBid = function () {
        $http.get('/api/bids/' + $scope.bidId + '/').
            success(function (data) {
                $scope.bid = data;
                $scope.bid_quantity = $scope.bid['quantity'];
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site" +
                    " rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
            });
    };


    $scope.get_page_type = function (url) {
        if (isInt($scope.getBidId(url))) {
            $scope.bidId = $scope.getBidId(url);
            return "GET";
        } else if ($scope.getBidId(url) == 'modifier') {
            return "UPDATE"
        } else if ($scope.getBidId(url) == 'creer') {
            return "CREATE"
        }
    };

    $scope.setRealAuthor = function () {
        $http.get('/api/users/current/').
            success(function (data) {
                $scope.bid['real_author'] = data;
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site " +
                    "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
            });
    };

    $scope.updateAddress = function () {
        $http.get('/api/users/current/address/').
            success(function (data) {
                $scope.localization = data.address;
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site " +
                    "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
            });
    };

    $scope.updateAssociations = function () {
        $http.get('/api/users/current/associations/').
            success(function (data) {
                $scope.associations = data.associations;
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site " +
                    "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
            });
    };

    $scope.updateStatus = function () {
        $http.get('/api/bids/status/').
            success(function (data) {
                $scope.status = data;
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site " +
                    "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
            });
    };

    $scope.init = function () {
        var url = $location.absUrl();

        if ($scope.get_page_type(url) == "GET") {
            $scope.getBid();

        } else if ($scope.get_page_type(url) == "CREATE") {
            $scope.updateCategories();
            $scope.updateAddress();
            $scope.setRealAuthor();
            $scope.updateStatus();
            $scope.updateAssociations();
            $scope.form_title = "Création d'une annonce";
            $scope.submit_button_name = "Créer"

        }
        else if ($scope.get_page_type(url) == "UPDATE") {
            $scope.updateCategories();
            $scope.updateAddress();
            $scope.updateAssociations();
            $scope.updateStatus();
            $scope.getBid();
            $scope.form_title = "Modification d'une annonce";
            $scope.submit_button_name = "Modifier"
        }

    };

    $scope.init();

    $scope.user_id = "";
    $scope.bid_id = "";

    $scope.acceptBid = function () {
        $scope.bid['status_bid'] = 'ACCEPTE';
        $http.put('/api/bids/' + $scope.bidId + '/', $scope.bid).
            success(function () {
                window.location.reload(true);
                $scope.errorMessage = "";
                $scope.successMessage = "Vous avez accepté cette annonce";
            }).error(function (data, status, headers, config) {
                if (data.code == 10217) {
                    $scope.successMessage = "";
                    $scope.errorMessage = data.message;
                } else if (data.code == 10218) {
                    $scope.successMessage = "";
                    $scope.errorMessage = data.message;
                } else {
                    $scope.successMessage = "";
                    $scope.errorMessage = "Veuillez nous excuser, notre site " +
                        "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
                }
            });
    };

    $scope.deleteBid = function () {
        if (confirm("Vous allez supprimer cette annonce. Cette action est irréversible. Continuer ?")) {
            $http.delete('/api/bids/' + $scope.bidId + '/').
                success(function () {
                    window.location = '/annonces/'
                }).error(function (data, status) {
                    if (status == 403) {
                        $scope.errorMessage = "Vous n'avez pas le droit de supprimer cette annonce"
                    } else {
                        $scope.errorMessage = "Veuillez nous excuser, notre site " +
                            "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
                    }
                });
        }
    };

    $scope.updateBid = function () {

        $http.put('/api/bids/' + $scope.bidId + '/', $scope.bid).
            success(function () {
                window.location = '/annonces/' + $scope.bidId;
            }).error(function (data) {
                if (data.code == 10216) {
                    $scope.errorMessage = data.message;
                } else {
                    $scope.errorMessage = "Veuillez nous excuser, notre site " +
                        "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
                }
            });
    };

});