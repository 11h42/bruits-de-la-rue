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
        moment.locale('fr', { });
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

bidsModule.controller('bidsController', function ($scope, $http, BidsService) {

    $scope.pageSize = 10;
    $scope.searchText = "";
    $scope.bids = [];
    $scope.currentPage = 0;

    BidsService.getBids('end', 1000, function (bids, errorMessage) {
        if (errorMessage) {
            $scope.errorMessage = errorMessage;
            return;
        }
        $scope.bids = bids
    });

    $scope.numberOfPages = function () {
        return Math.ceil($scope.bids.length / $scope.pageSize);
    };

    $scope.showBid = function (table_row) {
        BidsService.showBid(table_row)
    };
});

bidsModule.controller('indexController', function ($scope, $http, BidsService) {

    BidsService.getBids('end', 20, function (bids, errorMessage) {
        if (errorMessage) {
            $scope.errorMessage = errorMessage;
            return;
        }
        $scope.bids = bids
    });

    $scope.showBid = function (table_row) {
        BidsService.showBid(table_row)
    };
});

bidsModule.factory('BidsService', ['$http', function ($http) {
    return{
        getBids: function (order_by, limit, callback) {
            var bids = [];
            var errorMessage;
            $http.get('/api/bids/?order_by=' + order_by + '&limit=' + limit).
                success(function (data) {
                    bids = data.bids;
                    callback(bids);
                }).error(function () {
                    errorMessage = "Veuillez nous excuser," +
                        " notre site rencontre des difficultés techniques." +
                        " Nous vous invitons à réessayer dans quelques minutes.";
                    callback(bids, errorMessage);
                });
        },

        showBid: function (table_row) {
            window.location = '/annonces/' + table_row.bid.id + '/';
        }
    };
}])
;

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
        'status_bid': '',
        'photo': '',
        'creator': ''
    };

    $scope.mail = {
        'subject': '',
        'content': '',
        'user_to_mail': '',
        'send_copy': false
    };

    $scope.get_bid_photo_url = function () {
        if ($scope.bid.photo) {
            $http.get('/api/images/' + $scope.bid.photo + '/').
                success(function (data) {
                    $scope.bid_photo_url = data.url
                }).error(function () {
                    $scope.errorMessage = "Veuillez nous excuser, notre site" +
                        " rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
                });
        }
    };

    $scope.deletePhoto = function () {
        if ($scope.bid.photo) {
            $http.delete('/api/images/' + $scope.bid.photo + '/').
                success(function (data) {
                    $scope.successMessage = 'La photo de cette annonce à bien été supprimée.';
                    $scope.bid_photo_url = null;
                    $scope.bid.photo = null;
                }).error(function (data) {
                    if (data.message) {
                        $scope.errorMessage = data.message;
                    } else {
                        $scope.errorMessage = "Veuillez nous excuser, notre site" +
                            " rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
                    }
                })
        }
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
                $scope.get_bid_photo_url();
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
                $scope.bid['real_author'] = data['user']['username'];
            }).error(function () {
                $scope.errorMessage = "Veuillez nous excuser, notre site " +
                    "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
            });
    };
    $scope.sendMail = function () {
        if ($scope.mail.subject.length == 0
            || $scope.mail.content.length == 0) {
            $scope.errorMessage = "Les champs suivants sont requis : Sujet, Message";
        } else {
            $scope.mail.user_to_mail = $scope.bid.creator;
            $http.post('/api/mails/', $scope.mail).
                success(function () {
                    $scope.errorMessage = '';
                    $scope.successMessage = 'Votre email à bien été envoyé.';
                }).error(function () {
                    $scope.errorMessage = "Veuillez nous excuser, notre site " +
                        "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
                });
        }
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
            $scope.submit_button_name = "Créer";
            $(function () {

                $('#bid_image').fileupload({
                    dataType: 'json',
                    add: function (e, data) {
                        data.submit();
                    },
                    done: function (e, data) {
                        $scope.bid.photo = data.result.id;
                        $scope.get_bid_photo_url()
                    },
                    progressall: function (e, data) {
                        var progress = parseInt(data.loaded / data.total * 100, 10);
                        $('#progress').find('.bar').css(
                            'width',
                                progress + '%'
                        );
                    }
                });
            });
        }
        else if ($scope.get_page_type(url) == "UPDATE") {
            $scope.getCategories();
            $scope.getAdresses();
            $scope.getCurrentUserAssociations();
            $scope.getStatus();
            $scope.getBid();
            $scope.form_title = "Modification d'une annonce";
            $scope.submit_button_name = "Modifier";
            $(function () {

                $('#bid_image').fileupload({
                    dataType: 'json',
                    add: function (e, data) {
                        data.submit();
                    },
                    done: function (e, data) {
                        $scope.bid.photo = data.result.id;
                        $scope.get_bid_photo_url()
                    },
                    progressall: function (e, data) {
                        var progress = parseInt(data.loaded / data.total * 100, 10);
                        $('#progress').find('.bar').css(
                            'width',
                                progress + '%'
                        );
                    }
                });
            });

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
        delete $scope.bid['current_user_is_superuser'];
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

