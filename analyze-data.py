import pandas as pd
from importlib.resources import path
import os

path = '../MidtermProject-main/csv-files/'

df_list = []

for root, directories, files in os.walk(path, topdown=False):
    for name in files:
        file = os.path.join(root, name)
        df = pd.read_csv(file)
        df_list.append(df)

# Appraisal of the announcement of stock splits impact requires a measure for the abnormal return, which
# is conducted by subtracting the normal return of the firm over the event window from the observed
# return of the security over the same period.  

#TODO market_portfolio_proxy data (^OMXSPI), which we use to estimate an expected return based on market performance, 
# does not include data older than 2013, we but the security data period is from 2010 to 2020. 
# Find source with historical data from start of 2010.  

#TODO to calculate abnormal return we need a function that estimates the normal return of a security (see paper: https://www.diva-portal.org/smash/record.jsf?dswid=5370&pid=diva2%3A1576254&c=128&searchType=SIMPLE&language=en&query=linear+regression&af=%5B%22thesisLevel%3AM2%22%5D&aq=%5B%5B%5D%5D&aq2=%5B%5B%5D%5D&aqe=%5B%5D&noOfRows=50&sortOrder=author_sort_asc&sortOrder2=title_sort_asc&onlyFullText=false&sf=all)

df_names_list = []

for df in df_list:
    df_names_list.append(df["Ticker"])
    #print(df_names_list)

#TODO after normal return is estimated, create function that subtracts the estimated normal return of a security 
# from the observed return of the same security over the defined event window

#def normal_return_estimation(X)

#def abnormal_return(R, X):