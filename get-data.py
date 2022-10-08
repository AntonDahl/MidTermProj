#use pip install yfinance, pandas

from matplotlib import ticker
import pandas as pd
import yfinance as yf
import datetime
import os

event_window_forward = 5
event_window_backward = 5
estimation_period = 120
total_timeline_steps = 131

tickers = []
 
# Appraisal of the announcement of stock splits impact requires a measure for the abnormal return, which
# is conducted by subtracting the normal return of the firm over the event window from the observed
# return of the security over the same period.


def date_to_int(date_str):
     date_list = date_str.split("-")
     for i in range(len(date_list)):
         date_list[i] = int(date_list[i])
     return date_list

     
def find_time_interval(date, days_to_add, days_to_subtract):
    # 0 Sunday and 6 Saturday are skipped
    
    day_count1 = 0 
    day_count2 = 0

    # set the end and start dates equal to announcement date and change them according to the defined event windows

    end_date = datetime.date(date_to_int(date)[0], date_to_int(date)[1], date_to_int(date)[2])
    start_date = datetime.date(date_to_int(date)[0], date_to_int(date)[1], date_to_int(date)[2])   
    
    while day_count1 < days_to_add:
        end_date += datetime.timedelta(days=1)
        weekday = int(end_date.strftime('%w'))
        
        if weekday != 0 and weekday != 6:
            day_count1 += 1
    
    while day_count2 < days_to_subtract:
        start_date -= datetime.timedelta(days=1)
        weekday = int(end_date.strftime('%w'))
        
        if weekday != 0 and weekday != 6:
            day_count2 += 1
    
    return start_date, end_date



def string_to_list(string):
    listRes = list(string.split(" "))
    return listRes


# looping through the text file with stock split announcement dates and respective stock tickers. Appending rows to list as strings

with open('tickers.txt') as tickers_file:
    for line in tickers_file:
        tickers.append(line),

# looping through strings in list to extract announcement_date and ticker to prep for API call

for i in range(len(tickers)):
    tickers[i] = string_to_list(tickers[i])

for i in range(len(tickers)):
    tickers[i] = tickers[i][:2]
    
# manipulating ticker to match the one needed for API call

#TODO some of the API-calls output "No data found, symbol may be delisted" exception; manually check these companies for the 
# correct yahoo finance tickers and change it; either through code manipulation here, or manually inside the tickers.txt file.

for i in range(len(tickers)):
    tickers[i][1] = tickers[i][1].replace("b", "-B")
    tickers[i][1] = tickers[i][1].replace("a", "-A")    

# getting and saving the data from yahoo finance API as csv-files : start- and end-dates for a given ticker are based on the above defined time intervals

df_list = []
df_names = []

for list in tickers:
    announcement_date = list[0]
    company_ticker = list[1]
    
    date_tuple = find_time_interval(announcement_date, event_window_forward, event_window_backward+estimation_period)
    start_date = date_tuple[0]
    end_date = date_tuple[1]
    
    ticker = yf.Ticker(company_ticker)
    try:
        df = ticker.history(start="{}".format(start_date), end="{}".format(end_date), interval='1d', auto_adjust=True)
        #df["info"] = ticker.info
        df["Ticker"] = company_ticker
        df_list.append(df)

        # checking if name of ticker already exists in df_names list; if it does, modify name to allow for versioning and avoid overwriting csv-files

        if company_ticker not in df_names:
            df_names.append(company_ticker)
            df.to_csv("../MidtermProject-Main/csv-files/{}.csv".format(company_ticker))
        elif company_ticker in df_names and company_ticker+"1" not in df_names:
            df_names.append(company_ticker+"1")
            df["Ticker"] = company_ticker+"1"
            df.to_csv("../MidtermProject-Main/csv-files/{}.csv".format(company_ticker+"1"))
        elif company_ticker in df_names and company_ticker+"1" in df_names and company_ticker+"2" not in df_names:
            df_names.append(company_ticker+"2")
            df["Ticker"] = company_ticker+"2"
            df.to_csv("../MidtermProject-Main/csv-files/{}.csv".format(company_ticker+"2"))
        elif company_ticker in df_names and company_ticker+"1" in df_names and company_ticker+"2" in df_names and company_ticker+"3" not in df_names:
            df_names.append(company_ticker+"3")
            df["Ticker"] = company_ticker+"3"
            df.to_csv("../MidtermProject-Main/csv-files/{}.csv".format(company_ticker+"3"))
        elif company_ticker in df_names and company_ticker+"1" in df_names and company_ticker+"2" in df_names and company_ticker+"3" in df_names and company_ticker+"4" not in df_names:
            df_names.append(company_ticker+"4")
            df["Ticker"] = company_ticker+"4"
            df.to_csv("../MidtermProject-Main/csv-files/{}.csv".format(company_ticker+"4"))
        elif company_ticker in df_names and company_ticker+"1" in df_names and company_ticker+"2" in df_names and company_ticker+"3" in df_names and company_ticker+"4" in df_names and company_ticker+"5" not in df_names:
            df_names.append(company_ticker+"5")
            df["Ticker"] = company_ticker+"5"
            df.to_csv("../MidtermProject-Main/csv-files/{}.csv".format(company_ticker+"5"))
        elif company_ticker in df_names and company_ticker+"1" in df_names and company_ticker+"2" in df_names and company_ticker+"3" in df_names and company_ticker+"4" in df_names and company_ticker+"5" in df_names and company_ticker+"6" not in df_names:
            df_names.append(company_ticker+"6")
            df["Ticker"] = company_ticker+"6"
            df.to_csv("../MidtermProject-Main/csv-files/{}.csv".format(company_ticker+"6"))
        
    except Exception:
        (df, "could not get")

ticker = yf.Ticker("^OMXSPI")

market_portfolio_proxy = ticker.history(start="2010-01-01", end="2021-01-01", interval='1d', auto_adjust=True)
market_portfolio_proxy = market_portfolio_proxy.to_csv(("../MidtermProject-Main/csv-files/market_portfolio_proxy.csv"))
    
print(len(df_list))
print(len(df_names))

#def normal_return_estimation(X)

#def abnormal_return(R, X):
