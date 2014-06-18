
var app = angular.module('eco-dashboard', [ 'ngRoute' ,'tc.chartjs' ]);

app.factory('City', ['$http', function($http){

    cities = [];

    cities.push(
            //EXAMPLE SEATTLE OBJECT
            {
                "city_id"        : "206",
                "city_name"      : "Seattle",
                "country_name"   : "United States",
                "email"          : "daniel@seattle.org",
                "contact_number" : "12065558050",
                "council_address": "1st Ave, Seattle WA 98105",
                "index_data" : {
                    "final_index": 78,
                    "air_index": 65,
                    "water_index": 88,
                    "land_index": 45,
                    "waste_index": 99,
                    "energy_index": 33
                }
            }
    );

    return {
        get: function(cityId){
            console.log(cities);
            for( var city in cities){
                console.log(cities[city]);
                if (cities[city].city_id == cityId){
                    return cities[city];
                }
            }

            return null;

        },
    }

}]);

app.config(['$routeProvider', function($routeProvider){

	$routeProvider.
	when('/dashboard/:cityId', { //   #/dashboard
		templateUrl:'eval.html',
		controller: 'dashboardCtrl'
	}).

	when('/water/:cityId',{
		templateUrl:'static/report_water.html',
		controller: 'waterCtrl'
	}).
	when('/air/:cityId',{
		templateUrl:'static/report_air.html',
		controller: 'airCtrl'
	}).
	when('/land/:cityId',{
		templateUrl:'static/report_land.html',
		controller: 'landCtrl'
	}).
	when('/waste/:cityId',{
		templateUrl:'static/report_waste.html',
		controller: 'wasteCtrl'
	}).
	when('/energy/:cityId',{
		templateUrl:'static/report_energy.html',
		controller: 'energyCtrl'
	}).
   when('/projects/:cityId', { //   #/projects
       templateUrl:'static/projects.html',
       controller: 'projectsCtrl'
   }).
   when('/data/:cityId', { //   #/data
        templateUrl:'data_input.html',
        controller: 'dataCtrl'
   }).
   when('/options', { //   #/options
        templateUrl:'complete-eval.html',
        controller: 'dashboardCtrl'
   }).

    when('/projects/:cityId', { //   #/projects
        templateUrl:'projects.html',
        controller: 'projectsCtrl'
    }).
	otherwise({
        redirectTo: '/dashboard/206'
      });
  }]);


app.controller('dashboardCtrl', ['City', '$scope', '$location', '$routeParams', function(City, $scope, $location, $routeParams){

    city = City.get($routeParams.cityId);
    $scope.city = city;
    //console.log("cityId "+ $routeParams.cityId);

    if (city != null){

        //ELEMENT DATA SETUP
        for( var d in city.index_data) {

            console.log(city.index_data[d]);
            o = [
                {value : city.index_data[d], color : '#fff'},
                {value : 100 - city.index_data[d], color : 'transparent'}
            ];
            $scope[d] = o;
        }
    } else {

        $location.path('/');

    }


	$scope.chart_options = {
			percentageInnerCutout : 70,
			animationSteps : 60,
			animationEasing : "easeOutCubic",
			// animateScale : true,
			segmentShowStroke: false
	};
	console.log("Main Dashboard");
}]);

app.controller('waterCtrl', ['City', '$scope', '$location', '$routeParams', function(City, $scope, $location, $routeParams){

    /* Navigation Bar setup */
    //$(".side-nav .active").toggleClass("active");   //remove hughlight from other navigation elements
    //$(".side-nav .dropdown").addClass("open");      //open side navigation dropdown (with sub-indicies)
    /************************/

	city = City.get($routeParams.cityId);
    $scope.city = city;
    //console.log("cityId "+ $routeParams.cityId);

    if (city != null){

        //ELEMENT DATA SETUP
        for( var d in city.index_data) {

            console.log(city.index_data[d]);
            o = [
                {value : city.index_data[d], color : '#fff'},
                {value : 100 - city.index_data[d], color : 'transparent'}
            ];
            $scope[d] = o;
        }
    } else {

        $location.path('/');

    }


    $scope.chart_options = {
            percentageInnerCutout : 70,
            animationSteps : 60,
            animationEasing : "easeOutCubic",
            // animateScale : true,
            segmentShowStroke: false
    };
	console.log("WaterReport");

}]);
app.controller('airCtrl', ['City', '$scope', '$location', '$routeParams', function(City, $scope, $location, $routeParams){

    /* Navigation Bar setup */
    //$(".side-nav .active").toggleClass("active");   //remove hughlight from other navigation elements
    //$(".side-nav .dropdown").addClass("open");      //open side navigation dropdown (with sub-indicies)
    /************************/

    city = City.get($routeParams.cityId);
    $scope.city = city;
    //console.log("cityId "+ $routeParams.cityId);

    if (city != null){

        //ELEMENT DATA SETUP
        for( var d in city.index_data) {

            console.log(city.index_data[d]);
            o = [
                {value : city.index_data[d], color : '#fff'},
                {value : 100 - city.index_data[d], color : 'transparent'}
            ];
            $scope[d] = o;
        }
    } else {

        $location.path('/');

    }


    $scope.chart_options = {
            percentageInnerCutout : 70,
            animationSteps : 60,
            animationEasing : "easeOutCubic",
            // animateScale : true,
            segmentShowStroke: false
    };
    console.log("AirReport");

}]);
app.controller('landCtrl', ['City', '$scope', '$location', '$routeParams', function(City, $scope, $location, $routeParams){

    /* Navigation Bar setup */
    //$(".side-nav .active").toggleClass("active");   //remove hughlight from other navigation elements
    //$(".side-nav .dropdown").addClass("open");      //open side navigation dropdown (with sub-indicies)
    /************************/

    city = City.get($routeParams.cityId);
    $scope.city = city;
    //console.log("cityId "+ $routeParams.cityId);

    if (city != null){

        //ELEMENT DATA SETUP
        for( var d in city.index_data) {

            console.log(city.index_data[d]);
            o = [
                {value : city.index_data[d], color : '#fff'},
                {value : 100 - city.index_data[d], color : 'transparent'}
            ];
            $scope[d] = o;
        }
    } else {

        $location.path('/');

    }


    $scope.chart_options = {
            percentageInnerCutout : 70,
            animationSteps : 60,
            animationEasing : "easeOutCubic",
            // animateScale : true,
            segmentShowStroke: false
    };
    console.log("LandReport");

}]);

