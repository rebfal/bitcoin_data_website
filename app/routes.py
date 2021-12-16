from flask import request, render_template, Response, flash
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.model_selection import train_test_split


from app import app
from app.models import Bitcoin, EUR_USD, Gold, Nasdaq, SP_Futures, SP_VIX_Futures, TSLA

global market_dict
global choosenmarket

global globalMarket 
global globalChoosen

market_dict = {'bitcoin': Bitcoin,
               'eur_usd': EUR_USD,
               'gold': Gold, 
               'nasdaq': Nasdaq,
               'sp_500_futures': SP_Futures, 
               'sp_vix_futures': SP_VIX_Futures,
               'tesla': TSLA }

@app.route('/', methods= ['GET','POST'])
def home():
    if request.method  == 'POST':
        global choosenmarket
        if request.form['choose_market'] == 'Bitcoin':
            choosenmarket = market_dict['bitcoin']
        if request.form['choose_market'] == 'EUR/USD':
            choosenmarket = market_dict['eur_usd']    
        if request.form['choose_market'] == 'Gold Futures':
            choosenmarket = market_dict['gold']
        if request.form['choose_market'] == 'Nasdaq 100 Futures':
            choosenmarket = market_dict['nasdaq']
        if request.form['choose_market'] == 'S&P 500 Futures':
            choosenmarket = market_dict['sp_500_futures']
        if request.form['choose_market'] == 'sp_vix_futures':
            choosenmarket = market_dict['S&P 500 VIX Futures']
        if request.form['choose_market'] == 'Tesla':
            choosenmarket = market_dict['tesla']
            
        market = request.form['choose_market']
        choosen = True
    
    if request.method  == 'GET':
        market = 'Bitcoin'
        choosenmarket = Bitcoin
        choosen = False
    setVariables(market, choosen)
    
    return render_template('index.html', market = market, choosen = choosen)

def setVariables(market, choosen):
    global globalMarket
    global globalChoosen

    globalMarket = market
    globalChoosen = choosen


@app.route('/tables', methods = ['GET','POST'])
def show_tables():
    try:
        if request.method == "POST":
            # getting input with name = fname in HTML form
            #global choosenmarket
            
            searchdate = request.form.get("date")
            bitcoins = choosenmarket.query.filter_by(date = searchdate).order_by(choosenmarket.date).all()
            
        else:
            bitcoins = choosenmarket.query.order_by(choosenmarket.date).all()
            #bitcoins = bitcoins[0:10]

        return(render_template('tables.html', bitcoins = bitcoins, market = globalMarket))
        
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

            bitcoins = choosenmarket.query.filter(choosenmarket.date <= searchdate2).\
                filter(choosenmarket.date >= searchdate1).order_by(choosenmarket.date).all()
            
            number_of_bitcoins = choosenmarket.query.filter(choosenmarket.date <= searchdate2).\
                filter(choosenmarket.date >= searchdate1).order_by(choosenmarket.date).count()

            if number_of_bitcoins > number:
                while number_of_bitcoins > number:
                    bitcoins.pop(0)
                    number_of_bitcoins -= 1
            
        else:
            bitcoins = choosenmarket.query.order_by(choosenmarket.date).all()
        
        
        return(render_template('closing_prices.html', bitcoins = bitcoins, market = globalMarket))
          
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
        
        return(render_template('tree_sort.html', bitcoins = bitcoins, market = globalMarket))

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
    return(render_template('graph.html', market = globalMarket))


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
    
    dates = [bitcoin.date for bitcoin in choosenmarket.query.order_by(choosenmarket.date).all()] 
    prices = [bitcoin.price for bitcoin in choosenmarket.query.order_by(choosenmarket.date).all()]

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


