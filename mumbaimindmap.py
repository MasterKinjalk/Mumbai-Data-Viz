import folium
import json
from folium import plugins
from folium.plugins import PolyLineTextPath
from shapely.geometry import shape, Point

# Load GeoJSON for Mumbai's boundary
with open('boundary.geojson') as f:
    mumbai_boundary = json.load(f)

# # Load GeoJSON for slum clusters
with open('Mumbai/slumClusters.geojson') as f:
    slum_clusters = json.load(f)

# Initialize the map with CartoDB.VoyagerNoLabels tiles
mumbai_map = folium.Map(location=[19.0760, 72.8777], zoom_start=13, tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png', attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>', subdomains='abcd')

# Add Mumbai boundary with dashed lines
folium.GeoJson(
    mumbai_boundary,
    name="Mumbai Boundary",
    style_function=lambda x: {'color': 'black', 'weight': 2, 'dashArray': '10, 10'}
).add_to(mumbai_map)


# Add slum clusters to the map
folium.GeoJson(
    slum_clusters,
    name="Slum Clusters",
    style_function=lambda x: {'fillColor': 'orange', 'color': 'orange', 'weight': 1.5, 'fillOpacity': 0.5}
).add_to(mumbai_map)

data = json.load(open('mumbai_primary_roads.geojson', 'r'))
filtered_features = [feature for feature in data['features'] if feature['properties']['name']]

# Iterate over the GeoJSON features and add them as PolyLines
for feature in filtered_features:
    if 'name' in feature['properties']:  # Ensure the feature has a name
        name = feature['properties']['name']
        if isinstance(name, list):
            name = ' '.join(name)  # Join names with a comma if there are multiple
        # Extract the coordinates for the PolyLine
        line = feature['geometry']['coordinates']
        # GeoJSON uses [longitude, latitude] but Folium expects [latitude, longitude]
        line = [(lat, lon) for lon, lat in line]
        # Create and add the PolyLine to the map
        polyline = folium.PolyLine(locations=line, color='blue', weight=3).add_to(mumbai_map)
        # Add the road name on the PolyLine
        # PolyLineTextPath(
        #     polyline,
        #     '   ' + name + '   ',  # Spaces help in offsetting the text for better visibility
        #     repeat=True,
        #     offset=8,
        #     attributes={'font-weight': 'bold', 'font-size': '12'}
        # ).add_to(mumbai_map)


# Define locations with detailed descriptions
locations_detailed = {
    "Colaba": {"coords": (18.915091, 72.825969), "popup": "<b>Colaba</b>: Known for the Gateway of India, Taj Mahal Palace Hotel, and bustling Colaba Causeway market."},
    "Fort Area": {"coords": (18.9336, 72.8377), "popup": "<b>Fort Area</b>: Houses the Bombay High Court, Mumbai University, and the CST, a UNESCO World Heritage Site."},
    "Marine Drive": {"coords": (18.9440, 72.8232), "popup": "A 3.6 km long boulevard, also known as the Queen's Necklace."},
    "Dadar": {"coords": (19.0193, 72.8424), "popup": "<b>Dadar</b>: A hub for local markets and the Shivaji Park residential zone."},
    "Worli": {"coords": (19.0116, 72.8181), "popup": "<b>Worli</b>: Known for the Sea Link bridge and the Worli Fort."},
    "Parel/Lower Parel": {"coords": (19.0059, 72.8295), "popup": "Once home to Mumbai's mill industry, now a major area for high-rises and corporate offices."},
    "Bandra": {"coords": (19.0544, 72.8408), "popup": "<b>Bandra</b>: The 'Queen of the Suburbs,' famous for Bandstand promenade and Bollywood homes."},
    "Juhu": {"coords": (19.107021, 72.827528), "popup": "<b>Juhu</b>: Known for its beach, luxury hotels, and Bollywood star residences."},
    "Andheri": {"coords": (19.1197, 72.8464), "popup": "<b>Andheri</b>: A major commercial hub, home to the Bollywood film industry and the airport."},
    "Powai": {"coords": (19.1190, 72.9090), "popup": "<b>Powai</b>: Known for the Powai Lake and the Indian Institute of Technology Bombay."},
    "Borivali": {"coords": (19.2294, 72.8575), "popup": "<b>Borivali</b>: Known for the Sanjay Gandhi National Park, a natural respite from the city's hustle."},

    "Mumbai Harbour": {"coords": (18.9667, 72.8353), "popup": "East of the city, featuring Elephanta Island and serving as a significant port."}
}

