var map;
var sellerPosition;

function initialize() {
    console.log(parseFloat($("#lat").html()));
    console.log(parseFloat($("#lng").html()));
    var myOptions = {
        center: new google.maps.LatLng(parseFloat($("#lat").html()),
                                       parseFloat($("#lng").html())),
        zoom: 16,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        disableDefaultUI: true,
        disableDoubleClickZoom: true,
        draggable: false
    };

    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

    var marker = new google.maps.Marker({
        position: map.getCenter(),
        map: map,
        title: 'Select your location'
    });

    google.maps.event.addListener(marker, 'click', function() {
        map.setCenter(marker.getPosition());

    });

    google.maps.event.addListener(map, 'click', function(event) {
        sellerPosition = event.latLng;
        moveMarker(marker, event.latLng);

    });
}

function moveMarker(marker, location) {
    marker.setPosition(location);
    map.panTo(location);
    $("#text").html(sellerPosition.toString());
}

google.maps.event.addDomListener(window, 'load', initialize);