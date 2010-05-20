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

var xmlhttp;
var invalid_color = 'rgb(238, 238, 255)';
var valid_color = 'rgb(136, 255, 136)';

function testMe()
{
    alert("I work, there for I am.");
}

function validateCorrectedMetadata()
{
    // Look for all fields that are editable. Check if the color is set to valid or
    // invalid. If all valid, allow submit. If not, display message and don't allow
    // submission to proceed
    
    for (i = 0; i < document.metadata_form.elements.length; i++)
    {
        e = document.metadata_form.elements[i];
        
        // Ignore hidden fields
        if (e.type == 'hidden')
        {
            continue;
        }
        
        if (e.style.backgroundColor == invalid_color)
        {
            alert('Please correct all errors before submitting your metadata.')
            return false;
        }
    }
}

function hasWhiteSpace(value)
{
    reWhiteSpace = new RegExp(/^\s*$/);
    if (reWhiteSpace.test(value))
    {
        return true;
    }
    else
    {
        return false;
    }
}

function replaceWithCurrent(field_name)
{
    field_name_parts = field_name.split(':');
    
    // Loop over form elements. For those elements that have a similar name, replace value
    for (i = 0; i < document.metadata_form.elements.length; i++)
    {
        e = document.metadata_form.elements[i];
        
        // Skip hidden fields
        if (e.type == 'hidden')
        {
            continue;
        }
        
        element_id_parts = e.id.split(':');
        
        if
        (
            (element_id_parts[0] == field_name_parts[0]) &&
            (element_id_parts[2] == field_name_parts[2]) &&
            (element_id_parts[3] == field_name_parts[3])
        )
        {
            current_field = document.getElementById(field_name);
            e.value = current_field.value;
            e.style.background = current_field.style.background;
        }
    }
}

function validateTextLength(sender, column_name, max_length)
{
    // check if browser can perform xmlhttp
    xmlhttp=GetXmlHttpObject()
    if (xmlhttp==null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }

    // Is the term too long?
    if (sender.value.length > max_length)
    {
        sender.style.background = invalid_color;
    }
    else
    {
        sender.style.background = valid_color;
    }
    
    var url = "load_field_details.psp";
    url=url + "?column_name=" + column_name;

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            top.frames['bottom'].document.getElementById('selected_field_details').innerHTML = xmlhttp.responseText;
            top.frames['bottom'].document.getElementById('selected_field_values').innerHTML = '';
        }
    }
    
    //perform a GET 
    xmlhttp.open("GET",url,true);
    xmlhttp.send(null);
 }

function validateRegExField(sender, column_name, reg_exp)
{
    // check if browser can perform xmlhttp
    xmlhttp=GetXmlHttpObject()
    if (xmlhttp==null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }
    
    regexp = new RegExp(reg_exp);

    // Is the term in a valid date format?
    if ( (hasWhiteSpace(sender.value)) || (!regexp.test(sender.value)))
    {
        // Not a number
        sender.style.background = invalid_color;
    }
    else
    {
        sender.style.background = valid_color;
    }
    
    var url = "load_field_details.psp";
    url=url + "?column_name=" + column_name;

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            top.frames['bottom'].document.getElementById('selected_field_details').innerHTML = xmlhttp.responseText;
            top.frames['bottom'].document.getElementById('selected_field_values').innerHTML = '';
        }
    }
    
    //perform a GET 
    xmlhttp.open("GET",url,true);
    xmlhttp.send(null);
}

function findListTerms(sender, column_name)
{    
    // check if browser can perform xmlhttp
    xmlhttp_details = GetXmlHttpObject()
    xmlhttp_values = GetXmlHttpObject()

    // Make sure browser supports xmlhttp    
    if (xmlhttp_details == null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }

    term = sender.value;

    // URL for each loading page
    var url_details = "load_list_field_details.psp";
    url_details = url_details + "?search_term=" + term + "&column_name=" + column_name;

    var url_values = "load_list_field_values.psp";
    url_values = url_values + "?search_term=" + term + "&column_name=" + column_name + "&field_id=" + sender.id;

    // xmlhttp callbacks
    xmlhttp_details.onreadystatechange=function()
    {
        if (xmlhttp_details.readyState==4)
        {
            top.frames['bottom'].document.getElementById('selected_field_details').innerHTML = xmlhttp_details.responseText;
        }
    }
    
    xmlhttp_values.onreadystatechange=function()
    {
        if (xmlhttp_values.readyState==4)
        {
            top.frames['bottom'].document.getElementById('selected_field_values').innerHTML = xmlhttp_values.responseText;
        }
    }
    
    // Get details
    xmlhttp_details.open("GET", url_details, true);
    xmlhttp_details.send(null);
    
    // Get values 
    xmlhttp_values.open("GET", url_values ,true);
    xmlhttp_values.send(null);
}

function additionalFieldChecked(sender)
{
    // If the element already exists, just toggle checkbox
    cb = document.getElementById("sample:" + sender.id);
    if (cb != null)
    {
        cb.checked = sender.checked;
    }
    // Add it if never been added before
    else
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
