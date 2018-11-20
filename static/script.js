var map;
var countries = new Array();
var estates = new Array();

function getColor(d) {
    return d > 30 ? '#f1433a' : 
        d > 25 ? '#fb7f1f' : 
        d > 20 ? '#e6de31' : 
        d > 15 ? '#9ceb38' : 
        d > 10 ? '#00d58e' : 
        d > 5 ? '#03a2fa' : 
        '#2837ff'; 
}

function getRadius(d) {
    return d > 30 ? 9 : 
        d > 25 ? 8 : 
        d > 20 ? 7.5 : 
        d > 15 ? 7 : 
        d > 10 ? 6.5 : 
        d > 5 ? 6 : 
        5; 
}

function clearAllCircleMarker() {
    countries.forEach(element => {
        element.removeFrom(map);
    })
    estates.forEach(element => {
        element.removeFrom(map);
    })
}

function style(d) { 
    return { 
        fillColor: getColor(d), 
        weight: 0, 
        fillOpacity: .7
    }; 
}

function fill_countries_map(data) {
    data.countries.forEach(element => {
        countrie = element.countrie;
        coordinates = element.coordinates;
        countries[countrie] = L.circleMarker(coordinates);
    });
}

function fill_estates_map(data) {
    data.estates.forEach(element => {
        estate = element.estate;
        coordinates = element.coordinates;
        estates[estate] = L.circleMarker(coordinates);
    });
}

function show_search(id) {
    id = "#".concat(id);
    if ($(id).is(":visible")) { $(id).hide(); }
    else { $(id).show(); }
}

function response_api(data) {
    console.log(data);
    console.log('a');
}

function request_api() {
    let disease = $("#select-disease option").filter(":selected").val();
    let location = $("#item-location input[type='radio']:checked").val();
    let date_begin = $("#date-begin").val();
    let date_end = $("#date-end").val();
    
    let url = 'api?disease=' + disease + '&location=' + location + '&date_begin=' + date_begin + '&date_end=' + date_end;
    console.log(url);
    $.getJSON('url').done(response_api);
}

$(document).ready(function() {
    map = L.map('map').setView([0, 0], 2);

    L.esri.basemapLayer('Gray').addTo(map);

    $.getJSON("static/countrie.json").done(function(data) {
        fill_countries_map(data);
    });

    $.getJSON("static/estates.json").done(function(data) {
        fill_estates_map(data);
    });

    var date = new Date();
    var date_now = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
    $("#date-begin").val(date_now);
    $("#date-end").val(date_now);

    // Make the DIV element draggable:
    dragElement(document.getElementById("search"));

    function dragElement(elmnt) {
        var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        if (document.getElementById(elmnt.id + "-title")) {
            // if present, the header is where you move the DIV from:
            document.getElementById(elmnt.id + "-title").onmousedown = dragMouseDown;
        } else {
            // otherwise, move the DIV from anywhere inside the DIV: 
            elmnt.onmousedown = dragMouseDown;
        }

        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            // get the mouse cursor position at startup:
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            // call a function whenever the cursor moves:
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            // calculate the new cursor position:
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            // set the element's new position:
            if ((elmnt.offsetTop - pos2) >= 0) {
                if ((elmnt.offsetTop - pos2 + $("#search").height()) <= $(document).height()) {
                    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
                }
                else {
                    elmnt.style.top = ($(document).height() - $("#search").height()) + "px";
                }
            }
            else {
                elmnt.style.top = "0px";
            }

            if ((elmnt.offsetLeft - pos1) >= 0) {
                if ((elmnt.offsetLeft - pos1 + $("#search").width()) <= $(document).width()) {
                    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
                }
                else {
                    elmnt.style.left = ($(document).width() - $("#search").width()) + "px";
                }
            }
            else {
                elmnt.style.left = "0px";
            }
        }

        function closeDragElement() {
            // stop moving when mouse button is released:
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }
});

// function fill_countries_map(data) {
//     data.countries.forEach(element => {
//         countrie = element.countrie;
//         coordinates = element.coordinates;
//         countries[countrie] = L.circleMarker(coordinates)
//                                 .setRadius(getRadius(34))
//                                 .setStyle(style(35))
//                                 .bindPopup(countrie)
//                                 .addTo(map);
//     });
// }