# Improt libraries
import streamlit as st
import pandas as pd
import joblib
import altair as alt
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objs as go

import datetime as dt
from datetime import date
import os

import numpy as np

## read in excel dataset
df = pd.read_excel("data/data.xlsx", sheet_name="Ducks")


## convert date bought col to date, and extract year into a column
df['Date_Bought'] = pd.to_datetime(df['Date_Bought'],format='%Y%m%d')
df['Year'] = pd.to_datetime(df['Date_Bought'],format='%Y')
df = df.sort_values(by=['Date_Bought'], ascending=True)

## find avg weight measure, needed for rows where more than 1 duck is included in the total weight
df['Avg_Weight'] = np.round(df.Total_Weight/df.Quantity,2)

## transform and create new dfs to find ducks bought by state, country, purchase method, buyer, year, weight, and cumulative weight
state_df = df.groupby(["Purchase_State"]).agg({"Quantity":"sum"}).reset_index()
state_df = state_df[state_df["Purchase_State"]!=""]

county_df = df.groupby(["ISO_Code","Purchase_Country"]).agg({"Quantity":"sum"}).reset_index()

purchase_method_df = df.groupby(["Purchase_Method"]).agg({"Quantity":"sum"}).reset_index()

buyer_df = df.groupby(["Buyer"]).agg({"Quantity":"sum"}).reset_index()
buyer_df = buyer_df.sort_values(by=['Quantity'],ascending=True)
yearly_df = df.groupby(["Year"]).agg({"Quantity":"sum"}).reset_index()

weight_df = df.groupby(["Year"]).agg({"Total_Weight":"sum"}).reset_index()

# weight_cum_df = df.groupby(['Year']).sum().cumsum().reset_index()

## insert a title for the app and instructions

st.title("Analyducks")
st.subheader("A visual analysis of Allan K's rubber duck collection")
st.subheader("A visual analysis of Allan K's rubber duck collection")


# st.write(alt.Chart(buyer_df).mark_bar().encode(
#     x=alt.X('Buyer').sort("-y"),
#     y=alt.Y('Quantity'),
# ))


owner_bar = px.bar(buyer_df,x="Buyer", y="Quantity")
owner_bar.update_layout(title_text="Rubber Duck Distribution by Purchaser", 
                        title_x=0.3,
                        xaxis_title="Purchaser", 
                        yaxis_title="Quantity",
                        paper_bgcolor="rgba(0,0,0,0)",
                        )

st.plotly_chart(owner_bar, use_container_width=True)



