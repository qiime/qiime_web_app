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
