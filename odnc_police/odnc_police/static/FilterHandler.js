$(document).ready(function() {

        //this will build the options in the select
        var arrestincident ={
                option: "<option value='arrestincident'>Arrest/Incident</option>",
                data: "<div class='createdfilter' id='arrestincidenttodelete'><input type='radio' na$
        
        var officerinvolved = {
                option: "<option value='officerinvolved'>Officer Involved</option>",
                data: "<div class='createdfilter' id='officerinvolvedtodelete'><input type='text' na$
        }
        var date={
                option: "<option value='date'>Date</option>",
                data: "<input type='date' name='from'>  -  <input type='date' name='to'> <br>"
        }
        var county={
                option:"<option value='county'>County</option>",
                data:"<Select name='county'>"+
                                        "<option value ='orange'>Orange</option>"+
                                        "<option value= 'wake'>Wake</option>"+
                                "</select><br>"
        }
        var sex={
                option:"<option value='sex'>Sex</option>",
                data: "<input type='radio' name='sex' value = 'male'>Male   <input type='radio' name$
        }
        var offenseCode={
                option: "<option value='offenseCode'>Offense Code</option>",
                data: "<input type='text' name='offenseCode'> <br>"
        }
        var agency={
                option: "<option value='agency'>Agency</option>",
                data: "<Select name='agency'>"+
                                        "<option value ='raleigh'>Raleigh</option>"+
                                        "<option value= 'chapelhill'>Chapel Hill</option>"+
                                        "<option value='durham'>Durham</option>"+
                                        "<option value='greensboro'>Greensboro</option>"+
                                "</select><br>"
        }
        var name={
                option: "<option value='name'>Name</option>",
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
        var address={
                option: "<option value='address'>Address</option>",
                data: "<input type='text' name='address'> <br>"
        }
        var charge={
                option: "<option value='charge'>Charge</option>",
                data:"<input type='text' name='charge'> <br>"
        }
        var streetaddress={
                option: "<option value='streetaddress'>Street Address</option>",
                data: "<input type='text' name='streetaddress'> <br>"
        }
        var city={
                option: "<option value='city'>City</option>",
                data: "<input type='text' name='city'> <br>"
        }
        var state={
                option: "<option value='state'>State</option>",
                data: "<Select name='state'>"+
                                        "<option value ='AB'>Alabama</option>"+
                                        "<option value= 'AL'>Alaska</option>"+
                                        "<option value='AZ'>Arizona</option>"+
                                        "<option value='AR'>Arkansas</option>"+
                                        "<option value='CA'>California</option>"+
                                        "<option value='CO'>Colorado</option>"+
                                        "<option value='CT'>Connecticut</option>"+
                                        "<option value='DE'>Delaware</option>"+
                                        "<option value='GA'>Georgia</option>"+
                                        "<option value='HI'>Hawaii</option>"+
                                "</select><br>"
        }
        var zip={
                option: "<option value='zip'>Zip</option>",
                data:"<input type='text' name='zip'> <br>"
        }
        var latitude={
                option: "<option value='latitude'>Latitude</option>",
                data:"<input type='text' name='latitude'> <br>"
        }
        var longitude={
                option: "<option value='longitude'>Longitude</option>",
                data:"<input type='text' name='longitude'> <br>"
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

                        var filterToAdd = "<div id='selectordiv'><select id='filterselector'><option$

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

                        //is any of the selections have changed this will catch that change
                        if (this.value != selectionsMade[index]){

                                //change the value in the selections made array
                                selectionsMade[index]=this.value;

                                //lock in their choice
                                $("#incomingfilters > #filterselector").prop('disabled', true);

                                switch(this.value){
                                        case "arrestincident":
                                                $("#incomingfilters").append(arrestincident.data);
                                                var index = filterArray.indexOf(arrestincident.optio$
                                                if (index > -1){
                                                        filterArray.splice(index, 1);
                                                }
                                                break;
                                        case "officerinvolved":
                                                $("#incomingfilters").append(officerinvolved.data);
                                                var index = filterArray.indexOf(officerinvolved.opti$
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
                                        case "offenseCode":
                                                $("#incomingfilters").append(offenseCode.data);
                                                var index = filterArray.indexOf(offenseCode.option);
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
                                        case "address":
                                                $("#incomingfilters").append(address.data);
                                                var index = filterArray.indexOf(address.option);
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
                                        case "streetaddress":
                                                $("#incomingfilters").append(streetaddress.data);
                                                var index = filterArray.indexOf(streetaddress.option$
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
                                        case "state":
                                                $("#incomingfilters").append(state.data);
                                                var index = filterArray.indexOf(state.option);
                                                if (index > -1){
                                                        filterArray.splice(index, 1);
                                                }
                                                break;
                                        case "zip":
                                                $("#incomingfilters").append(zip.data);
                                                var index = filterArray.indexOf(zip.option);
                                                if (index > -1){
                                                        filterArray.splice(index, 1);
                                                }
                                                break;
                                        case "latitude":
                                                $("#incomingfilters").append(latitude.data);
                                                var index = filterArray.indexOf(latitude.option);
                                                if (index > -1){
                                                        filterArray.splice(index, 1);
                                                }
                                                break;
                                        case "longitude":
                                                $("#incomingfilters").append(longitude.data);
                                                var index = filterArray.indexOf(longitude.option);
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
                $("#filterselector").each(function(){
                        if(this.value=="arrestincident"){
                                $(this).remove();
                        }
                });
                $("#arrestincidenttodelete").remove();
                filterArray.push(arrestincident.option);
        });
});
