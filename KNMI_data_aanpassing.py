import pandas as pd
import os
import requests
import io
# Setup Environment
os.system('clear')  # Clear console (Linux/MacOS)


#%% KNMI retrieve ambient temperature data Netherland De Bilt from whole year 2024

df3 = pd.read_excel('KNMI_2024_temp_adapted2.xlsx')

df3['YYYYMMDDHH'] = pd.to_datetime(df3['YYYYMMDDHH'], format='%Y%m%d%H')
df3 = df3.rename(columns={'YYYYMMDDHH': 'datetime'})
df3 = df3.set_index('datetime')

df3 = df3.resample('15T').asfreq()
df3 = df3.interpolate(method='linear')



print(df3.head())
print(df3.tail())

df3.to_excel('KNMI_2024_temp_15Min.xlsx')
