import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('bus_data.db')
cursor = conn.cursor()

# Create indexes
try:
    # Indexes for the stops table
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_stop_id ON stops (stop_id);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_stop_lat_lon ON stops (stop_lat, stop_lon);')

    # Index for the routes table
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_route_id ON routes (route_id);')

    # Indexes for the trips table
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_trip_id ON trips (trip_id);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_route_id_on_trips ON trips (route_id);')

    # Indexes for the stop_times table
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_stop_id_on_stop_times ON stop_times (stop_id);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_trip_id_on_stop_times ON stop_times (trip_id);')

    # Commit changes
    conn.commit()
    print('Indexes created successfully.')

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
    print('Database connection closed.')
