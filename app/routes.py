from flask import request, render_template, Response
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from app import app
from app.models import Bitcoin


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