var map;
var countries = new Array();

/*function getColor(d) {
    return d == "Nordeste" ? '#800026' : 
        d == "Sudeste" ? '#BD0026' : 
        d == "Norte" ? '#E31A1C' : 
        d == "Sul" ? '#FC4E2A' : 
        d > 10 ? '#FD8D3C' : 
        d > 05 ? '#FEB24C' : 
        d > 0 ? '#FED976' : 
        '#FFEDA0'; 
}*/

function style(color) { 
    return { 
        fillColor: color, 
        weight: 0, 
        fillOpacity: .7
    }; 
}

function fill_estates_map(data) {
    data.countries.forEach(element => {
        countrie = element.countrie;
        coordinates = element.coordinates;
        countries[countrie] = L.circleMarker(coordinates)
                                .setRadius(10)
                                .setStyle(style("#000"))
                                .bindPopup(countrie)
                                .addTo(map);
    });
}

function show_search(id) {
    id = "#".concat(id);
    if ($(id).is(":visible")) { $(id).hide(); }
    else { $(id).show(); }
}

$(document).ready(function() {
    map = L.map('map').setView([0, 0], 2);

    L.esri.basemapLayer('Gray').addTo(map);

    $.getJSON("static/countrie.json").done(function(data) {
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
