from app import db
from app.models import Bitcoin, EUR_USD, Gold, Nasdaq, SP_Futures, SP_VIX_Futures, TSLA
import csv
import pandas as pd
from io import StringIO


def try_csv():
    
    
    with open('Data/BTC_USD Bitfinex Historical Data.csv', 'r') as bitcoin_file:
        csv_reader_bitcoin = csv.reader(bitcoin_file)
    

        with open('training_test4.csv', 'w') as new_file:
            csv_writer = csv.writer(new_file)

            for line in csv_reader_bitcoin:
                csv_writer.writerow(line[0:2])
            
    with open('Data/EUR_USD Historical Data.csv', 'r') as eurusd_file:
        csv_reader_eurusd = csv.reader(eurusd_file)
        with open('training_test4.csv', 'w') as new_file:
            csv_writer = csv.writer(new_file)
            for line in csv_reader_eurusd:
                    csv_writer.writerow(line[0:1])

# my_csv = pd.read_csv(filename)
# column = my_csv.column_name
    print('done with the test')


# dates = [bitcoin.date for bitcoin in Bitcoin.query.order_by(Bitcoin.date).filter(Bitcoin.date <= searchdate2).\
#                  filter(Bitcoin.date >= searchdate1).all()] 
# prices = [bitcoin.price for bitcoin in Bitcoin.query.order_by(Bitcoin.date).filter(Bitcoin.date <= searchdate2).\
#                  filter(Bitcoin.date >= searchdate1).all()]
           