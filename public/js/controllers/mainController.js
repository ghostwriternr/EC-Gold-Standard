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

        $scope.showSelectedText1 = function(index) {
            $scope.index1 = index;
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
        $scope.showSelectedText2 = function(index) {
            $scope.index2 = index;
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
                        entity1: $scope.firstSelected,
                        entity2: $scope.secondSelected,
                        heading1: $scope.paragraphs.Pairs[$scope.index1]['second']['title'],
                        heading2: $scope.paragraphs.Pairs[$scope.index2]['first']['title'],
                        sentence1: $scope.selectedText1,
                        sentence2: $scope.selectedText2
                    }
                })
                .then(function locationSuccessCallback(response) {
                    console.log(response);
                }, function locationErrorCallback(response) {
                    console.log(response);
                });
        };

        $scope.addComparable = function(answer) {
            $http({
                    url: '/api/updateComparable',
                    method: 'POST',
                    params: {
                        entity1: $scope.firstSelected,
                        entity2: $scope.secondSelected,
                        comparable: answer
                    }
                })
                .then(function locationSuccessCallback(response) {
                    console.log(response);
                }, function locationErrorCallback(response) {
                    console.log(response);
                });
        };
    }]);
