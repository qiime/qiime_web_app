$(function(){
    consent_info.parent_1_name.disabled = true
    consent_info.parent_2_name.disabled = true
    consent_info.parent_1_code.disabled = true
    consent_info.parent_2_code.disabled = true
    consent_info.deceased_parent.disabled = true
});

$(function(){
    $('input.submit').click(function(){
        for(var i = 0; i < document.consent_info.length; i++)
            document.consent_info[i].className = document.consent_info[i].className.replace
      (/(?:^|\s)highlight(?!\S)/ , '');
      document.getElementById("consent").className = document.getElementById("consent").className.replace
      (/(?:^|\s)highlight(?!\S)/ , '');
      
        var valid = true;
        if(!document.consent_info.consent.checked)
        {
            document.getElementById("consent").className += " highlight";
            valid = false;
        }
        if(document.consent_info.participant_name.value == "")
        {
            document.consent_info.participant_name.className += " highlight";
            valid = false;
        }
        if(document.consent_info.contact_code.value == "")
        {
            document.consent_info.contact_code.className += " highlight";
            valid = false;
        }
        
        if(document.consent_info.is_7_to_13.checked)
        {
            if(document.consent_info.parent_1_name.value == "")
            {
                document.consent_info.parent_1_name.className += " highlight";
                valid = false;
            }
            if(document.consent_info.parent_2_name.value == "")
            {
                document.consent_info.parent_2_name.className += " highlight";
                valid = false;
            }
            if(document.consent_info.parent_1_code.value == "")
            {
                document.consent_info.parent_1_code.className += " highlight";
                valid = false;
            }
            if(document.consent_info.parent_2_code.value == "")
            {
                document.consent_info.parent_2_code.className += " highlight";
                valid = false;
            }
        }
        
        if(!valid)
            return;
        else
            alert($('#consent_info').submit());
            $('#consent_info').submit();
    });
});

$(function(){
    $('input.is_7_to_13').click(function(){
        if(document.consent_info.is_7_to_13.checked)
        {
            consent_info.parent_1_name.disabled = false
            consent_info.parent_2_name.disabled = false
            consent_info.parent_1_code.disabled = false
            consent_info.parent_2_code.disabled = false
            consent_info.deceased_parent.disabled = false
        }
        else
        {
            consent_info.parent_1_name.disabled = true
            consent_info.parent_2_name.disabled = true
            consent_info.parent_1_code.disabled = true
            consent_info.parent_2_code.disabled = true
            consent_info.deceased_parent.disabled = true
        }
    });
});

