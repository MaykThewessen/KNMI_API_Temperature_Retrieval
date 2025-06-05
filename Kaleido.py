#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 16:59:12 2024

@author: mayk
"""

import plotly.express as px
df = px.data.iris()
fig = px.scatter(
        df, x="sepal_width", y="sepal_length", color="species"
)
fig.write_html('first_figure.html', auto_open=True)
fig.write_image("fig.pdf")



