import datetime as dt
import pandas as pd
import pandas_datareader.data as web

tickers = ['SGDUSD=X',
           'SGDEUR=X',
           'SGDCNY=X',
           'SGDJPY=X',
           'SGDGBP=X',
           'SGDINR=X',
           'SGDBRL=X',
           'SGDCAD=X',
           'SGDRUB=X',
           'SGDAUD=X',
           'SGDMXN=X',
           'SGDIDR=X',
           'SGDTRY=X',
           'SGDCHF=X',
           'SGDSAR=X']

def getFinancialData(startDate, endDate, ticker):
    df = web.DataReader(ticker, 'yahoo', startDate, endDate);
    return df['Adj Close']

def getIndividualCurrencyChanges(rawData):
    return rawData / rawData.shift(1);

def getWeightedCurrencyChanges(changes, gdps):
    pass

for i in range(0, len(tickers)):
    
    try:
        rawData = getFinancialData(dt.datetime(2007, 10, 21), dt.datetime(2017, 10, 20), tickers[i]);
        changes = getIndividualCurrencyChanges(rawData);
    except Exception: 
        pass
    
    rawData = getFinancialData(dt.datetime(2007, 10, 21), dt.datetime(2017, 10, 20), tickers[i]);
    changes = getIndividualCurrencyChanges(rawData);
    print(rawData.tail())


