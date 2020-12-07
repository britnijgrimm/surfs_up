#Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

#Import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Import Flask dependencies
from flask import Flask, jsonify

#Set up databse
engine = create_engine("sqlite:///hawaii.sqlite")

#Relfect database into clasees
Base = automap_base()
Base.prepare(engine, reflect=True)

#Create measurement and station class variables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session link to database
session = Session(engine)

#Define Flask app
app = Flask(__name__)

#Define welcome route
@app.route("/")

#Define routing for welcome route
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
 
#Define precipitation route
@app.route("/api/v1.0/precipitation")

#Define routing for precipitation route
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#Define stations route
@app.route("/api/v1.0/stations")

#Define routing for stations route
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#Define temps route
@app.route("/api/v1.0/tobs")

#Define routing for temps route
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#Define start and end temp routes
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#Define a function for temp statistical summary
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)