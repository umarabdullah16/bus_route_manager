import pandas as pd
import sqlite3

agency = pd.read_csv('GTFS/agency.txt')
calendar = pd.read_csv('GTFS/calendar.txt') 
fare_attributes = pd.read_csv('GTFS/fare_attributes.txt')
fare_rules = pd.read_csv('GTFS/fare_rules.txt')
routes = pd.read_csv('GTFS/routes.txt')
stop_times = pd.read_csv('GTFS/stop_times.txt')
stops = pd.read_csv('GTFS/stops.txt')
trips = pd.read_csv('GTFS/trips.txt')

conn = sqlite3.connect('bus_data.db')
cursor = conn.cursor()

agency.to_sql('agency', conn)
calendar.to_sql('calendar', conn)
fare_rules.to_sql('fare_rules', conn)
routes.to_sql('routes', conn)
fare_attributes.to_sql('fare_attributes', conn)
stop_times.to_sql('stop_times', conn)
stops.to_sql('stops', conn)
trips.to_sql('trips', conn)

cursor.execute('SELECT * FROM stops limit 5')
rows=cursor.fetchall()

for row in rows:
    print(row)

conn.commit()
conn.close()

