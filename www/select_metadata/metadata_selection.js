/*

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, Qiime Web Analysis"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Jesse Stombaugh"]
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Production"

*/



var xmlhttp


/* 
    This is the AJAX function which produces the list of terms below each input
    box. It takes as input:
        1) the ontology select box id
        2) the query string
        3) the input box id
        4) the txt box below input id
*/
function showResult(input_textbox,column_id,column_value)
{
    select_box_id=document.getElementById(column_id).parentNode.id
    var show_values=0;
    if (select_box_id=='box2View'){
        show_values=1;
    }
    xmlhttp=GetXmlHttpObject()
    
    //check if browser can perform xmlhttp
    if (xmlhttp==null){
        alert("Your browser does not support XML HTTP Request");
        return;
    }

    
    col_split_1=column_value.split('####SEP####');
    table_name=col_split_1[0];
    
    col_split_2=col_split_1[1].split('####STUDIES####');
    col_name=col_split_2[0];
    studies=col_split_2[1];
    
    array_key=column_value;

    //generate a url string where we pass our variables
    var url="select_metadata/metadata_reference_lookup.psp";

    /*
    var long_str=''
    for (var i in savedValues){
        split_sep=i.split('####SEP####');
        saved_table=split_sep[0]
        split_studies=split_sep[1].split('####STUDIES####');
        saved_table=split_studies[0]
        saved_studies=split_studies[1]
        saved_values=savedValues[i].split(',').join('__vals__').replace(/['"]/g,'')
        
        long_str+=saved_values
    }
    alert(long_str)
    */
    url=url + "?col_id=" + col_name + "&tab_name=" + table_name + "&show_values=" + show_values + "&studies=" + studies;
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4){

            //write the list of similar terms from the database  
            document.getElementById('field_ref_table').innerHTML=xmlhttp.responseText;
            document.getElementById('field_ref_table').style.border="1px solid #A5ACB2";
     
            if (array_key in savedValues){
                var value_select_box = document.getElementById(array_key)
                var list_of_saved_values=savedValues[array_key].split(',')
                for (var i=0;i<value_select_box.length;i++){
                    for (var j=0;j<list_of_saved_values.length;j++){                    
                        if (("'"+value_select_box.options[i].value+"'")==list_of_saved_values[j]){
                                value_select_box.options[i].selected=true;
                        }
                    }
                }
                //alert(savedValues[array_key]);
            }
        }
    }
    //perform a GET 
    xmlhttp.open("GET",url,true);
    xmlhttp.send(null)
   

}

function saveSelection(input_selectbox)
{
    var select_box_id=document.getElementById(input_selectbox)
    //var select_box_object=document.getElementById(select_box_id)
    var exists='False';
    var selected_values=get_selected(select_box_id)
    
    for (var i in savedValues){
        if (i==select_box_id.id){
            savedValues[select_box_id.id]=selected_values;
            exist='True';
            break;
        }
    }
    if (exist='False'){
        savedValues[select_box_id.id]=selected_values;
    }
    
    /*
    var select_value_array=new Array();
    select_value_array=savedValues[select_box_id.id].split(',');
    for (var i in select_value_array){
        alert(select_value_array[i])
    }
    */
    return
}


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

/*
This function changes the input box value when the user clicks on a term
in the list of terms
*/
function change_form_value(form_field,form_value,inputbox_id){
    //change the input box value
    document.getElementById(form_field).value=form_value;
    
    //Clear the list of ontology terms
    document.getElementById('input'+inputbox_id).innerHTML='';
    document.getElementById('input'+inputbox_id).style.border="0px";
    
    //Add a checkmark next to the input box
    document.getElementById('valid'+form_field).innerHTML='&#10003;';
    document.getElementById('valid'+form_field).style.color="green";
}

/*
when iterating through list of ontology terms, upon onfocus, this changes 
the background to cyan
*/
function setStyle(x)
{
    document.getElementById(x).style.background="cyan"
}

/* when iterating through list of ontology terms, when removing focus (onblur), this changes the background to cyan */ 

function removeStyle(x) { 
    document.getElementById(x).style.background="white" 
} 

/* This function makes only a group of columns from the DB visible */ 
var box1original=new Array() 
function select_group(identifier,selObject1,selObject2){ 
    var listbox_values=document.getElementById(selObject1);
    var moved_listbox_values=document.getElementById(selObject2); 
    
    var box2values=new Array() 
    for (var i=0;i<moved_listbox_values.options.length;i++){ 
        box2values[moved_listbox_values.options[i].innerHTML]=null
    }

    // if the full list has not been saved, then load it into a global variable
    if (box1original[0] == null){ 
        for (var i=0;i<listbox_values.options.length;i++){ 
            box1original[i]=new Array() 
            box1original[i][0]=listbox_values.options[i].id 
            box1original[i][1]=listbox_values.options[i].value
            box1original[i][2]=listbox_values.options[i].innerHTML
        } 
    }
    
    // Go trhough and write the html for the new option list
    var iter=0;
    var option_str=new Array();
    for (var i=0;i<box1original.length;i++){ 
        var group=box1original[i][0].split('#ENDGRP#')[0] 
        var field=box1original[i][2]
        
        if (identifier=='ALL'){
            if (field in box2values){
                //do nothing
            }else{
                option_str[iter]='<option id="'+box1original[i][0]+'" value="'+box1original[i][1]+'">'+box1original[i][2]+'</option>';
                iter=iter+1;
            }
        }else if (identifier==group){
            if (field in box2values){
                //do nothing
            }else{
                option_str[iter]='<option id="'+box1original[i][0]+'" value="'+box1original[i][1]+'">'+box1original[i][2]+'</option>';
                iter=iter+1;
            }
        }
    }

    listbox_values.innerHTML=option_str.join('\n')
}

