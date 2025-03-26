(function() {
 
    var zoomLevel = 12,
        mapCenter = [6.1603907, -75.6046390329014];
    
    var options = {
        center: mapCenter,
        zoom: zoomLevel
    };
  
    var Leaflet = L;
    
    var map = Leaflet.map('map', options);
    
    Leaflet.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);
    
    var ips,
        $body = $('body'),
        $locate = $('#locate'), 
        $findNearest = $('#find-nearest'),
        $status = $('#status');
    
    // Load the data from the external JSON file
    fetch('/static/js/ips.json')
        .then(response => response.json())
        .then(data => {
            // Proceed with the data processing
            $body.addClass('loaded');
            
            ips = Leaflet.geoJson(data, {
                
                pointToLayer: function(feature, latlng) {
                   return Leaflet.circleMarker(latlng, {
                       stroke: false,
                       fillColor: 'orange',
                       fillOpacity: 1,
                       radius: 10
                   });
                }
            }).addTo(map); 
            
            $locate.fadeIn().on('click', function(e) {
                
                $status.html('Encontrando tu localización');
                
                if (!navigator.geolocation){
                    alert("<p>Perdón, tu navegador no permite la Geolocalización.</p>");
                    return;
                }
                
                $body.removeClass('loaded');
                  
                navigator.geolocation.getCurrentPosition(success, error);
                
                $locate.fadeOut();
            });   
        });
  
    function success(position) {
        
        $body.addClass('loaded');
        
        var currentPos = [position.coords.latitude, position.coords.longitude];
        
        map.setView(currentPos, zoomLevel);
  
        var myLocation = Leaflet.marker(currentPos)
                            .addTo(map)
                            .bindTooltip("ESTAS AQUÍ!")
                            .openTooltip();
        
        $findNearest.fadeIn().on('click', function(e) {
                
            $findNearest.fadeOut();
                
            $status.html('encontrando la ips más cercana');
            
            queryFeatures(currentPos, 1);
            
            myLocation.unbindTooltip();
        });
    }
  
    function error() {
        alert("no fue posible encontrar tu localización");
    }
     
    function queryFeatures(currentPos, numResults) {
        
        var distances = [];
        
        ips.eachLayer(function (ips) {
            var distance = Leaflet.latLng(currentPos).distanceTo(ips.getLatLng())/1000;
            distances.push({ name: ips.feature.properties.ips_name, distance });
        });
        
        distances.sort(function(a, b) {
            return a.distance - b.distance;
        });
        
        var ipsLayer = Leaflet.featureGroup();
      
        ips.eachLayer(function(ips) {
            var distance = Leaflet.latLng(currentPos).distanceTo(ips.getLatLng())/1000;
            
            if(distance === distances[0].distance) { 
                ips.bindTooltip(distance.toLocaleString() + ' km de tu localización actual.');
                
                Leaflet.polyline([currentPos, ips.getLatLng()], {
                    color: 'orange',
                    weight: 2,
                    opacity: 1,
                    dashArray: "5, 10"
                }).addTo(ipsLayer);
            }

        });


        
        map.flyToBounds(ipsLayer.getBounds(), { duration: 3, easeLinearity: .1 });
        map.on('zoomend', function() {
            map.addLayer(ipsLayer);
        });

        var $assignedIps = $('#assigned-ips'); // Selecciona el elemento <h2>
        $assignedIps.html("Este es tu IPS asignado: " + distances[0].name);

        var inputElement = document.getElementById('ips_input');
            
         // Establecer el valor del input
        inputElement.value = distances[0].name;
+       
        $('#actions').show();

    }
    // Acciones de los botones
    $('#confirm').on('click', function() {
        alert("Confirmado");
    });

    $('#recheck').on('click', function() {
        $('#assigned-ips').html(''); // Limpia el <h2>
        $('#actions').hide();
        $locate.fadeIn(); // Muestra el botón de localización nuevamente

    });
})();
