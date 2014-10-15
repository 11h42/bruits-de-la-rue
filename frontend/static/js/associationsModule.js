var associationsModule = angular.module('associationsModule', []);

associationsModule.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});


associationsModule.controller('associationsController', function ($scope, $location, associationService) {
    $scope.associations = [];

    associationService.getAssociations('end', 1000, function (associations, errorMessage) {
        if (errorMessage) {
            $scope.errorMessage = errorMessage;
            return;
        }
        $scope.associations = associations
    });


    $scope.showAssociation = function (associationId) {
        associationService.showAssociation(associationId)
    };
});


associationsModule.controller('associationController', function ($scope, $location, $window, associationService, userService) {
    $scope.association = {};

    function getAssociationIdInUrl() {
        var url = $location.absUrl();
        var url_split = url.split('/');
        var indexOfId = url_split.indexOf('associations') + 1;
        var associationId = url_split[indexOfId];
        var isInt = /^\d+$/;

        if (isInt.test(associationId)) {
            return associationId
        }
    }

    var associationId = getAssociationIdInUrl();
    associationService.getAssociation(associationId, function (association, errorMessage) {
        if (errorMessage) {
            $scope.errorMessage = errorMessage;
            return;
        }
        $scope.association = association
    });


    userService.getUsers('end', 1000, function (users, errorMessage) {
        if (errorMessage) {
            $scope.errorMessage = errorMessage;
            return;
        }
        $scope.users = users
    });

    $scope.deleteAssociation = function (associationId) {
        if (confirm('Vous allez supprimer cette association. Cette action est irréversible. Continuer ?')) {
            associationService.deleteAssociation(associationId, function (association, errorMessage) {
                if (errorMessage) {
                    $scope.errorMessage = errorMessage;
                } else {
                    window.location = '/associations/';
                }
            })
        }
    };

    $scope.addUser = function (associationId, memberId) {
        associationService.addMember(associationId, memberId, function (memberLocation, errorMessage) {
            if (errorMessage) {
                $scope.errorMessage = errorMessage;
            } else {
                $scope.errorMessage = '';
                $window.location.reload();
            }
        })
    };

    $scope.deleteUser = function (userId) {
        if (confirm("Vous allez supprimer cet utilisateur de l'application. Cette action est irréversible. Continuer ?")) {
            associationService.deleteUser(userId, function (user, errorMessage) {
                if (errorMessage) {
                    $scope.errorMessage = errorMessage;
                } else {
                    $window.location.reload();
                }
            })
        }
    };


    $scope.deleteMember = function (associationId, memberId) {
        if (confirm("Vous allez supprimer cet utilisateur de l'association. Cette action est irréversible. Continuer ?")) {
            associationService.deleteMember(associationId, memberId, function (association, errorMessage) {
                if (errorMessage) {
                    $scope.errorMessage = errorMessage;
                } else {
                    $window.location.reload();
                }
            })
        }
    }

});

associationsModule.factory('associationService', ['$http', function ($http) {
    return {
        getAssociations: function (order_by, limit, callback) {
            $http.get('/api/associations/?order_by=' + order_by + '&limit=' + limit).success(function (data) {
                callback(data.associations);
            }).error(function () {
                callback([], 'Il nous est impossible de récupérer les associations pour le moment, retentez plus tard');
            });
        },
        getAssociation: function (associationId, callback) {
            $http.get('/api/associations/' + associationId + '/').success(function (data) {
                callback(data.association);
            }).error(function () {
                callback({}, 'Il nous est impossible de récupérer cette association pour le moment, retentez plus tard');
            })
        },
        deleteAssociation: function (associationId, callback) {
            $http.delete('/api/associations/' + associationId + '/').success(function (data) {
                callback(data);
            }).error(function () {
                callback({}, 'Vous ne pouvez pas supprimer cette association');
            })
        },
        addMember: function (associationId, memberId, callback) {
            $http.post('/api/associations/' + associationId + '/members/' + memberId + '/').success(function (data) {
                callback(data);
            }).error(function () {
                callback({}, 'Vous ne pouvez pas ajouter ce membre à cette association, retentez plus tard');
            })
        },
        deleteMember: function (associationId, memberId, callback) {
            $http.delete('/api/associations/' + associationId + '/members/' + memberId + '/').success(function (data) {
                callback(data);
            }).error(function () {
                callback({}, 'Vous ne pouvez pas supprimer ce membre de cette association');
            })
        },
        deleteUser: function (userId, callback) {
            $http.delete('/api/users/' + userId + '/').success(function (data) {
                callback(data);
            }).error(function () {
                callback({}, 'Vous ne pouvez pas supprimer cet utilisateur');
            })
        },
        createAssociation: function (association, callback) {
            $http.post('/api/associations/', association).
                success(function (data) {
                    callback(data.association_id);
                }).error(function () {
                    callback({}, 'Il nous est impossible de créer cette association pour le moment, retentez plus tard');
                });
        },
        updateAssociation: function (association, callback) {
            $http.put('/api/associations/' + association.id + '/', association).
                success(function (data) {
                    callback(data.association_id);
                }).error(function () {
                    callback({}, 'Il nous est impossible de mettre à jour cette association pour le moment, retentez plus tard');
                });
        },
        showAssociation: function (associationId) {
            window.location = '/associations/' + associationId + '/';
        },
        acceptAssociation: function (association, callback) {
            $http.put('/api/associations/' + association.id + '/accept/', association).
                success(function (data) {
                    callback(data);
                }).error(function () {
                    callback({}, "Il nous est impossible d'accepter cette association pour le moment, retentez plus tard");
                });
        }
    }
}]);


associationsModule.factory('userService', ['$http', function ($http) {
    return {
        getUsers: function (order_by, limit, callback) {
            $http.get('/api/users/?order_by=' + order_by + '&limit=' + limit).success(function (data) {
                callback(data.users);
            }).error(function () {
                callback([], "Il nous est impossible de récupérer les utilisateurs de l'application pour le moment, retentez plus tard");
            });
        }
    }
}]);