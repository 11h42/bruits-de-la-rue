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

bidsModule.filter('fromNow', function () {
    return function (dateString) {
        moment.locale('fr', {
            relativeTime: {
                future: "dans %s",
                past: "il y a %s",
                s: "secondes",
                m: "une minute",
                mm: "%d minutes",
                h: "une heure",
                hh: "%d heures",
                d: "un jour",
                dd: "%d jours",
                M: "a mois",
                MM: "%d mois",
                y: "a année",
                yy: "%d années"
            }
        });
        return moment(dateString).fromNow()
    };
});

bidsModule.filter('capitalize', function () {
    return function (input) {
        if (!input) {
            return input;
        }
        return input.charAt(0).toUpperCase() + input.slice(1).toLowerCase();
    };
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
                    $scope.getAdresses();
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
        for (key in $scope.bid) {
            if ($scope.bid[key] === '') {
                delete $scope.bid[key];
            }
        }

        if (!$scope.bid['title'] || !$scope.bid['description']) {
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

    $scope.getCategories = function () {
        $http.get('/api/categories/').
            success(function (data) {
                $scope.categories = data.categories;
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site" +
                    " rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
            });
    };


    //todo refactor
    function setSelects() {
        if ($scope.categories) {
            for (var i = 0; i < $scope.categories.length; i++) {
                if ($scope.categories[i]['name'] == $scope.bid.category['name']) {
                    $scope.bid.category = $scope.categories[i];
                }
            }
        }
        if ($scope.localization) {
            for (var j = 0; j < $scope.localization.length; j++) {
                if ($scope.localization[j]['title'] == $scope.bid.localization['title']) {
                    $scope.bid.localization = $scope.localization[j];
                }
            }
        }
        if ($scope.associations) {
            for (var k = 0; k < $scope.associations.length; k++) {
                if ($scope.associations[k]['name'] == $scope.bid.association['name']) {
                    $scope.bid.association = $scope.associations[k];
                }
            }
        }
        if ($scope.status) {
            for (var l = 0; l < $scope.status.length; l++) {
                if ($scope.status[l]['name'] == $scope.bid.status_bid) {
                    $scope.bid.status_bid = $scope.status[l];
                }
            }
        }
    }

    $scope.getBid = function () {
        $http.get('/api/bids/' + $scope.bidId + '/').
            success(function (data) {
                $scope.bid = data;
                $scope.bid_quantity = $scope.bid['quantity'];

                setSelects();
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

    $scope.getAdresses = function () {
        $http.get('/api/users/current/address/').
            success(function (data) {
                $scope.localization = data.address;
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site " +
                    "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
            });
    };

    $scope.getCurrentUserAssociations = function () {
        $http.get('/api/users/current/associations/').
            success(function (data) {
                $scope.associations = data.associations;
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site " +
                    "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
            });
    };

    $scope.getStatus = function () {
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
            $scope.getCategories();
            $scope.getAdresses();
            $scope.setRealAuthor();
            $scope.getStatus();
            $scope.getCurrentUserAssociations();
            $scope.form_title = "Création d'une annonce";
            $scope.submit_button_name = "Créer"
        }
        else if ($scope.get_page_type(url) == "UPDATE") {
            $scope.getCategories();
            $scope.getAdresses();
            $scope.getCurrentUserAssociations();
            $scope.getStatus();
            $scope.getBid();
            $scope.form_title = "Modification d'une annonce";
            $scope.submit_button_name = "Modifier"
        }
    };

    $scope.init();

    $scope.user_id = "";
    $scope.bid_id = "";

    $scope.acceptBid = function () {
        $http.put('/api/bids/' + $scope.bidId + '/accept/', $scope.bid).
            success(function () {
                window.location.reload(true);
                $scope.errorMessage = "";
                $scope.successMessage = "Vous avez accepté cette annonce";
            }).error(function (data, status, headers, config) {
                if (data.message) {
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
        delete $scope.bid['current_user_is_staff'];
        delete $scope.bid['current_user_id'];
        delete $scope.bid['creator'];
        console.log($scope.bid);
        $http.put('/api/bids/' + $scope.bidId + '/', $scope.bid).
            success(function () {
                window.location = '/annonces/' + $scope.bidId;
            }).error(function (data) {
                if (data.message) {
                    $scope.errorMessage = data.message;
                }
                else {
                    $scope.errorMessage = "Veuillez nous excuser, notre site " +
                        "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
                }
            });
    };

});