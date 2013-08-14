//functions for the portal toggle system
function selectTab(id) {
	document.querySelectorAll('.selected')[0].className = 'unselected';
	document.querySelectorAll('.portal_selected')[0].className = 'portal_unselected';
	document.getElementById(id+'_tab').className = 'selected';
	document.getElementById(id+'_content').className = 'portal_selected';
}

var xmlhttp;

function GetXmlHttpObject()
{
    if (window.XMLHttpRequest)
    {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        return new XMLHttpRequest();
    }

    if (window.ActiveXObject)
    {
        // code for IE6, IE5
        return new ActiveXObject("Microsoft.XMLHTTP");
    }
    return null;
}

function validatePetSurvey1()
{
    // disable the submit button so that the user doesn't click it again
    document.pet_survey.petsubmit.disabled = true;

    // check if browser can perform xmlhttp
    xmlhttp = GetXmlHttpObject()
    if (xmlhttp==null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }

    url = 'check_participant_name.psp?participant_name=' + document.pet_survey.animal_name.value

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            try
            {
                // participant_name already exists
                var responseText = xmlhttp.responseText.substring(0, xmlhttp.responseText.length - 1)
                if (responseText != '')
                {
                    alert(responseText);
                    document.pet_survey.animal_name.value = ''
                }

                validatePetSurvey2()
            }
            catch(e)
            {
                // Do nothing
            }
        }
    }

    // perform a GET
    xmlhttp.open("GET", url, true);
    xmlhttp.send(null);
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
	newinput +='"><option>Contact...</option><option>None</option><option>Little</option><option>Moderate</option><option>Extensive</option></select><a class="remove_field" href="#" onclick="removeField(\''+field_name+'_'+new_field_number+'\')" title="Remove this field">x</a>'
	
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", field_name+'_'+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+field_name);
	setDefaultText()

    var new_field_names = [];
    new_field_names.push(field_name + '_' + new_field_number);
    new_field_names.push(field_name + '_location_' + new_field_number);
    new_field_names.push(field_name + '_contact_' + new_field_number);

    return new_field_names;
}

function addTwoFields(field1_name,field2_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<input type="text" value="Name" name="'+field1_name+'_'+new_field_number+'" id="'+field1_name+'_'+new_field_number+'" class="small_text"/><input type="text" value="Relationship" name="'+field2_name+'_'+new_field_number+'" id="'+field2_name+'_'+new_field_number+'" class="small_text"/><a class="remove_field" href="#" onclick="removeField(\''+field1_name+'_'+new_field_number+'\')" title="Remove this field">x</a></input></div>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", field1_name+'_'+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+field1_name);
	setDefaultText()
    
    var new_field_values = [];
    new_field_values.push(field1_name+'_'+new_field_number);
    new_field_values.push(field2_name+'_'+new_field_number);

    return new_field_values;
}

function addDestinationFields(div_name,field1_name,field2_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<select name="'+field1_name+'_'+new_field_number+'" id="'+field1_name+'_'+new_field_number+'">'
	var num, name;
	newinput += '<option value="">Select an option</option>'
	for(var i =0; i < countries.length; i++) {
		num = countries[i][0];
		name = countries[i][1];
		newinput+= '<option value="'+num+'">'+name+'</option>'
	}
	newinput+= '</select>'
	newinput+= '<input type="text" value="Duration" name="'+field2_name+'_'+new_field_number+'" id="'+field2_name+'_'+new_field_number+'" class="smaller_text" onkeypress=\'validateNumber(event, false)\'/> days <a class="remove_field" href="#" onclick="removeField(\''+div_name+'_'+new_field_number+'\')" title="Remove this field">x</a></input></div>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", div_name+'_'+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+div_name);
	// getCountries(field1_name+'_'+new_field_number)
	setDefaultText()

    var retvalues = [];
    retvalues.push(field1_name+'_'+new_field_number);
    retvalues.push(field2_name+'_'+new_field_number);

    return retvalues;
}

function addField(field_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<div id="'+field_name+'_'+new_field_number+'"><input type="text" name="'+field_name+'_'+new_field_number+'" id="'+field_name+'_'+new_field_number+'"><a class="remove_field" href="#" onclick="removeField(\''+field_name+'_'+new_field_number+'\')" title="Remove this field">x</a></input></div>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", field_name+'_'+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+field_name);
	setDefaultText()

    return field_name + '_' + new_field_number;
}

function editHumanSurvey() {
    alert('You will not be able to save your progress during this survey. In order to save changes, please complete the survey. You will see a confirmation message in red text at the top of the page when your survey is successfully updated.')
    document.forms['edit_survey'].submit();
}

