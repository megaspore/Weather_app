
mapboxgl.accessToken = 'pk.eyJ1IjoiYmVuZ2llaHVudCIsImEiOiJjbDloNWh2ZncwODVhM3VyeXU1bHdwOTVkIn0.ZmecDzfsknlIZEiUd0ZOiw';
var mq = window.matchMedia( "(min-width: 420px)" );
    const mapcol = document.getElementsByClassName("menu_col")[0];
    if (mq.matches){
        
        var lat = -95.04;
        var lng = 38.907;
       
        mapcol.style.width="700px";
    } else {
        
        var lat = -95.04;
        var lng = 24.907;    
        document.querySelector('#map').style.height="360px";
        
        mapcol.style.width="24rem";
    };


const map = new mapboxgl.Map({


    
    container: 'map',
    // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
    // blank style: {version: 8,sources: {},layers: []},
    style: {version: 8,sources: {},layers: []},
    //style: 'mapbox://styles/bengiehunt/cl9h6g3me000s14qy62c9nwdz',
    center: [lat, lng],
    zoom: 3
});


    if (mq.matches){
        
        
        map.setZoom(3); //set map zoom level for desktop size
       
    } else {
        
            
        map.setZoom(2); //set map zoom level for mobile size
       
    };
    


// disable map zoom when using scroll
map.scrollZoom.disable();
// disable dragpan
map.dragPan.disable();
map.dragRotate.disable();
map.keyboard.disable();
map.touchZoomRotate.disable();
map.doubleClickZoom.disable();
map.boxZoom.disable();
var clickedStateId = null;

