(function( $ ) {
  $.widget( "ui.combobox", {
    _create: function() {
      this.wrapper = $( "<span>" )
        .addClass( "ui-combobox" )
        .insertAfter( this.element );

      this._createAutocomplete();
    },

    _createAutocomplete: function() {
      var selected = this.element.children( ":selected" ),
        value = selected.val() ? selected.text() : "";

      this.input = $( "<input>" )
        .appendTo( this.wrapper )
        .val( value )
        .attr( "title", "" )
        .addClass( "ui-state-default ui-combobox-input ui-widget ui-widget-content ui-corner-left" )
        .autocomplete({
          delay: 0,
          minLength: 0,
          source: $.proxy( this, "_source" )
        })
        .tooltip({
          tooltipClass: "ui-state-highlight"
        });

      this._on( this.input, {
        autocompleteselect: function( event, ui ) {
          ui.item.option.selected = true;
          this._trigger( "select", event, {
            item: ui.item.option
          });
        },

        autocompletechange: "_removeIfInvalid"
      });
    },

    _source: function( request, response ) {
      var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
      response( this.element.children( "option" ).map(function() {
        var text = $( this ).text();
        if ( this.value && ( !request.term || matcher.test(text) ) )
          return {
            label: text,
            value: text,
            option: this
          };
      }) );
    },

    _removeIfInvalid: function( event, ui ) {
      // Selected an item, nothing to do
      if ( ui.item ) {
        return;
      }

      // Search for a match (case-insensitive)
      var value = this.input.val(),
        valueLowerCase = value.toLowerCase(),
        valid = false;
      this.element.children( "option" ).each(function() {
        if ( $( this ).text().toLowerCase() === valueLowerCase ) {
          this.selected = valid = true;
          return false;
        }
      });

      // Found a match, nothing to do
      if ( valid ) {
        return;
      }
	  
      // Remove invalid value
      this.input
        .val( "" )
        .attr( "title", value + " didn't match any item" )
        .tooltip( "open" );
      this.element.val( "" );
      this._delay(function() {
        this.input.tooltip( "close" ).attr( "title", "" );
      }, 2500 );
      this.input.data( "ui-autocomplete" ).term = "";
    },

    _destroy: function() {
      this.wrapper.remove();
      this.element.show();
    }
  });
})( jQuery );

function validateAGForm() {
	var valid = true;
    for(var i = 0; i < document.agForm.length; i++) 
    {
		var input = document.agForm[i]
		if( (input.type == 'text' || input.type == 'select-one') && input.value == '')
		{
			input.className += " highlight"
			valid = false;
		}
		else
        	input.className = input.className.replace(/(?:^|\s)highlight(?!\S)/ , '');
    }
	
	if(valid)
    document.agForm.submit_flag.value=1;
		$('#agForm').submit();
}

function validateAGSingleSubmitForm() {
  var valid = true;
  for(var i = 0; i < document.agForm.length; i++) 
  {
    var input = document.agForm[i]
    if( (input.type == 'text' || input.type == 'select-one') && input.value == '')
    {
      input.className += " highlight"
      valid = false;
    }
    else {
      input.className = input.className.replace(/(?:^|\s)highlight(?!\S)/ , '');
    }
  }
  
  if(valid) {
    $('#agForm').submit();
  }
}

function validateEditParticipant() {
	var valid = true;
	
    for(var i = 0; i < document.edit_participant.length; i++) 
    {
  		var input = document.edit_participant[i]
  		if(input.type == 'text' && input.value == '')
  		{
  			input.className += " highlight"
  			valid = false;
  		}
  		else
        input.className = input.className.replace(/(?:^|\s)highlight(?!\S)/ , '');
      }
  	
	if(valid)
  {
		document.edit_participant.submit_flag.value=1;
    document.edit_participant.submit();
  }
}

function validateEditBarcode() {
  var valid = true;
  
    for(var i = 0; i < document.edit_barcode.length; i++) 
    {
      var input = document.edit_barcode[i]
      if(input.type == 'text' && input.value == '')
      {
        input.className += " highlight"
        valid = false;
      }
      else
        input.className = input.className.replace(/(?:^|\s)highlight(?!\S)/ , '');
      }
    
  if(valid)
  {
    document.edit_barcode.submit_flag.value=1;
    document.edit_barcode.submit();
  }
}

/* from http://stackoverflow.com/questions/46155/validate-email-address-in-javascript */
function validateEmail(email) { 
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email); 
} 

/* input field number validation*/
function validateNumber(evt) {
  var theEvent = evt || window.event;
  var key = theEvent.keyCode || theEvent.which;
  //say what these keys are
  if(theEvent.keyCode == 8 || theEvent.keyCode == 37|| theEvent.keyCode ==38|| theEvent.keyCode == 39|| theEvent.keyCode == 40 || theEvent.keyCode == 46 || theEvent.keyCode == 9)
  	return
  key = String.fromCharCode( key );
  var regex = /[0-9]|\./;
  if( !regex.test(key) ) {
    theEvent.returnValue = false;
    if(theEvent.preventDefault) theEvent.preventDefault();
  }
}

var old_field_number = 1

function getNextBarcode(current_barcode) {
  bc = String(current_barcode);
  while (bc.length < 9) {
    bc = '0' + bc;
  }
  return bc;
}

function addBarcodeField(field_name, current_barcode) {
  var new_field_number = old_field_number+1
  old_field_number = new_field_number
  next_barcode = getNextBarcode(current_barcode)
  var newinput = '<div id="'+field_name+'_'+new_field_number+'"><input type="text" name="'+field_name+'_'+new_field_number+'" id="'+field_name+'_'+new_field_number+'" onkeypress="validateNumber(event);" value="' + next_barcode + '"><a class="remove_field" href="javascript:removeField(\''+field_name+'_'+new_field_number+'\')" title="Remove this field">x</a></input></div>'
  var newTextBoxDiv = $(document.createElement('div')).attr("id", field_name+'_'+new_field_number);
  newTextBoxDiv.after().html(newinput);
  newTextBoxDiv.appendTo('#'+field_name);
  //setDefaultText();
}

function removeField(item_id) {
  var c = document.getElementById(item_id)
  c.parentNode.removeChild(c);
}

function setDefaultText() 
{
  $('input[type="text"], textarea').focus(function () 
  {
    defaultText = $(this).val();
    $(this).val('');
  });
  $('input[type="text"], textarea').blur(function () 
  {
    if ($(this).val() == "") 
    {
      $(this).val(defaultText);
    }
  });
}

