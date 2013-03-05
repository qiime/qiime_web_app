// console.log('derp')

var old_field_number = 1

function addThreeFields(field_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<input type="text" value="Type" name="'+field_name+"_"+new_field_number+'" class="smaller_text"/><select id="'+field_name+"_"+new_field_number+'_location"><option>Indoor</option><option>Outdoor</option><option>Confined</option></select><select id="'+field_name+"_"+new_field_number+'_contact"><option>None</option><option>Little</option><option>Moderate</option><option>Extensive</option></select><a class="add_field" href="javascript:removeField(\''+field_name+"_"+new_field_number+'\')" title="Remove this field">-</a>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", field_name+"_"+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+field_name);
}

function addTwoFields(field1_name,field2_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<input type="text" value="Name" name="'+field1_name+"_"+new_field_number+'" class="small_text"/><input type="text" value="Relationship" name="'+field2_name+"_"+new_field_number+'" class="small_text"/><a class="add_field" href="javascript:removeField(\''+field1_name+"_"+new_field_number+'\')" title="Remove this field">-</a></input></div>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", field1_name+"_"+new_field_number);
	newTextBoxDiv.after().html(newinput);
	newTextBoxDiv.appendTo('#'+field1_name);
}

function addField(field_name) {
	var new_field_number = old_field_number+1
	old_field_number = new_field_number
	var newinput = '<div id="'+field_name+"_"+new_field_number+'"><input type="text" name="'+field_name+"_"+new_field_number+'"><a class="add_field" href="javascript:removeField(\''+field_name+"_"+new_field_number+'\')" title="Remove this field">-</a></input></div>'
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", field_name+"_"+new_field_number);
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


/*stuff for only dietary questions survey */
function updateTotalIntake() {
	var total = 0;
	var prot = parseInt(document.getElementById('protein_per').value)
	var fat = parseInt(document.getElementById('fat_per').value)
	var carb = parseInt(document.getElementById('carbohydrate_per').value)
	total = prot+fat+carb
	document.getElementById('dietaryIntakeTotal').innerHTML = total
	// console.log(total)
}

function updateAnimalPlant() {
	var total = 0;
	var plant = parseInt(document.getElementById('plant_per').value)
	var animal = parseInt(document.getElementById('animal_per').value)
	total = plant+animal
	document.getElementById('plantAnimalTotal').innerHTML = total
}
/* end stuff for dietary questions */
