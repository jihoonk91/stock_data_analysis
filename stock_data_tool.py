#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 22:04:26 2022

@author: jihoon Kwon
"""

#Stock Data Tool using Yahoo Finance

import yfinance as yf
import pandas as pd
import yahooquery as yq
from datetime import datetime
import plotly.express as px
from sklearn.preprocessing import StandardScaler, MinMaxScaler

#If you're using spyder, required to plot on SVG file.
import plotly.io as pio
pio.renderers.default='svg'
#Else you can plot on your web browser. 
#import plotly.io as pio
#pio.renderers.default='browser'


#Using yahoo finance library to feed stock data
def data_crawler(ticker):
    df=yf.Ticker(ticker).history(period="max")
    df['ticker']=ticker
    return df

#Searching yahoo finance ticker 
def get_ticker(query, preferred_exchange='AMS'):
    try:
        data = yq.search(query)
    except ValueError: 
        print(query)
    else:
        quotes = data['quotes']
        if len(quotes) == 0:
            return 'No Ticker Found'

        symbol = quotes[0]['symbol']
        for quote in quotes:
            if quote['exchange'] == preferred_exchange:
                symbol = quote['symbol']
                break
        return symbol

#Transform a ticker list to dictionary
def get_ticker_dict(companies):    
    df = pd.DataFrame({'Company name': companies})
    df['Company symbol'] = df.apply(lambda x: get_ticker(x['Company name']), axis=1)
    df=dict(zip(df['Company name'], df['Company symbol']))
    return df

#Build a single DataFrame contains companies stock data 
def data_crawler_whole(companies):    
    df_list=pd.DataFrame()
    ticker_dict=get_ticker_dict(companies)
    for i in companies:
        df=data_crawler(ticker_dict[i])
        df_list=df_list.append(df)
    return df_list

#a=list(map(lambda x: data_crawler(ticker_dict[x]), companies))


def multiple_stock_plot(df, plot_save_location=None):
    if 'Date' not in df.columns: 
        df.reset_index(inplace=True)
    fig = px.line(df, x="Date", y=df.Close,
                  hover_data={"Date": "|%B %d, %Y"},
                  title='custom tick labels', 
                  color=df.ticker)
    fig.show()
    if plot_save_location:
        now = datetime.now().strftime("%Y%m%d")
        fig.write_html(plot_save_location+now+'.html')

def scaler(df, scaler_selection, unscale_column, companies,ticker_dict):
    if scaler_selection == 'standard':
        scaler = StandardScaler()
    elif scaler_selection =='minmax':
        scaler = MinMaxScaler()    
    
    original_columns = df.columns
    df_ticker=pd.DataFrame()
    for i in companies:
        df_seperate = df[df['ticker']==ticker_dict[i]]

        df_unscale = df_seperate[unscale_column].reset_index(drop=True)
        df_scale = df_seperate.loc[:, ~df_seperate.columns.isin(unscale_column)]
    
        df_scaled = scaler.fit_transform(df_scale)
        df_scaled = pd.DataFrame(df_scaled, columns=df_scale.columns)
        df_scaled = pd.concat([df_scaled, df_unscale], axis=1)
        
        df_ticker = df_ticker.append(df_scaled)
    df_ticker = df_ticker[original_columns]
    return df_ticker