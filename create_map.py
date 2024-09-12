import folium
import pandas as pd
import sqlite3

conn = sqlite3.connect('bus_data.db')
cursor = conn.cursor()

cursor.execute('SELECT stop_lat, stop_lon FROM stops')
rows = cursor.fetchall()

m = folium.Map(location=[28.7041, 77.1025], zoom_start=15)

for x,y in rows:
    folium.Marker([x,y], icon=folium.Icon(color="blue")).add_to(m)

m.save('bus_map_zoom.html')