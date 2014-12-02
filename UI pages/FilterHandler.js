$(document).ready(function() {
	
	//this will build the options in the select
	var arrestincident ={
		option: "<option value='arrestincident'>Arrest/Incident</option>",
		data: "<div class='createdfilter' id='arrestincidenttodelete'><input type='radio' name='arrestincident' value = 'arrest'>Arrest   <input type='radio' name='arrestincident' value = 'incident'>Incident <button type=button id='deletearrestincident'>-</button><br></div>"
	}
	var officerinvolved = {
		option: "<option value='officerinvolved'>Officer Involved</option>",
		data: "<div class='createdfilter' id='officerinvolvedtodelete'><input type='text' name='officerinvolved' placeholder='Name of Officer'> <button type=button id='deleteofficerinvolved'>-</button><br></div>"
	}
	var date={
		option: "<option value='date'>Date of Arrest/Incident</option>",
		data: "<div class='createdfilter' id='datetodelete'><input type='date' name='from'>  -  <input type='date' name='to'><button type=button id='deletedate'>-</button> <br></div>"
	}
	var county={
		option:"<option value='county'>County</option>",
		data:"<div class='createdfilter' id='countytodelete'><Select name='county'>"+
					"<option value ='orange'>Orange</option>"+
					"<option value= 'wake'>Wake</option>"+
				"</select><button type=button id='deletecounty'>-</button><br></div>"
	}
	var sex={
		option:"<option value='sex'>Sex</option>",
		data: "<div class='createdfilter' id='sextodelete'><input type='radio' name='sex' value = 'male'>Male   <input type='radio' name='sex' value = 'female'>Female<button type=button id='deletesex'>-</butotn><br></div>"
	}
	var agency={
		option: "<option value='agency'>Agency</option>",
		data: "<Select name='agency'>"+
					"<option value ='raleigh'>Raleigh</option>"+
					"<option value= 'chapel hill'>Chapel Hill</option>"+
					"<option value='durham'>Durham</option>"+
					"<option value='greensboro'>Greensboro</option>"+
				"</select><br>"
	}
	var name={
		option: "<option value='name'>Name of person involved</option>",
		data: "<input type='text' name='name'> <br>"
	}
	var race={
		option: "<option value='race'>Race</option>",
		data: "<Select name='race'>"+
					"<option value ='white'>White</option>"+
					"<option value= 'black'>Black</option>"+
					"<option value='asian'>Asian</option>"+
					"<option value='other'>other</option>"+
				"</select><br>"
	}
	var charge={			
		option: "<option value='charge'>Charge</option>",
		data:"<input type='text' name='charge'> <br>"
	}
	var city={
		option: "<option value='city'>City</option>",
		data: "<input type='text' name='city'> <br>"
	}

	//this variable helps handle whether filter is active or not
	var doNotAddFilter=true;

	//this array constructs the available selections
	var filterArray = [arrestincident.option, officerinvolved.option, date.option,
	 county.option, sex.option, agency.option, name.option, 
	 race.option, charge.option, city.option];
	
	//this array tracks all the selections that have been made
	var selectionsMade = [];

	//when the user clicks the add filter button
	$("#addFilter").click(function() {
		$("#incomingfilters").append(function() {

			var filterToAdd = "<div id='selectordiv'><select id='filterselector'><option value='not a choice'>Select a Filter </option>";

			for ( j = 0; j < filterArray.length; j++) {
				//dynamically adds all of the filters into the select
				filterToAdd += filterArray[j];
			}

			filterToAdd += "</select></div>";
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
		$("#incomingfilters #selectordiv > #filterselector").each(function(index){
			
			//if any of the selections have changed this will catch that change
			if (this.value != selectionsMade[index]){

				//change the value in the selections made array
				selectionsMade[index]=this.value;

				//lock in their choice
				$("#incomingfilters #selectordiv> #filterselector").prop('disabled', true);

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
					case "sex":
						$("#incomingfilters").append(sex.data);
						var index = filterArray.indexOf(sex.option);
						if (index > -1){
							filterArray.splice(index, 1);
						}
						break;
					case "agency":
						$("#incomingfilters").append(agency.data);
						var index = filterArray.indexOf(agency.option);
						if (index > -1){
							filterArray.splice(index, 1);
						}
						break;
					case "name":
						$("#incomingfilters").append(name.data);
						var index = filterArray.indexOf(name.option);
						if (index > -1){
							filterArray.splice(index, 1);
						}
						break;
					case "race":
						$("#incomingfilters").append(race.data);
						var index = filterArray.indexOf(race.option);
						if (index > -1){
							filterArray.splice(index, 1);
						}
						break;
					case "charge":
						$("#incomingfilters").append(charge.data);
						var index = filterArray.indexOf(charge.option);
						if (index > -1){
							filterArray.splice(index, 1);
						}
						break;
					case "city":
						$("#incomingfilters").append(city.data);
						var index = filterArray.indexOf(city.option);
						if (index > -1){
							filterArray.splice(index, 1);
						}
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
		if(filterArray.length==0){
			$("#addFilter").prop("disabled", true);
		}
	});

	$("#incomingfilters").on("click", "#deletearrestincident ", function(){
		$("#incomingfilters > #selectordiv > #filterselector").each(function(){
			if(this.value=='arrestincident'){
				$(this).remove();
			}
		});
		$("#arrestincidenttodelete").remove();
		filterArray.push(arrestincident.option);
	});

	$("#incomingfilters").on("click", "#deleteofficerinvolved", function(){
		$("#incomingfilters > #selectordiv > #filterselector").each(function(){
			if(this.value=='officerinvolved'){
				$(this).remove();
			}
		});
		$("#officerinvolvedtodelete").remove();
		filterArray.push(officerinvolved.option);
	});

	$("#incomingfilters").on("click", "#deletedate", function(){
		$("#filterselector").each(function(){
			if(this.value=="date"){
				$(this).remove();
			}
		});
		$("#incomingfilters > div").each(function(){})
		$("#datetodelete").remove();
		filterArray.push(date.option);
	});

	$("#incomingfilters").on("click", "#deletecounty", function(){
		$("#filterselector").each(function(){
			if(this.value=="county"){
				$(this).remove();
			}
		});
		$("#countytodelete").remove();
		filterArray.push(county.option);
	});

	$("#incomingfilters").on("click", "#deletesex", function(){
		$("#incomingfilters > #selectordiv > #filterselector").each(function(){
			if(this.value=='sex'){
				$(this).remove();
			}
		});
		$("#sextodelete").remove();
		filterArray.push(sex.option);
	});
});
