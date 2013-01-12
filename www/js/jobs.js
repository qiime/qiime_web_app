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

function submitAllJobs()
{
    // check if browser can perform xmlhttp
    xmlhttp = GetXmlHttpObject()
    if (xmlhttp==null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }

    var span_name ="submit_all_span";
    var url = "load_study.psp";

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            try
            {
                document.getElementById(span_name).innerHTML = xmlhttp.responseText;
            }
            catch(e)
            {
                // Do nothing
            }
        }
    }
    // perform a GET
    xmlhttp.open("GET", url, true);
    xmlhttp.send(null);
}

function checkQiimeJobLoadStatus()
{
    // check if browser can perform xmlhttp
    xmlhttp = GetXmlHttpObject()
    if (xmlhttp==null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }
    
    div_name ="qiime_load_status_div";
    var url = "check_job_status.psp?job_type_id=12,15";

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            try
            {
                document.getElementById(div_name).innerHTML = xmlhttp.responseText;
            }
            catch(e)
            {
                // Do nothing
            }
        }
    }
    
    // perform a GET 
    xmlhttp.open("GET", url, true);
    xmlhttp.send(null);
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
            try
            {
                document.getElementById(div_name).innerHTML = xmlhttp.responseText;
            }
            catch(e)
            {
                // Do nothing
            }
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
    var url = "check_job_status.psp?job_type_id=7,8,9,10,11,13";
    
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            try
            {
                document.getElementById(div_name).innerHTML = xmlhttp.responseText;
            }
            catch(e)
            {
                // Do nothing
            }
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
            try
            {
                document.getElementById(div_name).innerHTML = xmlhttp.responseText;
            }
            catch(e)
            {
                // Do nothing
            }
        }
    }
    
    // perform a GET 
    xmlhttp.open("GET", url, true);
    xmlhttp.send(null);
}

function checkEBISRAJobStatus()
{
    // check if browser can perform xmlhttp
    xmlhttp = GetXmlHttpObject()
    if (xmlhttp==null)
    {
        alert ("Your browser does not support XML HTTP Request");
        return;
    }
    
    div_name = "ebi_sra_statis_div";
    var url = "check_job_status.psp?job_type_id=14";

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4)
        {
            try
            {
                document.getElementById(div_name).innerHTML = xmlhttp.responseText;
            }
            catch(e)
            {
                // Do nothing
            }
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
         try
         {
             document.getElementById("meta_status_div").innerHTML = xmlhttp2.responseText;
         }
         catch(e)
         {
             // Do nothing
         }
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

function checkAllStudyJobs()
{
    // Looks a little strange... but not all divs refererenced in the below functions
    // may exist at any time. We still want to run all of them because setting individual
    // timers causes many of them to hang.
    setTimeout(checkQiimeJobStatus, 0);
    setTimeout(checkQiimeJobLoadStatus, 1000);
    setTimeout(checkEBISRAJobStatus, 2000);
    setTimeout(submitAllJobs, 3000);
}

function confirmFormSubmission(confirm_message, form_name)
{
    var agree = confirm(confirm_message);
    if (agree)
        document.forms[form_name].submit();
}
