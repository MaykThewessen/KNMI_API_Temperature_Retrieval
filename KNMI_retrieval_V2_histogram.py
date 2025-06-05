#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 13:44:10 2024

@author: mayk
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 12:13:31 2024

@author: mayk
"""
# https://github.com/EnergieID/KNMI-py
# https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script

#%% Retrieve KNMI data through API
import knmi

start   = '2023010101'
end     = '2023123101'
stations = [260]
#variables = 'TN:FG:'

#df= knmi.get_day_data_dataframe(stations, start, end)
#df = knmi.get_hour_data_dataframe(stations, start, end, inseason, variables)
df = knmi.get_hour_data_dataframe(stations, start, end)

# Show all stations information: knmi.stations
# station: 260 = De Bilt, 138 en 380 = Maastricht, 616 = Amsterdam, 250 = Terschelling, 

# print(df.disclaimer)
# print(df.stations)
# print(df.legend)

# df = df.rename(columns=df.legend)

# print(df)

#%% Plot
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from math import *

import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats('svg') # ('svg', 'png')
# import matplotlib as mpl
# mpl.rcParams['figure.dpi'] = 400



fig, ax = plt.subplots() #(dpi=600)


plt.plot(df["TN"]/10)    # , linewidth='0.2')
plt.plot(df["TG"]/10)    # , linewidth='0.2')
plt.plot(df["TX"]/10)    # , linewidth='0.2')
# plt.gca().invert_xaxis()

# ax.set_xlim([datetime.date(2024, 1, 1), datetime.date(2024, 1, 30)])
# ax.set_ylim([-3, 15])
# plt.ylim(1,15)
fig.autofmt_xdate()  # sets date ticks schuin onder x-as


plt.xlabel('Date')  # string must be enclosed with quotes '  '
plt.ylabel('Temperature')
plt.title(['KNMI station data, date range: '+start+'-'+end])
plt.legend(['T min','T avg','T max']) # legend entries as seperate strings in a list
plt.grid(True)


#%% Calculate Histogram
from matplotlib import colors

fig, axs = plt.subplots(1, 1)

# the histogram of the data 
data = df["TG"]/10
binwidth = 2
N, bins, patches = plt.hist(data,
                            bins=np.arange(min(data), max(data), 2).tolist(),# list(range(-20,45)),
                            edgecolor='black',
                            linewidth=0.5,
                            #density = True, 
                            # facecolor ='b', 
                            #alpha = 0.75
                            ) 
# Set grid lines
plt.grid(True)

# Ensure grid lines are drawn below the bars
plt.gca().set_axisbelow(True)  

# We'll color code by height, but you could use any scalar
fracs = N / N.max()

# we need to normalize the data to 0..1 for the full range of the colormap
norm = colors.Normalize(fracs.min(), fracs.max())

# Now, we'll loop through our objects and set the color of each accordingly
for thisfrac, thispatch in zip(fracs, patches):
    color = plt.cm.viridis(norm(thisfrac))
    thispatch.set_facecolor(color)


# Now we format the y-axis to display percentage
# axs.yaxis.set_major_formatter(PercentFormatter(ymax=100))
# manipulate
vals = axs.get_yticks()
axs.set_yticks(axs.get_yticks().tolist())
axs.set_yticklabels(['{:,.0%}'.format(x/100) for x in vals])

plt.ylabel('Ocurance')  # string must be enclosed with quotes '  '
plt.xlabel('Temperature')
plt.title(['KNMI station data'])
plt.legend(['T min'])


