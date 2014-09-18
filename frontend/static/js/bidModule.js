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

bidsModule.controller('bidsController', function ($scope, $http, BidService) {

    $scope.pageSize = 10;
    $scope.searchText = "";
    $scope.bids = [];
    $scope.currentPage = 0;

    BidService.getBids('end', 1000, function (bids, errorMessage) {
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
        BidService.showBid(table_row)
    };
});

bidsModule.controller('indexController', function ($scope, $http, BidService) {

    BidService.getBids('end', 20, function (bids, errorMessage) {
        if (errorMessage) {
            $scope.errorMessage = errorMessage;
            return;
        }
        $scope.bids = bids
    });

    $scope.showBid = function (table_row) {
        BidService.showBid(table_row)
    };
});


bidsModule.factory('getAddressesService', ['$http', function ($http) {
    return function (localization, errorMessage, bid) {
        $http.get('/api/users/current/address/').
            success(function (data) {
                localization = data.address;
            }).error(function () {
                errorMessage = "Veuillez nous excuser, notre site " +
                    "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";
            });
        if (localization) {
            for (var j = 0; j < localization.length; j++) {
                if (localization[j]['title'] == bid.localization['title']) {
                    bid.localization = localization[j];
                }
            }
        }
    }
}]);

bidsModule.factory('createAddressService', ['$scope', '$http', function ($scope, $http) {
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
                }).error(function () {

                    $scope.errorMessage = "Veuillez nous excuser, notre site " +
                        "rencontre des difficultés techniques. Nous vous invitons à réessayer dans quelques minutes.";

                });
        }
    };
}]);

var defaultErrorMessage = "Veuillez nous excuser, notre site rencontre des difficultés techniques.";

bidsModule.factory('AddressService', ['$http', function ($http) {
    return {
        getAddresses: function (callback) {
            $http.get('/api/addresses/').success(function (data) {
                callback(data.addresses)
            }).error(function () {
                callback([], defaultErrorMessage);
            });
        },
        createAddress: function (address, callback) {
            $http.post('/api/addresses/', address).success(function (data) {
                callback(data.address);
            }).error(function (data) {
                callback({}, data.message)
            });
        }
    }
}]);
bidsModule.factory('MailService', ['$http', function ($http) {
    return{
        sendMail: function (mail, callback) {
            $http.post('/api/mails/', mail).
                success(function (data) {
                    callback(data);
                }).error(function (data) {
                    callback([], defaultErrorMessage);
                });
        }
    }
}]);
bidsModule.factory('BidService', ['$http', function ($http) {
    return{
        getBids: function (order_by, limit, callback) {
            $http.get('/api/bids/?order_by=' + order_by + '&limit=' + limit).success(function (data) {
                callback(data.bids);
            }).error(function () {
                callback([], defaultErrorMessage);
            });
        },

        showBid: function (bidId) {
            window.location = '/annonces/' + bidId + '/';
        },

        getStatus: function (callback) {
            $http.get('/api/bids/status/').success(function (data) {
                callback(data.status);
            }).error(function () {
                callback([], defaultErrorMessage);
            });
        },

        getBid: function (bidId, callback) {
            $http.get('/api/bids/' + bidId + '/').success(function (data) {
                callback(data.bid);
            }).error(function () {
                callback(data, defaultErrorMessage);
            })
        },
        deleteBid: function (bidId, callback) {
            $http.delete('/api/bids/' + bidId + '/').success(function (data) {
                callback(data);
            }).error(function () {
                callback(data, defaultErrorMessage);
            })
        },
        createBid: function (bid, callback) {
            $http.post('/api/bids/', bid).
                success(function (data) {
                    callback(data.bid_id);
                }).error(function () {
                    callback({}, defaultErrorMessage);
                });
        },
        updateBid: function (bid, callback) {
            $http.put('/api/bids/' + bid.id + '/', bid).
                success(function (data) {
                    callback(data.bid_id);
                }).error(function () {
                    callback({}, defaultErrorMessage);
                });
        }

    }
}]);

bidsModule.factory('photoService', ['$http', function ($http) {
    return{
        deletePhoto: function (photoId, callback) {
            $http.delete('/api/images/' + photoId + '/').success(function () {
                callback()
            }).error(function () {
                callback("La photo n'a pas pu être supprimée")
            })
        },
        getPhotoUrl: function (photoId, callback) {
            $http.get('/api/images/' + photoId + '/').success(function (data) {
                callback(data)
            }).error(function () {
                callback(data, 'Impossible de récupérer la photo')
            });
        }
    }
}]);

bidsModule.factory('categoryService', ['$http', function ($http) {
    return function (callback) {
        $http.get('/api/categories/').success(function (data) {
            callback(data.categories);
        }).error(function () {
            callback(data, 'Impossible de récupérer les catégories')
        });
    };
}]);

bidsModule.factory('associationsService', ['$http', function ($http) {
    return function (callback) {
        $http.get("/api/associations/?filter_by=current_user").success(function (data) {
            callback(data.associations);
        }).error(function () {
            callback(data, 'Impossible de récupérer les catégories')
        });
    }
}]);

