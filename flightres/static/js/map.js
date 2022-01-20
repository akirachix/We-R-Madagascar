function permApproval(uid, status) {
    // console.log(uid, status)
}

$(document).ready(function () {
    // var lat = document.getElementById('map').getAttribute('value').split(',')[0]
    // var long = document.getElementById('map').getAttribute('value').split(',')[1

    var expandBtn = document.getElementsByClassName('expandData')

    flight_objects = flight_objects.replace(/&quot;/g, '"').replace(/uav_uuid__operator__company_name/g, 'company_name');
    flight_object = JSON.parse(flight_objects)

    for (var i = 0; i < expandBtn.length; i++) {
        expandBtn[i].addEventListener('click', function (e) {
            // object_id = e.target.id.split('_')[1];
            const closestPopupElement = e.target.closest('.highlight');
            e.stopPropagation();
            object_id = closestPopupElement.id.split('_')[1];
            console.log(closestPopupElement)
            console.log(object_id,'objectId');
            for (var j = 0; j < flight_object.length; j++) {
                if (object_id == flight_object[j].uav_uid) {
                    var lat = [];
                    var long = [];
                    var id = [];
                    var alti = [];
                    var status1 = [];
                    var cent = new L.LatLng(flight_object[j].latitude, flight_object[j].longitude);
                    
                    for(var k=0; k < flight_object.length; k++) {
                        if(flight_object[j].uav_uid != flight_object[k].uav_uid) {
                            if( flight_object[k].flight_start_date <= flight_object[j].flight_start_date && flight_object[j].flight_end_date <= flight_object[k].flight_end_date) {
                                var tar = new L.LatLng(flight_object[k].latitude, flight_object[k].longitude);
                                var distance_from_location = cent.distanceTo(tar) / 1000;
                                console.log(distance_from_location)
                                if (distance_from_location <= 10) {
                                    lat.push(flight_object[k].latitude);
                                    long.push(flight_object[k].longitude);
                                    alti.push(flight_object[k].altitude);
                                    status1.push(flight_object[k].status);
                                    id.push(flight_object[k].uav_uid);
                                };
                            }
                            else if(flight_object[j].flight_start_date <= flight_object[k].flight_end_date && flight_object[k].flight_end_date <= flight_object[j].flight_end_date){
                                var tar = new L.LatLng(flight_object[k].latitude, flight_object[k].longitude);
                                var distance_from_location = cent.distanceTo(tar) / 1000;
                                if (distance_from_location <= 10) {
                                    lat.push(flight_object[k].latitude);
                                    long.push(flight_object[k].longitude);
                                    alti.push(flight_object[k].altitude);
                                    status1.push(flight_object[k].status);
                                    id.push(flight_object[k].uav_uid);
                                };
                            }
                            
                            else if(flight_object[j].flight_start_date <= flight_object[k].flight_start_date && flight_object[k].flight_start_date <= flight_object[j].flight_end_date){
                                var tar = new L.LatLng(flight_object[k].latitude, flight_object[k].longitude);
                                var distance_from_location = cent.distanceTo(tar) / 1000;
                                if (distance_from_location <= 10) {
                                    lat.push(flight_object[k].latitude);
                                    long.push(flight_object[k].longitude);
                                    alti.push(flight_object[k].altitude);
                                    status1.push(flight_object[k].status);
                                    id.push(flight_object[k].uav_uid);
                                };
                            }
                            
                            else {
                                console.log("error");
                            };

                        };
                        
                    };
                    createModal(flight_object[j], flight_object[j].status, lat, long, alti, status1,id)
                    // pass id or sth from here to record the deny reason for a particular item
                    openDenyModal(flight_object[j].uav_uid, flight_object[j].rejection_reason, flight_object[j].assigned_to__username)
                }
            }
        })
    }

    function createModal(data, das, lat, long,alti, status1,id) {
        console.log(data);
        console.log(lat,'lat');
        console.log(long,'long');
        let assign_button = current_email===data.assigned_to__email?`<button   class="common-button is-bg unassign-btn" style="display: inline-block;margin-left:10px;">Unassign Self</button>`:``
        let approve_button = (current_email===data.assigned_to__email && data.status != 'Approved')?`<a href="/np/dashboard/approve_perm/`+ data.uav_uid + `/` + data.assigned_to__username + `/approve" class="common-button is-bg">Approve</a>`:`<a class="common-button is-bg is-disable">Approve</a>`
        let deny_button = (current_email===data.assigned_to__email && data.status != 'Rejected')?`<span  class="common-button is-border cancel-button" id="denyButton">Deny</span>`:`<span  class="common-button is-border cancel-button is-disable">Deny</span>`
        let assignee = data.assigned_to__username===null?`<button class="common-button is-bg assign-btn">Assign Self</button>`:`<p style="display: inline-block;">Assigned to <b> ${data.assigned_to__username}</b></p>`;
        let drone_insurance = data.flight_insurance_url===null?``:`<div class="col-md-4">
                                                                        <div class="file-upload">
                                                                            <a href="`+ data.flight_insurance_url + `" target="_blank" class="file-link">
                                                                                <div class="file-icon">
                                                                                    <i class="material-icons">description</i>
                                                                                </div>
                                                                                <p>Drone Insurance</p>
                                                                            </a>
                                                                        </div>
                                                                    </div>`
        var html1 = `
        <div class="popup-header">
            <h3>Permission Request for <b>ID `+ data.uav_uid + `</b></h3>
            ${assignee}
            ${assign_button}
        </div>
        <div class="popup-content">
            <div class="drone-details">
                <div class="row gx-md-3 gx-lg-3">
                    <div class="col-xl-5 col-sm-12">
                        <div class="drone-content col-left">
                            <ul>
                                <li>
                                    <h4>Operators info</h4>
                                    <div class="content-list">
                                        <p>
                                            <b>Company Name:</b>
                                            <span>`+ data.company_name + `</span>
                                        </p>
                                        <p>
                                            <b>Phone Number:</b>
                                            <span>`+ data.uav_uuid__operator__phone_number + `</span>
                                        </p>
                                        <p>
                                            <b>Email:</b>
                                            <span>`+ data.uav_uuid__operator__email + `</span>
                                        </p>
                                    </div>
                                </li>
                                <br>
                                <li>
                                    <h4>Flight info</h4>
                                    <div class="content-list">
                                        <p><b>Altitude:
                                            </b><span>`+ data.altitude + `</span>
                                        </p>
                                        <p><b>Start Date:
                                            </b><span>`+ data.flight_start_date + `</span>
                                        </p>
                                        <p><b>End Date:
                                            </b><span>`+ data.flight_end_date + `</span>
                                        </p>
                                        <p><b> Time:
                                            </b><span>`+ data.flight_time + `</span>
                                        </p>
                                        <p><b>Purpose:
                                            </b><span>`+ data.flight_purpose + `</span>
                                        </p>
                                        <p><b>Aircraft Name:
                                            </b><span>`+ data.uav_uuid__popular_name + `</span>
                                        </p>
                                        <p><b>Unique ID:
                                            </b><span>`+ data.uav_uuid + `</span>
                                        </p>
                                    </div>
                                </li>
                                <br>
                                <li>
                                    <h4>Pilot info</h4>
                                    <div class="content-list">
                                        <p><b>Pilot Name: </b><span>
                                            `+ data.pilot_id__name + `
                                            </span></p>
                                            <p><b>Pilot Phone Number:
                                            </b><span>`+ data.pilot_id__phone_number + `</span>
                                            </p>
                                            <p><b>Pilot Company:
                                            </b><span>`+ data.pilot_id__company + `</span>
                                            </p>
                                    </div>
                                </li>
                                <br>
                                <li>
                                    <h4>Documentation</h4>
                                    <div class="row g-2">
                                        <div class="col-md-4">
                                            <div class="file-upload">
                                                <a href="`+ data.pilot_id__cv_url + `" target="_blank" class="file-link">
                                                    <div class="file-icon">
                                                        <i class="material-icons">description</i>
                                                    </div>
                                                    <div class="file-info">
                                                        <div class ="file-wrap">
                                                            <p>Pilot CV</p>
                                                        </div>
                                                    </div>
                                                </a>
                                            </div>
                                        </div>
                                        <div class="col-md-4">
                                            <div class="file-upload">
                                                <a href="`+ data.flight_plan_url + `" target="_blank" class="file-link">
                                                    <div class="file-icon">
                                                        <i class="material-icons">description</i>
                                                    </div>
                                                    <p>Flight Plan</p>
                                                </a>
                                            </div>
                                        </div>
                                        ${drone_insurance}
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-xl-7 col-sm-12">
                        <div class="map-content col-right">
                            <div class="tab-content-holder current" id="location">
                                <div id="map" class="map" value="`+ data.latitude + `, ` + data.longitude + `" >
                                <div class="map-section">
                                <div class="legend-body" style='z-index:9090;min-width: 176px;max-width: 206px;position:absolute;left:auto;right:30px;bottom:50px;'>
                        <span class="title">Categories</span>
                        <ul class="legend">
                            
                            <li class="legend-item">
                                <a href="javascript:void()">
                                    <div class="circle-marker-legend is-green" tabindex="0" style="width: 25px;height: 25px;z-index: 381;outline: none;"><img width="15px" height="15px" src="/staticfiles/img/drone-icon.svg" alt="My image" style=""></div>
                                    <span class="label">Approved Flights</span>
                                    

                                </a>
                            </li>
                            <li class="legend-item">
                                <a href="javascript:void()">
                                    <div class="circle-marker-legend is-orange" tabindex="0" style="width: 25px;height: 25px;z-index: 381;outline: none;"><img width="15px" height="15px" src="/staticfiles/img/drone-icon.svg" alt="My image" style=""></div>
                                    <span class="label">Pending Flights</span>
                                </a>
                            </li>
                            <li class="legend-item">
                                <a href="javascript:void()">
                                    <div class="circle-marker-legend is-red" tabindex="0" style="width: 25px;height: 25px;z-index: 381;outline: none;"><img width="15px" height="15px" src="/staticfiles/img/drone-icon.svg" alt="My image" style=""></div>
                                    <span class="label">Rejected Flights</span>
                                </a>
                            </li>
                        </ul>
                    </div>
                    </div>
                    </div>
                            </div>
                            <div class="buttons is-end">
                                ${approve_button}
                                ${deny_button}
                            </div>
                        </div>        </div>                        </div>
                        </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
        `
        document.getElementById('flightPopUp').innerHTML = html1
        
        var btnAssignElement = document.querySelectorAll('.assign-btn');
        var btnUnassignElement = document.querySelectorAll('.unassign-btn');
        // console.log(btnElement,'btn')
        btnAssignElement.forEach(el=>{
            // console.log(el,'el');

            el.addEventListener('click',function(){
                $.ajax({url: `/np/dashboard/assign_perm/${data.uav_uid}/assign` , success: function(result){
                    // $("#div1").html(result);
                    // console.log(result,'result');
                    // closePopup();
                    data.assigned_to__email = result.assigned_to__email
                    data.assigned_to__username = result.assigned_to__username
                    
                    createModal(data, das, lat, long,alti, status1,id);
                    openDenyModal(data.uav_uid, data.rejection_reason, data.assigned_to__username)

                }});
                // console.log('assign clicked');
            })
        })
        btnUnassignElement.forEach(el=>{
            // console.log(el,'el');

            el.addEventListener('click',function(){
                $.ajax({url: `/np/dashboard/assign_perm/${data.uav_uid}/unassign` , success: function(result){
                    // $("#div1").html(result);
                    // console.log(result,'result');
                    // closePopup();
                    // console.log(data,lat,long,alti);
                    data.assigned_to__email = result.assigned_to__email
                    data.assigned_to__username = result.assigned_to__username
                    createModal(data, das, lat, long,alti, status1,id);
                }});
                // console.log('unassign clicked');
            })
        })
        plotMap(data, das, lat, long,alti, status1,id)
    }

    function plotMap(data, das, lat, long,alti, status1,id) {

        
        var greenIcon = L.icon({
            iconUrl: 'https://www.flaticon.com/svg/static/icons/svg/2945/2945641.svg',


            iconSize:     [38, 50], // size of the icon
            shadowSize:   [50, 64], // size of the shadow
            iconAnchor:   [19, 46], // point of the icon which will correspond to marker's location
            shadowAnchor: [4, 62],  // the same for the shadow
            popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
        });
        var mainIcon = L.icon({
            iconUrl: 'https://file.io/6rVETxzWgbQo',


            iconSize:     [38, 95], // size of the icon
            shadowSize:   [50, 64], // size of the shadow
            iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
            shadowAnchor: [4, 62],  // the same for the shadow
            popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
        });
        var testIcon = L.divIcon({
            className: `circle-marker ${data.status === 'Approved' ?"is-green": data.status === 'Rejected'? 'is-red':'is-orange'}`,
            // html: "<img src='/static/img/drone-icon.svg' alt='drone-img'/>",
            // html:`<img src='{% static "img/drone-icon.svg" %}' alt="My image">`,
            html:`<img src='/staticfiles/img/drone-icon.svg' alt="My image">`,
            iconSize:     [38, 50], // size of the icon
            shadowSize:   [50, 64], // size of the shadow
            // iconAnchor:   [19, 46], // point of the icon which will correspond to marker's location
            // shadowAnchor: [4, 62],  // the same for the shadow
            // popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
       
        });
        
        var map = L.map('map',{
            maxZoom:19, 
            fullscreenControl: {
                pseudoFullscreen: false
            }}).setView([data.latitude, data.longitude,data.altitude], 8);
        // var map = L.map('map', {
        //     // layers: [base],
        //     center: new L.LatLng(lat, lon),
        //     zoom: 12,
        // });
        var a = parseFloat(data.latitude);
        var b = parseFloat(data.longitude);
        customPopup1 = '<div class="bind-popup"> <div class="bind-header"> <table style="width:100%"><tr><th>ID</th><th>Altitude</th><th>Status</th></tr><tr><td>'+ data.uav_uid +'</td><td>'+ data.altitude +'</td><td>'+ data.status +'</td> </tr></table> <p><i class="fa fa-map-marker"></i> </p><em><span> </span> </em></div><a href="openSpace_details.html" class="openSpace_btn"></a></div><ul><li></li><li></li></ul>'

        var mar = [];
        var cir = [];

        // console.log(flight_object)
        var markers = L.markerClusterGroup();
        for(i=0;i<lat.length;i++){
            var c = parseFloat(lat[i]);
            var d = parseFloat(long[i]);
            customPopup = '<div class="bind-popup"> <div class="bind-header"> <table style="width:100%"><tr><th>ID</th><th>Altitude</th><th>Status</th></tr><tr><td>'+ id[i] +'</td><td>'+ alti[i] +'</td><td>'+ status1[i] +'</td></tr></table> <p><i class="fa fa-map-marker"></i> </p><em><span> </span> </em></div><a href="openSpace_details.html" class="openSpace_btn"></a></div><ul><li></li><li></li></ul>'
            var anothertestIcon = L.divIcon({
                className: `circle-marker ${status1[i] === 'Approved' ?"is-green": status1[i] === 'Rejected'? 'is-red':'is-orange'}`,
                // html: "<img src='/static/img/drone-icon.svg' alt='drone-img'/>",
                // html:`<img src='{% static "img/drone-icon.svg" %}' alt="My image">`,
                html:`<img src='/staticfiles/img/drone-icon.svg' alt="My image">`,
                iconSize:     [38, 50], // size of the icon
                shadowSize:   [50, 64], // size of the shadow
                // iconAnchor:   [19, 46], // point of the icon which will correspond to marker's location
                // shadowAnchor: [4, 62],  // the same for the shadow
                // popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
           
            });
            // mar[i] = L.marker([lat[i], long[i]], {icon:greenIcon}).addTo(map);
            mar[i] = L.marker([lat[i], long[i]], {icon:anothertestIcon})
            markers.addLayer(mar[i]);
            // if(status1[i] == 'Approved') {
            //     cir[i] = L.circle([lat[i], long[i]], {
            //         color: 'green',
            //         fillColor: 'green',
            //         fillOpacity: 0.5,
            //         radius: 1000
            //     }).addTo(map);

            // } else if(status1[i] == 'Pending') {
            //     cir[i] = L.circle([lat[i], long[i]], {
            //         color: 'orange',
            //         fillColor: 'orange',
            //         fillOpacity: 0.5,
            //         radius: 1000
            //     }).addTo(map);

            // } else if(status1[i] == 'Rejected') {
            //     cir[i] = L.circle([lat[i], long[i]], {
            //         color: 'red',
            //         fillColor: 'red',
            //         fillOpacity: 0.5,
            //         radius: 1000
            //     }).addTo(map);

            // };

            mar[i].bindPopup(customPopup);
        }
        // var testIcon = L.divIcon({
        //     className: `circle-marker ${data.status === 'Approved' ?"is-green": data.status === 'Rejected'? 'is-red':'is-orange'}`,
        //     // html: "<img src='/static/img/drone-icon.svg' alt='drone-img'/>",
        //     // html:`<img src='{% static "img/drone-icon.svg" %}' alt="My image">`,
        //     html:`<img src='/staticfiles/img/drone-icon.svg' alt="My image">`,
        //     iconSize:     [38, 50], // size of the icon
        //     shadowSize:   [50, 64], // size of the shadow
        //     // iconAnchor:   [19, 46], // point of the icon which will correspond to marker's location
        //     // shadowAnchor: [4, 62],  // the same for the shadow
        //     // popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
       
        // });
        // console.log(data,'data');
        var mark = L.marker([data.latitude, data.longitude], {icon:testIcon}).addTo(map);
        markers.addLayer(mark);
        map.addLayer(markers);

        mark.bindPopup(customPopup1);

        // if(das == 'Approved') {
        //     var circle = L.circle([data.latitude, data.longitude], {
        //         color: 'green',
        //         fillColor: 'green',
        //         fillOpacity: 0.5,
        //         radius: 1000
        //     }).addTo(map);

        // } else if(das == 'Pending') {
        //     var circle = L.circle([data.latitude, data.longitude], {
        //         color: 'orange',
        //         fillColor: 'orange',
        //         fillOpacity: 0.5,
        //         radius: 1000
        //     }).addTo(map);

        // } else {
        //     var circle = L.circle([data.latitude, data.longitude], {
        //         color: 'red',
        //         fillColor: 'red',
        //         fillOpacity: 0.5,
        //         radius: 1000
        //     }).addTo(map);

        // };
        
        noFlyZone = noFlyZone.replace(/&quot;/g, '"')
        var noFlyZone_json = JSON.parse(noFlyZone)
        for (var x = 0; x < noFlyZone_json.length; x++) {
            var noFlyZoneLayer = new L.GeoJSON.AJAX("/uploads/shp_files/"+ String(noFlyZone_json[x]), {style : {
                "color": "red",
                "weight": 3,
                "opacity": 1
            }}).addTo(map);
            
        }
        osm = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZ2VvbWF0dXBlbiIsImEiOiJja2E5bDFwb2swdHNyMnNvenZxa2Vpeml2In0.fCStqdwmFYFP-cUvb5vMCw', {
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
        //alert('test');
        var geojsonLayer = new L.GeoJSON.AJAX("../../../staticfiles/data/nepal.geojson",{style:{
            "color": "#04AA66",
            "weight": 5,
            "opacity": 0.65
        }});       
            geojsonLayer.addTo(map);

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

        layerswitcher = L.control.layers(baseLayers, {}, { collapsed: true }).addTo(map);

        
        // var legend = L.control({position: 'bottomleft'});
        // legend.onAdd = function (map) {

        // var div = L.DomUtil.create('div', 'info legend');
        // labels = ['<strong>Categories</strong>'],
        // categories = ['Approved','Pending','Rejected'];
        // color=['Green','orange','Red'];

        // for (var i = 0; i < categories.length; i++) {

        //         div.innerHTML += 
        //         labels.push(
        //             '<i class="circle" style="opacity: 0.5;background:' + color[i] + '"></i> ' +
        //         (categories[i] ? categories[i] : '+'));

        //     }
        //     div.innerHTML = labels.join('<br>');
        // return div;
        // };
        // legend.addTo(map);
    }

});

