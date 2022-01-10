#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 17:13:41 2022

@author: Louis
"""
import streamlit as st
import pandas as pd
from gsheetsdb import connect

st.write("My First Streamlit Web App")

df = pd.DataFrame({"one": [1, 2, 3], "two": [4, 5, 6], "three": [7, 8, 9]})
st.write(df)

st.title("Connect to Google Sheets")
gsheet_url = "https://docs.google.com/spreadsheets/d/1lzBX_abeF44H0HX9jy-AIfq1Hgf-AXU4p4uuEeD9624/edit?usp=sharing"
conn = connect()
rows = conn.execute(f'SELECT * FROM "{gsheet_url}"')
df_gsheet = pd.DataFrame(rows)
st.write(df_gsheet)
