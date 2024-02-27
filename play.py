# import osmnx as ox
# import networkx as nx
# import folium

# # Configure OSMnx for efficient caching and logging
# ox.config(use_cache=True, log_console=True)

# # Define the location and desired road type
# location = "Mumbai, India"
# road_type = '["highway"~"primary"]'  # Corrected syntax, double quotes for string
# G = ox.graph_from_place(location, network_type='drive', custom_filter=road_type)

# # --- Folium map creation ---
# min_latitude, max_latitude = float('inf'), float('-inf')
# min_longitude, max_longitude = float('inf'), float('-inf')

# for node, data in G.nodes(data=True):
#     latitude, longitude = data['y'], data['x']
#     min_latitude = min(min_latitude, latitude)
#     max_latitude = max(max_latitude, latitude)
#     min_longitude = min(min_longitude, longitude)
#     max_longitude = max(max_longitude, longitude)

# north, south, east, west = max_latitude, min_latitude, max_longitude, min_longitude
# center_latitude = (north + south) / 2
# center_longitude = (east + west) / 2

# mumbai_map=folium.Map(location=[19.0760, 72.8777], zoom_start=10, 
#           tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png', 
#           attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>', 
#           subdomains='abcd')

# # Convert edges to GeoJSON, ensuring correct coordinate order for Folium
# edges_geojson = ox.graph_to_gdfs(G, nodes=False, edges=True).to_json()
# folium.GeoJson(edges_geojson, name="Mumbai Primary Roads", style_function=lambda feature: {
#     'color': 'blue',  # Customize road color
#     'weight': 3  # Adjust road thickness
# }).add_to(mumbai_map)

# # Save the map to an HTML file
# mumbai_map.save('mumbai_primary_roads.html')


import osmnx as ox
import geopandas as gpd

# Configure OSMnx for efficient caching and logging
ox.config(use_cache=True, log_console=True)

# Define the location and desired road type
location = "Mumbai, India"
road_type = '["highway"~"primary"]'  # Use the correct syntax for the custom filter

# Fetch the graph for the specified location and road type
G = ox.graph_from_place(location, network_type='drive', custom_filter=road_type)

# Convert the graph to GeoDataFrames
nodes, edges = ox.graph_to_gdfs(G)

# Since we're interested in the roads' names and their geometries, let's focus on the 'edges' DataFrame
# Some roads might not have a name (NaN values), we can handle this as needed, e.g., by filling NaN with a placeholder
edges['name'] = edges['name']

# Save the edges GeoDataFrame as GeoJSON
geojson_data = edges.to_json()

# You can directly save this GeoJSON data to a file
with open('mumbai_primary_roads.geojson', 'w') as f:
    f.write(geojson_data)

print("GeoJSON data saved as 'mumbai_primary_roads.geojson'.")