$('.leaflet-popup-content, .leaflet-popup-content-wrapper').css('width', '300px');


function openDenyModal(flight_id, rejection_reason, unam) {
    let denyElement = document.getElementById('denyButton')
    denyElement.addEventListener('click', () => {
        // console.log("show pop");
        let smallPopup = document.getElementById('open-modal-deny');
        if (rejection_reason != null) {
            var rej = rejection_reason;
        } else {
            var rej = ''
        };
        
        smallPopup.classList.add('open');
        html1 = `
            <div class="popup-header">
                <h5>Reason for Denial</h5>
            </div>
            <input value="${rej}" type="textarea" placeholder="Reason for rejection" id="reasonInput"
                style="height: 54px; width: 375px; align-self: center;" for="reason"
                ; name="reason" ; ></input>
            <br>
            <div class="buttons is-end" style="height:35px;">
                <button onclick="sendReason(${flight_id})" uname="${unam}" type="submit" style="margin-right:3px" class="common-button is-bg close-icon" id="denySubmit">Submit</button>
            </div>`
        document.getElementById("submit-deny-div").innerHTML = html1
        //closePopup()
    })
}

function sendReason(flight_id) {
    
    let inputValue = document.getElementById('reasonInput').value
    let uname = document.getElementById('denySubmit').getAttribute('uname')
    console.log(typeof uname)
    let url = `/np/dashboard/deny_perm/`+ flight_id + `/` + uname + ``
    let data = { value: inputValue };

    fetch(url, {
        method: "POST",
        // data: {'getdata': JSON.stringify(data)},
        body: JSON.stringify(data),
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(res => {
        document.getElementById('submit-deny-div').innerHTML = '';
        let smallPopup = document.getElementById('open-modal-deny');
        let largePopup = document.getElementById('open-modal');
        smallPopup.classList.remove('open');
        largePopup.classList.remove('open');
        location = window.location;
        // console.log("Success", res);
        // console.log(flight_id, data);
    });

}

function closePopup() {
    let closeDenyPopElement = document.getElementById('denyClose')
    closeDenyPopElement.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('submit-deny-div').innerHTML = '';
    });
}