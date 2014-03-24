document.getElementById("btn_submit").addEventListener("click", function() {
	var form = document.getElementById("form_input");
	var array = new Array();
	var upperLimit = [300, 374, 500, 600, 2000, 40, 50];

	for (var i = 0; i < form.length - 1; i++) {
		var value = form.elements[i].value;

		if (value > 0 && value <= upperLimit[i] && value != null) {
			var ind = "ind_" + i;
			array[i] = {
				ind : value
			};
		} else {
			alert("Wrong Input Number.");
			return;
		}
	}

	var result = {
		"cat_ID" : "1",
		"indicators" : array
	};

	var JSONresult = JSON.stringify(result);

	var req = new XMLHttpRequest();
	req.open("POST", "http://127.0.0.1:5000/saveScore", false);
	req.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
	req.send(JSONresult);

	if (req.status == 200) {
		alert(req.responseText);
	} else {
		alert("Error executing XMLHttpRequest call!");
	}
});
