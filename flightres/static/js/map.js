$(document).ready(function () {
    // var map = L.map('map').setView([27.7, 85.4], 7);
    var map = L.map('map', {
        // layers: [base],
        center: new L.LatLng(27.7, 85.4),
        zoom: 12,
    });

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
    // var markerIcon = [
    // 	["Kritipur",27.67988,85.27544],
    // 	["Pokhara",28.26689,83.96851],
    // 	["Waling",27.98333,83.76667],
    // 	["Banepa",27.62979,85.52138],
    // 	["Butwal",27.70055,83.44836],
    // 	];

    // 	for (var i = 0; i < markerIcon.length; i++) {
    // 		marker = new L.marker([markerIcon[i][1],markerIcon[i][2]])
    // 			.bindPopup(markerIcon[i][0])
    // 			.addTo(map);
    // 	}

    var baseLayers = {
        "OpenStreetMap": osm,
        "Google Streets": googleStreets,
        "Google Hybrid": googleHybrid,
        "Google Satellite": googleSat,
        "Google Terrain": googleTerrain,

    };

    // var latLong = [{
    // 	"lat": 27.67988,
    // 	"lng": 85.27544
    //   }, {
    // 	"lat": 28.26689,
    // 	"lng": 83.96851
    //   }, {
    // 	"lat": 27.98333,
    // 	"lng": 83.76667
    //   }, {
    // 	"lat": 27.62979,
    // 	"lng": 85.52138
    //   }, {
    // 	"lat": 27.70055,
    // 	"lng": 83.44836
    //   }];
    customPopup = '<div class="bind-popup"> <div class="bind-header"><h5>Proposed FLight Location</h5> <p><i class="fa fa-map-marker"></i> </p><em><span> </span> </em></div><a href="openSpace_details.html" class="openSpace_btn"></a></div><ul><li></li><li></li></ul>'
    var customOptions =
        {
            'maxWidth': '400',
            'width': '200',
            'className': 'popupCustom'
        }
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
