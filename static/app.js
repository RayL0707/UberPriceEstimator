
var app = angular.module('plunker', ['google-maps', 'gm']);
app.service('datapack', function() {
    var weatherinfo = {};
    var routeinfo = {}; 
    return {
        getweather: function() {
            return weatherinfo;
        },
        setweather: function(value) {
            
            weatherinfo = value;
        },
        getroute: function() {
            return routeinfo;
        },
        setroute: function(value) {
            routeinfo=value;
        }
    }
});

//---------------------weather data fetch-----------------------------
app.controller('WeatherCtrl', function($scope, $http, $timeout, datapack) {
  $http.get("http://api.openweathermap.org/data/2.5/weather?q=New%20York&appid=1e75a19653a560d0aaa8bf94c3f203f4").then(function (response) {
      $scope.myData = [response.data,[false,false,false,false,false,false,false],'clean'];
      $scope.temper=($scope.myData[0].main.temp*1.8-459.67).toFixed(2);
      $scope.winds=($scope.myData[0].wind.speed*2.237).toFixed(2);
      $scope.wicon=[false,false,false,false,false,false,false];
      $scope.wtr=($scope.myData[0].weather[0].main).toLowerCase();
      $scope.myData[2]=$scope.wtr;
      var list = [
      "clear-day",
      "partly-cloudy-day",
      "cloudy",
      "sleet",
      "snow",
      "fog",
      "wind",
      "clear-night", 
      "partly-cloudy-night",
      "rain"  
     ];

     var list1 = [
      "clear",
      "broken clouds",
      "clouds",
      "rain",
      "snow",
      "mist",
      "unknown"
     ];
      var icons = new Skycons({"color":"#777c75"});
    for(i = list.length; i--;)
  icons.set(list[i], list[i]);
  icons.play();
  
      //------------------convert weather data-------------------
      if ($scope.wtr=="clear sky"|| $scope.wtr=="clear")//clear
        {$scope.weather=1;
          $(document).snowfall({round:false,minSize:420,maxsize:420,maxSpeed:0,minSpeed:0,image :"i/sun1.png",flakeCount:1});
        }
      else if ($scope.wtr=="scattered clouds"|| $scope.wtr=="broken clouds")//overcast
         {$scope.weather=2;
         $(document).snowfall({round:false,minSize:400,maxsize:420,maxSpeed:0,minSpeed:0,image :"i/bcloud.png",flakeCount:8});
       }
       else if ($scope.wtr=="few clouds"|| $scope.wtr=="clouds")//cloudy
         {$scope.weather=3;
          $(document).snowfall({round:false,minSize:400,maxsize:420,maxSpeed:0,minSpeed:0,image :"i/cloud.png",flakeCount:4});
         }
       else if ($scope.wtr=="shower rain"|| $scope.wtr=="rain"|| $scope.wtr=="thunderstorm")//rain
         {$scope.weather=4;
          $(document).snowfall({round:false,minSize:350,maxsize:360,maxSpeed:12,minSpeed:10,image :"i/rain.png",flakeCount:25});
         }
       else if ($scope.wtr=="snow")//snow
         {$scope.weather=5;
          $(document).snowfall({round:true,minSize:4,maxSize:35,text:'XX',image :"i/snowflake.png",flakeColor:'',collection:'',flakeCount:50});
         }
       else if ($scope.wtr=="mist"|| $scope.wtr=="haze"|| $scope.wtr=="fog")//haze
         {$scope.weather=6;
          $(document).snowfall({round:false,minSize:300,maxsize:300,maxSpeed:0,minSpeed:0,image :"i/mist.png",flakeCount:25});
         }
       else//unknown
         {$scope.weather=7;}
       var check=$scope.weather-1
           $scope.myData[1][check]=true;
      var weatherinfo={'temp':$scope.temper,'wind':$scope.winds,'weather':$scope.weather};
        
      //--------------------add weather effects---------------------------
        $scope.manualWeather = function (){
        
          $(document).snowfall('clear');
          if ($scope.weatherpick==1)
          {$(document).snowfall({round:false,minSize:420,maxsize:420,maxSpeed:0,minSpeed:0,image :"i/sun1.png",flakeCount:1});
        $scope.weather=1;}
          else if ($scope.weatherpick==2)
          {$(document).snowfall({round:false,minSize:400,maxsize:420,maxSpeed:0,minSpeed:0,image :"i/bcloud.png",flakeCount:8});
        $scope.weather=2;}
          else if ($scope.weatherpick==3)
          {$(document).snowfall({round:false,minSize:400,maxsize:420,maxSpeed:0,minSpeed:0,image :"i/cloud.png",flakeCount:4});
        $scope.weather=3;}
          else if ($scope.weatherpick==4)
          {$(document).snowfall({round:false,minSize:350,maxsize:360,maxSpeed:12,minSpeed:10,image :"i/rain.png",flakeCount:25});
        $scope.weather=4;}
          else if ($scope.weatherpick==5)
          {$(document).snowfall({round:true,minSize:4,maxSize:35,text:'XX',image :"i/snowflake.png",flakeColor:'',collection:'',flakeCount:50});
        $scope.weather=5;}
          else if ($scope.weatherpick==6)
          {$(document).snowfall({round:false,minSize:300,maxsize:300,maxSpeed:0,minSpeed:0,image :"i/mist.png",flakeCount:25});
        $scope.weather=6;}
        weatherinfo['weather']=$scope.weather;
        
        $scope.myData[2]=list1[$scope.weatherpick-1];
        
        datapack.setweather(JSON.stringify(weatherinfo));
        
        console.log(weatherinfo,$scope.myData[2]);
        };      
  
      
      datapack.setweather(JSON.stringify(weatherinfo));
      
  });
});


