from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlite3 import Connection as SQLite3Connection

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bitcoindata.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

db = SQLAlchemy(app)

# configure sqlite3 to enforce foreign key contraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


from app.models import Bitcoin, EUR_USD

def create_bitcoin():
    df = pd.read_csv('Data/BTC_USD Bitfinex Historical Data.csv')
    df['Date']= pd.to_datetime(df['Date'])
    
    for index, row in df.iterrows():
        new_bitcoin = Bitcoin(
            date = row['Date'],
            price = row['Price'].replace(',', '').replace('.',','),
            open = row['Open'].replace(',', '').replace('.',','),
            high = row['High'].replace(',', '').replace('.',','),
            low = row['Low'].replace(',', '').replace('.',','),
            vol = row['Vol.'].replace('.', '').replace('K','000'),
            change = row['Change %'].replace('%', '')
        )

        db.session.add(new_bitcoin)
    db.session.commit()

def create_EUR_USD():
    df = pd.read_csv('Data/BTC_USD Bitfinex Historical Data.csv')
    df['Date']= pd.to_datetime(df['Date'])
    
    for index, row in df.iterrows():
        new_bitcoin = EUR_USD(
            date = row['Date'],
            price = row['Price'].replace(',', '').replace('.',','),
            open = row['Open'].replace(',', '').replace('.',','),
            high = row['High'].replace(',', '').replace('.',','),
            low = row['Low'].replace(',', '').replace('.',','),
            change = row['Change %'].replace('%', '')
        )

        db.session.add(new_bitcoin)
    db.session.commit()

def create_db():
    create_bitcoin()
    create_EUR_USD()
    
from app import routes