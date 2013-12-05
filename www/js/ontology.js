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
var geocoder;
var map;
var marker;
var latitude=new Array();
var longitude=new Array();
var elevation=new Array();
var markersArray = [];
var infoWindowArray = [];

/*This changes the color of the table background when a user mouses over the Tool buttons. */
function mouseover(key){
    cell=document.getElementById(key);
    if (cell.bgcolor=='black'){
        cell.bgcolor=='blue';
    }else{
        cell.bgcolor=='black';
    }
}

/* These two function turn on/off the visibility of the two tools */
function displayOntology(){
    document.getElementById("ontology_lookup").style.display='';
    document.getElementById("geographic_location").style.display='none';
    document.getElementById("map_canvas").style.visibility='hidden';
}

function displayGeography(){
    document.getElementById("ontology_lookup").style.display='none';
    document.getElementById("geographic_location").style.display='';
    document.getElementById("map_canvas").style.visibility='visible';
}

/* Initializes the Google Map. */
function initialize(){
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(0,0);
    var myOptions = {
        zoom: 1,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
}

/* Removes the overlays from the map, but keeps them in the array*
//not used, since we are re-initializing the map
function clearOverlays() {
    if (markersArray) {
        for (i in markersArray) {
            markersArray[i].setMap(null)
            //infoWindowArray[i].close()
        }
        markersArray.length = 0;
        //infoWindowArray.length = 0; 
        //markersArray=new Array();
    }
}
*/

var elevator = new google.maps.ElevationService();

/* This function preps the addresses and calls the geocoder */
function codeAddress() {
    //we reinitialize each time this is called, so it recenters on the world
    //I did this since it is difficult to zoom based on the lat/lngs
    initialize();
    
    //get the locations from the input box
    var address = document.getElementById("address").value;
    
    //convert the input box into an array
    address_array=convert_terms_to_array(address)
    
    //iterate over the addresses and append the "loc:" tag to the beginning
    //which overwrites google point of interest detector
    saved_address_array=new Array();
    for (var i=0; i<address_array.length-1; i++){
        if (address_array[i] != ''){
            address_array[i]='loc:'+address_array[i].replace(/^loc:/i, '')
            saved_address_array[i]='loc:'+address_array[i].replace(/^loc:/i, '')
        }else if (address_array[i] == '' && address_array[i-1]!=''){
            address_array[i]=address_array[i-1]
            saved_address_array[i]=address_array[i-1]
        }else{
            saved_address_array[i]=address_array[i]
        }
    }

    //get a unique list of the address
    unique_addresses=unique(address_array)
    
    //no longer needed since we are re-initializing
    //clearOverlays();
    
    latitude=new Array();
    longitude=new Array();
    elevation=new Array();
    var latlong
    var iterator=0;
    timer_ms=0;
    if (geocoder) {
        
        //give status updates
        document.getElementById("loading_status").innerHTML='Loading coordinates'
        
        //iterate over the addresses and append a timing event, since google
        //has a query limit per second
        for (var i=0; i<unique_addresses.length; i++){
            if (unique_addresses[i]!=''){
                var lat2=setTimeout('geocode_results('+i+')',timer_ms)
                timer_ms+=700
            }
        }
        //append to the status after all points should have loaded
        setTimeout("document.getElementById('loading_status').innerHTML='Completed'",timer_ms) 
    }
}


/* This function gets the Lat/Long using Google Maps Geocoder API. */
function geocode_results(i){
    
    //query google maps for lat/lngs
    geocoder.geocode( { 'address': unique_addresses[i]}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var latlong = new google.maps.LatLng(results[0].geometry.location.lat(),results[0].geometry.location.lng()); 
            
            /* This function gets the Elevation using Google Maps Elevations API. */
            elevator.getElevationForLocations({'locations':[latlong]}, function(results2, status2){
                if (status == google.maps.ElevationStatus.OK) {
                    // Retrieve the first result
                    if (results2[0]) {
                        //assign lat/lng/elev to arrays
                        latitude[unique_addresses[i]]=results2[0].location.lat()
                        longitude[unique_addresses[i]]=results2[0].location.lng()
                        elevation[unique_addresses[i]]=results2[0].elevation;
                        
                        //put a pointer on the map
                        markersArray[unique_addresses[i]] = new StyledMarker({styleIcon:new StyledIcon(StyledIconTypes.MARKER,
                                                                             {size:(100,100),color:'#FF0000'}),
                                                                              position:latlong,map:map,
                                                                              title:unique_addresses[i].replace(/^loc:/i, '')+'\nLatitude: '+latitude[unique_addresses[i]].toFixed(2)+'\nLongitude: '+longitude[unique_addresses[i]].toFixed(2)+'\nElevation: '+elevation[unique_addresses[i]].toFixed(2),
                                                                              flat:true});
                        
                    } else {
                        alert("No elevation results found!");
                    }
                }
            });
        }else{
            alert(status)
            alert("Unable to find the Location you specified!");
        }  
    })
}
/* This function outputs the Lat/Long/Elev to the Console. */
function output_latlong(){
    //generate the output content
    type=document.getElementById('latlngType').value
    var content='';
    for (var i=0; i<saved_address_array.length; i++) {
            if (type=='Latitude'){
                content=content+latitude[saved_address_array[i]]+'<br>';
            }else if (type=='Longitude'){
                content=content+longitude[saved_address_array[i]]+'<br>';
            }else if (type=='Elevation'){
                content=content+elevation[saved_address_array[i]]+'<br>';
            }
        
    }

    //write page
    top.consoleRef=window.open('','myconsole','width=350,height=400,menubar=0,toolbar=1,status=0,scrollbars=1,resizable=1')
    top.consoleRef.document.writeln('<html><head><title>Console</title></head><body bgcolor=white onLoad="self.focus()">'+content+'</body></html>')
    top.consoleRef.document.close()
}

