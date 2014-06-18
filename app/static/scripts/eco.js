
var app = angular.module('eco', [ 'ngRoute' ,'tc.chartjs' ]);


app.config(['$httpProvider', function($httpProvider) {
		$httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common['X-Requested-With'];
    }
]);

app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'home.html',
        controller: 'homeCtrl'
      }).
      when('/city/:cityId', {
        templateUrl: 'city_profile.html',
        controller: 'cityProfileCtrl'
      }).
      when('/about-us', {
        templateUrl: 'aboutus.html',
        controller: 'aboutUsCtrl'
      }).
      when('/how-it-works', {
      	templateUrl: 'howitworks.html',
      	controller: 'worksCtrl'
      }).
      when('/login', {
      	templateUrl: 'login.html',
      	controller: 'loginCtrl'
      }).
      when('/city-list', {
      	templateUrl: 'city_list.html',
      	controller: 'cityListCtrl'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);

app.factory('City', ['$http', function($http){

	cities = [];

	cities.push(
			//EXAMPLE SEATTLE OBJECT
			{
				"city_id"        : "206",
				"city_name"      : "Seattle",
				"country_name"   : "United States",
				"email"		     : "daniel@seattle.org",
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
		seattle: function(){
			return {

				// city_id
				// Unique identifier. Will begin with initial of city, followed by a 3 digit number. Eg: A001
				// city_name

				// Name of the city
				// country_name

				// Name of the country to which the city belongs
				// state_name

				// Name of the state to which the city belongs
				// email

				// Contact email of the city council
				// contact_number

				// Contact number of the city council
				// council_address

				// Contact address of the city council
				// "city_id"        : "206"
				// "city_name"      : "Seattle",
				// "country_name"   : "United States",
				// "email"		     : "daniel@seattle.org",
				// "contact_number" : "12065558050",
				// "council_address": "1st Ave, Seattle WA 98105"
			}
		}
	}

}]);


app.controller('homeCtrl', ['$scope', function($scope){

	$('nav').removeClass("navbar-fixed-top").addClass("navbar-fixed-bottom");

}]);


app.controller('cityProfileCtrl', ['City', '$scope', '$location', '$routeParams', function(City, $scope, $location, $routeParams){
	console.log("CITY PROFILE");

	//set navigation bar on the top of the page
	$(".navbar").removeClass("navbar-fixed-bottom");
	$(".navbar").addClass("navbar-fixed-top");

	city = City.get($routeParams.cityId);

	console.log("cityId "+ $routeParams.cityId);

	// colors = {
	// 	'final' : 'transparent',
	// 	'air'   : '#BEE7F2',
	// 	'water' : "#00A1EF",
	// 	'land' : "#63CE0A",
	// 	'waste' : "#a1a1a1",
	// 	'energy': "#FAEE40"
	// };


	if (city != null){

		$scope.city = city;

		//ELEMENT DATA SETUP
		for( var d in city.index_data) {

			console.log(city.index_data[d]);
			o = [
				{value : city.index_data[d], color : '#fff'},
				{value : 100 - city.index_data[d], color : 'transparent'}
			]
			$scope[d] = o;
		}

		$scope.chart_options = {
			percentageInnerCutout : 70,
			animationSteps : 60,
			animationEasing : "easeOutCubic",
			// animateScale : true,
			segmentShowStroke: false
		};

		console.log($('.collapse').collapse)
   		$('.indicators').hover(
		  function(d){
		  	console.log(d.target);
			$(d.target).closest('.indicators').find('.collapse').collapse('show');
		},function(d){
			$(d.target).closest('.indicators').find('.in').collapse('hide');
		});



	} else {

		$location.path('/');

	}

	//jQuery page control block (animations)
	$(document).ready(function(){
		//scrolling to a sub-index block
		$("#affix_menu li").click(function(){
			$.easing.power = function(t, millisecondsSince, startValue, endValue, totalDuration) {
    			return Math.pow(t,3);
			};

			event.preventDefault();
			$('html, body').animate({
    				scrollTop: $($(this).find("a").attr("href")).offset().top-100
 				},
 				1500,
 				'power'
 			);
		});

		//Showing only out of screen objects in navigation menu
		$(window).scroll(function(){
			$(".subindices").each(function(){
				var blockTop = $(this).offset().top + $(this).height()*0.25;
				var blockBottom = blockTop+$(this).height()*0.6;
				var windowTop = $(document).scrollTop();
				var windowBottom = windowTop+$(window).height();
				var $menuObject = $("#affix_menu ."+$(this).attr("id"));		//menu object related to the current block
				if(blockTop >= windowTop & blockBottom <= windowBottom){		//if block on screen
					$menuObject.fadeOut();
				} else {														//if block off screen
					$menuObject.fadeIn();
				}
			});
		});
	});
	// .jQuery control block
}]);

app.controller('aboutUsCtrl', ['$scope', function($scope){

}]);

app.controller('loginCtrl', ['$scope', '$http', '$location', function($scope, $http ,$location){

	//decoration
	//fixing the possitoin of grass even on scrolling
	stickGrassBottom();
	$(window).scroll(function(){
		stickGrassBottom();
	}).
	resize(function(){
		stickGrassBottom();
	});



	//Login processing

	$("#login").click(function(e){
		e.preventDefault();

		console.log($('#loginEmail'));

		$http({
			method: 'POST',
			url : 'http://tranquil-garden-7617.herokuapp.com/login',
			data : {
				email : $('#loginEmail').val(),
				password : $('#loginPasswd').val()
			}
		}).
		success(function(data){
			$location('/dashboard.html');
		}).
		error(function(status){

		});
	});


	//show signing up block and hide login block on Sing Up button click
	$('#singnup-show').click(function(e){
		e.preventDefault();
		$(".login-wrapper").slideUp();
		$(".signup-wrapper").slideDown();
	});

	// Highlight field green if it not empty
	$(".signup-wrapper input").focusout(function(e){
			if($(this).val()!="" && this.id != "signEmail" && this.id != "signPasswd" && this.id != "signPasswdRep"){
				$(this).parent().parent().addClass("has-success");
			}
	});

	//email varification
	$("#signEmail, #signConEmail, #loginEmail").focusout(function(e){
			if(isEmail($(this).val())){
				$(this).parent().parent().removeClass("has-error");
				$(this).parent().parent().addClass("has-success");
			} else {
				$(this).parent().parent().addClass("has-error");
				$(this).parent().parent().removeClass("has-success");
			}
	});

	//password verifications
	$("#signPasswd, #loginPasswd").focusout(function(e){
		if(checkPasswd($(this))){
			$(this).parent().parent().removeClass("has-error");
			$(this).parent().parent().addClass("has-success");
		} else {
			$(this).parent().parent().addClass("has-error");
			$(this).parent().parent().removeClass("has-success");
		}
	});

	$("#signPasswdRep").focusout(function(e){
		if(checkPasswdRep($("#signPasswd"), $(this))){
			$(this).parent().parent().removeClass("has-error");
			$(this).parent().parent().addClass("has-success");
		} else {
			$(this).parent().parent().addClass("has-error");
			$(this).parent().parent().removeClass("has-success");
		}
	});

	// phone number verification
	$("#signContPhone").focusout(function(e){
		if(isPhone(this.value)){
			$(this).parent().parent().removeClass("has-error");
			$(this).parent().parent().addClass("has-success");
		} else {
			$(this).parent().parent().addClass("has-error");
			$(this).parent().parent().removeClass("has-success");
		}
	});

	/*
	// Ign Up Button (All checks and Submission)
	$("#signup-button").click(function(e){
		e.preventDefault();

		/*CHECKING THE FIELDS*/
		/*
		var fieldsCheck=true;

		$(".signup-wrapper input").each(function(e){
			if(!$(this).val() && this.id != "signState"){
				$(this).parent().parent().addClass("has-error");
				$(this).parent().parent().removeClass("has-success");
				fieldsCheck = false;
			}
		});

		//checking email addresses
		if(!isEmail($("#signEmail").val()) && !isEmail($("#signConEmail").val())){
			fieldsCheck = false;
		}

		//checking phone number
		if(!isPhone($("#signContPhone").val())){
			fieldsCheck = false;
		}
		//checking password and its repetion
		if(!(checkPasswd($("#signPasswd")) && checkPasswdRep($("#signPasswd"),$("#signPasswdRep")))){
			fieldsCheck = false;
		}

		//if all checks succesfull - sign up!
		if(fieldsCheck){
			alert("All Correct. Sent to Server");
			$(".signup-error").hide();

				// All checks are successful
				// Post the data to the server

				//Build the messgae
				var msg = {
					'user_name' : $("#signConName").val(),
					'password' : $("#signPasswd").val(),
					'email' : $("#signEmail").val(),
					'city_id_admin' : 1
				}

				//post
				$http({
					method: 'POST',
					url : 'http://tranquil-garden-7617.herokuapp.com/register',
					message : msg
				}).
				success(function(data, status){
					alert("Success!");
					console.log(data);
				}).
				error(function(){
					alert("FAIL!");
					console.error(status);
				});

		} else {
			$(".signup-error").fadeOut();
			$(".signup-error").fadeIn();
		}
	});
	*/
	// Function: sticking position of grass to bottom of the page
	function stickGrassBottom(){
		var winHeight = $(window).height();
		var scrollPosition = $(window).scrollTop();
		var grassPositoin = winHeight + scrollPosition - 100;
		$(".beauties").css("top",grassPositoin+"px");
	}
	//Email Varification Function
		function isEmail(email){
			var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
			if(emailReg.test(email) && email != ""){
				return true;
			} else {
				return false;
			}
		}

	//Password Varification Function
		function checkPasswd($passwd){
			if($passwd.val().length > 7 && $passwd.val().length < 17){
				return true;
			} else {
				return false;
			}
		}

	//Password Repetition Varification Function
		function checkPasswdRep($passwd, $passwdrep){
			if($passwd.val() == $passwdrep.val()){
				return true;
			} else {
				return false;
			}
		}
	//Check for number values
	function isPhone(str){
		var rule = /[a-z-!$%^&*()_+|~=`{}\[\]:";'<>?,.\/]/i;
		if(rule.test(str)){
			return false;
		} else {
			return true;
		}
	}
}]);

app.controller('cityListCtrl', ['$scope', function($scope){

}]);

// app.controller('dashboardCtrl', ['$scope', function($scope){

// 	console.log("Wat wat");

// }]);
