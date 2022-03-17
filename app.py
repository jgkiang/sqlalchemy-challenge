
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start/end")

@app.route("/api/v1.0/precipitation")
def prcp():
    recent_prcp = session.query(str(Measurement.date), Measurement.prcp).filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').order_by(Measurement.date).all()
    prcp_dict = dict(recent_prcp)
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Measurement.station).group_by(Measurement.station).all()
    stations_list = list(np.ravel(stations))
    return jsonify(stations_list)    

@app.route("/api/v1.0/tobs")
def tobs():
    tobs = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date > '2016-08-23').filter(Measurement.date <= '2017-08-23').filter(Measurement.station == "USC00519281").all()
    tobs_list = list(np.ravel(tobs))
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start=None):  
    start_only = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    start_only_list = list(np.ravel(start_only))
    return jsonify(start_only_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    start_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    start_end_list = list(np.ravel(start_end))
    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)