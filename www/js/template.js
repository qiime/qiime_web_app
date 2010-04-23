/*

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, Qiime Web Analysis"
__credits__ = ["Jesse Stombaugh", "Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Production"

*/

var xmlhttp

/*
Loads and writes field values for the selected package types
*/
function testMe()
{
    alert("I work, there for I am.");
}

function additionalFieldChecked(sender)
{
    var table = document.getElementById("selected_additional_fields");
    var table_row = document.createElement("TR");
    var table_data1 = document.createElement("TD");
    var checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = "true";
    checkbox.id = "sample:" + sender.id;
    checkbox.name = "sample:" + sender.id;
    var table_data2 = document.createElement("TD");
    table_data2.appendChild(document.createTextNode(sender.id));
    
    table_data1.appendChild(checkbox);
    table_row.appendChild(table_data1);
    table_row.appendChild(table_data2);
    table.appendChild(table_row);
}

function loadAdditionalFields()
{
    // Make sure a package type has been selected
    search_term = document.getElementById('search_term');
    //if (search_term.value == "")
    //{
     //   return;
    //}
    
    // check if browser can perform xmlhttp
    xmlhttp=GetXmlHttpObject()
    if (xmlhttp==null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }

    var url = "load_additional_fields.psp";
    url=url + "?search_term=" + search_term.value;

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            // Clear the table first
            //document.getElementById('package_fields').innerHTML = "";
            
            document.getElementById('additional_fields_results').innerHTML = xmlhttp.responseText;
            
            //package_fields = xmlhttp.responseText.split('#');
            //writeFieldValues('package_fields', package_fields);
        }
    }
    //perform a GET 
    xmlhttp.open("GET",url,true);
    xmlhttp.send(null);
}

function loadTemplateFields()
{
    // Make sure a package type has been selected
    package_type=document.getElementById('package_type');
    if ( package_type.selectedIndex == 0 )
    {
        alert('You must select an valid package type.');
        return;
    }
    
    // check if browser can perform xmlhttp
    xmlhttp=GetXmlHttpObject()
    if (xmlhttp==null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }

    var url = "load_template_fields.psp";
    url=url + "?package_type_id=" + package_type[package_type.selectedIndex].value;

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            // Clear the table first
            //document.getElementById('package_fields').innerHTML = "";
            
            document.getElementById('package_fields').innerHTML = xmlhttp.responseText;
            
            //package_fields = xmlhttp.responseText.split('#');
            //writeFieldValues('package_fields', package_fields);
        }
    }
    //perform a GET 
    xmlhttp.open("GET",url,true);
    xmlhttp.send(null);
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
