function getCountries(id) {
       document.getElementById(id).source = countries; 
 }
 
 function setDefaultText() {
     $('input[type="text"], textarea').focus(function () {
         defaultText = $(this).val();
         $(this).val('');
     });
     $('input[type="text"], textarea').blur(function () {
         if ($(this).val() == "") {
             $(this).val(defaultText);
         }
         });
 }

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
	setDefaultText()
}

function addTwoFields(field1_name,field2_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<input type="text" value="Name" name="'+field1_name+'_'+new_field_number+'" id="'+field1_name+'_'+new_field_number+'" class="small_text"/><input type="text" value="Relationship" name="'+field2_name+'_'+new_field_number+'" id="'+field2_name+'_'+new_field_number+'" class="small_text"/><a class="remove_field" href="javascript:removeField(\''+field1_name+'_'+new_field_number+'\')" title="Remove this field">x</a></input></div>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", field1_name+'_'+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+field1_name);
	setDefaultText()
}

function addDestinationFields(div_name,field1_name,field2_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<select name="'+field1_name+'_'+new_field_number+'" id="'+field1_name+'_'+new_field_number+'">'
	newinput += '<option value="">Select an option</option>'
	for(var i =0; i < countries.length; i++)
		newinput+= '<option>'+countries[i]+'</option>'
	newinput+= '</select>'
	newinput+= '<input type="text" value="Duration" name="'+field2_name+'_'+new_field_number+'" id="'+field2_name+'_'+new_field_number+'" class="smaller_text"/> days <a class="remove_field" href="javascript:removeField(\''+div_name+'_'+new_field_number+'\')" title="Remove this field">x</a></input></div>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", div_name+'_'+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+div_name);
	// getCountries(field1_name+'_'+new_field_number)
	setDefaultText()
}

function addField(field_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<div id="'+field_name+'_'+new_field_number+'"><input type="text" name="'+field_name+'_'+new_field_number+'" id="'+field_name+'_'+new_field_number+'"><a class="remove_field" href="javascript:removeField(\''+field_name+'_'+new_field_number+'\')" title="Remove this field">x</a></input></div>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", field_name+'_'+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+field_name);
	setDefaultText()
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
	document.getElementById(item_id).className = document.getElementById(item_id).className.replace
      (/(?:^|\s)invisible(?!\S)/ , '');
}

function setInvisible(item_id) {
	document.getElementById(item_id).className += " invisible"
}

$(function()
{
    $( document ).tooltip();
});


function updateTotals() {
	if(updateTotalIntake() && updateAnimalPlant())
	{
		document.getElementById('submit6').disabled = false
		document.getElementById('dietaryIntakeTotal').className = "";
		document.getElementById('plantAnimalTotal').className = "";
	}
	else
		document.getElementById('submit6').disabled = true
}

/*stuff for only dietary questions survey */
function updateTotalIntake() {
	var total = 0;
	var prot = parseInt(document.getElementById('protein_per').value)
	if(isNaN(prot))
		document.getElementById('protein_per').value = 0
	var fat = parseInt(document.getElementById('fat_per').value)
	if(isNaN(fat))
		document.getElementById('fat_per').value = 0
	var carb = parseInt(document.getElementById('carbohydrate_per').value)
	if(isNaN(carb))
		document.getElementById('carbohydrate_per').value = 0
	total = prot+fat+carb
	if(isNaN(total))
		return
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
	if(isNaN(plant))
		document.getElementById('plant_per').value = 0
	var animal = parseInt(document.getElementById('animal_per').value)
	if(isNaN(animal))
		document.getElementById('animal_per').value = 0
	total = plant+animal
	if(isNaN(total))
		return
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
	if(isNaN(document.getElementById(item_id).value))
		document.getElementById(item_id).value = 0
	else if(document.getElementById(item_id).value < 0)
		document.getElementById(item_id).value = 0
	else if(document.getElementById(item_id).value > 100)
		document.getElementById(item_id).value = 100
	updateTotalIntake()
	updateAnimalPlant()
}

