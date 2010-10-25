/*

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Production"

*/

var xmlhttp;

function testMe()
{
    alert('just testing');
}

// Need to factor this funciton out into its own file
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

function checkJobStatus(job_type_id)
{
    // check if browser can perform xmlhttp
    xmlhttp = GetXmlHttpObject()
    if (xmlhttp==null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }
    
    var url = "check_job_status.psp?job_type_id="+job_type_id;

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            document.getElementById("job_status_div").innerHTML = xmlhttp.responseText;
        }
    }
    
    // perform a GET 
    xmlhttp.open("GET", url, true);
    xmlhttp.send(null);
 }