/* 
    This is the AJAX function which produces the list of terms below each input
    box. It takes as input:
        1) the ontology select box id
        2) the query string
        3) the input box id
        4) the txt box below input id
*/
function showResult(ont_id,str,inputbox_id,txt_id)
{
    // If the substring length is empty, then do nothing
    if (str.length==0)
    {
        return;
    } 
    // If the substring is at least one in length, then search for similar terms
    // in the ontologies selected. This is where we can set the length to start
    //searches (i.e. after 3 letters are present.
    else if (str.length>0){ 
        //remove text or checkmark next to the input box and change font color
        //to black
        document.getElementById('valid'+inputbox_id).innerHTML="";
        document.getElementById('valid'+inputbox_id).style.color="black";
        
        xmlhttp=GetXmlHttpObject()
        
        //check if browser can perform xmlhttp
        if (xmlhttp==null){
            alert ("Your browser does not support XML HTTP Request");
            return;
        }
        
        //get the list of ontologies using the ontology id
        ont_list=document.getElementById(ont_id)
        
        //get only the selected ontologies and convert to PL/SQL formatted text
        selected_ont=get_selected(ont_list)
        
        //generate a url string where we pass our variables
        var url="ontology_search.psp";
        url=url+"?ont="+selected_ont+"&q="+str+"&inputid="+inputbox_id+"&txt_id="+txt_id;
        url=url+"&sid="+Math.random();
        
        
        xmlhttp.onreadystatechange=function()
        {
            if (xmlhttp.readyState==4){
                //write the list of similar terms from the database  
                document.getElementById('input'+inputbox_id).innerHTML=xmlhttp.responseText;
                document.getElementById('input'+inputbox_id).style.border="1px solid #A5ACB2";
                xmlhttp.close();
            }
        }
        //perform a GET 
        xmlhttp.open("GET",url,true);
        xmlhttp.send(null)
    }
}

