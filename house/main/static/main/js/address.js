$(function() {
  function initialize($canvas) {
    var lat = $canvas.data('initial-lat');
    var lng = $canvas.data('initial-lng');

    var latlng = new google.maps.LatLng(lat, lng);
    var mapOptions = {
       zoom: 15,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map($canvas[0], mapOptions);
    var marker = new google.maps.Marker({
       map: map,
       animation: google.maps.Animation.DROP,
       position: latlng,
       title: "Your current location (drag to pinpoint more exactly)",
       draggable: true,
       position_changed: function() {
         $('#id_latitude').val(this.position.lat());
         $('#id_longitude').val(this.position.lng());
       }
    });
    return map;
  }
  initialize($('#map-canvas'));

});
