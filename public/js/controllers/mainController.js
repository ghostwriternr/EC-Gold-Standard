angular.module('mainCtrl', [])
    .controller('mainController', ['$scope', '$http', function($scope, $http) {
        $scope.allList = [];
        $scope.allArr = [];
        var init = function() {
            $http({
                    url: '/api/getList',
                    method: 'GET'
                })
                .then(function locationSuccessCallback(response) {
                    console.log(response);
                    $scope.allList = response.data;
                }, function locationErrorCallback(response) {
                    console.log(response);
                });
        };
        init();
        $scope.$watchGroup(['firstSelected', 'secondSelected'], function(newValues, oldValues, scope) {
            if (!(newValues[0] == null || newValues[1] == null)) {
                console.log(newValues[0], newValues[1]);
                getParagraphs();
            }
        });
        var getParagraphs = function() {
            $http({
                    url: '/api/getParas',
                    method: 'GET',
                    params: {
                        first: $scope.firstSelected,
                        second: $scope.secondSelected
                    }
                })
                .then(function locationSuccessCallback(response) {
                    $scope.paragraphs = response.data;
                    console.log($scope.paragraphs);
                }, function locationErrorCallback(response) {
                    console.log(response.status);
                });
        };

        $scope.showSelectedText1 = function() {
            $scope.selectedText1 = $scope.getSelectionText1();
        };
        $scope.getSelectionText1 = function() {
            var text = "";
            if (window.getSelection) {
                text = window.getSelection().toString();
            } else if (document.selection && document.selection.type != "Control") {
                text = document.selection.createRange().text;
            }
            console.log(text);
            return text;
        };
        $scope.showSelectedText2 = function() {
            $scope.selectedText2 = $scope.getSelectionText2();
        };
        $scope.getSelectionText2 = function() {
            var text = "";
            if (window.getSelection) {
                text = window.getSelection().toString();
            } else if (document.selection && document.selection.type != "Control") {
                text = document.selection.createRange().text;
            }
            console.log(text);
            return text;
        };

        $scope.addPair = function() {
            $http({
                    url: '/api/addPair',
                    method: 'POST',
                    params: {
                        
                    }
                })
                .then(function locationSuccessCallback(response) {
                    console.log(response);
                    $scope.allList = response.data;
                }, function locationErrorCallback(response) {
                    console.log(response);
                });
        }
    }]);
