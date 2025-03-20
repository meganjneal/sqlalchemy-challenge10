# Import dependencies  
import numpy as np  
import pandas as pd  
import datetime as dt  
from sqlalchemy.ext.automap import automap_base  
from sqlalchemy.orm import Session  
from sqlalchemy import create_engine, func  
from flask import Flask, jsonify  
  
# Database Setup  
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
    session = Session(engine)  
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]  
    one_year_ago = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)  
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()  
    session.close()  
      
    prcp_dict = {}  
    for date, prcp in results:  
        prcp_dict[date] = prcp  
      
    return jsonify(prcp_dict)  
  
# Stations route  
@app.route("/api/v1.0/stations")  
def stations():  
    session = Session(engine)  
    results = session.query(Station.station).all()  
    session.close()  
      
    stations = list(np.ravel(results))  
    return jsonify(stations)  
  
# Temperature Observations route  
@app.route("/api/v1.0/tobs")  
def tobs():  
    session = Session(engine)  
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]  
    one_year_ago = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)  
      
    most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()  
    results = session.query(Measurement.tobs).filter(Measurement.station == most_active_station[0]).filter(Measurement.date >= one_year_ago).all()  
      
    session.close()  
    temps = list(np.ravel(results))  
    return jsonify(temps)  
  
# Temperature stats route for start and start-end range  
@app.route("/api/v1.0/<start>")  
@app.route("/api/v1.0/<start>/<end>")  
def temp_stats(start, end=None):  
    session = Session(engine)  
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]  
      
    if end:  
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()  
    else:  
        results = session.query(*sel).filter(Measurement.date >= start).all()  
      
    session.close()  
    temps = list(np.ravel(results))  
    return jsonify(temps)  
  
if __name__ == '__main__':  
    app.run(debug=True)  