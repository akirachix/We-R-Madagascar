
$(document).ready(function () {
    var map = L.map('map').setView([lat, long], 15);
    // var map = L.map('map', {
    //     // layers: [base],
    //     center: new L.LatLng(lat, long),
    //     zoom: 12,
    // });
    var mark = L.marker([lat, long]).addTo(map);

    var circle = L.circle([lat, long], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 100
    }).addTo(map);

    osm = L.tileLayer('https://api.mapbox.com/styles/v1/upendraoli/cjuvfcfns1q8r1focd0rdlgqn/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoidXBlbmRyYW9saSIsImEiOiJjaWYwcnFnNmYwMGY4dGZseWNwOTVtdW1tIn0.uhY72SyqmMJNTKa0bY-Oyw', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });
    googleHybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });
    googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });
    googleTerrain = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    });


    var baseLayers = {
        "OpenStreetMap": osm,
        "Google Streets": googleStreets,
        "Google Hybrid": googleHybrid,
        "Google Satellite": googleSat,
        "Google Terrain": googleTerrain,

    };


    customPopup = '<div class="bind-popup"> <div class="bind-header"><h5>Proposed FLight Location</h5> <p><i class="fa fa-map-marker"></i> </p><em><span> </span> </em></div><a href="openSpace_details.html" class="openSpace_btn"></a></div><ul><li></li><li></li></ul>'

    // var Kritipur = L.circle([lat, lon], {
    //     color: '#047c41',
    //     fillColor: '#047c41',
    //     fillOpacity: 0.7,
    //     radius: 400
    // }).addTo(map);

    // Kritipur.bindPopup(customPopup, customOptions);
    // var long = '{{ object.longitude }}'
    // console.log("TWO")
    // console.log(long)
    // map.flyTo([lat, lon], 13)
    //   myMap.panTo([2, 22]);

    layerswitcher = L.control.layers(baseLayers, {}, {collapsed: true}).addTo(map);
});

$('.leaflet-popup-content, .leaflet-popup-content-wrapper').css('width', '300px');
