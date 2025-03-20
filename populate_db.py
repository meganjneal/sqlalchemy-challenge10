import os  
import pandas as pd  
import sqlite3  
  
# Get current directory and data paths - now pointing to Resource folder  
current_dir = os.path.dirname(os.path.abspath(__file__))  
resource_dir = os.path.join(current_dir, 'Resources')  
measurements_path = os.path.join(resource_dir, 'hawaii_measurements.csv')  
stations_path = os.path.join(resource_dir, 'hawaii_stations.csv')  
  
# Read the CSV files  
print("Reading CSV files...")  
measurements_df = pd.read_csv(measurements_path)  
stations_df = pd.read_csv(stations_path)  
  
# Create connection to SQLite database  
print("Creating database connection...")  
db_path = os.path.join(current_dir, 'hawaii.sqlite')  
  
# Remove the database if it exists  
if os.path.exists(db_path):  
    os.remove(db_path)  
    print("Removed existing database")  
  
conn = sqlite3.connect(db_path)  
  
# Create the tables with explicit primary keys  
print("Creating tables...")  
conn.execute('''  
CREATE TABLE IF NOT EXISTS measurement (  
    station TEXT,  
    date TEXT,  
    prcp REAL,  
    tobs INTEGER,  
    PRIMARY KEY (station, date)  
)  
''')  
  
conn.execute('''  
CREATE TABLE IF NOT EXISTS station (  
    station TEXT PRIMARY KEY,  
    name TEXT,  
    latitude REAL,  
    longitude REAL,  
    elevation REAL  
)  
''')  
  
# Insert the data using 'append' so we don't replace the tables  
print("Writing measurement table...")  
measurements_df.to_sql('measurement', conn, if_exists='append', index=False)  
  
print("Writing station table...")  
stations_df.to_sql('station', conn, if_exists='append', index=False)  
  
conn.close()  
print("Database has been populated successfully.")  