const mypoly = 'http://127.0.0.1:8000/routes/polys/?format=json'
const mypoint = 'http://127.0.0.1:8000/routes/points/?format=json'
var test = JSON.stringify(mypoly);
console.log(test)
//const mypoly = 'http://127.0.0.1:8000/geofile'
//const mypoint = 'http://127.0.0.1:8000/geofile'     
map.on('load', () => {



    document.querySelector('#hexlegend').style.display = 'none';
    
    map.addSource('places', {
        'type': 'geojson',
        'data': mypoint,
        'generateId': true 
    
    });

    map.addSource('hexes', {
        'type': 'geojson',
        'data': mypoly
    });    
    
    //7 day rmse highs layer
    map.addLayer({
        'id': '7day rmse highs',
        'type': 'fill',
        'source': 'hexes',
        'layout': {
            // Make the layer visible by default.
            'visibility': 'visible'
            },
        'paint': {
            'fill-color': 
                {
                property: '_7_days_rmse_temp_max', 
                default: "grey",             
                stops: [[0, 'black'], [1.0, '#1F214D'], [2, '#50366F'], [4, '#BF3475'], [5, '#EE6C45'], [6, '#FFCE61'], [7, '#FFE58A'], [9, '#f9e9da'], [10, 'white']]               
                },
                'fill-opacity': 0.8,
                
        }
    }); 

    // 7 dayrmse legend generation
    const seven_day_rmse_colors = [
        'grey',
        '#1F214D',
        '#50366F',
        '#FD8D3C',
        '#BF3475',
        '#E31A1C',
        '#FFCE61',
        '#FFE58A',
        '#f9e9da',
        'white'

        ];
    const seven_day_rmse_layers = [
        'none',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7-8',
        '9',
        '10'
      ];
        const rmseleg= document.getElementById('legend');
        seven_day_rmse_layers.forEach((layer, i) => {
            var color = seven_day_rmse_colors[i];
            var item = document.createElement('div');
            var key = document.createElement('span');
            key.className = 'legend-key';
            key.style.backgroundColor = color;
          
            var value = document.createElement('span');
            value.innerHTML = `${layer}`;
            item.appendChild(key);
            item.appendChild(value);
            rmseleg.appendChild(item);
          });
    

    // Add a layer showing the  active hexes 
    map.addLayer({
        'id': 'Hexes',
        'type': 'fill',
        'source': 'hexes',
        'layout': {
            // Make the layer visible by default.
            'visibility': 'none'
            },
        'paint': {
            'fill-color': {
                property: 'active',
                //stops: [[false, 'grey'], [true, '#FF1493']]
                stops: [[0, 'grey'], [1, '#FF1493']]
                },
            'fill-opacity': 0.8
        }
    });

    //active hex legend
    const hex_colors = [
        '#FF1493',
        'grey'

        ];
    const hex_layers = [
        'Active',
        'Not active',
        
      ];
        const hexleg= document.getElementById('hexlegend');
        hex_layers.forEach((layer, i) => {
            var color =  hex_colors[i];
            var item = document.createElement('div');
            var key = document.createElement('span');
            key.className = 'legend-key';
            key.style.backgroundColor = color;
          
            var value = document.createElement('span');
            value.innerHTML = `${layer}`;
            item.appendChild(key);
            item.appendChild(value);
             hexleg.appendChild(item);
          });

    map.addLayer({
        'id': 'outline',
        'type': 'line',
        'source': 'hexes',
        'layout': {},
        'paint': {
        'line-color': '#000',
        'line-width': 3
        }
    });

    //places layer where data is accessed through by clicking
    map.addLayer({
        'id': 'places',
        
        'type': 'circle',
        'source': 'places',
        'paint': {
        'circle-color': "white",
        'circle-radius': 6, 
        'circle-opacity':[
            'case',
            ['boolean', ['feature-state', 'click'], false],
            0.5,
            0
            ]
        }
    });     
});

 // After the last frame rendered before the map enters an "idle" state.
 map.on('idle', () => {
    
    // If these two layers were not added to the map, abort
    if (!map.getLayer('Hexes') || !map.getLayer('7day rmse highs')) {
        return;
    }
     
    // Enumerate ids of the layers.
    const toggleableLayerIds = ['Hexes', '7day rmse highs'];
     
    // Set up the corresponding toggle button for each layer.
    for (const id of toggleableLayerIds) {
    // Skip layers that already have a button set up.
        if (document.getElementById(id)) {
            continue;
        }
     
        // Create a link.
        const link = document.createElement('button');
        link.id = id;
        link.href = '#';
        link.textContent = id;
        link.className = 'btn menu_btn btn-secondary ';
     
        // Show and hide all other layers when the toggle is clicked.
        link.onclick = function(e) {
            var clickedLayer = this.textContent;
            e.preventDefault();
            e.stopPropagation();
            
            for (var j = 0; j < toggleableLayerIds.length; j++) {
              if (clickedLayer === toggleableLayerIds[j]) {
                menu.children[j].className = 'menu_btn btn btn-info';
                map.setLayoutProperty(toggleableLayerIds[j], 'visibility', 'visible');
                document.querySelector('#legend').style.display = 'block';
                document.querySelector('#hexlegend').style.display = 'none';
              }
              else {
                menu.children[j].className = 'menu_btn btn btn-secondary';
                map.setLayoutProperty(toggleableLayerIds[j], 'visibility', 'none');  
                document.querySelector('#legend').style.display = 'none';
                document.querySelector('#hexlegend').style.display = 'block';
                }
            }
          };
     
        const menu = document.getElementById('menu');
        menu.appendChild(link);
        

    }
});   

    // Create a popup, but don't add it to the map yet.
    const popup = new mapboxgl.Popup({
        closeButton: false,
        className: 'popup',
        closeOnClick: false
    });

    const table = document.getElementById('table');
    const station = document.getElementById('station');
    const forcast_accuracy = document.getElementById('forcast_accuracy');

    map.on('mouseenter', 'places', (e) => {
        map.getCanvas().style.cursor = 'pointer';

        const coordinates = e.features[0].geometry.coordinates.slice();
        const location = e.features[0].properties.location.split(",");
        popup.setLngLat(coordinates).setHTML(` <img class="pinimg" src=https://cdn.icon-icons.com/icons2/2460/PNG/512/location_pin_place_map_address_placeholder_icon_149099.png alt="">
                                                ${(location[0])}${(location[1])}`).addTo(map);

        map.on('click', 'places', (e) => {
            // Copy coordinates array.
                        
            const accuracy = Math.floor((((e.features[0].properties.temp_max_observation 
                + e.features[0].properties.temp_min_observation) 
                - (Math.abs(e.features[0].properties.bias_temp_max) 
                + Math.abs(e.features[0].properties.bias_temp_min)))/(e.features[0].properties.temp_max_observation 
                    + e.features[0].properties.temp_min_observation)) * 100);
            const maxtempfcast = parseFloat(e.features[0].properties.temp_max_forecast);
            const mintempfcast = (e.features[0].properties.temp_min_forecast);
            const maxtempobsrv = parseFloat(e.features[0].properties.temp_max_observation);
            const mintempobsrv = parseFloat(e.features[0].properties.temp_min_observation);
            const dayminacc = Math.floor(mintempfcast - mintempobsrv)
            const daymaxacc = Math.floor(maxtempfcast - maxtempobsrv)


            // Populate the popup and set its coordinates
            // based on the feature found.
                    
            
            
            station.innerHTML = (`${location[1]}, ${location[2]}, ${location[3]}, ${location[4]}`);                                                                      
            forcast_accuracy.innerHTML = (`${accuracy}%`);

            table.innerHTML = (`<table class="table table-borderless">
            <thead>
              <tr>
                <th  scope="col"></th>
                <th class="light_purple" scope="col">Forcast</th>
                <th scope="col">Weather</th>
                <th class="light_blue" scope="col">Accuracy</th>
              </tr>
              <tbody>
              <tr>
                <th scope="row">High Temp.</th>
                <td class="light_purple">${maxtempfcast.toFixed(2)}&deg</td>
                <td>${maxtempobsrv.toFixed(2)}&deg</td>
                <td class="light_blue">${daymaxacc.toFixed(2)}&deg</td>
              </tr>
              <tr>
                <th scope="row">Low Temp.</th>
                <td class="light_purple">${mintempfcast.toFixed(2)}&deg</td>
                <td>${mintempobsrv.toFixed(2)}&deg</td>
                <td class="light_blue">${dayminacc.toFixed(2)}&deg</td>
              </tr>
              
            </tbody>
          </table>
            </thead>
          `)
        if (e.features.length > 0) {
            if (clickedStateId) {
                map.setFeatureState(
                    { source: 'places', id: clickedStateId },
                    { click: false }
                );
            }
            clickedStateId = e.features[0].id;
            map.setFeatureState(
                { source: 'places', id: clickedStateId },
                { click: true }
            );
        }
        })      
    });
    
    map.on('mouseleave', 'places', () => {
        map.getCanvas().style.cursor = '';
        popup.remove();
        
    });
    
