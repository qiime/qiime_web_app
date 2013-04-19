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

function validateNewParticipant() {
    for(var i = 0; i < document.newParticipant.length; i++) 
    {
        document.newParticipant[i].className = document.newParticipant[i].className.replace(/(?:^|\s)highlight(?!\S)/ , '');
    }
	
	var valid = true;
	
	if(!validateEmail(document.newParticipant.email.value))
	{
		document.newParticipant.email.className += " highlight"
		valid = false;
	}
	
	if(document.newParticipant.participantname.value == "")
	{
		document.newParticipant.participantname.className += " highlight"
		valid = false;
	}
	
	if(document.newParticipant.address.value == "")
	{
		document.newParticipant.address.className += " highlight"
		valid = false;
	}
	if(document.newParticipant.city.value == "")
	{
		document.newParticipant.city.className += " highlight"
		valid = false;
	}
	if(document.newParticipant.state.value == "")
	{
		document.newParticipant.state.className += " highlight"
		valid = false;
	}
	if(document.newParticipant.zip.value == "")
	{
		document.newParticipant.zip.className += " highlight"
		valid = false;
	}
	if(document.newParticipant.country.value == "")
	{
		document.newParticipant.country.className += " highlight"
		valid = false;
	}
	
	if(valid)
		$('#newParticipant').submit();
}

/* from http://stackoverflow.com/questions/46155/validate-email-address-in-javascript */
function validateEmail(email) { 
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
} 