//----------------------main map function-----------------------------
app.controller('MainCtrl', function($scope, $document,datapack,$http) {
  var showprice=false;
  // map object
    $scope.map = {
      control: {},
      center: {
          latitude: 40.758896,
          longitude: -73.985130
      },
      zoom: 12,
      options: {
         mapTypeId: google.maps.MapTypeId.SATELLITE
      }
    };
          var image = {
          url: 'i/columbia.png',       
          size: new google.maps.Size(40, 40),
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(0, 32)
        };
    //marker object
    $scope.marker = {
      icon:image,
      center: {
          latitude: 40.8095,
          longitude: -73.964
      }
    };
 
    var directionsDisplay = new google.maps.DirectionsRenderer();
    var directionsService = new google.maps.DirectionsService();
    var geocoder = new google.maps.Geocoder();


  $scope.$on('gmPlacesAutocomplete::placeChanged', function(){
      // get directions using google maps api
      $scope.getDirections = function () {
        var request = {
          origin: $scope.directions.origin.getPlace().formatted_address,
          destination: $scope.directions.destination.getPlace().formatted_address,
          travelMode: google.maps.DirectionsTravelMode.DRIVING
        };

        directionsService.route(request, function (response, status) {
          if (status === google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
            directionsDisplay.setMap($scope.map.control.getGMap());
            directionsDisplay.setPanel(document.getElementById('directionsList'));
            $scope.directions.showList = true;
            var travelinfo=JSON.stringify(response);
            var travelinfos=JSON.parse(travelinfo);
            var distanceinmile=travelinfos['routes'][0]['legs'][0]['distance']['value']*0.000621371
            var durationinmin=travelinfos['routes'][0]['legs'][0]['duration']['value']*1.0/60
            
            //------------------covert time------------------------------
            var d=new Date();
            var hrs=d.getHours();
            var timehr=8;
            if (hrs>=0 && hrs<3)
              {timehr=1;}
            else if (hrs>=3 && hrs<6)
              {timehr=2;}
            else if (hrs>=6 && hrs<9)
              {timehr=3;}
            else if (hrs>=9 && hrs<12)
              {timehr=4;}
            else if (hrs>=12 && hrs<15)
              {timehr=5;}
            else if (hrs>=15 && hrs<18)
              {timehr=6;}
            else if (hrs>=18 && hrs<21)
              {timehr=7;}
        //----------------------------convert time----------------------------

            var routeinfo={'passengerNo':$scope.passengerNo,'origin':$scope.directions.origin.getPlace().formatted_address,'destination':$scope.directions.destination.getPlace().formatted_address,'distanceinmile':distanceinmile,'durationinmin':durationinmin,'timeNo':timehr};
            datapack.setroute(JSON.stringify(routeinfo));
    
        //----------------------send data to server---------------------------
            var datas=JSON.stringify([JSON.parse(datapack.getweather()),JSON.parse(datapack.getroute())]);//string(array)
            console.log(JSON.parse(datas));
            $scope.showprice=true;
            $scope.uberprice=13.03;
            $http({
              method : 'POST',
              url : 'http://localhost:5000/getPrice',
              data : JSON.parse(datas), //parse to json before sending
              'Content-Type': 'application/json'           
              }).success(function(data){
                  /*called for result & error because 200 status*/
                  $scope.uberprice = data.toFixed(2);
              })
              .error(function(data){
                  alert(data)
              });

            //----------------------send data to server----------------------------
 
          } else {
            alert('Google route unsuccesfull!');
          }
        });
      }
    });



});