app.controller('wasteCtrl', ['City', '$scope', '$location', '$routeParams', function(City, $scope, $location, $routeParams){

    /* Navigation Bar setup */
    //$(".side-nav .active").toggleClass("active");   //remove hughlight from other navigation elements
    //$(".side-nav .dropdown").addClass("open");      //open side navigation dropdown (with sub-indicies)
    /************************/

    city = City.get($routeParams.cityId);
    $scope.city = city;
    //console.log("cityId "+ $routeParams.cityId);

    if (city != null){

        //ELEMENT DATA SETUP
        for( var d in city.index_data) {

            console.log(city.index_data[d]);
            o = [
                {value : city.index_data[d], color : '#fff'},
                {value : 100 - city.index_data[d], color : 'transparent'}
            ];
            $scope[d] = o;
        }
    } else {

        $location.path('/');

    }


    $scope.chart_options = {
            percentageInnerCutout : 70,
            animationSteps : 60,
            animationEasing : "easeOutCubic",
            // animateScale : true,
            segmentShowStroke: false
    };
    console.log("WasteReport");

}]);

app.controller('energyCtrl', ['City', '$scope', '$location', '$routeParams', function(City, $scope, $location, $routeParams){

    /* Navigation Bar setup */
    //$(".side-nav .active").toggleClass("active");   //remove hughlight from other navigation elements
    //$(".side-nav .dropdown").addClass("open");      //open side navigation dropdown (with sub-indicies)
    /************************/

    city = City.get($routeParams.cityId);
    $scope.city = city;
    //console.log("cityId "+ $routeParams.cityId);

    if (city != null){

        //ELEMENT DATA SETUP
        for( var d in city.index_data) {

            console.log(city.index_data[d]);
            o = [
                {value : city.index_data[d], color : '#fff'},
                {value : 100 - city.index_data[d], color : 'transparent'}
            ];
            $scope[d] = o;
        }
    } else {

        $location.path('/');

    }


    $scope.chart_options = {
            percentageInnerCutout : 70,
            animationSteps : 60,
            animationEasing : "easeOutCubic",
            // animateScale : true,
            segmentShowStroke: false
    };
    console.log("EnergyReport");

}]);

app.controller('projectsCtrl', ['$scope', function($scope){



    $scope.project_data = {

        labels : ["January","February","March","April","May","June","July"],
        datasets : [
            {
                fillColor : "rgba(220,220,220,0.5)",
                strokeColor : "rgba(220,220,220,1)",
                pointColor : "rgba(220,220,220,1)",
                pointStrokeColor : "#fff",
                data : [65,59,90,81,56,55,40]
            },
            {
                fillColor : "rgba(151,187,205,0.5)",
                strokeColor : "rgba(151,187,205,1)",
                pointColor : "rgba(151,187,205,1)",
                pointStrokeColor : "#fff",
                data : [28,48,40,19,96,27,100]
            }
        ]
    }

    $scope.project_donut = [
        {
            value: 30,
            color:"#F7464A"
        },
        {
            value : 50,
            color : "#E2EAE9"
        },
        {
            value : 100,
            color : "#D4CCC5"
        },
        {
            value : 40,
            color : "#949FB1"
        },
        {
            value : 120,
            color : "#4D5360"
        }
    ]


    $scope.chart_options = {
            percentageInnerCutout : 70,
            animationSteps : 60,
            animationEasing : "easeOutCubic",
            // animateScale : true,
            segmentShowStroke: false
    };




    console.log("Wat wat");

}]);

app.controller('dataCtrl', ['$scope', function($scope){

	$scope.chart_options = {
			percentageInnerCutout : 70,
			animationSteps : 60,
			animationEasing : "easeOutCubic",
			// animateScale : true,
			segmentShowStroke: false
	};
	console.log("EnergyReport");

}]);
