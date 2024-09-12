import folium
import osmnx as ox
import networkx as nx
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Connect to the SQLite database
conn = sqlite3.connect('bus_data.db')
cursor = conn.cursor()
print('Connected to database')

# Part 1: Plotting Routes on the Map

routes = []  # List to store routes

# Fetch route IDs from the routes table (limit to 50 for testing)
cursor.execute('SELECT route_id FROM routes limit 100')
rows = cursor.fetchall()

# Extract stops for each route
for row in rows:
    cursor.execute(
        '''
        SELECT s.stop_lat, s.stop_lon
        FROM stops s
        INNER JOIN stop_times st ON s.stop_id = st.stop_id
        INNER JOIN trips t ON st.trip_id = t.trip_id
        INNER JOIN routes r ON t.route_id = r.route_id
        WHERE r.route_id = ?
        ORDER BY st.stop_sequence
        ''', (row[0],)
    )
    stops = cursor.fetchall()
    if len(stops) > 1:  # Only consider routes with more than one stop
        routes.append(stops)

print(f'Extracted {len(routes)} routes from the database')

# Initialize a Folium map centered on a central point (Delhi, India)
m = folium.Map(location=[28.7041, 77.1025], zoom_start=15)

# Fetch the road network graph from OpenStreetMap for the specified area
G = ox.graph_from_point((28.7041, 77.1025), dist=100000, network_type='drive')

def find_route(G, origin_point, destination_point):
    """
    Calculate the shortest path between two points using the road network graph.
    """
    try:
        # Find the nearest nodes to the origin and destination points
        orig_node = ox.distance.nearest_nodes(G, X=origin_point[1], Y=origin_point[0])
        dest_node = ox.distance.nearest_nodes(G, X=destination_point[1], Y=destination_point[0])

        # Calculate the shortest path between the nodes
        route = nx.shortest_path(G, orig_node, dest_node, weight='length')

        # Extract the coordinates for each node in the route
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        return route_coords
    except Exception as e:
        print(f"Error calculating route: {e}")
        return []

def generate_colors(n):
    """
    Generate n distinct colors using Matplotlib colormap.
    """
    cmap = plt.cm.get_cmap('tab20', n)  # Using 'tab20' colormap for up to 20 distinct colors
    return [mcolors.to_hex(cmap(i)) for i in range(n)]

# Generate colors for each route
num_routes = len(routes)
colors = generate_colors(num_routes)

# Add each route to the map with a different color
for i, route in enumerate(routes):
    if len(route) >= 2:  # Ensure there are at least two points to plot a route
        # Calculate the real-road route using OSMnx
        real_route = find_route(G, route[0], route[1])
        
        if real_route:  # Only add to map if a valid route is calculated
            # Add a polyline for the route on the map
            folium.PolyLine(
                locations=real_route,
                color=colors[i],
                weight=5,  # Line thickness
                opacity=0.8
            ).add_to(m)
            print(f'Route {i+1} added to map')
        else:
            print(f'Route {i+1} could not be plotted due to missing path data')

# Part 2: Plotting Stops on the Same Map

try:
    # Fetch all stop coordinates from the stops table
    cursor.execute('SELECT stop_lat, stop_lon FROM stops')
    stops = cursor.fetchall()
    print(f'Fetched {len(stops)} stops from the database')

    # Loop through each stop coordinate and add a marker to the map
    for x, y in stops:
        folium.Marker(
            [x, y], 
            icon=folium.Icon(color="blue"),
            tooltip=f"Stop: ({x:.4f}, {y:.4f})"  # Tooltip to display coordinates
        ).add_to(m)

    print('Markers for stops added to the map')

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

# Close the cursor and connection
finally:
    cursor.close()
    conn.close()
    print('Database connection closed')

# Save the combined map to an HTML file
m.save('combined_map.html')
print('Combined map saved to combined_map.html')
