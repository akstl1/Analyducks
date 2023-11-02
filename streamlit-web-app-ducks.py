# Improt libraries
import streamlit as st
import pandas as pd
# import joblib
# import altair as alt
# import plotly.figure_factory as ff
import plotly.express as px
# import plotly.graph_objs as go

import datetime as dt
from datetime import date
# import os

import numpy as np

# from streamlit_card import card

## read in excel dataset
df = pd.read_excel("data/data.xlsx", sheet_name="Ducks")

## convert date bought col to date, and extract year into a column
df['Date_Bought'] = pd.to_datetime(df['Date_Bought'],format='%m/%d/%Y').dt.date
# df['Year'] = pd.to_datetime(df['Date_Bought'],format='%Y')
df['Year'] = pd.DatetimeIndex(df['Date_Bought']).year
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

weight_cum_df = df.groupby(['Year']).sum().cumsum().reset_index()

## insert a title for the app and instructions
st.set_page_config(page_title="Analyducks", layout="wide")
st.title("Analyducks")
st.subheader("A visual analysis of Allan K's rubber duck collection")
st.write("[Click here to view my portfolio](https://akstl1.github.io/)")


## calcs for KPI cards

# weight KPI
duck_weight = df["Total_Weight"].sum()

# total ducks bought KPI
total_ducks = df["Quantity"].sum()

# unique purchase countries KPI
unique_countries = df.Purchase_Country.nunique()

# unique purchase cities KPI
unique_cities = df.Purchase_City.nunique()

# ducks bought within last year KPI
today = date.today()
today_yr = today.year
today_day = today.day
today_month = today.month
ducks_bought_last_year = df[df["Date_Bought"]>=dt.date(today_yr-1,today_month,today_day)].Quantity.sum()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Weight",total_ducks)
col2.metric("Total Bought",duck_weight)
col3.metric("Weight",unique_countries)
col4.metric("Weight",unique_cities)
col5.metric("Weight",ducks_bought_last_year)


owner_bar = px.bar(buyer_df,x="Buyer", y="Quantity")
owner_bar.update_layout(title_text="Rubber Duck Distribution by Purchaser", 
                        title_x=0.3,
                        xaxis_title="Purchaser", 
                        yaxis_title="Quantity",
                        paper_bgcolor="rgba(0,0,0,0)",
                        )

st.plotly_chart(owner_bar, use_container_width=True)

## pie chart showing purchase method of ducks

purchase_fig = px.pie(purchase_method_df, values='Quantity', names='Purchase_Method')
purchase_fig.update_layout(title_text="Purchase Method Distribution",
                           title_x=0.5,
                           paper_bgcolor="rgba(0,0,0,0)"
                           )

st.plotly_chart(purchase_fig, use_container_width=True)

## 3d scatter of length, height, width

three_d_fig = px.scatter_3d(df, x='Length', 
                            y='Width', 
                            z="Height",
                            size='Avg_Weight',
                            color='Avg_Weight',
                            labels={'Avg_Weight':'Avg. Weight'}
                            )

three_d_fig.update_layout(title_text="Rubber Duck Length vs Width vs Height (cm)",
                          title_x=0.5,
                          paper_bgcolor="rgba(0,0,0,0)"
                          )
camera = dict(
    eye=dict(x=0, y=2, z=1),
    # up=dict(x=1, y=1, z=0),
)

# camera = dict(
#     center=dict(x=0, y=0, z=0))

three_d_fig.update_layout(scene_camera=camera)

st.plotly_chart(three_d_fig, use_container_width=True)

## bar plot showing weight of ducks bought each year, cumulative

weight_bar_cumulative = px.bar(weight_cum_df,x="Year", y="Total_Weight")
weight_bar_cumulative.update_layout(title_text="Cumulative Collection Weight (g)",
                                    title_x=0.5,
                                    xaxis_title="Purchase Year", 
                                    yaxis_title="Cumulative Weight (g)",
                                    paper_bgcolor="rgba(0,0,0,0)"
                                    )

st.plotly_chart(weight_bar_cumulative, use_container_width=True)

## bar plot showing number of ducks bought per year 

year_bar = px.bar(yearly_df,x="Year", y="Quantity")
year_bar.update_layout(title_text="Rubber Ducks Bought Per Year", 
                       title_x=0.5,
                       xaxis_title="Purchase Year",
                       yaxis_title="Quantity",
                       paper_bgcolor="rgba(0,0,0,0)"
                       )

