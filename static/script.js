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
    console.log(data);
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
});