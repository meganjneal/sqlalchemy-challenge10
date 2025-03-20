# Import dependencies  
import numpy as np  
import pandas as pd  
import datetime as dt  
from sqlalchemy.ext.automap import automap_base  
from sqlalchemy.orm import Session  
from sqlalchemy import create_engine, func  
from flask import Flask, jsonify  
  
# Database Setup  
# Adjusted path: the SQLite database is located in the Resources folder inside SurfsUp.  
engine = create_engine("sqlite:///Resources/hawaii.sqlite")  
  
# Reflect database into new model  
Base = automap_base()  
Base.prepare(engine, reflect=True)  
  
# Save references to tables  
Measurement = Base.classes.measurement  
Station = Base.classes.station  
  
# Flask Setup  
app = Flask(__name__)  
  
# Home page - list available routes  
@app.route("/")  
def welcome():  
    return (  
        "Welcome to the Hawaii Climate API!<br/>"  
        "Available Routes:<br/>"  
        "/api/v1.0/precipitation<br/>"  
        "/api/v1.0/stations<br/>"  
        "/api/v1.0/tobs<br/>"  
        "/api/v1.0/&lt;start&gt;<br/>"  
        "/api/v1.0/&lt;start&gt;/&lt;end&gt;"  
    )  
  
# Precipitation route  
@app.route("/api/v1.0/precipitation")  
def precipitation():  
    # Create session  
    session = Session(engine)  
      
    # Find the most recent date  
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]  
      
    # Calculate the date one year ago from the most recent date  
    one_year_ago = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)  
      
    # Query precipitation data for the last 12 months  
    results = session.query(Measurement.date, Measurement.prcp).\  
        filter(Measurement.date >= one_year_ago).all()  
      
    session.close()  
      
    # Create dictionary with date as key and prcp as value  
    prcp_dict = {}  
    for date, prcp in results:  
        prcp_dict[date] = prcp  
      
    return jsonify(prcp_dict)  
  
# Stations route  
@app.route("/api/v1.0/stations")  
def stations():  
    # Create session  
    session = Session(engine)  
      
    # Query for all stations  
    results = session.query(Station.station).all()  
      
    session.close()  
      
    # Convert list of tuples into normal list  
    stations = list(np.ravel(results))  
      
    return jsonify(stations)  
  
# Temperature Observations (tobs) route  
@app.route("/api/v1.0/tobs")  
def tobs():  
    session = Session(engine)  
      
    # Find most recent date  
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]  
    one_year_ago = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)  
      
    # Find most active station  
    most_active_station = session.query(Measurement.station).\  
        group_by(Measurement.station).\  
        order_by(func.count(Measurement.station).desc()).first()  
      
    # Get temperature observations for the most active station for the last 12 months  
    results = session.query(Measurement.tobs).\  
        filter(Measurement.station == most_active_station[0]).\  
        filter(Measurement.date >= one_year_ago).all()  
      
    session.close()  
      
    # Convert list of tuples to list  
    temps = list(np.ravel(results))  
      
    return jsonify(temps)  
  
# Temperature stats route for start and start-end range  
@app.route("/api/v1.0/<start>")  
@app.route("/api/v1.0/<start>/<end>")  
def temp_stats(start, end=None):  
    session = Session(engine)  
      
    # Define selection: min, avg, and max temperature  
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]  
      
    if end:  
        results = session.query(*sel).\  
            filter(Measurement.date >= start).\  
            filter(Measurement.date <= end).all()  
    else:  
        results = session.query(*sel).\  
            filter(Measurement.date >= start).all()  
      
    session.close()  
      
    # Flatten the results list  
    temps = list(np.ravel(results))  
      
    return jsonify(temps)  
  
if __name__ == '__main__':  
    app.run(debug=True)  