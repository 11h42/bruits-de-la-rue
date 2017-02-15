var bidsModule = angular.module('bidsModule', ['ui.bootstrap.datetimepicker']);

bidsModule.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});


bidsModule.controller('bidsController', function ($scope, bidService) {
    $scope.bids = [];
    bidService.getBids('-end', 1000, function (bids, errorMessage) {
        if (errorMessage) {
            $scope.errorMessage = errorMessage;
            return;
        }
        $scope.bids = bids
    });

    $scope.showBid = function (bidId) {
        bidService.showBid(bidId)
    };
});


bidsModule.controller('bidController', function ($scope, $location, bidService, categoryService, addressService, associationsService, mailService) {
    $scope.bid = {
        'title': null,
        'description': null,
        'type': null,
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

    $scope.desired_amount = null;

    $scope.address = {
        'title': null,
        'recipient_name': null,
        'address1': null,
        'address2': null,
        'zipcode': null,
        'town': null
    };

    function getBidIdInUrl() {
        var url = $location.absUrl();
        var url_split = url.split('/');
        var indexOfId = url_split.indexOf('annonces') + 1;
        var bidId = url_split[indexOfId];
        var isInt = /^\d+$/;

        if (isInt.test(bidId)) {
            return bidId
        }
    }

    function getAllInformation(callback) {
        associationsService(function (associations) {
            $scope.associations = associations;
            categoryService(function (categories) {
                $scope.categories = categories;
                addressService.getAddresses(function (addresses) {
                    $scope.addresses = addresses;
                    callback($scope.associations, $scope.categories, $scope.addresses)
                });
            });
        });
    }

    var bidId = getBidIdInUrl();
    if (bidId) {
        bidService.getBid(bidId, function (bid) {
            $scope.bid = bid;

            getAllInformation(function (associations, categories, addresses) {
                if ($scope.bid.association) {
                    for (var i = 0; i < associations.length; i++) {
                        if (associations[i].id == $scope.bid.association.id) {
                            $scope.bid.association = $scope.associations[i];
                        }
                    }
                }
                if ($scope.bid.category) {
                    for (var j = 0; j < categories.length; j++) {
                        if (categories[j].id == $scope.bid.category.id) {
                            $scope.bid.category = $scope.categories[j];
                        }
                    }
                }
                if ($scope.bid.localization) {
                    for (var k = 0; k < addresses.length; k++) {
                        if (addresses[k].id == $scope.bid.localization.id) {
                            $scope.bid.localization = $scope.addresses[k];
                        }
                    }
                }
            });
        });
    } else {
        getAllInformation(function () {
        })
    }

    $scope.createAddress = function () {
        addressService.createAddress($scope.address, function (address_location, errorMessage) {
            if (errorMessage) {
                $scope.errorMessage = errorMessage;
            } else {
                $('#create_address').modal('hide');
                $scope.errorMessage = '';
                addressService.getAddressWithLocation(address_location, function (address) {
                    $scope.addresses.push(address);

                    for (var k = 0; k < $scope.addresses.length; k++) {
                        if ($scope.addresses[k].id == address.id) {
                            $scope.bid.localization = $scope.addresses[k];
                        }
                    }
                });
            }
        })
    };

    $scope.createBid = function () {
        bidService.createBid($scope.bid, function (bid_id, errorMessage) {
            if (errorMessage) {
                $scope.errorMessage = errorMessage;
            } else {
                window.location = '/annonces/' + bid_id + '/';
            }
        })
    };

    $scope.validBid = function (){
        bidService.validBid($scope.bid.id, function (bid_id, errorMessage) {
            if (errorMessage) {
                $scope.errorMessage = errorMessage;
            } else {
                window.location = '/annonces/';
            }
        })
    };

    $scope.createOrUpdateBid = function () {
        if ($scope.bid.id) {
            bidService.updateBid($scope.bid, function (bid_id, errorMessage) {
                if (errorMessage) {
                    $scope.errorMessage = errorMessage;
                } else {
                    window.location = '/annonces/' + bid_id + '/';
                }
            })
        } else {

            bidService.createBid($scope.bid, function (bid_id, errorMessage) {
                if (errorMessage) {
                    $scope.errorMessage = errorMessage;
                } else {
                    window.location = '/annonces/' + bid_id + '/';
                }
            })
        }
    };

    $scope.deleteBid = function () {
        if (confirm('Vous allez supprimer cette annonce. Cette action est irréversible. Continuer ?')) {
            bidService.deleteBid($scope.bid.id, function (bid, errorMessage) {
                if (errorMessage) {
                    $scope.errorMessage = errorMessage;
                } else {
                    window.location = '/';
                }
            })
        }
    };

    $scope.acceptBid = function () {
        var desiredAmount = $scope.desired_amount;
        if (desiredAmount > $scope.bid.quantity || desiredAmount < 0 || desiredAmount == undefined) {
            $scope.errorMessage = 'Veuillez indiquer une quantité valide'
        } else {
            bidService.acceptBid({desired_amount: desiredAmount, id: $scope.bid.id}, function (data, err) {
                if (err) {
                    $scope.errorMessage = err;
                } else {
                    $('#accept_bid').modal('hide');
                    $scope.errorMessage = '';
                    $scope.successMessage = "Vous avez accepté cette annonce, prenez contact avec l'auteur pour continuer l'échange"
                }
            })
        }
    };

    $scope.mail = {
        'user_to_mail': null,
        'subject': null,
        'content': null
    };

    $scope.sendMail = function () {
        $scope.mail.user_to_mail = $scope.bid.creator;
        $('#send_mail').modal('hide');
        mailService.sendMail($scope.mail, function (mail, errorMessage) {
            if (errorMessage) {
                $scope.errorMessage = errorMessage;
            } else {
                $scope.errorMessage = '';
                $scope.successMessage = 'Votre message a bien été envoyé';
            }
        })
    };

});


bidsModule.factory('bidService', ['$http', function ($http) {
    return {
        getBids: function (order_by, limit, callback) {
            $http.get('/api/bids/?order_by=' + order_by + '&limit=' + limit).success(function (data) {
                callback(data.bids);
            }).error(function () {
                callback([], 'Il nous est impossible de récupérer les annonces pour le moment, retentez plus tard');
            });
        },
        getBid: function (bidId, callback) {
            $http.get('/api/bids/' + bidId + '/').success(function (data) {
                callback(data.bid);
            }).error(function () {
                callback({}, 'Il nous est impossible de récupérer cette annonce pour le moment, retentez plus tard');
            })
        },
        validBid: function (bidId, callback) {
            $http.post('/api/bids/' + bidId + '/valid/').success(function () {
                callback(bidId);
            }).error(function () {
                callback({}, 'Vous ne pouvez pas valider une annonce, avez-vous les droits?');
            })
        },
        deleteBid: function (bidId, callback) {
            $http.delete('/api/bids/' + bidId + '/').success(function (data) {
                callback(data);
            }).error(function () {
                callback({}, 'Vous ne pouvez pas supprimer cette annonce');
            })
        },
        createBid: function (bid, callback) {
            $http.post('/api/bids/', bid).success(function (data) {
                callback(data.bid_id);
            }).error(function (error) {
                callback({}, error.message);
            });
        },
        updateBid: function (bid, callback) {
            $http.put('/api/bids/' + bid.id + '/', bid).success(function (data) {
                callback(data.bid_id);
            }).error(function () {
                callback({}, 'Il nous est impossible de mettre à jour cette annonce pour le moment, retentez plus tard');
            });
        },
        showBid: function (bidId) {
            window.location = '/annonces/' + bidId + '/';
        },
        acceptBid: function (bid, callback) {
            $http.put('/api/bids/' + bid.id + '/accept/', bid).success(function (data) {
                callback(data);
            }).error(function () {
                callback({}, "Il nous est impossible d'accepter cette annonce pour le moment, retentez plus tard");
            });
        }
    }
}]);


bidsModule.factory('categoryService', ['$http', function ($http) {
    return function (callback) {
        $http.get('/api/categories/').success(function (data) {
            callback(data.categories);
        }).error(function (data) {
            callback(data, 'Impossible de récupérer les catégories')
        });
    };
}]);

bidsModule.factory('mailService', ['$http', function ($http) {
    return {
        sendMail: function (mail, callback) {
            $http.post('/api/mails/', mail).success(function (data) {
                callback(data);
            }).error(function (data) {
                callback([], "Il nous est impossible d'envoyer un email pour le moment, veuillez retentez dans quelques minutes");
            });
        }
    }
}]);

bidsModule.factory('addressService', ['$http', function ($http) {
    return {
        getAddresses: function (callback) {
            $http.get('/api/addresses/').success(function (data) {
                callback(data.addresses)
            }).error(function () {
                callback([], 'Impossible de récupérer les adresses');
            });
        },
        createAddress: function (address, callback) {
            $http.post('/api/addresses/', address).success(function (data, status, headers, config) {
                console.log(headers('location'));
                callback(headers('location'));
            }).error(function () {
                callback({}, 'Impossible de créer une adresse, vérifiez que tous les champs obligatoires sont présents et que le code postal est bien un chiffre')
            });
        },
        getAddressWithLocation: function (location, callback) {
            $http.get(location).success(function (data) {
                callback(data);
            }).error(function () {
                callback({}, 'Il nous est impossible de récupérer cette annonce pour le moment, retentez plus tard');
            })
        }
    }
}]);

bidsModule.factory('associationsService', ['$http', function ($http) {
    return function (callback) {
        $http.get("/api/associations/").success(function (data) {
            callback(data.associations);
        }).error(function () {
            callback([], 'Impossible de récupérer les associations, recharger la page dans quelques instants')
        });
    }
}]);

bidsModule.directive('validNumber', function () {
    return {
        require: '?ngModel',
        link: function (scope, element, attrs, ngModelCtrl) {
            if (!ngModelCtrl) {
                return;
            }

            ngModelCtrl.$parsers.push(function (val) {
                var clean = val.replace(/[^0-9]+/g, '');
                if (val !== clean) {
                    ngModelCtrl.$setViewValue(clean);
                    ngModelCtrl.$render();
                }
                return clean;
            });

            element.bind('keypress', function (event) {
                if (event.keyCode === 32) {
                    event.preventDefault();
                }
            });
        }
    };
});

bidsModule.filter('fromNow', function () {
    return function (dateString) {
        moment.locale('fr', {});
        return moment(dateString).fromNow()
    };
});