function parseMultiplesString(form_name, field_name) {
    // check if there was any input
    var theString = $(document.forms[form_name].elements[field_name])[0]
    if (theString)
        theString = $(document.forms[form_name].elements[field_name])[0].value;
    else
        return '';

    // if there were multiple inputs, use regex to parse out the values
    var regex = /Field\('\S+?', '(.+?)'\)/g;
    var hits = [], found;
    // probably want to do something else here to avoid element ID conflicts
    while (found = regex.exec(theString)) {
        hits.push(found[1]);
        regex.lastIndex = found.index + 1;
    }

    // if there was only one value, the regex does not apply, and the field
    // should be read as-is
    if (theString.substring(0, 8) != '[Field(\'' && theString != '') {
        hits[0] = theString;
    }

    return hits;
    
}

// function to write default values for the supplements field (survey2.psp)
function setSupplementsDefaults(form_name, field_name, default_field_name) {
    var hits = parseMultiplesString(form_name, default_field_name); 
    var new_field_names = [];
    new_field_names.push(field_name + '_1');

    for (var i = 1; i < hits.length; i++) {
        new_field_names.push(addField(field_name, field_name));
    }

    setMultiplesDefaults_text(form_name, new_field_names, hits);
}

// function to write default values for the special dietary restrictions field (survey2.psp)
function setDietaryRestrictionsDefaults(form_name, field_name, default_field_name) {
    // like the supplements field, this is only text, so we can use the same
    // function
    setSupplementsDefaults(form_name, field_name, default_field_name);
}

// function to write default values for the drugs field (survey5.psp)
function setGeneralMedsDefaults(form_name, field_name, default_field_name) {
    // like the supplements field, this is only text, so we can use the same
    // function
    setSupplementsDefaults(form_name, field_name, default_field_name);
}

// function to write default values for the antibiotics field (survey5.psp)
function setAntibioticMedsDefaults(form_name, field_name, default_field_name) {
    // like the supplements field, this is only text, so we can use the same
    // function
    setSupplementsDefaults(form_name, field_name, default_field_name);
}

// function to write default values for the diabetes medications field (optional_questions.psp)
function setDiabetesMedsDefaults(form_name, field_name, default_field_name) {
    // like the supplements field, this is only text, so we can use the same
    // function
    setSupplementsDefaults(form_name, field_name, default_field_name);
}

// function to write default values for the diabetes medications field (optional_questions.psp)
function setMigraineMedsDefaults(form_name, field_name, default_field_name) {
    // like the supplements field, this is only text, so we can use the same
    // function
    setSupplementsDefaults(form_name, field_name, default_field_name);
}

// function to write default values for the travel options field (survey3.psp)
function setTravelOptionsDefaults(form_name, travel_location, travel_duration, travel_location_default, travel_duration_default) {
    var hits_travel_location = parseMultiplesString(form_name, travel_location_default);
    var hits_travel_duration = parseMultiplesString(form_name, travel_duration_default);
    
    var new_field_names_travel_location = [];
    var new_field_names_travel_duration = [];

    new_field_names_travel_location.push(travel_location + '_1');
    new_field_names_travel_duration.push(travel_duration + '_1');

    var new_field_names;
    // loop only uses one of the lengths, but they should always be equal
    for (var i = 0; i < hits_travel_location.length - 1; i++) {
        // addDestinationFields returns a list of 2-element lists
        new_field_names = addDestinationFields('travel_options', travel_location, travel_duration);
        new_field_names_travel_location.push(new_field_names[0]);
        new_field_names_travel_duration.push(new_field_names[1]);
    }

    setMultiplesDefaults_select(form_name, new_field_names_travel_location, hits_travel_location);
    setMultiplesDefaults_text(form_name, new_field_names_travel_duration, hits_travel_duration);
}

// function to write default values for the related participants field (survey3.psp)
function setRelatedParticipantsDefaults(form_name, field_name_related, field_name_relation, default_field_name_related, default_field_name_relation) {
    var hits_related = parseMultiplesString(form_name, default_field_name_related); 
    var hits_relation = parseMultiplesString(form_name, default_field_name_relation); 

    var new_field_names_related = [];
    var new_field_names_relation = [];

    new_field_names_related.push(field_name_related + '_1');
    new_field_names_relation.push(field_name_relation + '_1');

    var new_field_names;
    // loop only uses hits_related.length, but this value will always equal hits_relation.length
    for (var i = 0; i < hits_related.length - 1; i++) {
        // addTwoFields returns a list of 2-element lists
        new_field_names = addTwoFields(field_name_related, field_name_relation);
        new_field_names_related.push(new_field_names[0]);
        new_field_names_relation.push(new_field_names[1]);
    }

    setMultiplesDefaults_text(form_name, new_field_names_related, hits_related);
    setMultiplesDefaults_text(form_name, new_field_names_relation, hits_relation);
}

