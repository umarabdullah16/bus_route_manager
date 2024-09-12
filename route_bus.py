import folium
import osmnx as ox
import networkx as nx
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('bus_data.db')
cursor = conn.cursor()
print('Connected to database')
routes = []
cursor.execute('SELECT route_id FROM routes limit 50')
rows = cursor.fetchall()
for row in rows:

    cursor.execute(
        '''
        SELECT s.stop_lat, s.stop_lon
        FROM stops s
        INNER JOIN stop_times st ON s.stop_id = st.stop_id
        INNER JOIN trips t ON st.trip_id = t.trip_id
        INNER JOIN routes r ON t.route_id = r.route_id
        WHERE r.route_id = ?
        ''', (row[0],)  # Pass the route_id as a tuple
    )
    stops = cursor.fetchall()
    routes.append(stops)
print('Routes extracted from database')

m=folium.Map(location=[28.7041, 77.1025], zoom_start=15)
G = ox.graph_from_point((28.7041, 77.1025), dist=3000, network_type='drive')


def find_route(G, origin_point, destination_point):
    # Find the nearest nodes to the origin and destination points
    orig_node = ox.distance.nearest_nodes(G, X=origin_point[1], Y=origin_point[0])
    dest_node = ox.distance.nearest_nodes(G, X=destination_point[1], Y=destination_point[0])
    
    # Calculate the shortest path between the nodes
    route = nx.shortest_path(G, orig_node, dest_node, weight='length')
    
    # Extract the coordinates for each node in the route
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
    print('Route calculated')
    return route_coords

num_routes = len(routes)

def generate_colors(n):
    cmap = plt.cm.get_cmap('tab20', n)
    print("Colors")  # 'tab20' provides 20 distinct colors; can change based on needs
    return [cmap(i) for i in range(n)]

colors = generate_colors(num_routes)

for i, route in enumerate(routes):
    # Calculate the real-road route using OSMnx
    real_route = find_route(G, route[0], route[1])
    
    # Add a polyline for the route on the map
    folium.PolyLine(
        locations=real_route,
        color=colors[i],
        weight=5,  # Line thickness
        opacity=0.8
    ).add_to(m)
    print('Route added to map')

# Save the map to an HTML file

m.save('routes_map.html')
print('Map saved to routes_map.html')