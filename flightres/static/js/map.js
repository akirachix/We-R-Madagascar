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
            object_id = e.target.id.split('_')[1]
            for (var j = 0; j < flight_object.length; j++) {
                if (object_id == flight_object[j].uav_uid) {
                    var lat = [];
                    var long = [];
                    var alti = [];

                    for(var k=0; k < flight_object.length; k++) {
                        if(flight_object[k].flight_start_date > flight_object[j].flight_start_date && flight_object[k].flight_start_date < flight_object[j].flight_end_date) {
                            lat.push(flight_object[k].latitude);
                            long.push(flight_object[k].longitude);
                            alti.push(flight_object[k].altitude);
                        };
                    };
                    createModal(flight_object[j], lat, long, alti)
                    // pass id or sth from here to record the deny reason for a particular item
                    openDenyModal(flight_object[j].uav_uid, flight_object[j].rejection_reason)
                }
            }
        })
    }

    function createModal(data, lat, long, alti) {
        let assign_button = current_email===data.assigned_to__email?`<a href="/np/dashboard/assign_perm/` + data.uav_uid + `/unassign" class="common-button is-bg" style="display: inline-block;margin-left:10px;">Unassign Self</a>`:``
        let approve_button = current_email===data.assigned_to__email?`<a href="/np/dashboard/approve_perm/`+ data.uav_uid + `/approve" class="common-button is-bg">Approve</a>`:`<a class="common-button is-bg is-disable">Approve</a>`
        let deny_button = current_email===data.assigned_to__email?`<span  class="common-button is-border cancel-button" id="denyButton">Deny</span>`:`<span  class="common-button is-border cancel-button is-disable">Deny</span>`
        let assignee = data.assigned_to__username===null?`<a href="/np/dashboard/assign_perm/` + data.uav_uid + `/assign" class="common-button is-bg">Assign Self</a>`:`<p style="display: inline-block;">Assigned to <b> ${data.assigned_to__username}</b></p>`;
        var html1 = `
        <div class="popup-header">
            <h3>Permission Request for <b>UIN `+ data.uav_uuid + `</b></h3>
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
                                        <div class="col-md-4">
                                            <div class="file-upload">
                                                <a href="`+ data.flight_insurance_url + `" target="_blank" class="file-link">
                                                    <div class="file-icon">
                                                        <i class="material-icons">description</i>
                                                    </div>
                                                    <p>Drone Insurance</p>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-xl-7 col-sm-12">
                        <div class="map-content col-right">
                            <div class="tab-content-holder current" id="location">
                                <div id="map" class="map" value="`+ data.latitude + `, ` + data.longitude + `" ></div>
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
        plotMap(data, lat, long, alti)
    }

    function plotMap(data, lat, long, alti) {
        var greenIcon = L.icon({
            iconUrl: 'https://www.flaticon.com/svg/static/icons/svg/2945/2945641.svg',


            iconSize:     [30, 50], // size of the icon
            shadowSize:   [50, 64], // size of the shadow
            iconAnchor:   [15, 44], // point of the icon which will correspond to marker's location
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
        var map = L.map('map').setView([data.latitude, data.longitude], 8);
        // var map = L.map('map', {
        //     // layers: [base],
        //     center: new L.LatLng(lat, lon),
        //     zoom: 12,
        // });

        customPopup1 = '<div class="bind-popup"> <div class="bind-header"> <table style="width:100%"><tr><th>Latitude</th><th>Longitude</th><th>Altitude</th></tr><tr><td>'+ parseFloat(data.latitude).toFixed(5) +'</td><td>'+ parseFloat(data.longitude).toFixed(5) +'</td><td>7777</td> </tr></table> <p><i class="fa fa-map-marker"></i> </p><em><span> </span> </em></div><a href="openSpace_details.html" class="openSpace_btn"></a></div><ul><li></li><li></li></ul>'

        var mar = [];
        var cir = [];

        // console.log(flight_object)
        for(i=0;i<lat.length;i+=2){
            customPopup = '<div class="bind-popup"> <div class="bind-header"> <table style="width:100%"><tr><th>Latitude</th><th>Longitude</th><th>Altitude</th></tr><tr><td>'+ parseFloat(lat[i]).toFixed(5) +'</td><td>'+ parseFloat(long[i]).toFixed(5) +'</td><td>'+ alti[i] +'</td> </tr></table> <p><i class="fa fa-map-marker"></i> </p><em><span> </span> </em></div><a href="openSpace_details.html" class="openSpace_btn"></a></div><ul><li></li><li></li></ul>'

            mar[i] = L.marker([lat[i], long[i]],{icon:greenIcon}).addTo(map);
            cir[i] = L.circle([lat[i], long[i]], {
                color: 'red',
                fillColor: '#f03',
                fillOpacity: 0.5,
                radius: 100
            }).addTo(map);
            mar[i].bindPopup(customPopup);
        }
        var mark = L.marker([data.latitude, data.longitude]).addTo(map);
        mark.bindPopup(customPopup1);
        var circle = L.circle([data.latitude, data.longitude], {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0.5,
            radius: 100
        }).addTo(map);

        osm = L.tileLayer('https://api.mapbox.com/styles/v1/upendraoli/cjuvfcfns1q8r1focd0rdlgqn/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoidXBlbmRyYW9saSIsImEiOiJjaWYwcnFnNmYwMGY4dGZseWNwOTVtdW1tIn0.uhY72SyqmMJNTKa0bY-Oyw', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        })

        googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }).addTo(map);
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
    }

});

$('.leaflet-popup-content, .leaflet-popup-content-wrapper').css('width', '300px');


function openDenyModal(flight_id, rejection_reason) {
    let denyElement = document.getElementById('denyButton')
    denyElement.addEventListener('click', () => {
        // console.log("show pop");
        let smallPopup = document.getElementById('open-modal-deny');
        smallPopup.classList.add('open');
        html1 = `
            <div class="popup-header">
                <h5>Reason for Denial</h5>
            </div>
            <input value="${rejection_reason}" type="textarea" placeholder="Reason for rejection" id="reasonInput"
                style="height: 54px; width: 375px; align-self: center;" for="reason"
                ; name="reason" ; ></input>
            <br>
            <div class="buttons is-end" style="height:35px;">
                <button onclick="sendReason(${flight_id})" type="submit" style="margin-right:3px" class="common-button is-bg close-icon" id="denySubmit">Submit</button>
            </div>`
        document.getElementById("submit-deny-div").innerHTML = html1
        closePopup()
    })
}

function sendReason(flight_id) {
    let inputValue = document.getElementById('reasonInput').value
    let url = `/np/dashboard/deny_perm/`+ flight_id +``
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