// function to set default values for addint pets on survey_3.psp
function setPetsDefaults(form_name, field_name_pet_type, field_name_pet_housing, field_name_pet_contact, pet_type_default, pet_housing_default, pet_contact_default) {
    var pet_type_hits = parseMultiplesString(form_name, pet_type_default); 
    var pet_housing_hits = parseMultiplesString(form_name, pet_housing_default); 
    var pet_contact_hits = parseMultiplesString(form_name, pet_contact_default); 

    var new_field_names_pet_type = [];
    var new_field_names_pet_housing = [];
    var new_field_names_pet_contact = [];

    new_field_names_pet_type.push(field_name_pet_type + '_1');
    new_field_names_pet_housing.push(field_name_pet_housing + '_1');
    new_field_names_pet_contact.push(field_name_pet_contact + '_1');

    var new_field_names;
    // loop only uses only one of the "hits" variables here, but they should all be the same length
    // use length - 1 because the first already exists
    for (var i = 0; i < pet_type_hits.length - 1; i++) {
        // addThreeFields returns a list of 2-element lists
        new_field_names = addThreeFields(field_name_pet_type);

        new_field_names_pet_type.push(new_field_names[0]);
        new_field_names_pet_housing.push(new_field_names[1]);
        new_field_names_pet_contact.push(new_field_names[2]);
    }

    setMultiplesDefaults_text(form_name, new_field_names_pet_type, pet_type_hits);
    setMultiplesDefaults_select(form_name, new_field_names_pet_housing, pet_housing_hits);
    setMultiplesDefaults_select(form_name, new_field_names_pet_contact, pet_contact_hits);
}

// this function is used to set default values for "multiples" on the survey
// where the type of the form element is text input.
function setMultiplesDefaults_text(form_name, new_field_names, hits) {
    for (var i = 0; i < hits.length; i++) {
        var theElement = document.forms[form_name].elements[new_field_names[i]];
        theElement.value = hits[i];
    }
}

// this function is used to set default values for select boxes
function setMultiplesDefaults_select(form_name, new_field_names, hits) {
    for (var i = 0; i < hits.length; i++) {
        var theElement = document.forms[form_name].elements[new_field_names[i]];
        for (var j = 0; j < theElement.options.length; j++) {
            if (theElement.options[j].value == hits[i])
                theElement.selectedIndex = j;
        }
    }
}

function addHuman() {
	field_name = "human"
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<div id="'+field_name+'_'+new_field_number+'"><input type="text" class="small_text" value="Age" name="'+field_name+'_'+new_field_number+'_age" id="'+field_name+'_'+new_field_number+'_age" onkeypress="validateNumber(event, false)"> years <br /><select name="'+field_name+'_'+new_field_number+'_sex" id="'+field_name+'_'+new_field_number+'_sex"><option value="">Select an option</option><option>Male</option><option>Female</option><option>Other</option></select><a class="remove_field" href="#" onclick="removeField(\''+field_name+'_'+new_field_number+'\')" title="Remove this pet">x</a></input></div>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", field_name+'_'+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+field_name);
	setDefaultText()
}

