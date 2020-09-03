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
            for (j = 0; j < flight_object.length; j++) {
                if (object_id == flight_object[j].uav_uid) {
                    createModal(flight_object[j])
                    // pass id or sth from here to record the deny reason for a particular item
                    openDenyModal(flight_object[j].uav_uid)
                }
            }
        })
    }

    function createModal(data) {
        var html1 = `
        <div class="popup-header">
            <h3>Permission Request for <b>ID `+ data.uav_uid + `</b></h3>
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
                                            </span>
                                            <p><b>Pilot Phone Number:
                                            </b><span>`+ data.pilot_id__phone_number + `</span>
                                            </p>
                                    </div>
                                </li>
                                <li>
                                    <h4>Documentation</h4>
                                    <div class="row g-2">
                                        <div class="col-md-4">
                                            <div class="file-upload">
                                                <a href="`+ data.pilot_cv_url + `" class="file-link">
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
                                                <a href="`+ data.flight_plan_url + `" class="file-link">
                                                    <div class="file-icon">
                                                        <i class="material-icons">description</i>
                                                    </div>
                                                    <p>Flight Plan</p>
                                                </a>
                                            </div>
                                        </div>
                                        <div class="col-md-4">
                                            <div class="file-upload">
                                                <a href="`+ data.flight_insurance_url + `" class="file-link">
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
                                <div id="map" class="map" value="`+ data.latitude + `, ` + data.longitude + `"></div>
                            </div>
                            <div class="buttons is-end">
                                <a href="/np/dashboard/approve_perm/`+ data.uav_uid + `/approve" class="common-button is-bg">Approve</a>
                                <span  class="common-button is-border cancel-button" id="denyButton"
                                >Deny</span>
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
        plotMap(data)
    }

    function plotMap(data) {
        var map = L.map('map').setView([data.latitude, data.longitude], 8);
        // var map = L.map('map', {
        //     // layers: [base],
        //     center: new L.LatLng(lat, lon),
        //     zoom: 12,
        // });
        var mark = L.marker([data.latitude, data.longitude]).addTo(map);

        // console.log(flight_object)

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

        layerswitcher = L.control.layers(baseLayers, {}, { collapsed: true }).addTo(map);
    }

});

$('.leaflet-popup-content, .leaflet-popup-content-wrapper').css('width', '300px');


function openDenyModal(flight_id) {
    let denyElement = document.getElementById('denyButton')
    denyElement.addEventListener('click', () => {
        // console.log("show pop");
        let smallPopup = document.getElementById('open-modal-deny');
        smallPopup.classList.add('open');
        html1 = `
            <div class="popup-header">
                <h5>Reason for Denial</h5>
            </div>
            <input type="textarea" placeholder="Reason for denial" id="reasonInput"
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