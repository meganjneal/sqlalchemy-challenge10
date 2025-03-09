 # Import dependencies - start with what we need for basic Flask setup  
 import numpy as np  
 import pandas as pd  
 # Add datetime for working with dates  
 import datetime as dt  
   
 # Import SQLAlchemy pieces we need  
 from sqlalchemy.ext.automap import automap_base  
 from sqlalchemy.orm import Session  
 from sqlalchemy import create_engine, func  
   
 # Import Flask  
 from flask import Flask, jsonify  
   
 # Debug print to make sure imports worked  
 print("All imports successful!")  
   
 #################################################  
 # Database Setup - similar to what we did in Jupyter  
 #################################################  
 # Create engine to hawaii.sqlite  
 engine = create_engine("sqlite:///hawaii.sqlite")  
   
 # Use automap_base() to reflect database tables  
 Base = automap_base()  
 Base.prepare(engine, reflect=True)  
   
 # Save references to the tables (just like in Jupyter)  
 Measurement = Base.classes.measurement  
 Station = Base.classes.station  
   
 # Debug print to check tables  
 print("Found these tables:", Base.classes.keys())  
   
 #################################################  
 # Flask Setup - create app  
 #################################################  
 app = Flask(__name__)  
   
 # Debug print to make sure Flask started  
 print("Flask app created!")  
   
 #################################################  
 # Flask Routes - where we define our web pages  
 #################################################  
   
 # Home page - list all routes available  
 @app.route("/")  
 def welcome():  
     # Debug print when someone hits the home page  
     print("Someone visited the home page!")  
       
     return """  
     Welcome to the Hawaii Climate API!<br/>  
     Available Routes:<br/>  
     /api/v1.0/precipitation<br/>  
     /api/v1.0/stations<br/>  
     /api/v1.0/tobs<br/>  
     /api/v1.0/&lt;start&gt;<br/>  
     /api/v1.0/&lt;start&gt;/&lt;end&gt;  
     """  
   
 # Precipitation route  
 @app.route("/api/v1.0/precipitation")  
 def precipitation():  
     # Create session  
     session = Session(engine)  
       
     # Debug print  
     print("Getting precipitation data...")  
       
     # Find the most recent date (just like in Jupyter)  
     recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()  
       
     # Calculate date 1 year ago from recent date  
     # Convert string date to datetime  
     recent_date = dt.datetime.strptime(recent_date[0], '%Y-%m-%d')  
     one_year_ago = recent_date - dt.timedelta(days=365)  
       
     # Get precipitation data for last 12 months  
     results = session.query(Measurement.date, Measurement.prcp).\  
         filter(Measurement.date >= one_year_ago).\  
         order_by(Measurement.date).all()  
       
     # Close the session  
     session.close()  
       
     # Create a dictionary of date: prcp  
     precipitation_dict = {}  
     for date, prcp in results:  
         precipitation_dict[date] = prcp  
       
     # Debug print  
     print(f"Found {len(precipitation_dict)} days of precipitation data")  
       
     return jsonify(precipitation_dict)  
   
 # Stations route  
 @app.route("/api/v1.0/stations")  
 def stations():  
     # Create session  
     session = Session(engine)  
       
     # Debug print  
     print("Getting station list...")  
       
     # Get all stations  
     results = session.query(Station.station).all()  
       
     # Close session  
     session.close()  
       
     # Convert results to a list  
     station_list = []  
     for station in results:  
         station_list.append(station[0])  
       
     # Debug print  
     print(f"Found {len(station_list)} stations")  
       
     return jsonify(station_list)  
   
 # Temperature observations route  
 @app.route("/api/v1.0/tobs")  
 def tobs():  
     # Create session  
     session = Session(engine)  
       
     # Debug print  
     print("Getting temperature data...")  
       
     # Find the most active station (like we did in Jupyter)  
     most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\  
         group_by(Measurement.station).\  
         order_by(func.count(Measurement.station).desc()).first()  
       
     # Get most recent date and calculate 1 year ago  
     recent_date = session.query(Measurement.date).\  
         order_by(Measurement.date.desc()).first()[0]  
     recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d')  
     one_year_ago = recent_date - dt.timedelta(days=365)  
       
     # Get temperature data for most active station  
     results = session.query(Measurement.tobs).\  
         filter(Measurement.station == most_active_station[0]).\  
         filter(Measurement.date >= one_year_ago).all()  
       
     # Close session  
     session.close()  
       
     # Convert to list  
     temp_list = []  
     for temp in results:  
         temp_list.append(temp[0])  
       
     # Debug print  
     print(f"Found {len(temp_list)} temperature observations")  
       
     return jsonify(temp_list)  
   
 # Start and Start/End routes  
 @app.route("/api/v1.0/<start>")  
 @app.route("/api/v1.0/<start>/<end>")  
 def temp_range(start, end=None):  
     # Create session  
     session = Session(engine)  
       
     # Debug print  
     print(f"Calculating temperature stats from {start} to {end if end else 'end'}")  
       
     # Select statement for min, avg, max temps  
     sel = [func.min(Measurement.tobs),   
            func.avg(Measurement.tobs),   
            func.max(Measurement.tobs)]  
       
     # If we have both start and end date  
     if end:  
         results = session.query(*sel).\  
             filter(Measurement.date >= start).\  
             filter(Measurement.date <= end).all()  
     # If we only have start date  
     else:  
         results = session.query(*sel).\  
             filter(Measurement.date >= start).all()  
       
     # Close session  
     session.close()  
       
     # Create list of results  
     temp_stats = list(results[0])  
       
     # Debug print  
     print(f"Temperature stats: Min={temp_stats[0]}, Avg={temp_stats[1]:.1f}, Max={temp_stats[2]}")  
       
     return jsonify(temp_stats)  
   
 # Run the app  
 if __name__ == '__main__':  
     # Debug print  
     print("Starting the Flask app...")  
     app.run(debug=True)  
