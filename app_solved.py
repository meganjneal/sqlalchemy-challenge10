from flask import Flask, jsonify  
from sqlalchemy import create_engine, func, MetaData  
from sqlalchemy.orm import Session, declarative_base  
import numpy as np  
  
# Database Setup  
engine = create_engine("sqlite:///hawaii.sqlite")  
metadata = MetaData()  
metadata.reflect(engine)  
print("Tables reflected:", list(metadata.tables.keys()))  
Base = declarative_base(metadata=metadata)  
  
# Define ORM classes based on the reflected database tables.  
class Measurement(Base):  
    __table__ = metadata.tables['measurement']  
    __mapper_args__ = {'primary_key': [__table__.c.station, __table__.c.date]}  # Composite primary key  
  
class Station(Base):  
    __table__ = metadata.tables['station']  
  
# Create session link from Python to the DB  
session = Session(engine)  
  
# Flask Setup  
app = Flask(__name__)  
  
# Flask Routes  
@app.route("/")  
def welcome():  
    return (  
        "Available Routes:<br/>"  
        "/api/v1.0/precipitation<br/>"  
        "/api/v1.0/stations<br/>"  
        "/api/v1.0/tobs<br/>"  
        "/api/v1.0/temp/<start><br/>"  
        "/api/v1.0/temp/<start>/<end>"  
    )  
  
@app.route("/api/v1.0/precipitation")  
def precipitation():  
    # Query all dates and precipitation values  
    results = session.query(Measurement.date, Measurement.prcp).all()  
    precip = {date: prcp for date, prcp in results}  
    return jsonify(precip)  
  
@app.route("/api/v1.0/stations")  
def stations():  
    # Return a list of stations  
    results = session.query(Station.station).all()  
    stations_list = [station for station, in results]  
    return jsonify(stations_list)  
  
@app.route("/api/v1.0/tobs")  
def tobs():  
    # Query dates and temperature observations of the most active station for the last year of data.  
    active_station = session.query(  
        Measurement.station,   
        func.count(Measurement.station)  
    ).group_by(  
        Measurement.station  
    ).order_by(  
        func.count(Measurement.station).desc()  
    ).first()[0]  
      
    results = session.query(  
        Measurement.date,   
        Measurement.tobs  
    ).filter(  
        Measurement.station == active_station  
    ).all()  
      
    temps = {date: tobs for date, tobs in results}  
    return jsonify(temps)  
  
@app.route("/api/v1.0/temp/<start>")  
@app.route("/api/v1.0/temp/<start>/<end>")  
def temp_range(start, end=None):  
    # Return min, avg, and max temps for dates greater than or equal to start   
    # and, if provided, less than or equal to end.  
    if end:  
        results = session.query(  
            func.min(Measurement.tobs),   
            func.avg(Measurement.tobs),   
            func.max(Measurement.tobs)  
        ).filter(  
            Measurement.date >= start  
        ).filter(  
            Measurement.date <= end  
        ).all()  
    else:  
        results = session.query(  
            func.min(Measurement.tobs),   
            func.avg(Measurement.tobs),   
            func.max(Measurement.tobs)  
        ).filter(  
            Measurement.date >= start  
        ).all()  
      
    temps = list(np.ravel(results))  
    return jsonify(temps)  
  
if __name__ == "__main__":  
    app.run(debug=True)  