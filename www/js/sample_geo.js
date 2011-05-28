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
var latitude;
var longitude;
var elevation;
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


function displayGeography(){
    document.getElementById("ontology_lookup").style.display='none';
    document.getElementById("geographic_location").style.display='';
    document.getElementById("map_canvas").style.visibility='visible';
}

/* Initializes the Google Map. */
/*
function initialize(){
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(40.01,-105.27);
    var myOptions = {
        zoom: 7,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
}

*/

/* Removes the overlays from the map, but keeps them in the array */
function clearOverlays() {
    if (markersArray) {
        for (i in markersArray) {
            markersArray[i].setMap(null);
            infoWindowArray[i].close()
        }
        markersArray.length = 0;
        infoWindowArray.length = 0; 
    }
}

/* This function gets the Lat/Long using Google Maps Geocoder API. */
/*
function codeAddress() {
    var infowindow = new google.maps.InfoWindow();
    var elevator = new google.maps.ElevationService();
    var address = document.getElementById("address").value;
    var latlong
    if (geocoder) {
        var lat2=geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                clearOverlays();
                map.setZoom(7);  
                map.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    map: map, 
                    position: results[0].geometry.location
                });
                markersArray.push(marker);
                latitude=results[0].geometry.location.lat()
                longitude=results[0].geometry.location.lng()
                var formal_address=results[0].formatted_address
                var latlong = new google.maps.LatLng(latitude,longitude); 
                *//* This function gets the Elevation using Google Maps Elevations API. *//*
                elevator.getElevationForLocations({'locations':[latlong]}, function(results, status){
                    if (status == google.maps.ElevationStatus.OK) {
                        // Retrieve the first result
                        if (results[0]) {
                            elevation=results[0].elevation;
                            infowindow.setContent('<table class="overlay"><tr><th colspan="2" style="font-weight:bold"><u>'+formal_address+'</u></th></tr><tr><td>Latitude:</td><td>'+latitude.toFixed(2)+'&deg;</td></tr><tr><td>Longitude:</td><td>'+longitude.toFixed(2)+'&deg;</td></tr><tr><td>Elevation:</td><td>'+elevation.toFixed(2)+'m</td></tr></table>');
                            infowindow.open(map, marker);
                            infoWindowArray.push(infowindow);
                        } else {
                            alert("No elevation results found!");
                        }
                    }
                });
            }else{
                alert("Unable to find the Location you specified!");
            }  
        });
    }
}
*/

/* This function outputs the Lat/Long/Elev to the Console. */
function output_latlong(){
    num_rows=document.getElementById('numRows').value
    type=document.getElementById('latlngType').value

    var content='';
    for (var i=0; i<num_rows; i++) {
        if (type=='Latitude'){
            content=content+latitude+'<br>';
        }else if (type=='Longitude'){
            content=content+longitude+'<br>';
        }else if (type=='Elevation'){
            content=content+elevation+'<br>';
        }
    }

top.consoleRef=window.open('','myconsole','width=350,height=400,menubar=0,toolbar=1,status=0,scrollbars=1,resizable=1')
    //write page
    top.consoleRef.document.writeln('<html><head><title>Console</title></head><body bgcolor=white onLoad="self.focus()">'+content+'</body></html>')
    top.consoleRef.document.close()
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

function initialize() {
  var myOptions = {
    zoom: 1,
    center: new google.maps.LatLng(0,0),
    mapTypeId: google.maps.MapTypeId.HYBRID
  }
  var map = new google.maps.Map(document.getElementById("map_canvas"),
                                myOptions);

  setMarkers(map, latlongs_db);
}

/**
 * Data for the markers consisting of a name, a LatLng and a zIndex for
 * the order in which these markers should display on top of each
 * other.
 */
var beaches = [
  ['Bondi Beach', -33.890542, 151.274856, 4],
  ['Coogee Beach', -33.923036, 151.259052, 5],
  ['Cronulla Beach', -34.028249, 151.157507, 3],
  ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
  ['Maroubra Beach', -33.950198, 151.259302, 1]
];

function setMarkers(map, locations) {
  // Add markers to the map

  //http://google-maps-utility-library-v3.googlecode.com/svn/trunk/styledmarker/docs/examples.html
  for (var i = 0; i < locations.length; i++) {
    var loc = locations[i];
    var myLatLng = new google.maps.LatLng(loc[1], loc[2]);
    /*var styleMaker1 = new google.maps.Marker({  
      position: myLatLng,  
      map: map,  
      icon: './img/emp.png',
      size(5,5,widthUnit?:px, heightUnit?:px)
    });*/
	var styleMaker1 = new StyledMarker({styleIcon:new StyledIcon(StyledIconTypes.MARKER,{size:(100,100),color:loc[4]}),position:myLatLng,map:map,title:loc[0]});
  }
}