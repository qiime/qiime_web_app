// console.log('derp')
var old_field_number = 1

function addThreeFields(field_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<input type="text" value="Type" name="'
	newinput +=field_name
	newinput +='_'
	newinput +=new_field_number
	newinput +='" id="'+field_name+'_'+new_field_number
	newinput +='" class="smaller_text"/><select id="'
	newinput += field_name
	newinput +='_location_'
	newinput +=new_field_number
	newinput +='" name="'+field_name+'_location_'+new_field_number
	newinput +='"><option>Housing...</option><option>Indoor</option><option>Outdoor</option><option>Confined</option></select><select id="'
	newinput +=field_name
	newinput +='_contact_'
	newinput +=new_field_number
	newinput +='" name="'+field_name+'_contact_'+new_field_number
	newinput +='"><option>Contact...</option><option>None</option><option>Little</option><option>Moderate</option><option>Extensive</option></select><a class="remove_field" href="javascript:removeField(\''+field_name+'_'+new_field_number+'\')" title="Remove this field">x</a>'
	
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", field_name+'_'+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+field_name);
}

function addTwoFields(field1_name,field2_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<input type="text" value="Name" name="'+field1_name+'_'+new_field_number+'" id="'+field1_name+'_'+new_field_number+'" class="small_text"/><input type="text" value="Relationship" name="'+field2_name+'_'+new_field_number+'" id="'+field2_name+'_'+new_field_number+'" class="small_text"/><a class="remove_field" href="javascript:removeField(\''+field1_name+'_'+new_field_number+'\')" title="Remove this field">x</a></input></div>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", field1_name+'_'+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+field1_name);
}

function addDestinationFields(div_name,field1_name,field2_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<input type="text" value="Location" name="'+field1_name+'_'+new_field_number+'" id="'+field1_name+'_'+new_field_number+'" class="small_text"/> <input type="text" value="Duration" name="'+field2_name+'_'+new_field_number+'" id="'+field2_name+'_'+new_field_number+'" class="smaller_text"/> days <a class="remove_field" href="javascript:removeField(\''+div_name+'_'+new_field_number+'\')" title="Remove this field">x</a></input></div>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", div_name+'_'+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+div_name);
}

function addField(field_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<div id="'+field_name+'_'+new_field_number+'"><input type="text" name="'+field_name+'_'+new_field_number+'" id="'+field_name+'_'+new_field_number+'"><a class="remove_field" href="javascript:removeField(\''+field_name+'_'+new_field_number+'\')" title="Remove this field">x</a></input></div>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", field_name+'_'+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+field_name);
}

function removeField(item_id) {
	var c = document.getElementById(item_id)
	c.parentNode.removeChild(c);
}

function otherSelect(select_id,item_id,other_index) {
	if(document.getElementById(select_id).selectedIndex == other_index)
	{
		setVisible(item_id)
	}else{
		setInvisible(item_id)
	}
}

function anySelect(select_id,item_id,other_indices) {
	if(other_indices.indexOf(document.getElementById(select_id).selectedIndex) > -1)
	{
		setInvisible(item_id)
	}else{
		setVisible(item_id)
	}
}

function setVisible(item_id) {
	// console.log(item_id)
	document.getElementById(item_id).className = document.getElementById(item_id).className.replace
      (/(?:^|\s)invisible(?!\S)/ , '');
}

function setInvisible(item_id) {
	// console.log(item_id)
	document.getElementById(item_id).className = "invisible"
}

$(function()
{
    $( document ).tooltip();
});


function updateTotals() {
	if(updateTotalIntake() && updateAnimalPlant())
	{
		document.getElementById('continue').disabled = false
		document.getElementById('dietaryIntakeTotal').className = "";
		document.getElementById('plantAnimalTotal').className = "";
	}
	else
		document.getElementById('continue').disabled = true
}

