# Improt libraries
import streamlit as st
import pandas as pd
import joblib

import datetime as dt
from datetime import date
import os

import numpy as np

## read in excel dataset
df = pd.read_excel("data/data.xlsx", sheet_name="Ducks")


## convert date bought col to date, and extract year into a column
df['Date_Bought'] = pd.to_datetime(df['Date_Bought']).dt.date
df['Year'] = pd.to_datetime(df['Date_Bought']).dt.year
df = df.sort_values(by=['Date_Bought'], ascending=True)

## find avg weight measure, needed for rows where more than 1 duck is included in the total weight
df['Avg_Weight'] = np.round(df.Total_Weight/df.Quantity,2)

## transform and create new dfs to find ducks bought by state, country, purchase method, buyer, year, weight, and cumulative weight
state_df = df.groupby(["Purchase_State"]).agg({"Quantity":"sum"}).reset_index()
state_df = state_df[state_df["Purchase_State"]!=""]

county_df = df.groupby(["ISO_Code","Purchase_Country"]).agg({"Quantity":"sum"}).reset_index()

purchase_method_df = df.groupby(["Purchase_Method"]).agg({"Quantity":"sum"}).reset_index()

buyer_df = df.groupby(["Buyer"]).agg({"Quantity":"sum"}).reset_index()

yearly_df = df.groupby(["Year"]).agg({"Quantity":"sum"}).reset_index()

weight_df = df.groupby(["Year"]).agg({"Total_Weight":"sum"}).reset_index()

weight_cum_df = df.groupby(['Year']).sum().cumsum().reset_index()

## insert a title for the app and instructions

st.title("Analyducks")
st.subheader("A visual analysis of Allan K's rubber duck collection")
st.subheader("A visual analysis of Allan K's rubber duck collection")

st.write(df)
# st.bar_chart(buyer_df,"Buyer", "Quantity")



