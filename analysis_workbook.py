#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 23:29:50 2022

@author: jihoon
"""

import stock_data_tool
import technical_analysis_tool
import warnings


companies = ['Abbott Laboratories', 'ABBVIE', 'Abercrombie', 'Abiomed', 'Accenture Plc']
ticker_dict=stock_data_tool.get_ticker_dict(companies)
df=stock_data_tool.data_crawler_whole(companies)

plot_save_location = 'D:\\'

stock_data_tool.multiple_stock_plot(df,plot_save_location)

df=technical_analysis_tool.RSI(df)


import matplotlib.pyplot as plt
plt.style.use('dark_background')
warnings.filterwarnings('ignore')

column_list = ['RSI']

df=df[df['ticker']=='ABT']
df[column_list].plot(figsize = (18,8))
plt.title('RSI',position = (0.5,1.05),fontsize = 23)
plt.xlabel('Close', fontsize = 17)
plt.ylabel('RSI Values (0 - 100)', fontsize = 17)
plt.axhline(30, ls = '--', c='y', alpha = 0.9)
plt.grid(b=True, color='DarkTurquoise', alpha=0.3, linestyle=':', linewidth=2)
plt.legend( loc='upper left', fontsize = 13)
plt.axhline(70, ls = '--', c='y', alpha = 0.9);


