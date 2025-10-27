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
# https://daggegevens.knmi.nl/klimatologie/uurgegevens

#%% Retrieve KNMI data through API
from knmy import knmy
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import pytz

start   = '20240817' 
end     = '20250816' 
variables_selected = ['TEMP']
inseason=False
parse=True

stations_selected = [260] # De Bilt
disclaimer, stations, variables, data_260 = knmy.get_hourly_data(stations=stations_selected, start=start, end=end,inseason=inseason, variables=variables_selected, parse=parse)

# Check if we got any data
if data_260 is None or data_260.empty:
    print("Error: No data returned from KNMI API for station 260")
    print("This could be due to:")
    print("1. Invalid date range")
    print("2. No data available for the specified period")
    print("3. API issues")
    exit(1)

# Debug: Check the structure of the returned data
print("Data 260 structure:")
print(data_260.head())
print("\nData 260 columns:")
print(data_260.columns)
print("\nData 260 shape:")
print(data_260.shape)

# Print all rows to see the actual content
print("\nAll rows in data_260:")
for idx, row in data_260.iterrows():
    print(f"Row {idx}: {row.to_dict()}")

# Based on the output, row 11 contains the actual column headers
# and data starts from row 12
header_row_idx = 11
print(f"\nUsing row {header_row_idx} as header row")
print("Header row:", data_260.iloc[header_row_idx])

# Extract data starting from the row after the header
data_260_clean = data_260.iloc[header_row_idx + 1:].copy()

# Set the correct column names from the header row
new_columns = data_260.iloc[header_row_idx].tolist()
# Clean up column names (remove any '#' symbols and get the actual column names)
# The actual column names are: STN, YYYYMMDD, HH, T, T10N, TD
new_columns = ['STN', 'YYYYMMDD', 'HH', 'T', 'T10N', 'TD']
print(f"New column names: {new_columns}")

# Set the new column names
data_260_clean.columns = new_columns

# Reset index
data_260_clean = data_260_clean.reset_index(drop=True)

print(f"\nAfter extracting data - Data 260 shape: {data_260_clean.shape}")
print("Data 260 clean structure:")
print(data_260_clean.head())

# Check if we have valid data
if data_260_clean.empty:
    print("Warning: No valid data found!")
    print("Original data sample:")
    print(data_260.head(20))
    exit(1)

# 1. Read the CSV data without parsing dates
df = data_260_clean.copy()
# Convert temperature columns to numeric, handling any non-numeric values
df['Tdew'] = pd.to_numeric(df['TD'], errors='coerce') / 10  # Convert temperature to Celsius
df['Tair'] = pd.to_numeric(df['T'], errors='coerce') / 10  # Convert temperature to Celsius
df['T_260'] = df['Tair']

df = df.drop('STN', axis=1)
df = df.drop('T10N', axis=1)

# 2. Combine 'YYYYMMDD' and 'HH' to create a datetime column
# First, drop rows with missing values in critical columns
df = df.dropna(subset=['YYYYMMDD', 'HH'])

# Now create datetime column
df['datetime'] = df['YYYYMMDD'].astype(str) + (df['HH'].astype(int) - 1).astype(str).str.zfill(2) + '00'  # Subtract 1 from HH, Adding '00' for minutes and seconds
df['datetime'] = pd.to_datetime(df['datetime'], format='%Y%m%d%H%M%S')

# Convert to Amsterdam timezone (Europe/Amsterdam)
amsterdam_tz = pytz.timezone('Europe/Amsterdam')
df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert(amsterdam_tz)

df = df.set_index('datetime')
print(df)

# Save data to CSV
output_filename = f"KNMI_data_{stations['name'][260]}_{variables_selected}_{start}_{end}.csv"
df.to_csv(output_filename)
print(f"Data saved to {output_filename}")

# Show all stations information: knmi.stations
# station: 260 = De Bilt, 138 en 380 = Maastricht, 616 = Amsterdam, 250 = Terschelling, 

# print(disclaimer)
# print(stations)
# print(variables)
# print(data)
# print(df.legend)

#%% Plotly HTML plotting
# Create subplots
fig = make_subplots(rows=2, cols=1, subplot_titles=(
    "Hourly Temperature and Dew Point over time",
    f"De Bilt: Tair Max: {df['T_260'].max():.1f}°C, Min: {df['T_260'].min():.1f}°C, Avg: {df['T_260'].mean():.1f}°C<br>Tdew Max: {df['Tdew'].max():.1f}°C, Min: {df['Tdew'].min():.1f}°C, Avg: {df['Tdew'].mean():.1f}°C<br><br>"
    f"Temperature Distribution"
))

# Temperature over time plot
fig.add_trace(go.Scatter(x=df.index, y=df["T_260"], mode='lines', name=f"Air Temperature at Station: {stations['name'][260]}"), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df["Tdew"], mode='lines', name=f"Dew Point Temperature at Station: {stations['name'][260]}"), row=1, col=1)

fig.update_xaxes(title_text="Date", row=1, col=1)
fig.update_yaxes(title_text="Temperature [°C]", row=1, col=1)

# Histogram plot
data_hist1 = df["T_260"]
data_hist2 = df["Tdew"]
fig.add_trace(go.Histogram(x=data_hist1, name=f"Air Temperature at Station: {stations['name'][260]}", autobinx=False, xbins=dict(start=min(data_hist1), end=max(data_hist1), size=2.0), histnorm='', opacity=0.7), row=2, col=1)
fig.add_trace(go.Histogram(x=data_hist2, name=f"Dew Point Temperature at Station: {stations['name'][260]}", autobinx=False, xbins=dict(start=min(data_hist2), end=max(data_hist2), size=2.0), histnorm='', opacity=0.7), row=2, col=1)

fig.update_xaxes(title_text="Temperature [°C]", row=2, col=1)
fig.update_yaxes(title_text="Ocurrence [hours/year]", row=2, col=1) # , tickformat=".0%"

fig.update_layout(title_text=f"KNMI Station Data, Date Range: {start}-{end}", title_x=0.5)

# Save figure to html
output_filename = f"KNMI_data_{stations['name'][260]}_{variables_selected}_{start}_{end}.html"
fig.write_html(output_filename, auto_open=True)
print(f"Data and plots saved to {output_filename}")