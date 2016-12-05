var rosary = angular.module('rosary', []); 

rosary.controller('rosaryControler', function($scope){
    var socket = io.connect('https://' + document.domain + ':' + location.port + '/rosary')
    
    $scope.prayer = []
    $scope.text = ''; 
    
    socket.on('prayer', function(prayer){ 
        console.log(prayer); 
        $scope.prayer.push(prayer); 
        $scope.$apply();
        var elem = document.getElementById('msgpane');
        elem.scrollTop = elem.scrollHeight; 
        
        
    });
    
    socket.on('connect', function(){
       console.log('connected'); 
        
    });
    
});