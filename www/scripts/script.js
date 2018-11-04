var map, geojson, layer_a, polygon;
var estate = new Array();

function getColor(d) {
    return d == "Nordeste" ? '#800026' : 
        d == "Sudeste" ? '#BD0026' : 
        d == "Norte" ? '#E31A1C' : 
        d == "Sul" ? '#FC4E2A' : 
        //d > 10 ? '#FD8D3C' : 
        //d > 05 ? '#FEB24C' : 
        //d > 0 ? '#FED976' : 
        '#FFEDA0'; 
}

function style(feature) { 
    return { 
        fillColor: getColor(feature.properties.REGIAO), 
        weight: 2, 
        opacity: 1, 
        color: 'white', 
        dashArray: '3', 
        fillOpacity: 0.7 
    }; 
}

function popup(feature, layer) { 
    layer_a = layer;
    if (feature.properties && feature.properties.NOME_UF) 
    { 
        layer.bindPopup(feature.properties.NOME_UF);
    } 
}

function fill_estates_map(data) {
    /*geojson = L.geoJson(estates, { 
        style: style, onEachFeature: popup 
    }).addTo(map);
    console.log(geojson);*/
    data.features.forEach(element => {
        //uf = element.properties.UF_05;
        coordinates = element.geometry.coordinates;
        console.log(L.GeoJSON.coordsToLatLng(coordinates));
        /*estate[uf] =*/ L.polygon(coordinates).addTo(map);
        console.log(element);
    });
}

$(document).ready(function() {
    // Cria o mapa
    map = L.map('map').setView([ -15.7801, -47.9292], 4);

    L.esri.basemapLayer('Topographic').addTo(map);

    //L.control.scale().addTo(map);
    L.marker([-15.7801, -47.9292],{draggable: false}).addTo(map).bindPopup("Brasília");

    // Pinta os estados no mapa
    $.getJSON("scripts/estates.json").done(function(data) {
        fill_estates_map(data);
    });
});