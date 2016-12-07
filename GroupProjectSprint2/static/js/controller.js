var rosary = angular.module('rosary', []); 

rosary.controller('rosaryControler', function($scope){
    var socket = io.connect('https://' + document.domain + ':' + location.port + '/rosary');
    
    $scope.prayer = [];
    $scope.text = '';
    
    socket.on('prayer', function(p){ 
        console.log($scope.prayer);
        console.log(p); 
        $scope.prayer.push(p); 
        $scope.$apply();
        var elem = document.getElementById('msgpane');
        elem.scrollTop = elem.scrollHeight; 
        
    });
    
   $scope = function send() {
        console.log('sending message: ', $scope.text);
        socket.emit('message', $scope.text);
        $scope.text = '';
    };
    
    socket.on('connect', function(){
       console.log('connected'); 
        
    });
    
});