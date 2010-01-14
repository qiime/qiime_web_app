
function reset_select(selObject){
    for (i=0;i<selObject.options.length;i++){
        selObject.options[i].selected=false;
    }
}

function select_all(listbox_id){
    var listbox_values=document.getElementById(listbox_id);
    for (i=0;i<listbox_values.options.length;i++){
        listbox_values.options[i].selected=true;
    }
}

function select_none(listbox_id){
    var listbox_values=document.getElementById(listbox_id);
    for (i=0;i<listbox_values.options.length;i++){
        listbox_values.options[i].selected=false;
    }
}

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