/* 
    This is the AJAX function which validates the terms in each input
    box. It takes as input:
        1) the ontology select box id
        2) the initial list of ontology terms from user
        3) the table where all results should be written
        4) whether this is the first call of this function
        5) whether this is an export call
*/
function validateInput(ont_id,ont_term_list,table_id,new_data,export_data)
{
    //if no data is input produce an alert
    if (ont_term_list.length==0){
        alert("Paste some data in the input box!");
        return;
    }
    
    //get the list of ontologies using the ontology id
    ontologies=document.getElementById(ont_id)
    
    //get only the selected ontologies and convert to PL/SQL formatted text
    selected_ont=get_selected(ontologies)
    
    //if no ontology is selected produce an alert
    if (selected_ont==''){
        alert("Select at least one Ontology!")
        return;
    }

    //take the pasted terms from user and convert those terms to an array
    ont_term_array=convert_terms_to_array(ont_term_list);
    
    //save this original list of terms from the user into an array
    original_ont_term_array=ont_term_array;
    
    //create an array to store the terms from the input boxes as they are being
    //modified
    updated_unique_terms=new Array();
    
    //if this is the first call to this function, create a unique list of terms
    //build the input boxes
    if (new_data == 'True')
    {
        //original_ont_term_array=new Array();
        original_unique_terms=new Array();
        
        //remove old input boxes, so the user can re-use the app over and over
        clear_inputs(table_id)
        
        //generate unique list and input boxes     
        unique_ont_array=write_input_boxes(ont_term_array,table_id);
        
        //store unique ontology terms for later use
        original_unique_terms=unique_ont_array;
        updated_unique_terms=unique_ont_array;
    }
    //If this is not the first call, retrieve values from input boxes
    else
    {
        //get the values from the input boxes
        unique_ont_array=get_inputs(unique_ont_array);
        updated_unique_terms=unique_ont_array;
    }
    
    //check if browser can perform xmlhttp
    xmlhttp=GetXmlHttpObject()
    if (xmlhttp==null){
        alert ("Your browser does not support XML HTTP Request");
        return;
    }
    /*
    var url="ontology_validate.psp";
    url=url+"?ont_id="+selected_ont+"&ont_terms="+unique_ont_array;
    url=url+"&sid="+Math.random();
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            //since the response from the PL/SQL is a string using the "#' 
            //delimitor, so we need to split and write them to the table
            validity=xmlhttp.responseText.split('#')
            for (var i=0; i<validity.length;i++){
                //determine if an input value is valid and write 'Invalid' or a 
                //checkbox accordingly
                if (validity[i]=='Valid' || validity[i]=='Valid\n'){
                    document.getElementById('validtxtbox'+(i)).innerHTML='&#10003;';
                    document.getElementById('validtxtbox'+(i)).style.color="green"; 
                }else if (validity[i]=='Invalid' || validity[i]=='Invalid\n'){
                    document.getElementById('validtxtbox'+(i)).innerHTML=validity[i];
                    document.getElementById('validtxtbox'+(i)).style.color="red";
                }
            }
        }
    }
    //perform a GET 
    xmlhttp.open("GET",url,true);
    xmlhttp.send(null)
    */
    //If the data is supposed to be exported, write the data to the new window
    if (export_data=='True'){
        write_data_to_new_window(original_ont_term_array,original_unique_terms,updated_unique_terms);
    }
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

/*
when iterating through list of ontology terms, when removing focus (onblur), 
this changes the background to cyan
*/
function removeStyle(x)
{
    document.getElementById(x).style.background="white"
}

/*
This function checks to see if all input boxes are valid, updates the original
list of terms from the user, with the corrected terms, then calls the
function to write the data to the new window
*/
function write_data_to_new_window(original_ont_term_array, original_unique_terms, updated_unique_terms){

    //Determine that all terms are valid
    for (var i=0;i<original_unique_terms.length;i++){
        if (original_unique_terms[i]!=''){
            validity=document.getElementById('validtxtbox'+(i)).innerHTML
            if ( validity=='' || validity=='Click Input Box...'){
                alert('You need choose valid terms!');
                return;
            }else if (validity=='Invalid' || validity=='Invalid\n'){
                alert('You have invalid terms!');
                return;
            }
        }
    }
    
    //generate a new array with update terms based on the valid input boxes
    output_array=new Array();
    //using length-1 since we appended an empty element to the list in the
    //convert_terms_to_array function.
    for (var j=0;j<original_ont_term_array.length-1;j++){
        for (var k=0;k<original_unique_terms.length;k++){
            if (original_ont_term_array[j]==original_unique_terms[k]){
                output_array.push(updated_unique_terms[k]);
            }
        }
        if(original_ont_term_array[j]=='' && j!=0){
            output_array.push(output_array[j-1]);
        }else if(original_ont_term_array[j]=='' && j==0){
            output_array.push('n/a');
        }
    }
    
    //write the array to the new window
    writeConsole(output_array.join('<br>'));
}

/*
This function creates a new console window and writes an html page containing
the corrected list of terms
*/
function writeConsole(content) 
{
    //open new window
    top.consoleRef=window.open('','myconsole','width=350,height=400,menubar=0,toolbar=1,status=0,scrollbars=1,resizable=1')
    //write page
    top.consoleRef.document.writeln('<html><head><title>Console</title></head><body bgcolor=white onLoad="self.focus()">'+content+'</body></html>')
    top.consoleRef.document.close()
}

/*
This function gets the terms from the input boxes and puts them into an array
*/
function get_inputs(unique_ont_array){
    new_unique_ont_array= new Array();
    for (var i = 0; i<unique_ont_array.length;i++){
        if (unique_ont_array[i]!=''){
            new_unique_ont_array[i]=document.getElementById('txtbox'+i).value;
        }
    }    
    return new_unique_ont_array;    
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

/*
This function writes the input boxes into the results table. Each input box has
4 fields that are created as follows:

==================  ======================
input-box-validity  input-box
------------------  ----------------------
empty field         list-of-ontology-terms
==================  ======================
...

*/
function write_input_boxes(ont_term_array,table_id){
    
    //create the header fields in the table (2 columns)
    unique_ont_array=unique(ont_term_array);
    var otable = document.getElementById(table_id);
    var row1 = document.createElement("TR");
    var th1 = document.createElement("TH");
    th1.appendChild(document.createTextNode("Valid:"));
    row1.appendChild(th1);
    var th2 = document.createElement("TH");
    th2.appendChild(document.createTextNode("Distinct Terms from Input List:"));
    row1.appendChild(th2);
    otable.appendChild(row1);
    
    for (var i = 0; i<unique_ont_array.length;i++){
        //make sure the array field is not empty, which happens when performing
        //javascript split() and join() functions
        if (unique_ont_array[i]!=''){            
            
            //create the input-box-validity field
            var row2 = document.createElement("TR");
            var td1 = document.createElement("TD");
            td1.id='validtxtbox'+i;
            td1.style.width='130px';
            td1.appendChild(document.createTextNode('Click Input Box...'));
            
            row2.appendChild(td1);
            
            //create the input-box field
            var td2 = document.createElement("TD");
            var input1 = document.createElement("input");
            input1.value=unique_ont_array[i];
            input1.id='txtbox'+i;
            input1.setAttribute('size','50');
            input1.setAttribute('onkeyup',"showResult('ontologies',this.value,this.id,this.id)");
            input1.setAttribute('onclick',"showResult('ontologies',this.value,this.id,this.id)");
            td2.appendChild(input1);
            row2.appendChild(td2);
            otable.appendChild(row2);

            //create the empty field
            var row3 = document.createElement("TR");
            var td3 = document.createElement("TD");
            row3.appendChild(td3);

            //ccreate the list-of-ontology-terms field
            var td4 = document.createElement("TD");
            td4.id='input'+input1.id;
            row3.appendChild(td4);
            otable.appendChild(row3);
        }
    }
    return unique_ont_array;
}

//this function resets the default select option and is for the select box
//above the ontology select field
function reset_select(selObject){
    for (i=0;i<selObject.options.length;i++){
        selObject.options[i].selected=false;
    }
}

//this function selects all from the select options and is for the select box
//above the ontology select field
function select_all(listbox_id){
    var listbox_values=document.getElementById(listbox_id);
    for (i=0;i<listbox_values.options.length;i++){
        listbox_values.options[i].selected=true;
    }
}

//this function selects none from the select options and is for the select box
//above the ontology select field
function select_none(listbox_id){
    var listbox_values=document.getElementById(listbox_id);
    for (i=0;i<listbox_values.options.length;i++){
        listbox_values.options[i].selected=false;
    }
}

//this function inverts the selection from the select options and is for the 
//select box above the ontology select field
function select_invert(listbox_id){
    var listbox_values=document.getElementById(listbox_id);
    for (i=0;i<listbox_values.options.length;i++){
        if (listbox_values.options[i].selected==true){
            listbox_values.options[i].selected=false;
        }else{
            listbox_values.options[i].selected=true;
        }
    }
}