function addPet() {
	field_name = "pet"
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<div id="'+field_name+'_'+new_field_number+'"><select name="'+field_name+'_'+new_field_number+'" id="'+field_name+'_'+new_field_number+'"><option value="">Select an option</option><option>Dog</option><option>Cat</option><option>Small mammal</option><option>Large mammal</option><option>Fish</option><option>Bird</option><option>Reptile</option><option>Amphibian</option><option>Other</option></select><a class="remove_field" href="#" onclick="removeField(\''+field_name+'_'+new_field_number+'\')" title="Remove this pet">x</a></input></div>'
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
      (/(?:^|\s)invisible(?!\S)/g , '');
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
	var minor = !document.getElementById('is_juvenile').checked
    document.getElementById("parent_1_name").disabled = minor
    document.getElementById("parent_2_name").disabled = minor
    document.getElementById("deceased_parent").disabled = minor
    document.getElementById("juvenile_age_less_than_7").disabled = minor
    document.getElementById("juvenile_age_more_than_7").disabled = minor
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

    if(document.consent_info.is_juvenile.checked)
    {
        if(!document.consent_info.deceased_parent.checked)
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
        document.add_sample[i].className = document.add_sample[i].className.replace(/(?:^|\s)highlight(?!\S)/g , '');
    }
    document.getElementById("sample_site_div").className = document.getElementById("sample_site_div").className.replace(/(?:^|\s)highlight(?!\S)/g , '');
	
    var valid = true;
	
    if(document.add_sample.sample_date.value == "" || !isValidDate(document.add_sample.sample_date.value))
    {
        document.add_sample.sample_date.className += " highlight";
        valid = false;
    }
    if(document.add_sample.sample_time.value == "" || !validateHhMm(document.add_sample.sample_time.value))
    {
        document.add_sample.sample_time.className += " highlight";
        valid = false;
    }
    if((typeof(document.add_sample.sample_site) != 'undefined' && document.add_sample.sample_site.selectedIndex == 0) || (typeof(document.add_sample.environment_sampled) != 'undefined' && document.add_sample.environment_sampled.selectedIndex == 0))
    {
        document.getElementById("sample_site_div").className += " highlight";
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

function validatePasswordReset() {
    for(var i = 0; i < document.change_password.length; i++) 
    {
        document.change_password[i].className = document.change_password[i].className.replace(/(?:^|\s)highlight(?!\S)/ , '');
    }
	
    var valid = true;
	
	if(document.change_password.current_password.value == "")
	{
        document.change_password.current_password.className += " highlight";
        valid = false;
	}
	
	if(document.change_password.new_password.value == "")
	{
        document.change_password.new_password.className += " highlight";
        valid = false;
	}
	
	if(document.change_password.confirm_password.value == "")
	{
        document.change_password.confirm_password.className += " highlight";
        valid = false;
	}
	
    if(!valid) 
	{
        return;
	}
    else 
	{
        $('#change_password').submit();
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

function validatePetSurvey2() {
	var valid = true;
    for(var i = 0; i < document.pet_survey.length; i++) 
    {
		if(document.pet_survey[i].type == 'text')
		{
			if(document.pet_survey[i].value == 'Age' || document.pet_survey[i].value == 'Name')
				document.pet_survey[i].value = ''
		}
        document.pet_survey[i].className = document.pet_survey[i].className.replace(/(?:^|\s)highlight(?!\S)/ , '');
    }
	
    if(document.pet_survey.animal_name.value == "")
	{
		document.pet_survey.animal_name.className += " highlight"
		valid = false;
	}

	if(valid)
		$('#pet_survey').submit();
	else
    {
		window.scrollTo(0, 0);
    }

    document.pet_survey.petsubmit.disabled = false;
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
  if (theEvent.which == 0) {
    // this is a "special key," and theEvent.keyCode is not the ASCII value
    // allow arrow keys (37-40), backspace (8), tab (9), and delete (46)
    if(theEvent.keyCode == 8 || theEvent.keyCode == 37|| theEvent.keyCode ==38|| theEvent.keyCode == 39|| theEvent.keyCode == 40 || theEvent.keyCode == 46 || theEvent.keyCode == 9)
      theEvent.returnValue = true;
  }
  else {
    // this is a normal key, and theEvent.keyCode is the ASCII value
    var key = theEvent.keyCode || theEvent.which;
    // some browsers treat backspace as a normal key, so allow that
    if (key == 8) {
      theEvent.returnValue = true;
      return;
    }
    key = String.fromCharCode( key );
    var regex = /[a-zA-Z0-9.\- ]/;
    if( !regex.test(key) ) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
    }
  }
}

/* input field number validation*/
function validateNumber(evt, integer) {
  var theEvent = evt || window.event;
  if (theEvent.which == 0) {
    // this is a "special key," and theEvent.keyCode is not the ASCII value
    // allow arrow keys (37-40), backspace (8), tab (9), and delete (46)
    if(theEvent.keyCode == 8 || theEvent.keyCode == 37|| theEvent.keyCode ==38|| theEvent.keyCode == 39|| theEvent.keyCode == 40 || theEvent.keyCode == 46 || theEvent.keyCode == 9)
      theEvent.returnValue = true;
  }
  else {
    // this is a normal key, and theEvent.keyCode is the ASCII value
    var key = theEvent.keyCode || theEvent.which;
    // some browsers treat backspace as a normal key, so allow that
    if (key == 8) {
      theEvent.returnValue = true;
      return;
    }
    key = String.fromCharCode( key );
    // make sure the character typed is a number or a period
    var regex = /[0-9]|\./;
    if (integer) regex = /[0-9]/;
    if( !regex.test(key) ) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
    }
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
        return /(?:(?:0[0-9])|(?:1[0-2])):[0-5][0-9]\s(?:am|pm)/i.test(inputField);
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
