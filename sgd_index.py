import datetime as dt
from dateutil import parser
import pandas as pd
import pandas_datareader.data as web

tickers = ['SGDUSD=X',
           'SGDEUR=X',
           'SGDCNY=X',
           'SGDJPY=X',
           'SGDGBP=X',
           'SGDBRL=X',
           'SGDCAD=X',
           'SGDRUB=X',
           'SGDAUD=X',
           'SGDMXN=X',
           'SGDIDR=X',
           'SGDTRY=X',
           'SGDCHF=X',
           'SGDSAR=X']

countries = ['US',
             'EU',
             'CN',
             'JP',
             'GB',
             'BR',
             'CA',
             'RU',
             'AU',
             'MX',
             'ID',
             'TR',
             'CH',
             'SA']

def getGDPData(country):
    df = pd.read_csv("data\\gdp\\" + country + ".csv", index_col = 1, names = ['Country', 'GDP']);
    return df

def getForexData(ticker):
    df = pd.read_csv("data\\forex\\" + ticker + ".csv", index_col = 0, names = ['Price', 'Change']);
    return df

def getIndexChanges(forex, gdp):
    
    gdp.drop(gdp.tail(1).index,inplace=True)
    forex.drop(forex.tail(1).index,inplace=True)
    
    indexChanges = []
    
    #Loop through every day
    for i in range(0, len(forex)):
        
        dateTime = parser.parse(forex.index.values[i])
        year = dateTime.year;
        if year == 2017:
            year = 2016
        
        indexChanges.append(calculateWeightedGeometricMean(forex.iloc[i], gdp.loc[str(year)]))
        
    return indexChanges

def calculateWeightedGeometricMean(forex, gdp):
    
    a = 1;
    
    #Loop through every country/currency
    for i in range(0, len(forex)):
        
        #clean data  
        try:
            val = float(forex.iloc[i])
        except ValueError:
            forex.iloc[i] = '1'
            
        if forex.iloc[i] == '0':
            forex.iloc[i] = '1';
        
        try:
            val = float(gdp.iloc[i])
        except ValueError:
            gdp.iloc[i] = '1'
            
        if gdp.iloc[i] == '0':
            gdp.iloc[i] = '1';
        
        a = a * pow(float(forex.iloc[i]), float(gdp.iloc[i]) / 10000000000.0) #divide 10,000,000,000 ten billion
        
    a = pow(a, 1 / calculateSumOfGDP(gdp))
    
    return a
        
def calculateSumOfGDP(gdps):
    
    a = 0.0
    
    for gdp in gdps:
        a = a + float(gdp)
        
    return a / 10000000000.0

def getIndex(indexChanges):
    
    indices = []
    index = 100.0
    
    for i in range(0, len(indexChanges)):
        
        #Clean data
        if indexChanges[i] != indexChanges[i]:
            indexChanges[i] = 1.0
        
        index = index * indexChanges[i]
        indices.append(index)
        
    return indices
    

gdpAllDf = pd.DataFrame()
forexAllDf = pd.DataFrame()

for i in range(0, len(countries)):
    
    gdpDf = getGDPData(countries[i])
    gdpDf = gdpDf.iloc[::-1] #Reverse, to be in ascending date
    forexDf = getForexData(tickers[i])
    
    gdpAllDf[countries[i]] = gdpDf['GDP'];
    forexAllDf[tickers[i]] = forexDf['Change'];
    
indexChanges = getIndexChanges(forexAllDf, gdpAllDf)
indices = getIndex(indexChanges)

df = pd.DataFrame(indices);
df.to_csv('SGD_Index.csv');
    
    
    
    
    
   


