from os import error
import io
from sqlite3 import Connection as SQLite3Connection
from datetime import date, datetime
from flask import Flask, request, jsonify, render_template, Response
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bitcoindata.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

db = SQLAlchemy(app)
now = datetime.now()

class Bitcoin(db.Model):
        __tablename__ = "bitcoindata2"
        date = db.Column(db.Date, primary_key=True)
        price = db.Column(db.String(200))
        open = db.Column(db.String(200))
        high = db.Column(db.String(200))
        low = db.Column(db.String(200))
        vol = db.Column(db.String(200))
        change = db.Column(db.String(200))


def create_db():
    
    df = pd.read_csv('BTC_USD Bitfinex Historical Data.csv')
    df['Date']= pd.to_datetime(df['Date'])
    
    for index, row in df.iterrows():
        new_bitcoin = Bitcoin(
            date = row['Date'],
            price = row['Price'],
            open = row['Open'],
            high = row['High'],
            low = row['Low'],
            vol = row['Vol.'],
            change = row['Change %']
        )
        db.session.add(new_bitcoin)
    db.session.commit()