st.plotly_chart(year_bar, use_container_width=True)

## bar plot showing number of ducks bought per year, cumulative

year_bar_cumulative = px.bar(weight_cum_df,x="Year", y="Quantity")
year_bar_cumulative.update_layout(title_text="Total Rubber Ducks Owned",
                                  title_x=0.5,
                                  xaxis_title="Purchase Year", 
                                  yaxis_title="Quantity",
                                  paper_bgcolor="rgba(0,0,0,0)"
                                  )

st.plotly_chart(year_bar_cumulative, use_container_width=True)

# st.plotly_chart(year_bar_cumulative, use_container_width=True)

map_fig = px.scatter_geo(df,
        lon = 'Longitude',
        lat = 'Latitude',
        hover_name="Name"      
        )

map_fig.update_traces(marker=dict(color="Red"))

# st.plotly_chart(map_fig, use_container_width=True)

## choropleth showing duck purchase by country

country_fig = px.choropleth(county_df, locations="ISO_Code",
                    color="Quantity", 
                    hover_name="Purchase_Country"
                    # color_continuous_scale="YlGn"
                    )
country_fig.add_trace(map_fig.data[0])

country_fig.update_geos(
    visible=True, resolution=50, scope="world", showcountries=True, countrycolor="Black"
)
country_fig.update_geos(projection_type="natural earth")
country_fig.update_layout(title_text="Rubber Duck Purchase By Country",title_x=0.5,width=1000)

st.plotly_chart(country_fig, use_container_width=True)

## choropleth showing duck purchase by US state

state_fig = px.choropleth(state_df,locations="Purchase_State", 
                          locationmode="USA-states", 
                          color="Quantity", 
                          scope="usa"
                        #   color_continuous_scale="YlGn"
                          )
state_fig.update_layout(title_text="Rubber Duck Purchase By State",title_x=0.5)
state_fig.add_trace(map_fig.data[0])

st.plotly_chart(state_fig, use_container_width=True)

st.write(df[["Name","Purchase_City","Purchase_Country","Date_Bought","About Me","Total_Weight","Height","Width","Length"]])

# hasClicked = card(
#   title="Hello World!",
#   text="Some description",
#   image="http://placekitten.com/200/300",
#   url="https://github.com/gamcoh/st-card"
# )


# res = card(
#     title="Streamlit Card",
#     text="This is a test card",
#     image="https://placekitten.com/500/500",
#     styles={
#         "card": {
#             "width": "30%",
#             "height": "500px",
#             "border-radius": "60px",
#             "box-shadow": "0 0 10px rgba(0,0,0,0.5)"
#         },
#         "text": {
#             "font-family": "serif"
#         }
#     }
# )


# cols = st.columns(3,gap="small")

# for i, x in enumerate(cols):
#     x.selectbox(f"Input # {i}",[1,2,3], key=i)
 
img_nm = "DuckFamily.jpg"    
names = [i for i in df['Name']]   
desc = [i for i in df['About Me']]     
ducks = len(df['Quantity'])
n_cols=5
n_rows=int(1+ducks//n_cols)
rows = [st.columns(n_cols,gap="small") for _ in range(n_rows)]
cols = [column for row in rows for column in row]
st.write(n_rows)
for col,i,d in zip(cols,names,desc):
    col.image("./img/DuckFamily.jpg")
    col.subheader(i)
    col.write(d)
    # with col:
    #     res=card(
    #         title=i,
    #         text=d,
    #         image="https://placekitten.com/500/500",
    #         on_click=lambda: print("Clicked!"),
    #         styles={
    #             "card": {
    #                 "width": "100%",
    #                 "height": "200px",
    #                 "border-radius": "2px",
    #                 "padding": "5px",
    #                 "box-shadow": "0 0 10px rgba(0,0,0,0.5)"
    #             },
    #             "text": {
    #                 "font-family": "serif"
    #             },
    #             "title": {
    #                 "font-size":"10px"
    #                 }
    #         }
    #     )

css='''
<style>
    section.main>div {
        padding-bottom: 1rem;
    }
    [data-testid="column"]>div>div>div>div>div {
        overflow: auto;
        height: 70vh;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)
