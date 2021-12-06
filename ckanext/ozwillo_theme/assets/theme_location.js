"use strict";

/* theme_location
 *
 * This JavaScript module gets a geojson from osm given a location name
 * *
 */

ckan.module('theme_location', function ($) {
  return {
    initialize : function () {
      var val = document.getElementById("field-spatial-name");
      val.style.width = "100%";
      var osmkey = this.options.osmkey;
      var key_id = '';
      var value_id = '';
      var spatial_key = '';
      var spatial_value = '';
      var spatial_name_key = '';
      var spatial_name_value = '';

      // Check extras fields to see witch one are spatial fields or choose empty ones and hide them
      for (var i = 0; i < 5; i++) {
        key_id = 'field-extras-' + i + '-key';
        value_id = 'field-extras-' + i + '-value';
        try {
          var myField = $('#' + key_id)[0];
          var fieldValue = myField.value;
        } catch(err) {
          console.log(key_id);
          continue
        }
        if (fieldValue === 'spatial') {
          spatial_key = key_id;
          spatial_value = value_id;
          myField.parentElement.parentElement.parentElement.style.display = 'none';
        } else if (fieldValue === 'spatial-name') {
          spatial_name_key = key_id;
          spatial_name_value = value_id;
          myField.parentElement.parentElement.parentElement.style.display = 'none';
        }
      }
      if (spatial_key === '' || spatial_name_key === '') {
        for (var i = 0; i < 5; i++) {
          key_id = 'field-extras-' + i + '-key';
          value_id = 'field-extras-' + i + '-value';
          try {
            var myField = $('#' + key_id)[0];
            var fieldValue = myField.value;
          } catch(err) {
            console.log(key_id);
            continue
          }
          if (fieldValue === '') {
            if (spatial_key === '') {
              spatial_key = key_id;
              spatial_value = value_id;
              myField.parentElement.parentElement.parentElement.style.display = 'none';
            } else if (spatial_name_key === '') {
              spatial_name_key = key_id;
              spatial_name_value = value_id;
              myField.parentElement.parentElement.parentElement.style.display = 'none';
            }
          }
        }
      }

      // Wait for the user to finish typing before getting the geojson
      $(document).on('input', '#field-spatial-name', function(){
        var origin_val = val.value;
        setTimeout(function(){
          if (origin_val === val.value && val.value !== '') {
            nominatim(val.value);
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
            document.getElementById(spatial_key).value = 'spatial';
            document.getElementById(spatial_value).value = JSON.stringify(data[0]['geojson']);
            document.getElementById(spatial_name_key).value = 'spatial-name';
            document.getElementById(spatial_name_value).value = val.value;
          } catch (TypeError) {
            console.log("Error: no result found for the location you entered");
          }
        })
        .fail(function(jqXhr, textStatus, error) {
          console.log("Error: " + textStatus + ", " + error);
        });
      }
    }
  };
});