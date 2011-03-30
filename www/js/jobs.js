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

function checkQiimeJobStatus()
{
    // check if browser can perform xmlhttp
    xmlhttp = GetXmlHttpObject()
    if (xmlhttp==null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }
    
    div_name ="qiime_status_div";
    var url = "check_job_status.psp?job_type_id=3";

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            document.getElementById(div_name).innerHTML = xmlhttp.responseText;
        }
    }
    
    // perform a GET 
    xmlhttp.open("GET", url, true);
    xmlhttp.send(null);
}

function checkQiimeMetaAnalysisStatus()
{
    // check if browser can perform xmlhttp
    xmlhttp = GetXmlHttpObject()
    if (xmlhttp==null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }
    
    div_name ="qiime_status_div";
    var url = "check_job_status.psp?job_type_id=7,8,9";
    
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            document.getElementById(div_name).innerHTML = xmlhttp.responseText;
        }
    }
    
    
    // perform a GET 
    xmlhttp.open("GET", url, true);
    xmlhttp.send(null);
}

function checkMGRASTJobStatus()
{
    // check if browser can perform xmlhttp
    xmlhttp = GetXmlHttpObject()
    if (xmlhttp==null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }
    
    div_name = "mg_rast_statis_div";
    var url = "check_job_status.psp?job_type_id=6";

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            document.getElementById(div_name).innerHTML = xmlhttp.responseText;
        }
    }
    
    // perform a GET 
    xmlhttp.open("GET", url, true);
    xmlhttp.send(null);
}

// This function is for showing the mapping and OTU tables when using meta-analysis
function checkMetaAnalysisStatus()
{
 // check if browser can perform xmlhttp
 xmlhttp2 = GetXmlHttpObject()
 if (xmlhttp2==null)
 {
     alert ("Your browser does not support XML HTTP Request");
     return;
 }

 var url2 = "check_meta_analysis_status.psp";

 xmlhttp2.onreadystatechange=function()
 {
     if (xmlhttp2.readyState==4)
     {
         document.getElementById("meta_status_div").innerHTML = xmlhttp2.responseText;
     }
 }

 // perform a GET 
 xmlhttp2.open("POST", url2, true);
 xmlhttp2.send(null);
}

// This function is for showing the mapping and OTU tables when using meta-analysis
function VerifyDeletion(input_url)
{
    var r=confirm("Are you sure you want to delete this data?");
    if (r==true)
        window.location=input_url

}
