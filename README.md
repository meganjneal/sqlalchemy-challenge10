# sqlalchemy-challenge10
   
 ## Overview  
climate data from Hawaii using Python, SQLAlchemy, and Flask. I analyzed precipitation data, station data, and temperature observations.  
   
 ## Folder Structure  
 - **SurfsUp/**  
   - **Resources/**: Contains data files (`hawaii.sqlite`, `hawaii_measurements.csv`, `hawaii_stations.csv`)  
   - **climate_starter.ipynb**: Jupyter Notebook for climate analysis  
   - **app.py**: Flask app for the API  
   
 ## API Routes  
 - `/` - List available routes  
 - `/api/v1.0/precipitation` - Precipitation data for the last 12 months  
 - `/api/v1.0/stations` - List of weather stations  
 - `/api/v1.0/tobs` - Temperature observations from the most active station  
 - `/api/v1.0/<start>` - Temperature stats from a start date  
 - `/api/v1.0/<start>/<end>` - Temperature stats for a date range  
   
 ## Tools  
 - Python, SQLAlchemy, Flask, Pandas, Matplotlib  
