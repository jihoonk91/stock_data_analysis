#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 23:29:50 2022

@author: jihoon
"""

import stock_data_tool
import technical_analysis_tool
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

# Pick companies to evaluate
companies = ['Abbott Laboratories', 'ABBVIE', 'Abercrombie', 'Abiomed', 'Accenture Plc']

# Get Stock Data of the companies
ticker_dict=stock_data_tool.get_ticker_dict(companies)
df=stock_data_tool.data_crawler_whole(companies)

# Parameter to save Interaction Plot as html
plot_save_location = 'D:\\'

# To draw a chart
stock_data_tool.multiple_stock_plot(df,plot_save_location)
df=technical_analysis_tool.RSI(df)

# Normalization
scaler_column=['Date','ticker','RSI']
scaler_selection='minmax'
df=stock_data_tool.scaler(df, scaler_selection, scaler_column, companies, ticker_dict)
# Draw a specific company stock RSI graph.
column_list = ['RSI']
df=df[df['ticker']=='ABT']

plt.style.use('dark_background')
plt.figure(figsize=(18,8))
plt.plot(df['Date'],df['RSI'])
plt.title('RSI',position = (0.5,1.05),fontsize = 23)
plt.xlabel('Date', fontsize = 17)
plt.ylabel('RSI Values (0 - 100)', fontsize = 17)
plt.axhline(30, ls = '--', c='y', alpha = 0.9)
plt.grid(b=True, color='DarkTurquoise', alpha=0.3, linestyle=':', linewidth=2)
plt.legend( loc='upper left', fontsize = 13)
plt.axhline(70, ls = '--', c='y', alpha = 0.9)




# Overbought - Oversold model
df_last=df[df['Date']==df['Date'].max()]
a=df_last.groupby(['ticker']).sum().reset_index()
plt.style.use('ggplot')
plt.figure(figsize=(18,8))
plt.title('Over Bought Over Sold model',position = (0.5,1.05),fontsize = 23)
for i in a['ticker'].tolist():
    plt.scatter(a[a['ticker']==i]['Close'],a[a['ticker']==i]['RSI'],label=i)

plt.xlabel('Close', fontsize = 17)
plt.ylabel('RSI Values (0 - 100)', fontsize = 17)
plt.axhline(y=50, color='r', linewidth=1)
plt.axvline(x=0.5, color='r', linewidth=1)
plt.xlim([0, 1]) 
plt.ylim([0, 100]) 


plt.text(0.75, 75, 'Over bought',
        color='Red', fontsize=15)

plt.text(0.25, 25, 'Over Sold',
        color='green', fontsize=15)


plt.legend()
plt.show()


