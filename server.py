from enum import unique
from os import error
import io
from sqlite3 import Connection as SQLite3Connection
from datetime import date, datetime
from sqlite3.dbapi2 import connect
from typing import get_args
from sqlalchemy import event
from sqlalchemy import engine
from sqlalchemy.orm import query
from sqlalchemy.types import Integer, DateTime
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify, render_template, Response
from flask_sqlalchemy import SQLAlchemy
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bitcoindata.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

# configure sqlite3 to enforce foreign key contraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bitcoindata.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

db = SQLAlchemy(app)
now = datetime.now()

class Bitcoin(db.Model):
        __tablename__ = "data_bitcoin"
        date = db.Column(db.Date, primary_key=True, unique=True)
        price = db.Column(db.String(200))
        open = db.Column(db.String(200))
        high = db.Column(db.String(200))
        low = db.Column(db.String(200))
        vol = db.Column(db.String(200))
        change = db.Column(db.String(200))

class EUR_USD(db.Model):
        __tablename__ = "data_EUR_USD"
        date = db.Column(db.Date, primary_key=True, unique=True)
        price = db.Column(db.String(200))
        open = db.Column(db.String(200))
        high = db.Column(db.String(200))
        low = db.Column(db.String(200))
        change = db.Column(db.String(200))

def create_db():
    create_bitcoin()
    create_EUR_USD()
    #create_gold_futures()
    #create_Nasdaq_100()
    #create_S&P_500_futures()
    #create_S&P_500_VIX()
    #create_TSLA()



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


@app.route('/')
def home():
    prices = [bitcoin.price for bitcoin in Bitcoin.query.all()]
    dates = [bitcoin.date for bitcoin in Bitcoin.query.all()]
    return render_template('index.html', legend='prices', prices = prices, dates = dates)


@app.route('/tables', methods = ['GET','POST'])
def show_tables():
    try:
        if request.method == "POST":
            # getting input with name = fname in HTML form
            searchdate = request.form.get("date")
            bitcoins = Bitcoin.query.filter_by(date = searchdate).order_by(Bitcoin.date).all()
            
        else:
            bitcoins = Bitcoin.query.order_by(Bitcoin.date).all()
            #bitcoins = bitcoins[0:10]

        return(render_template('tables.html', bitcoins = bitcoins))
        
    except Exception as e:
        error_text = '<p> The error: <br>' + str(e) + '</p>'
        hed = '<h1> Something went wrong. </h1>'
        return hed + error_text

    
@app.route('/closing_prices', methods = ['GET','POST'])
def show_closing_prices():
    try:
        if request.method == "POST":
           
            searchdate1 = request.form.get("date1")
            searchdate2 = request.form.get("date2")
            number = int(request.form.get("number"))

            bitcoins = Bitcoin.query.filter(Bitcoin.date <= searchdate2).\
                filter(Bitcoin.date >= searchdate1).order_by(Bitcoin.date).all()
            
            number_of_bitcoins = Bitcoin.query.filter(Bitcoin.date <= searchdate2).\
                filter(Bitcoin.date >= searchdate1).order_by(Bitcoin.date).count()

            if number_of_bitcoins > number:
                while number_of_bitcoins > number:
                    bitcoins.pop(0)
                    number_of_bitcoins -= 1
            
        else:
            bitcoins = Bitcoin.query.order_by(Bitcoin.date).all()
        
        
        return(render_template('closing_prices.html', bitcoins = bitcoins))
          
    except Exception as e:
        error_text = '<p> The error: <br>' + str(e) + '</p>'
        hed = '<h1> Something went wrong. </h1>'
        return hed + error_text

@app.route('/tree_sort', methods = ['GET','POST'])

def tree_sort():
    try:
        if request.method == "POST":
           
            #searchdate1 = request.form.get("date1")
            #searchdate2 = request.form.get("date2")
            searchdate1 = '2021-08-08'
            searchdate2 = '2021-08-31'
            
            price_float =[]

            dates = [bitcoin.date for bitcoin in Bitcoin.query.order_by(Bitcoin.date).filter(Bitcoin.date <= searchdate2).\
                 filter(Bitcoin.date >= searchdate1).all()] 
            prices = [bitcoin.price for bitcoin in Bitcoin.query.order_by(Bitcoin.date).filter(Bitcoin.date <= searchdate2).\
                 filter(Bitcoin.date >= searchdate1).all()]
           
            prices = np.array(prices)
            for price in prices:
                price = price.replace(",","")
                price = float(price)
                price_float.append(price)
            
            dates = np.array(dates)
            
            zip_iterator = zip(dates, price_float)
            a_dictionary = dict(zip_iterator)

            bstree = BSTree()
            for key in a_dictionary:
                bstree.add(a_dictionary[key], key)
            
            print(bstree) 
            bstree.inorder()
            arraytree = []
            print(bstree)
            for node in bstree:
                arraytree.append(node)
            bitcoins = arraytree
        else:
            bitcoins = Bitcoin.query.order_by(Bitcoin.date).all()
        
        return(render_template('tree_sort.html', bitcoins = bitcoins))

    except Exception as e:
        error_text = '<p> The error: <br>' + str(e) + '</p>'
        hed = '<h1> Something went wrong. </h1>'
        return hed + error_text

class BSTNode:
    def __init__(self, key, key_dict):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.date = key_dict
 
    def insert(self, node):
        if self.key > node.key:
            if self.left is None:
                self.left = node
                node.parent = self
            else:
                self.left.insert(node)
        elif self.key <= node.key:
            if self.right is None:
                self.right = node
                node.parent = self
            else:
                self.right.insert(node)
 
    def inorder(self):
        if self.left is not None:
            self.left.inorder()
        print(self.key, self.date, end=' ')
        if self.right is not None:
            self.right.inorder()
 
class BSTree:
    def __init__(self):
        self.root = None
 
    def inorder(self):
        if self.root is not None:
            self.root.inorder()
 
    def add(self, key, key_dict):
        new_node = BSTNode(key, key_dict)
        if self.root is None:
            self.root = new_node
        else:
            self.root.insert(new_node)


@app.route('/graph')
def showGraph():
    return(render_template('graph.html'))


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def getNewDates():
    searchdate1 = request.form.get("date1")
    searchdate2 = request.form.get("date2")
    return [searchdate1, searchdate2]

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    
    dates = [bitcoin.date for bitcoin in Bitcoin.query.order_by(Bitcoin.date).all()] 
    prices = [bitcoin.price for bitcoin in Bitcoin.query.order_by(Bitcoin.date).all()]

    price_y =[]
    ypoints = np.array(prices)
    for element in ypoints:
        element = element.replace(",","")
        element = float(element)
        price_y.append(element)
    xpoints = np.array(dates)
    print(price_y[10:30])
    axis.plot(xpoints, price_y)
    return fig



if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    create_db()
    app.run(host='localhost', port=5000)
    app.run(debug=True)

