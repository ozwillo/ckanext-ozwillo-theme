"use strict";

/* theme_location
 *
 * This JavaScript module gets a geojson from osm given a location name
 *
 * TODO: Find how to manage the required field without the popup (ckan builtin)
 *
 */

ckan.module('theme_location', function ($) {
  return {
    initialize : function () {
      var setAlert= true;
      var val = document.getElementById("field-spatial-name");
      var osmkey = this.options.osmkey;
      var errorvalue = this.options.errorvalue;
      var element = document.getElementById('custom_fields');
      element.firstElementChild.firstElementChild.style.display = 'none';

      // Wait for the user to finish typing before getting the geojson
      $(document).on('input', '#field-spatial-name', function(){
        var origin_val = val.value;
        setTimeout(function(){
          if (origin_val === val.value && val.value !== '') {
            nominatim(val.value)
          }
        } , 2000);
      });

      // Typeahead
      $( function() {
        $( "#field-spatial-name" ).autocomplete({
          minLength: 2,
          select: function( event, ui ) { nominatim(ui.item.value) },
          source: function (request, response) {
            var query = request.term;
            var url = 'https://search.osmnames.org/fr/q/' + query + '.js?key=' + osmkey;
            $.ajax( {
              url: url,
              success: function( data ) {
                var results = data['results'];
                var source_result = [];
                results.forEach( function (i) {
                  if (i['type'] === 'administrative') {
                    source_result.push({
                        label: i['display_name'],
                        value: i['display_name']
                    })
                  }
                });
                response( source_result );
              }
            })
          }
        });
      });

      // Call OSM to get the geojson
      function nominatim(city) {
        var url = 'https://nominatim.openstreetmap.org/search/' + city + '?polygon_geojson=1';
        $.getJSON(url, {
          format:"json"
        })
        .done(function(data) {
          try {
            document.getElementById("field-extras-0-key").value = 'spatial';
            document.getElementById("field-extras-0-value").value = JSON.stringify(data[0]['geojson']);
          } catch (TypeError) {
            if (setAlert) {
              alert(errorvalue);
              setAlert = false;
            }
          }
        })
        .fail(function(jqXhr, textStatus, error) {
          console.log("Error: " + textStatus + ", " + error);
        });
      }
    }
  };
});