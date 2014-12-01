$(document).ready(function() {
	
	//this will build the options in the select
	var arrestincident ={
		option: "<option value='arrestincident'>Arrest/Incident</option>",
		data: "<input type='radio' value = arrest'>Arrest   <input type='radio' value = 'incident'>Incident<br>"
	}
	var officerinvolved = {
		option: "<option value='officerinvolved'>Officer Involved</option>",
		data: "<input type='text' placeholder='Name of Officer'><br>"
	}
	var date={
		option: "<option value='date'>Date</option>",
		data: "<input type='date' name='from'>  -  <input type='date' name='to'><br>"
	}
	var county={
		option:"<option value='county'>County</option>",
		data:"<Select name=county>"+
					"<option value ='orange'>Orange</option>"+
					"<option value= 'wake'>Wake</option>"+
				"</select><br>"
	}
	var sex={
		option:"<option value='sex'>Sex</option>",
		data: "<input type='radio' value = 'male'>Male   <input type='radio' value = 'female'>Female<br>"
	}
	var offenseCode={
		option: "<option value='offenseCode'>Offense Code</option>"
	}
	var agency={
		option: "<option value='agency'>Agency</option>"
	}
	var name={
		option: "<option value='name'>Name</option>"
	}
	var race={
		option: "<option value='race'>Race</option>"
	}
	var address={
		option: "<option value='address'>Address</option>"
	}
	var charge={			
		option: "<option value='charge'>Charge</option>"
	}
	var streetaddress={
		option: "<option value='streetaddress'>Street Address</option>"
	}
	var city={
		option: "<option value='city'>City</option>"
	}
	var state={
		option: "<option value='state'>State</option>"
	}
	var zip={
		option: "<option value='zip'>Zip</option>"
	}
	var latitude={
		option: "<option value='latitude'>Latitude</option>"
	}
	var longitude={
		option: "<option value='longitude'>Longitude</option>"
	}

	//this variable helps handle whether filter is active or not
	var doNotAddFilter=true;

	//this array constructs the available selections
	var filterArray = [arrestincident.option, officerinvolved.option, date.option,
	 county.option, sex.option, offenseCode.option, agency.option, name.option, 
	 race.option, address.option, charge.option, streetaddress.option,
	 city.option, state.option, zip.option, latitude.option, longitude.option];
	
	//this array tracks all the selections that have been made
	var selectionsMade = [];

	//when the user clicks the add filter button
	$("#addFilter").click(function() {
		$("#incomingfilters").append(function() {

			var filterToAdd = "<select class='filterselector'><option value='not a choice'>Select a Filter </option>";

			for ( j = 0; j < filterArray.length - 1; j++) {
				//dynamically adds all of the filters into the select
				filterToAdd += filterArray[j];
			}

			filterToAdd += "</select>";
			return filterToAdd;
		});

		//disable the add filter button until it is changed to a legit value
		$("#addFilter").prop("disabled", true);

		//add that not a choice has been added to selections
		selectionsMade.push("not a choice");

		//initializes this variable to false
		doNotAddFilter=false;
	});

	//whenever a selection is made, this is the function that will catch that change
	$("#incomingfilters").on('change', function() {
		$("#incomingfilters > select").each(function(index){
			
			//is any of the selections have changed this will catch that change
			if (this.value != selectionsMade[index]){

				//change the value in the selections made array
				selectionsMade[index]=this.value;

				//lock in their choice
				$("#incomingfilters > select").prop('disabled', true);

				switch(this.value){
					case "arrestincident":
						$("#incomingfilters").append(arrestincident.data);
						var index = filterArray.indexOf(arrestincident.option);
						if (index > -1){
							filterArray.splice(index, 1);
						}
						break;
					case "officerinvolved":
						$("#incomingfilters").append(officerinvolved.data);
						var index = filterArray.indexOf(officerinvolved.option);
						if (index > -1){
							filterArray.splice(index, 1);
						}
						break;
					case "date":
						$("#incomingfilters").append(date.data);
						var index = filterArray.indexOf(date.option);
						if (index > -1){
							filterArray.splice(index, 1);
						}
						break;
					case "county":
						$("#incomingfilters").append(county.data);
						var index = filterArray.indexOf(county.option);
						if (index > -1){
							filterArray.splice(index, 1);
						}
						break;
					case "county":
						$("#incomingfilters").append("<br>");
						break;
					case "sex":
						$("#incomingfilters").append("<br>");
						break;
					case "offenseCode":
						$("#incomingfilters").append("<br>");
						break;
					case "agency":
						$("#incomingfilters").append("<br>");
						break;
					case "name":
						$("#incomingfilters").append("<br>");
						break;
					case "race":
						$("#incomingfilters").append("<br>");
						break;
					case "address":
						$("#incomingfilters").append("<br>");
						break;
					case "charge":
						$("#incomingfilters").append("<br>");
						break;
					case "streetaddress":
						$("#incomingfilters").append("<br>");
						break;
					case "city":
						$("#incomingfilters").append("<br>");
						break;
					case "state":
						$("#incomingfilters").append("<br>");
						break;
					case "zip":
						$("#incomingfilters").append("<br>");
						break;
					case "latitude":
						$("#incomingfilters").append("<br>");
						break;
					case "longitude":
						$("#incomingfilters").append("<br>");
						break;
				}
			}
			if(this.value === "not a choice"){
				//one of the values is not a choice, disable the filter
				doNotAddFilter = true;
			}
		});
		if(!doNotAddFilter){
			//the filter is reenableed
			$("#addFilter").prop("disabled", false);

		}
		else{
			//the filter is disabled
			$("#addFilter").prop("disabled", true);
		}
	});
});
