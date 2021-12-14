from flask import request, render_template, Response, sessions
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from app import app
from app.models import Bitcoin, EUR_USD, Gold, Nasdaq, SP_Futures, SP_VIX_Futures, TSLA
# from ..algoritms.BTStree import BSTNode, BSTree

# global class_dict 
# class_dict = {'bitcoin': Bitcoin, 'eurusd': EUR_USD, 'gold': Gold, 'nasdaq': Nasdaq, 'sp500': SP_Futures, 'sp500vix': SP_VIX_Futures, 'tesla': TSLA}


@app.route('/', methods = ['GET','POST'])
def home():

    if request.method == 'POST':
        market = 

    

    return render_template('index.html')

@app.route('/table/<market>', methods = ['GET','POST'])

def show_tables(market):
    # class_dict = {'bitcoin': 'Bitcoin', 'eurusd': 'EUR_USD', 'gold': 'Gold', 'nasdaq': 'Nasdaq', 'sp500': 'SP_Futures', 'sp500vix': 'SP_VIX_Futures', 'tesla': 'TSLA'}
    # market_class = class_dict[market]
    if market == 'bitcoin':
        market_class = Bitcoin

    if market == 'gold':
        market_class = Gold

    
    
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




    
@app.route('/closing_prices/bitcoin', methods = ['GET','POST'])
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

@app.route('/tree_sort/bitcoin', methods = ['GET','POST'])
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


@app.route('/graph/bitcoin')
def showGraph():
    return(render_template('graph.html'))


@app.route('/plot.png/bitcoin')
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