function toggleConsent() {
	var minor = !document.getElementById('is_7_to_13').checked
    document.getElementById("parent_1_name").disabled = minor
    document.getElementById("parent_2_name").disabled = minor
    document.getElementById("deceased_parent").disabled = minor
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

    if(document.consent_info.participant_email.value == "" || !validateEmail(document.consent_info.participant_email.value))
    {
        document.consent_info.participant_email.className += " highlight";
        valid = false;
    }

    if(!document.consent_info.deceased_parent.checked && document.consent_info.is_7_to_13.checked)
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

/*validation for add new sample*/
function verifyAddSample() {
    for(var i = 0; i < document.add_sample.length; i++) 
    {
        document.add_sample[i].className = document.add_sample[i].className.replace(/(?:^|\s)highlight(?!\S)/ , '');
    }
	
    var valid = true;
	
    if(document.add_sample.sample_date.value == "" || !isValidDate(document.add_sample.sample_date.value))
    {
        document.add_sample.sample_date.className += " highlight";
        valid = false;
    }
    if(document.add_sample.sample_time.value == "" || validateHhMm(document.add_sample.sample_time.value))
    {
        document.add_sample.sample_time.className += " highlight";
        valid = false;
    }
	
    if(!valid) 
	{
	    //alert($('#consent_info').submit());
        return;
	}
    else 
	{
        //alert($('#consent_info').submit());
        $('#add_sample').submit();
	}
}

/*validation for verification*/
function validateVerification() {
    for(var i = 0; i < document.verification_submit.length; i++) 
    {
        document.verification_submit[i].className = document.verification_submit[i].className.replace(/(?:^|\s)highlight(?!\S)/ , '');
		
		if(document.verification_submit[i].type == 'checkbox')
		{
			document.getElementById(document.verification_submit[i].id).className = document.verification_submit[i].className.replace(/(?:^|\s)highlight(?!\S)/ , '');
		}
    }
	
    var valid = true;
	
    if(document.verification_submit.email_verification_code.value == "")
    {
        document.verification_submit.email_verification_code.className += " highlight";
        valid = false;
    }
	
	for(var i = 0; i < document.verification_submit.length; i++)
	{
		if(document.verification_submit[i].type == 'checkbox' && !document.verification_submit[i].checked)
		{
			document.getElementById(document.verification_submit[i].id).className += " highlight";
			valid = false;
		}
	}
	
    if(!valid) 
	{
        return;
	}
    else 
	{
        $('#verification_submit').submit();
	}
}

/*field verification for help email send*/
function verifyHelpRequest() {
    for(var i = 0; i < document.help_request.length; i++) 
    {
        document.help_request[i].className = document.help_request[i].className.replace(/(?:^|\s)highlight(?!\S)/ , '');
    }
	
    var valid = true;
	
	if(document.help_request.first_name.value == "")
	{
        document.help_request.first_name.className += " highlight";
        valid = false;
	}
	
	if(document.help_request.last_name.value == "")
	{
        document.help_request.last_name.className += " highlight";
        valid = false;
	}
	
	if(document.help_request.email_address.value == "")
	{
        document.help_request.email_address.className += " highlight";
        valid = false;
	}
	
	if(document.help_request.message_body.value == "")
	{
        document.help_request.message_body.className += " highlight";
        valid = false;
	}
	
    if(!valid) 
	{
        return;
	}
    else 
	{
        $('#help_request').submit();
	}
}

/*clear empty boxes for survey3*/
function validateSurvey3() {
    for(var i = 0; i < document.survey_3.length; i++) 
    {	
		if(document.survey_3[i].type == 'text')
		{
			if(document.survey_3[i].value == 'Duration'|| document.survey_3[i].value == 'Type' || document.survey_3[i].value == 'Name' || document.survey_3[i].value == 'Relationship')
				document.survey_3[i].value = ''
		}
    }
    $('#survey_3').submit();
}

function validateSurvey1() {
    for(var i = 0; i < document.survey_1.length; i++) 
    {
        document.survey_1[i].className = document.survey_1[i].className.replace(/(?:^|\s)highlight(?!\S)/ , '');
    }
	
    var valid = true;
 	
	if(!isValidDate(document.survey_1.birth_date.value) && document.survey_1.birth_date.value != "")
	{
		document.survey_1.birth_date.className += " highlight"
		valid = false;
	}
	
	if(document.survey_1.height_in.value.replace(/[0-9]/g,"").length > 0)
	{
		document.survey_1.height_in.className += " highlight"
		valid = false;
	}
	
 	if(document.survey_1.height_cm.value.replace(/[0-9]/g,"").length > 0)
	{
		document.survey_1.height_cm.className += " highlight"
		valid = false;
	}
	
 	if(document.survey_1.weight_lbs.value.replace(/[0-9]/g,"").length > 0)
	{
		document.survey_1.weight_lbs.className += " highlight"
		valid = false;
	}
	
 	if(document.survey_1.weight_kg.value.replace(/[0-9]/g,"").length > 0)
	{
		document.survey_1.weight_kg.className += " highlight"
		valid = false;
	}
	
	if(valid)
		$('#survey_1').submit();
 
}

function verifyOptionalQuestions() {
    for(var i = 0; i < document.optional_questions.length; i++) 
    {
        document.optional_questions[i].className = document.optional_questions[i].className.replace(/(?:^|\s)highlight(?!\S)/ , '');
    }
	
	var valid = true;
	
	if(document.optional_questions.pregnant_due_date != null && !isValidDate(document.optional_questions.pregnant_due_date.value) && document.optional_questions.pregnant_due_date.value != "")
	{
		document.optional_questions.pregnant_due_date.className += " highlight"
		valid = false;
	}

	if(document.optional_questions.diabetes_diagnose_date != null && !isValidDate(document.optional_questions.diabetes_diagnose_date.value) && document.optional_questions.diabetes_diagnose_date.value != "")
	{
		document.optional_questions.diabetes_diagnose_date.className += " highlight"
		valid = false;
	}
	
	if(valid)
		$('#optional_questions').submit();
}

/* from http://stackoverflow.com/questions/46155/validate-email-address-in-javascript */
function validateEmail(email) { 
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
} 

function validateText(evt) {
    var theEvent = evt || window.event;
    var key = theEvent.keyCode || theEvent.which;
    key = String.fromCharCode( key );
    var regex = /["'<>]/;
    if( regex.test(key) ) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
    }

}

/* input field number validation*/
function validateNumber(evt) {
  var theEvent = evt || window.event;
  var key = theEvent.keyCode || theEvent.which;
  //say what these keys are
  if(theEvent.keyCode == 8 || theEvent.keyCode == 37|| theEvent.keyCode ==38|| theEvent.keyCode == 39|| theEvent.keyCode == 40 || theEvent.keyCode == 46 || theEvent.keyCode == 9)
  	return
  key = String.fromCharCode( key );
  var regex = /[0-9]|\./;
  if( !regex.test(key) ) {
    theEvent.returnValue = false;
    if(theEvent.preventDefault) theEvent.preventDefault();
  }
}

/* input field date validation from http://stackoverflow.com/questions/276479/javascript-how-to-validate-dates-in-format-mm-dd-yyyy
*/
function isValidDate(date)
{
    var matches = /^(\d{2})[-\/](\d{2})[-\/](\d{4})$/.exec(date);
    if (matches == null) return false;
    var d = matches[2];
    var m = matches[1] - 1;
    var y = matches[3];
    var composedDate = new Date(y, m, d);
    return composedDate.getDate() == d &&
            composedDate.getMonth() == m &&
            composedDate.getFullYear() == y;
}

/* input field time validation modified from
http://stackoverflow.com/questions/5563028/how-to-validate-with-javascript-an-input-text-with-hours-and-minutes
*/
function validateHhMm(inputField) {
        return /(?:[0-1]?[0-9]|[2][1-4]):[0-5]?[0-9]:[0-5]?[0-9]\s?(?:am|pm)?/.test(this.value);
    }

function inToCm() {
	var cur_cm = parseFloat(document.getElementById('height_cm').value)
	var inches = parseFloat(document.getElementById('height_in').value)
	var centimeters = inches * 2.54
	
	if(isNaN(cur_cm)) { /* update if there isn't a value */
		if(!isNaN(inches))
			document.getElementById('height_cm').value = centimeters.toFixed(0)
	} else if(Math.abs(centimeters - cur_cm) > 1) { /* update if the value is reasonably changed */
	    document.getElementById('height_cm').value = centimeters.toFixed(0)
	} else {}
}

function cmToIn() {
	var cur_in = parseFloat(document.getElementById('height_in').value)
	var centimeters = parseFloat(document.getElementById('height_cm').value)
	var inches = centimeters * 0.39
	
	if(isNaN(cur_in)) { /* update if there isn't a value */
		if(!isNaN(centimeters))
	    	document.getElementById('height_in').value = inches.toFixed(0)
	} else if(Math.abs(inches - cur_in) > 2) { /* update if the value is reasonably changed */
	    document.getElementById('height_in').value = inches.toFixed(0)
	} else {}
}

function lbsToKg() {
	var cur_kg = parseFloat(document.getElementById('weight_kg').value)
	var pounds = parseFloat(document.getElementById('weight_lbs').value)
	var kg = pounds * 0.45
	
	if(isNaN(cur_kg)) { /* update if there isn't a value */
		if(!isNaN(pounds))
	    	document.getElementById('weight_kg').value = kg.toFixed(0)
	} else if(Math.abs(kg - cur_kg) > 1) { /* update if the value is reasonably changed */
	    document.getElementById('weight_kg').value = kg.toFixed(0)
	} else {}
}

function kgToLbs() {
	var cur_lbs = parseFloat(document.getElementById('weight_lbs').value)
	var kg = parseFloat(document.getElementById('weight_kg').value)
	var pounds = kg * 2.20
	
	if(isNaN(cur_lbs)) { /* update if there isn't a value */
		if(!isNaN(kg))
	    	document.getElementById('weight_lbs').value = pounds.toFixed(0)
	} else if(Math.abs(pounds - cur_lbs) > 3) { /* update if the value is reasonably changed */
	    document.getElementById('weight_lbs').value = pounds.toFixed(0)
	} else {}
}

function reset(formID) {
	document.getElementById(formID).reset();
}
