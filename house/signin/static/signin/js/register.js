function initialize_map() {

  var latlng = new google.maps.LatLng(-34.397, 150.644);
  var mapOptions = {
    zoom: 8,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }
  return new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
}



$(function() {
  if (!$('#id_address').val()) {
    $('#id_address')[0].focus();
  }

  //var map = initialize_map();
  var geocoder = new google.maps.Geocoder();

  $('.alternatives a.wasnot').click(function() {
    $('.alternatives').hide();
    $('#id_address')[0].focus();
    return false;
  });

  function _start_loading() {
    $('.loading').show();
  }

  function _stop_loading() {
    $('.loading').hide();
  }

  function _search(address) {
    console.log('SEARCHING', address);
    geocoder.geocode({'address': address}, function(results, status) {
      _stop_loading();
      if (status == google.maps.GeocoderStatus.OK) {
        $.each(results, function(i, result) {
          $('.alternatives li').remove();
          $('<li></li>')
            .append($('<a href="#"></a>')
                    .text(result.formatted_address)
                    .click(function() {
                      it_was(result);
                      return false;
                    }))
            .appendTo($('.alternatives ul'));
          $('.alternatives').show();
        });
      } else {
      }
    });
  }

  function it_was(result) {
    $('.alternatives').hide();
    $('#id_latitude').val(result.geometry.location.lat());
    $('#id_longitude').val(result.geometry.location.lng());
    $.each(result.address_components, function (i, e) {
      if (e.types[0] == 'street_number') {
        $('#id_line1').val(e.long_name);
      } else if (e.types[0] == 'route') {
        if ($('#id_line1').val()) {
          $('#id_line1').val($('#id_line1').val() + ', ' + e.long_name);
        } else {
          $('#id_line1').val(e.long_name);
        }
      } else if (e.types[0] == 'locality') {
        $('#id_city').val(e.long_name);
      } else if (e.types[0] == 'administrative_area_level_1') {
        $('#id_state').val(e.long_name);
      } else if (e.types[0] == 'postal_code') {
        $('#id_zip_code').val(e.long_name);
      } else {
        console.log(e.types[0], e.long_name);
      }
    });
    $('form.search-form').hide();
    $('form.register').show();
  }

  $('form.search-form').on('submit', function() {
    var address = $.trim($('#id_address').val());
    if (!address.length) return;
    _start_loading();
    _search(address);
    return false;
  });

  $('#id_address').on('keyup', function() {
    $('.alternatives:visible').hide();

  });

  if ($('.existing').size()) {
    $('form.register').show();
    $('form.search-form').hide();
  }
});
