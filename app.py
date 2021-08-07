#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pymysql
import streamlit as st
from datetime import datetime
import plotly.express as px 
from dataprocessor import get_config

db = get_config()

def query_db(sql: str, db = db):

    with pymysql.connect(**db) as conn:

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a command: this creates a new table
        cur.execute(sql)

        # Obtain data
        data = cur.fetchall()
        
        column_names = [desc[0] for desc in cur.description]

        conn.commit()

        # Close the cursor
        cur.close()

        df = pd.DataFrame(data=data, columns=column_names)

        return df

def risk_level(x):
    '''
    convert confirmed numbers to a category num, which is specified the risk level.
    '''
    if x > 0 and x <= 1000:
        output = 1
    elif x < 10000:
        output = 2
    elif x < 50000:
        output = 3
    elif x < 100000:
        output = 4
    elif x < 500000:
        output = 5
    elif x < 1000000:
        output = 6
    else:
        output = 7
    return output 


# select us covid19 data from postgresql, and convert it into pandas dataframe
df_us_latest = query_db("select * from covid19_us where report_date = (select max(report_date) from covid19_us)")
df_us_latest['risk_level'] = df_us_latest['confirmed'].apply(lambda x: risk_level(x))
fig1 = px.scatter_mapbox(df_us_latest, lat='lat', lon='lon', hover_name='province_state', hover_data=['confirmed','deaths','report_date'],
                        color_discrete_sequence=["fuchsia"], zoom=3, title="US Covid19", 
                        color='risk_level', mapbox_style="open-street-map")


st.plotly_chart(fig1)



