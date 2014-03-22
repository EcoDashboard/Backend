document.getElementById("btn_submit").addEventListener("click", function() {
	var form = document.getElementById("form_input");
	var array = new Array();
	var JSONresult;
	var upperLimit = [300, 374, 500, 600, 2000, 40, 50];
	
	for (var i = 0; i < form.length - 1; i++) {
		var value  = form.elements[i].value;
		
		if (value > 0 && value <= upperLimit[i] && value != null) {
			array[i] = value;
		}
		else {
			alert("Wrong Input Number.");
			return;
		}
	}
	
	JSONresult = "{\"cat_ID\":\"1\",\"Indicators\":[";
	for (var i = 0; i < form.length - 2; i++) {
		JSONresult += "{\"Ind_" + (i + 1) + "\"," + array[i] + "},";
	}
	JSONresult += "{\"Ind_" + 7 + "\"," + array[6] + "}";
	JSONresult += "]}";
    var req = new XMLHttpRequest();
    req.open("POST", "http://127.0.0.1:5000/saveScore", true);
	req.setRequestHeader("Content-type", "application/json");
	req.send(NULL);
	
	req.onreadystatechange  = function(){
	if (http_request.readyState == 4  ){
	if(req.status == 200) {
        alert(req.responseText);
	}
	}
});
