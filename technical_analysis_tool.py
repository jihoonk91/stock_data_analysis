#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 22:59:57 2022

@author: jihoon
"""


# Tool for techniccal analysis
import pandas as pd

def SMA(data,period = 30, column = 'Close') :
    df = data[column].rolling(window = period).mean()
    return df

# Relative Strength Index
# a momentum indicator that measures the magnitude of recent price 
# changes to analyze overbought or oversold conditions.

def RSI(data, period = 14, column = 'Close') :
    if len(data['ticker'].unique()) >2:
        data_append=pd.DataFrame()
        for i in data['ticker'].unique():
            df_part=data[data['ticker']==i]
            delta = df_part[column].diff(1).dropna()
            up = delta.copy()
            down = delta.copy()
            
            up[up < 0] = 0
            down[down > 0] = 0
            df_part['up'] = up
            df_part['down'] = down
            
            AVG_Gain = SMA(df_part, period, column = 'up')
            AVG_Loss = abs(SMA(df_part,period,column = 'down'))
            RS = AVG_Gain / AVG_Loss
            
            RSI = 100.0 - (100.0 / (1.0+RS))
            df_part['RSI'] = RSI
            data_append=data_append.append(df_part)
            
        return data_append
    else:
        delta = data[column].diff(1).dropna()
        up = down = delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        data['up'] = up
        data['down'] = down
        
        AVG_Gain = SMA(data, period, column = 'up')
        AVG_Loss = abs(SMA(data,period,column = 'down'))
        RS = AVG_Gain / AVG_Loss
        
        RSI = 100.0 - (100.0 / (1.0+RS))
        data['RSI'] = RSI
        
    return data