with open('tourist_places.json') as f:
    tourist_places= json.load(f)

# Add markers for detailed descriptions within the cluster
for data in tourist_places:
    folium.Marker(
        location=(data['latitude'],data['longitude']),
        popup=f"{data['name']}: {data['description']}",
        icon=folium.Icon(color="blue", prefix='fa', icon="camera")
    ).add_to(mumbai_map)

# Add markers for detailed descriptions within the cluster
for place, details in locations_detailed.items():
    folium.Marker(
        location=details["coords"],
        popup=f"{place}: {details['popup']}",
        icon=folium.Icon(color="green", prefix='fa', icon="map-marker")
    ).add_to(mumbai_map)

# Initialize MarkerCluster for prominent places
marker_cluster = plugins.MarkerCluster().add_to(mumbai_map)






# Process each feature in the GeoJSON file
for feature in mumbai_boundary['features']:
    # Ensure the geometry type is Polygon (or MultiPolygon if those exist)

    # Calculate the centroid of the polygon
    polygon = shape(feature['geometry'])
    centroid = polygon.centroid
    
    # Extract place name or any other identifier you have in your GeoJSON properties
    place_name = feature['properties'].get('name', 'No Name')  # Adjust 'name' key as per your GeoJSON
    
    # Add a marker to the map at the centroid location
    folium.Marker(
        location=[centroid.y, centroid.x],  # Note: Shapely's centroid attributes are y (latitude), x (longitude)
        popup=f"{place_name}",
        icon=folium.Icon(color="purple", prefix='fa', icon="map-marker")
    ).add_to(marker_cluster)


# Define your HTML content for the legend
legend_html = """
<div style="position: fixed; 
     bottom: 40px; left: 40px; width: 500px; height: 210px; 
     background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
     border-radius: 6px;
     padding: 10px;
     ">
     <b>Legend:</b><br>
     <i style="background: black; width: 12px; height: 12px; display: inline-block;"></i> Black dashed lines: Mumbai boundary of Districts thus <b>Edges</b> <br>
     <i style="background: black; width: 12px; height: 12px; display: inline-block;"></i> Black semi-transparent areas: Mumbai <b>Districts</b> <br>
     <i style="background: blue; width: 12px; height: 12px; display: inline-block;"></i> Blue solid lines: Primary roads(<b>Path</b>)<br>
     <i style="background: orange; opacity: 0.7; width: 12px; height: 12px; display: inline-block;"></i> Orange semi-transparent areas: Slum clusters(Another form of <b>District</b>)<br>
     <i class="fa fa-map-marker" aria-hidden="true" style="color: purple;"></i> Purple markers: Centroids of Mumbai's administrative areas<br>
     <i class="fa fa-map-marker" aria-hidden="true" style="color: green;"></i> Green markers: Prominent locations and their historical info on cick,also<b>nodes</b><br>
     <i class="fa fa-camera" aria-hidden="true" style="color: blue;"></i> Blue markers: Tourist places/<b>Landmarks</b> and their significane on click,also<b>nodes</b><br>
</div>
"""

# Create a Folium Element for the custom legend
legend_element = folium.Element(legend_html)

# Add the legend to the map
marker_cluster.get_root().html.add_child(legend_element)



# Save the map as an HTML file
marker_cluster.save('mumbai_map_with_slums.html')