/*
This function gets a list of selected ontologies, concatenates them and formats
them as a string to be used by PL/SQL
*/
function get_selected(selObject){
    var arSelected = new Array(); 
    
    for (i=0;i<selObject.options.length;i++){
        if (selObject.options[i].selected==true){
            arSelected.push('\''+selObject.options[i].value+'\'');
        };
    }
    onts=arSelected.join(',');
    return onts
    
}
/*
This function takes an array and produces another array with only unique values
*/
function unique(a){
    for( var i=a.length; --i>-1; ) {
        for( var j=a.length; --j>-1; ) 
        {   
            //must convert to uppercase for comparison, so there are no 
            //case-sensitivity issues
            if(i != j && a[i].toUpperCase() == a[j].toUpperCase() && a[j]!='') a.splice(i,1);
        }
    }
    
    //filter out the empty strings
    var unique_terms=new Array();
    for (var k=0;k<a.length;k++){
        if (a[k] != ''){
            unique_terms.push(a[k]);
        }
    }
    return unique_terms; 
}

/*
This function clears the result table, so the user can perform many searches
*/
function clear_inputs(table_id){
    for(var i = document.getElementById(table_id).rows.length; i > 0;i--)
    {
        document.getElementById(table_id).deleteRow(i -1);
    }
}

/*
This function checks that text was typed in the input textarea and then takes
that list and converts the string into an array based on new-line character
*/
function convert_terms_to_array(ont_term_list){
    ont_term_array=ont_term_list.split('\n')
    //need to add another element to array, since there may not be a new line
    //at the end of the list
    ont_term_array.push('');
    if (ont_term_array=='')
    {
        alert("Input a list of terms!")
        return;
    }
    filtered_array=new Array();
    for (var i=0;i<ont_term_array.length;i++){
        filtered_array.push(ont_term_array[i])
/*        if (ont_term_array[i]!=''){
            filtered_array.push(ont_term_array[i])
        }*/
    }    
    return filtered_array;
}


//this function resets the default select option and is for the select box
//above the ontology select field
function reset_select(selObject){
    selObject.options[0].selected=true;
}

//this function selects all from the select options and is for the select box
//above the ontology select field
function select_all(listbox_id){
    var listbox_values=document.getElementById(listbox_id);
    for (var i=0;i<listbox_values.options.length;i++){
        listbox_values.options[i].selected=true;
    }
}

//this function selects none from the select options and is for the select box
//above the ontology select field
function select_none(listbox_id){
    var listbox_values=document.getElementById(listbox_id);
    for (var i=0;i<listbox_values.options.length;i++){
        listbox_values.options[i].selected=false;
    }
}

//this function inverts the selection from the select options and is for the 
//select box above the ontology select field
function select_invert(listbox_id){
    var listbox_values=document.getElementById(listbox_id);
    for (var i=0;i<listbox_values.options.length;i++){
        if (listbox_values.options[i].selected==true){
            listbox_values.options[i].selected=false;
        }else{
            listbox_values.options[i].selected=true;
        }
    }
}

//this function selects all from the select options and is for the select box
//above the ontology select field
function select_all_col_values(listbox_id){
    var listbox_values=document.getElementById(listbox_id);
    for (var i=0;i<listbox_values.options.length;i++){
        listbox_values.options[i].selected=true;
    }
    saveSelection(listbox_id);
    return
}

//this function selects none from the select options and is for the select box
//above the ontology select field
function select_none_col_values(listbox_id){
    var listbox_values=document.getElementById(listbox_id);
    for (var i=0;i<listbox_values.options.length;i++){
        listbox_values.options[i].selected=false;
    }
    saveSelection(listbox_id);
    return
}

//this function inverts the selection from the select options and is for the 
//select box above the ontology select field
function select_invert_col_values(listbox_id){
    var listbox_values=document.getElementById(listbox_id);
    for (var i=0;i<listbox_values.options.length;i++){
        if (listbox_values.options[i].selected==true){
            listbox_values.options[i].selected=false;
        }else{
            listbox_values.options[i].selected=true;
        }
    }
    saveSelection(listbox_id);

    return
}


function getStats(form_object)
{
    xmlhttp=GetXmlHttpObject()
    
    //check if browser can perform xmlhttp
    if (xmlhttp==null){
        alert("Your browser does not support XML HTTP Request");
        return;
    }
    
    form_object=form_object['otu_table_info']
    //generate a url string where we pass our variables
    var url="select_metadata/get_otu_table_stats.psp";

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4){
            //write the list of similar terms from the database  
            document.getElementById('field_ref_table').innerHTML=xmlhttp.responseText;
            document.getElementById('field_ref_table').style.border="1px solid #A5ACB2";
        }
    }

    //perform a POST 
    xmlhttp.open("POST",url,true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.setRequestHeader("Content-length", form_object.length);
    xmlhttp.send(form_object)
}