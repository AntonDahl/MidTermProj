import pandas as pd
from importlib.resources import path
import os
import datetime

path = '../MidtermProject-main/csv-files/'

# importing OMXSPI market proxy data as dataframe - converting date format to match same as securities data

market_portfolio_proxy = pd.read_csv("../MidtermProject-main/OMXSPI.csv/OMXSPI.csv")
#print(market_portfolio_proxy)
try:
    for row in market_portfolio_proxy.itertuples():
        #print(row)
        #print(str(market_portfolio_proxy.at[row.Index, 'Date']))
        market_portfolio_proxy.at[row.Index, 'Date'] = datetime.datetime.strptime(str(market_portfolio_proxy.at[row.Index, 'Date']), '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d')

    #print(market_portfolio_proxy)
except:
    pass

# importing csv-files from directory as dataframes in list

df_list = []

for root, directories, files in os.walk(path, topdown=False):
    for name in files:
        file = os.path.join(root, name)
        if file != "../MidtermProject-main/csv-files/.DS_Store":
            #print("this is the file", file)
            df = pd.read_csv(file)
            #print(df)
            df_list.append(df)
        else:
            pass

# Appraisal of the announcement of stock splits impact requires a measure for the abnormal return, which
# is conducted by subtracting the normal return of the firm over the event window from the observed
# return of the security over the same period.   

#TODO to calculate abnormal return we need a function that estimates the normal return of a security (see paper: https://www.diva-portal.org/smash/record.jsf?dswid=5370&pid=diva2%3A1576254&c=128&searchType=SIMPLE&language=en&query=linear+regression&af=%5B%22thesisLevel%3AM2%22%5D&aq=%5B%5B%5D%5D&aq2=%5B%5B%5D%5D&aqe=%5B%5D&noOfRows=50&sortOrder=author_sort_asc&sortOrder2=title_sort_asc&onlyFullText=false&sf=all)

df_names_list = []

for df in df_list:
    df_names_list.append(df["Ticker"])
    #print(df_names_list)

#TODO after normal return is estimated, create function that subtracts the estimated normal return of a security 
# from the observed return of the same security over the defined event window

#def normal_return_estimation(X)

#def abnormal_return(R, X):