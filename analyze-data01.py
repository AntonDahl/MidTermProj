from heapq import merge
import pandas as pd
from importlib.resources import path
import os
import datetime
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt

path = '../MidtermProject-main/csv-files/'

# importing OMXSPI market proxy data as dataframe - converting date format to match same as securities data
market_portfolio_proxy = pd.read_csv("../MidtermProject-main/OMXSPI.csv/OMXSPI.csv")

try:
    for row in market_portfolio_proxy.itertuples():
        market_portfolio_proxy.at[row.Index, 'Date'] = datetime.datetime.strptime(str(market_portfolio_proxy.at[row.Index, 'Date']), 
        '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d')
except:
    pass


def daily_return(df):
    
    for row in df.itertuples():
        day_return = row.Close - row.Open
        day_return_percentage = (day_return / row.Close) * 100
        df.at[row.Index, "Return"] = day_return_percentage
    

# import df's from csv-files
df_dict = {}        

for root, directories, files in os.walk(path, topdown=False):
    for name in files:
        file = os.path.join(root, name)
        if file != "../MidtermProject-main/csv-files/.DS_Store":
            #print("this is the file", file)
            df = pd.read_csv(file)
            #print(df)
            df_dict[df["Ticker"][1]] = df
        else:
            pass

# add daily return in percentage as column in each stock df, we will use this to calculate Beta values for each stock
for df in df_dict:
    daily_return(df_dict[df])

# do same for market portfolio proxy
daily_return(market_portfolio_proxy)

# calculate Beta for stocks
beta_dict = {}

for df in df_dict:
    
    merge_on_date = pd.merge(df_dict[df], market_portfolio_proxy, on=['Date'], how='inner')
    estimation_period_df = merge_on_date[:len(merge_on_date)-11]
    x_values = estimation_period_df["Return_x"].values.reshape(-1,1)
    y_values = estimation_period_df["Return_y"].values.reshape(-1,1)
    reg = linear_model.LinearRegression()
    beta_dict[df_dict[df]["Ticker"][1]] = reg.fit(x_values, y_values).coef_

# calculate normal return given estimation period T=-125 to T=-5, assuming alpha = 0 and rf = 0
normal_return_dict = {}


def normal_return(df):
    merge_on_date = pd.merge(df, market_portfolio_proxy, on=['Date'], how='inner')
    estimation_period_df = merge_on_date[:len(merge_on_date)-11]
    market_mean_daily_return = estimation_period_df["Return_y"].mean()
    market_mean_period_return = market_mean_daily_return * len(estimation_period_df)
    normal_return_stock = beta_dict[df["Ticker"][1]][0][0] * market_mean_period_return
    normal_return_dict[df["Ticker"][1]] = normal_return_stock


for df in df_dict:
    normal_return(df_dict[df])

print(normal_return_dict)

# calculate abnormal return for the given event window period T=-5 to T=5

event_window = 11
abnormal_return_dict = {}

#TODO:
# here the authors are a little bit unclear on which time period they assign the extimations of the normal return; 
# the equation (4) states that it is the same time period as the abnormal returns. However, the authors states on 
# page 20:
#
# The estimation window is the period prior to the event window which is used to estimate the normal return
# which would be expected given that the event did not take place. The estimation period occurs before
# the event window and contains a much larger time period because the expected normal return demands
# more observations in order for the estimation to be as accurate as possible.


def abnormal_return(df):
    merge_on_date = pd.merge(df, market_portfolio_proxy, on=['Date'], how='inner')
    event_window_df = merge_on_date[len(merge_on_date)-11:]
    observed_return_of_stock = event_window_df["Return_x"].values.reshape(-1,1).sum()
    normal_return_of_stock = normal_return_dict[df["Ticker"][1]]
    abnormal_return_of_stock = observed_return_of_stock - normal_return_of_stock
    abnormal_return_dict[df["Ticker"][1]] = abnormal_return_of_stock


daily_abnormal_return_dict = {}


def daily_abnormal_return(df):
    merge_on_date = pd.merge(df, market_portfolio_proxy, on=['Date'], how='inner')
    event_window_df = merge_on_date[len(merge_on_date)-11:]
    daily_observed_return_of_stock = event_window_df["Return_x"].values.reshape(-1,1)
    normal_return_of_stock = normal_return_dict[df["Ticker"][1]]

    daily_abnormal_return_list = []
    
    for i in range(len(daily_observed_return_of_stock)):
        daily_abnormal_return = daily_observed_return_of_stock[i] - normal_return_of_stock
        daily_abnormal_return_list.append(daily_abnormal_return.tolist()[0])
    
    daily_abnormal_return_dict[df["Ticker"][1]] = np.array(daily_abnormal_return_list)


# possible outliers: STRAX.ST 31.84, BORG.ST4 19.827, ITAB.ST -31.335025252190906, FAG.ST1 23.272183969354053, LAGR-B.ST 18.328433922821,
# BETS-B.ST1 -23.737635010837362, FING-B.ST -29.7031275493231

for df in df_dict:
    abnormal_return(df_dict[df])

total = 0

for key in abnormal_return_dict:
    total += abnormal_return_dict[key]
average_abnormal_return = total / len(df_dict)


print(average_abnormal_return)


for df in df_dict:
    daily_abnormal_return(df_dict[df])


# loop through each element of each list and sum the elements if elements are equal
daily_abnormal_return_list_of_lists = []
summed_daily_abnormal_return_list = []

for key in daily_abnormal_return_dict:
    daily_abnormal_return_list_of_lists.append(daily_abnormal_return_dict[key]) 
daily_abnormal_return_list_of_lists = np.array(daily_abnormal_return_list_of_lists)

summed_daily_abnormal_return_list = daily_abnormal_return_list_of_lists.sum(axis=0)

for i in range(len(summed_daily_abnormal_return_list)):
    summed_daily_abnormal_return_list[i] = summed_daily_abnormal_return_list[i] / len(df_dict)

print(summed_daily_abnormal_return_list)


#plt.plot([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5], summed_daily_abnormal_return_list)
plt.plot([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5], summed_daily_abnormal_return_list, marker='o', color='black')
plt.legend()
plt.axis([-5, 5, 0.4, 1])
plt.suptitle('Average Abnormal Return over Event Window', fontsize=18)
plt.xlabel('Days', fontsize=16)
plt.ylabel('AAR (%)', fontsize=16)
plt.show()