@app.route('/predictions', methods = ['GET','POST'])
def prediction_table():
    names = {'bitcoin': 'Bitcoin',
               'eur_usd': 'EUR/USD',
               'gold': 'Gold', 
               'nasdaq': 'Nasdaq',
               'sp_500_futures': 'S&P Futures', 
               'sp_vix_futures': 'S&P VIX Futures',
               'tesla': 'Tesla' }
    market_dictionary = {} 
    market_list = []
    for key in market_dict:
        selected_market = market_dict[key]
        market_list.append(key)
        first_value = float([bitcoin.price for bitcoin in selected_market.query.order_by(selected_market.date.desc()).filter(selected_market.date).limit(1).all()][0].replace(',','.'))
        days = [5, 10, 20, 30, 90]
        prices_days = []
        
        for day in days:
            last_value = float([bitcoin.price for bitcoin in selected_market.query.order_by(selected_market.date.desc()).filter(selected_market.date).limit(day).all()][-1].replace(',','.'))
            change_this_day = (first_value/(last_value) - 1)*100
            prices_days.append(round(change_this_day,4))

        market_dictionary[names[key]] = prices_days   
     
    #samma frame som  genereras i tablen på predictknappen
    df = pd.DataFrame(market_dictionary.items(), columns = ['Market', 'percentages'])
    df_split = df.percentages.apply(pd.Series)
    df_split['Market'] = market_list
    df_split = df_split.rename(columns = {0 :'5 days', 1:'10 days', 2:'20 days', 3:'30 days', 4:'90 days' })

    
    dates = [bitcoin.date for bitcoin in Bitcoin.query.order_by(Bitcoin.date).all()] 
    bitcoin_prices = [float(bitcoin.price.replace(',', '.')) for bitcoin in Bitcoin.query.order_by(Bitcoin.date).all()]
    data = {
        'Dates': dates,
        'Bitcoin prices': bitcoin_prices,   
    }    
    df_tot = pd.DataFrame(data)   

    eur_usd_dates = [bitcoin.date for bitcoin in EUR_USD.query.order_by(EUR_USD.date).all()]
    eur_usd_prices = [float(bitcoin.price.replace(',', '.'))for bitcoin in EUR_USD.query.order_by(EUR_USD.date).all()]
    data_eur = {
        'Dates': eur_usd_dates,
        'EUR USD prices': eur_usd_prices
    } 
    df_eur = pd.DataFrame(data_eur)
    
    gold_dates = [bitcoin.date for bitcoin in Gold.query.order_by(Gold.date).all()]
    gold_prices = [float(bitcoin.price.replace(',', '.'))for bitcoin in Gold.query.order_by(Gold.date).all()]
    data_gold = {
        'Dates': gold_dates,
        'EUR USD prices': gold_prices
    } 
    df_gold = pd.DataFrame(data_gold)

    nasdaq_dates = [bitcoin.date for bitcoin in Nasdaq.query.order_by(Nasdaq.date).all()]
    nasdaq_prices = [float(bitcoin.price.replace(',', '.'))for bitcoin in Nasdaq.query.order_by(Nasdaq.date).all()]
    data_nasdaq ={
        'Dates': nasdaq_dates,
        'EUR USD prices': nasdaq_prices
    }
    df_nasdaq = pd.DataFrame(data_nasdaq)

    sp_500_prices = [float(bitcoin.price.replace(',', '.')) for bitcoin in SP_Futures.query.order_by(SP_Futures.date).all()]
    sp_500_dates = [bitcoin.date for bitcoin in SP_Futures.query.order_by(SP_Futures.date).all()]
    data_sp_500 ={
        'Dates': sp_500_dates,
        'EUR USD prices': sp_500_prices
    }
    df_sp_500 = pd.DataFrame(data_sp_500)

    sp_vix_prices = [float(bitcoin.price.replace(',', '.')) for bitcoin in SP_VIX_Futures.query.order_by(SP_VIX_Futures.date).all()]
    sp_vix_dates = [bitcoin.date for bitcoin in SP_VIX_Futures.query.order_by(SP_VIX_Futures.date).all()]
    data_sp_vix ={
        'Dates': sp_vix_dates,
        'EUR USD prices': sp_vix_prices
    }
    df_sp_vix = pd.DataFrame(data_sp_vix)

    tsla_prices = [float(bitcoin.price.replace(',', '.')) for bitcoin in TSLA.query.order_by(TSLA.date).all()]
    tsla_dates = [bitcoin.date for bitcoin in TSLA.query.order_by(TSLA.date).all()]

    data_tsla ={
        'Dates': tsla_dates,
        'EUR USD prices': tsla_prices
    }
    df_tsla = pd.DataFrame(data_tsla)

    df_tot = df_tot.join(df_eur.set_index('Dates'), on='Dates')
    df_tot = df_tot.merge(df_gold, on='Dates', how='left')
    df_tot = df_tot.merge(df_nasdaq, on='Dates', how='left')
    df_tot = df_tot.merge(df_sp_500, on='Dates', how='left')
    df_tot = df_tot.merge(df_sp_vix, on='Dates', how='left')
    df_tot = df_tot.merge(df_tsla, on='Dates', how='left')
    df_tot.fillna(method='ffill', inplace=True)
    df_tot.columns = ['Date', 'Bitcoin_prices', 'EUR USD prices', 'Gold prices', 'Nasdaq prices', 'SP 500 prices', 'SP 500 VIX prices', 'Tesla prices']
    
    train_filter = df_tot.loc[df_tot['Date'] <= pd.to_datetime('2019-12-31')]
    test_filter = df_tot.loc[df_tot['Date'] >= pd.to_datetime('2020-01-01')]
   

    print(train_filter)
    print(test_filter)

    train_filter.to_csv('Train file.csv')
    test_filter.to_csv('Test file.csv')
    df_split.to_csv('Features file.csv')

    #XGBOOST
    print(df_split)
    x,y = df_split.iloc[:,:-1],df_split.iloc[:,:-1]
    #data_dmatrix = xgb.DMatrix(data=x, label=y)

    #TEST
    test_x = test_filter.drop(columns=['Bitcoin_prices','Date'],axis=1)
    test_y = test_filter['Bitcoin_prices']

    #TRAIN
    train_x = test_filter.drop(columns=['Bitcoin_prices', 'Date'],axis=1)
    train_y = test_filter['Bitcoin_prices']


    # model = XGBClassifier()
    # model.fit(train_x, train_y)

    # predict_train = model.predict(train_x)
    # print('\nTarget on train data',predict_train) 

    xg_reg = xgb.XGBRegressor(objective='reg:linear', colsample_by_max_depth = 5, alpha = 10, n_estimators = 10)
    xg_reg.fit(train_x, train_y)
    preds_test = xg_reg.predict(test_x)
    rmse = np.sqrt(mean_squared_error(test_y, preds_test))
    print(preds_test)
    print("RSME: %f" % (rmse))

    bitcoin_preds = [None]*2
    bitcoin_preds[0] = preds_test
    bitcoin_preds[1] = test_y
    print(bitcoin_preds)
    
   #accuracy_train = accuracy_score(train_y,predict_train)
    #print('\naccuracy_score on train dataset : ', accuracy_train)


    return render_template('predictions.html', markets = market_dictionary, market = globalMarket)
   