/*stuff for only dietary questions survey */
function updateTotalIntake() {
	var total = 0;
	var prot = parseInt(document.getElementById('protein_per').value)
	var fat = parseInt(document.getElementById('fat_per').value)
	var carb = parseInt(document.getElementById('carbohydrate_per').value)
	total = prot+fat+carb
	if(total > 100)
	{
		document.getElementById('dietaryIntakeTotal').className += " highlight"
		document.getElementById('dietaryIntakeTotal').innerHTML = total
		return false;
	}
	else
	{
		document.getElementById('dietaryIntakeTotal').className = document.getElementById('dietaryIntakeTotal').className.replace(/(?:^|\s)highlight(?!\S)/ , '');
		document.getElementById('dietaryIntakeTotal').innerHTML = total
		return true;
	}
		
	
	// console.log(total)
}

function updateAnimalPlant() {
	var total = 0;
	var plant = parseInt(document.getElementById('plant_per').value)
	var animal = parseInt(document.getElementById('animal_per').value)
	total = plant+animal
	if(total > 100)
	{
		document.getElementById('plantAnimalTotal').className += " highlight"
		document.getElementById('plantAnimalTotal').innerHTML = total
		return false;
	}
	else
	{
		document.getElementById('plantAnimalTotal').className = document.getElementById('plantAnimalTotal').className.replace(/(?:^|\s)highlight(?!\S)/ , '');
		document.getElementById('plantAnimalTotal').innerHTML = total
		return true;
	}
	
}
/* end stuff for dietary questions */

/* number validation for percentage fields */
function validatePercentage(item_id) {
	if(document.getElementById(item_id).value < 0)
		document.getElementById(item_id).value = 0
	else if(document.getElementById(item_id).value > 100)
		document.getElementById(item_id).value = 100
	updateTotalIntake()
	updateAnimalPlant()
}

/*validation for new participant*/
function validateConsent()
{
    for(var i = 0; i < document.consent_info.length; i++) 
    {
        document.consent_info[i].className = document.consent_info[i].className.replace(/(?:^|\s)highlight(?!\S)/ , '');
    }
  	document.getElementById("consent").className = document.getElementById("consent").className.replace(/(?:^|\s)highlight(?!\S)/ , '');
    var valid = true;
        
    if(!document.consent_info.consent.checked)
    {
        document.getElementById("consent").className += " highlight";
        valid = false;
    }

    if(document.consent_info.participant_name.value == "")
    {
        document.consent_info.participant_name.className += " highlight";
        valid = false;
    }
        
    if(document.consent_info.is_7_to_13.checked)
    {
        if(document.consent_info.parent_1_name.value == "")
        {
            document.consent_info.parent_1_name.className += " highlight";
            valid = false;
        }
        if(document.consent_info.parent_2_name.value == "")
        {
            document.consent_info.parent_2_name.className += " highlight";
            valid = false;
        }
    }
        
    if(!valid) 
	{
	    //alert($('#consent_info').submit());
        return;
	}
    else 
	{
        //alert($('#consent_info').submit());
        $('#consent_info').submit();
	}
}

/* input field number validation*/
function validateNumber(evt) {
  var theEvent = evt || window.event;
  var key = theEvent.keyCode || theEvent.which;
  key = String.fromCharCode( key );
  var regex = /[0-9]|\./;
  if( !regex.test(key) ) {
    theEvent.returnValue = false;
    if(theEvent.preventDefault) theEvent.preventDefault();
  }
}

function inToCm() {
	var inches = document.getElementById('height_in').value
	var centimeters = inches * 2.54
	document.getElementById('height_cm').value = centimeters
}

function cmToIn() {
	var centimeters = document.getElementById('height_cm').value
	var inches = centimeters * 0.393701
	document.getElementById('height_in').value = inches
}

function lbsToKg() {
	var pounds = document.getElementById('weight_lbs').value
	var kg = pounds * 0.453592
	document.getElementById('weight_kg').value = kg
}

function kgToLbs() {
	var kg = document.getElementById('weight_kg').value
	var pounds = kg * 2.20462
	document.getElementById('weight_lbs').value = pounds
}