bidsModule.factory('UserFactory', ['$http', function ($http) {
    return {
        getCurrentUser: function (callback) {
            $http.get('/api/users/0/?filter_by=current_user').success(function (data) {
                callback(data.user);
            }).error(function () {
                callback(data, defaultErrorMessage)
            });
        }
    }
}]);
bidsModule.controller('bidController', function ($scope, $http, $location, AddressService, BidService, photoService, categoryService, associationsService, MailService, UserFactory) {
    $scope.pageSize = 10;
    $scope.searchText = "";
    $scope.bids = [];
    $scope.currentPage = 0;
    $scope.numberOfPages = function () {
        return Math.ceil($scope.bids.length / $scope.pageSize);
    };

    $scope.form_title = 'Créer une annonce'; // TODO GOOD TITLE IF ITS AN UPDATE OR A CREATE

    $scope.bid = {
        'title': null,
        'description': null,
        'type': 'SUPPLY',
        'quantity': null,
        'begin': moment(),
        'end': null,
        'category': null,
        'real_author': null,
        'localization': null,
        'association': null,
        'status_bid': null,
        'photo': null,
        'creator': null
    };

    $scope.address = {
        'title': null,
        'recipient_name': null,
        'address1': null,
        'address2': null,
        'zipcode': null,
        'town': null
    };

    $scope.mail = {
        'user_to_mail': null,
        'subject': null,
        'content': null
    };

    $scope.user = {"username": null, "is_superuser": null, "is_staff": null, "id": null, "email": null};

    var url = $location.absUrl();
    var url_split = url.split('/');
    var indexOfId = url_split.indexOf('annonces') + 1;
    var bidId = url_split[indexOfId];
    var isInt = /^\d+$/;

    if (isInt.test(bidId)) {
        BidService.getBid(bidId, function (bid) {
            $scope.bid = bid;
            if ($scope.bid.photo) {
                photoService.getPhotoUrl($scope.bid.photo, function (data) {
                    $scope.bid_photo_url = data.url
                });
            }
        });
    } else {
        BidService.getBids('end', 1000, function (bids) {
            $scope.bids = bids;
        });
    }
    UserFactory.getCurrentUser(function (user) {
        $scope.user = user;
    });
    associationsService(function (associations) {
        $scope.associations = associations
    });

    BidService.getStatus(function (status) {
        $scope.status = status;
    });

    categoryService(function (categories) {
        $scope.categories = categories
    });

    AddressService.getAddresses(function (addresses) {
        $scope.addresses = addresses;
    });

    $scope.detelePhoto = function () {
        photoService.deletePhoto($scope.bid.photo, function () {
            $scope.bid_photo_url = ''
        })
    };

    $scope.createAddress = function () {
        AddressService.createAddress($scope.address, function (address, errorMessage) {
            if (errorMessage) {
                $scope.errorMessage = errorMessage;
            } else {
                $('#create_address').modal('hide');
                $scope.errorMessage = '';
                $scope.bid.localization = address;
            }
        })

    };

    $scope.sendMail = function () {
        $scope.mail.user_to_mail = $scope.bid.creator;
        MailService.sendMail($scope.mail, function (mail, errorMessage) {
            if (errorMessage) {
                $scope.errorMessage = errorMessage;
            } else {
                $('#send_mail').modal('hide');
                $scope.successMessage = 'Votre message à bien été envoyé';
            }
        })

    };

    $scope.showBid = function (table_row) {
        BidService.showBid(table_row)
    };

    $(function fileupload() {

        $('#bid_image').fileupload({
            dataType: 'json',
            add: function (e, data) {
                data.submit();
            },
            done: function (e, data) {
                var photoId = data.result.id;
                $scope.bid.photo = photoId;
                photoService.getPhotoUrl(photoId, function (data) {
                    $scope.bid_photo_url = data.url
                });
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

    $scope.createBid = function () {
        BidService.createBid($scope.bid, function (bid_id, errorMessage) {
            if (errorMessage) {
                $scope.errorMessage = errorMessage;
            } else {
                window.location = '/annonces/' + bid_id + '/';
            }
        })
    };

    $scope.updateBid = function () {
        BidService.updateBid($scope.bid, function (bid_id, errorMessage) {
            if (errorMessage) {
                $scope.errorMessage = errorMessage;
            } else {
                window.location = '/annonces/' + bid_id + '/';
            }
        })
    };

    $scope.deleteBid = function () {
        if (confirm('Vous allez supprimer cette annonce. Cette action est irréversible. Continuer ?')) {
            BidService.deleteBid($scope.bid.id, function (bid, errorMessage) {
                if (errorMessage) {
                    $scope.errorMessage = errorMessage;
                } else {
                    window.location = '/annonces/';
                }
            })
        }
    };

    $scope.acceptBid = function () {
        $http.put('/api/bids/' + $scope.bid.id + '/accept/', $scope.bid).
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
});