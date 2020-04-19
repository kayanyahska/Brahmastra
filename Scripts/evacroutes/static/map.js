let map, heatmap, clusterLayer, tooltipTemplate;
function GetMap() {
    let content = document.getElementById('content');
    let victims = content.querySelectorAll('.victim');
    map = new Microsoft.Maps.Map('#myMap', {
        credentials: 'Aqxws6GyR0KaQH-uo9w92nqNeePHAzsbkVDbrpiayIiAwfTbXcML-wj1XLEBPQcQ',
        center: new Microsoft.Maps.Location(18.0056, 79.5572),
        zoom: 11,
        mapTypeId: Microsoft.Maps.MapTypeId.aerial,
    });
    tooltipTemplate = `<div id="tooltip"><p><b>{title}</b></p><p>{time}</p></div>`;
    //Create an infobox to use as a tooltip when hovering.
    tooltip = new Microsoft.Maps.Infobox(map.getCenter(), {
        visible: false,
        showPointer: false,
        showCloseButton: false,
        offset: new Microsoft.Maps.Point(-75, 10)
    });

    tooltip.setMap(map);
    
    //Create an infobox for displaying detailed information.
    infobox = new Microsoft.Maps.Infobox(map.getCenter(), {
        visible: false
    });

    infobox.setMap(map);
    let pins = [],locs=[];
    victims.forEach(victim => {
        let phoneNumber = victim.querySelector('.phone_number').textContent;
        let lat = victim.querySelector('.lat').textContent;
        let lon = victim.querySelector('.lon').textContent;
        let time = victim.querySelector('.time').textContent+" ago";
        let location = new Microsoft.Maps.Location(lat,lon);
        locs.push(location);
        //Create custom Pushpin

        var pin = new Microsoft.Maps.Pushpin(location,{
            color: 'red'
        });

        //Store some metadata with the pushpin.
        pin.metadata = {
            title: phoneNumber,
            description: time
        };
        pins.push(pin);
        //Add a click event handler to the pushpin.
        Microsoft.Maps.Events.addHandler(pin, 'click', pushpinClicked);
        Microsoft.Maps.Events.addHandler(pin, 'mouseover', pushpinHovered);
        Microsoft.Maps.Events.addHandler(pin, 'mouseout', closeTooltip);

        //Add pushpin to the map.
        // map.entities.push(pin);
    })
    Microsoft.Maps.loadModule("Microsoft.Maps.Clustering", function () {
        //Create a ClusterLayer with options and add it to the map.
        clusterLayer = new Microsoft.Maps.ClusterLayer(pins, {
            clusteredPinCallback: customizeClusteredPin
        });
        map.layers.insert(clusterLayer);
    });
    Microsoft.Maps.loadModule('Microsoft.Maps.HeatMap', function () {
        heatmap = new Microsoft.Maps.HeatMapLayer(locs);
        map.layers.insert(heatmap);
        map.layers[1].setVisible(false);
    });
}
function pushpinClicked(e) {
    //Make sure the infobox has metadata to display.
    if (e.target.metadata) {
        //Set the infobox options with the metadata of the pushpin.
        infobox.setOptions({
            location: e.target.getLocation(),
            title: e.target.metadata.title,
            description: e.target.metadata.description,
            visible: true
        });
    }
}
function pushpinHovered(e) {
    //Hide the infobox
    infobox.setOptions({ visible: false });

    //Make sure the infobox has metadata to display.
    if (e.target.metadata) {
        //Set the infobox options with the metadata of the pushpin.
        tooltip.setOptions({
            location: e.target.getLocation(),
            htmlContent: tooltipTemplate.replace('{title}', e.target.metadata.title).replace('{time}',e.target.metadata.description),
            visible: true
        });
    }
}

function closeTooltip() {
    //Close the tooltip.
    tooltip.setOptions({
        visible: false
    });
}

function customizeClusteredPin(cluster) {
    //Add click event to clustered pushpin
    cluster.setOptions({
        color: 'red'
    });
    Microsoft.Maps.Events.addHandler(cluster, 'click', clusterClicked);
}

function clusterClicked(e) {
 if (e.target.containedPushpins) {
     var locs = [];
     for (var i = 0, len = e.target.containedPushpins.length; i < len; i++) {
         //Get the location of each pushpin.
         locs.push(e.target.containedPushpins[i].getLocation());
     }

     //Create a bounding box for the pushpins.
     var bounds = Microsoft.Maps.LocationRect.fromLocations(locs);

     //Zoom into the bounding box of the cluster. 
     //Add a padding to compensate for the pixel area of the pushpins.
     map.setView({ bounds: bounds, padding: 100 });
 }
}
let hmbut=document.getElementById('heatmap');
hmbut.addEventListener("click",(e) => {
    if(map.layers[0].getVisible()){
        map.layers[0].setVisible(false);
        map.layers[1].setVisible(true);
    }
    else{
        map.layers[0].setVisible(true);
        map.layers[1].setVisible(false);
    }
});