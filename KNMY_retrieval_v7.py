#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 13:44:10 2024
@author: mayk
"""
#%% Sources and manuals used:
# https://github.com/EnergieID/KNMI-py
# https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script
# https://www.daggegevens.knmi.nl/klimatologie/uurgegevens


#%% Retrieve KNMI data through API
from knmy import knmy
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import os
os.system('clear')

start   = '20180101'
end     = '20251027'
variables_selected = ['TEMP']
inseason=False
parse=True

stations_selected1 = [260] # De Bilt
disclaimer, stations1, variables, data_260 = knmy.get_hourly_data(stations=stations_selected1, start=start, end=end,inseason=inseason, variables=variables_selected, parse=parse)

stations_selected2 = [380] # Maastricht
disclaimer, stations2, variables, data_380 = knmy.get_hourly_data(stations=stations_selected2, start=start, end=end,inseason=inseason, variables=variables_selected, parse=parse)



# 1. Read the CSV data without parsing dates
df = data_260
df['TD'] = df['TD'] / 10  # Convert temperature to Celsius
df['T'] = df['T'] / 10  # Convert temperature to Celsius
df['T_260'] = df['T']

df = df.drop('STN', axis=1)
df = df.drop('T10N', axis=1)

#combine two dataframes, where df2.T is put into df.T_380
df2 = data_380
df['T_380'] = df2['T']/10

# 2. Combine 'YYYYMMDD' and 'HH' to create a datetime column
df['datetime'] = df['YYYYMMDD'].astype(str) + (df['HH'].astype(int) - 1).astype(str).str.zfill(2) + '00'  # Subtract 1 from HH, Adding '00' for minutes and seconds
df['datetime'] = pd.to_datetime(df['datetime'], format='%Y%m%d%H%M%S', utc=True).dt.tz_convert('Europe/Amsterdam') - pd.Timedelta(hours=1) # Convert from UTC to CET timezone (Europe/Amsterdam handles CET/CEST automatically)

df = df.set_index('datetime')
print(df)

df = df.drop(['YYYYMMDD', 'HH'], axis=1)

# Save data to excel
output_filename = f"KNMI_data_{stations_selected1}_{start}_{end}.csv"
df[['T']].to_csv(output_filename, index=True)
print(f"Data saved to {output_filename}")

print(df[['T']])
print(df[['T']].describe().round(1))


