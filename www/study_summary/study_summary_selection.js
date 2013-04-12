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
function showStudySummary(select_box_id)
{
    select_box=document.getElementById(select_box_id)
    selected_item_id = select_box.options[select_box.selectedIndex].id
    study_name=select_box.options[select_box.selectedIndex].value

    xmlhttp=GetXmlHttpObject()
    
    //check if browser can perform xmlhttp
    if (xmlhttp==null){
        alert("Your browser does not support XML HTTP Request");
        return;
    }

    // Reset the table while loading
    document.getElementById('field_ref_table').innerHTML = "Loading...";
    
    study_id=selected_item_id.split('_')[0]

    //generate a url string where we pass our variables
    var url="study_summary/study_reference_lookup.psp";
    url=url + "?study_id=" + study_id+"&study_name="+study_name;
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4){
            //write the list of terms from the database  
            document.getElementById('field_ref_table').innerHTML=xmlhttp.responseText;
            document.getElementById('field_ref_table').style.border="1px solid #A5ACB2";
        }
    }
    //perform a GET 
    xmlhttp.open("GET",url,true);
    xmlhttp.send(null)
   

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

function show_hide_samples(div_id,sym_id) {
    // this code toggles the samples
    var div = document.getElementById(div_id);
    var sym = document.getElementById(sym_id);
    if(div.style.display == 'block'){
        div.style.display = 'none';
        sym.innerHTML='&#x25BA;';
    }else{
        div.style.display = 'block';
        sym.innerHTML='&#x25BC;';
    }
}
