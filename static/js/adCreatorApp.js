angular.module('adCreatorApp', [])
    .constant('folderAdUrl', '/folder_ad')
    .controller('folderAdCtrl', function ($scope, $http, $location, folderAdUrl) {
        $scope.data = {};
        $scope.data.folder = {};

        $scope.reloadData = function (url) {
            $http.get(url)
                .success(function (data) {
                    $scope.data.folder = data;
                    $location.path(data.pk);
                })
                .error(function (error) {
                    $scope.data.error = error;
                });
        };

        // Checks if url pattern has correct format.
        if (!(/^(\/\d+)?$/.test($location.path()))) {
            $scope.data.error = 'Incorrect url pattern format.';
        }

        $scope.reloadData(folderAdUrl + $location.path() + '/');
    });
