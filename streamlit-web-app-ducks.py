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
# import dash_bootstrap_components as dbc


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
st.markdown("<h1 style='text-align: center;'>Analyducks</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>A visual analysis of Allan K's rubber duck collection</h1>", unsafe_allow_html=True)
st.markdown(
    """<a style='display: block; text-align: center;' href="https://akstl1.github.io/">Click here to view my portfolio</a>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    
    .st-emotion-cache-j5r0tf {
        background-color: #000000;
        }
    </style>
    """, 
    unsafe_allow_html=True
    
    )
# <div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="157.7624969482422" data-testid="stVerticalBlock" class="st-emotion-cache-9xwmxx e1f1d6gn1"><div data-stale="false" width="157.7624969482422" class="element-container st-emotion-cache-az4wv8 e1f1d6gn3" data-testid="element-container"><div data-testid="stMetric"><label data-testid="stMetricLabel" visibility="0" class="st-emotion-cache-1tenn4l e1i5pmia2"><div class="st-emotion-cache-1wivap2 e1i5pmia3"><div data-testid="stMarkdownContainer" class="st-emotion-cache-xujc5b e1nzilvr5"><p>Total Ducks Owned</p></div></div></label><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e1i5pmia1"><div class="st-emotion-cache-1wivap2 e1i5pmia3"> 133 </div></div></div></div></div></div></div>
# <div data-testid="stHorizontalBlock" class="st-emotion-cache-ocqkz7 e1f1d6gn4"><div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="157.7624969482422" data-testid="stVerticalBlock" class="st-emotion-cache-9xwmxx e1f1d6gn1"><div data-stale="false" width="157.7624969482422" class="element-container st-emotion-cache-az4wv8 e1f1d6gn3" data-testid="element-container"><div data-testid="stMetric"><label data-testid="stMetricLabel" visibility="0" class="st-emotion-cache-1tenn4l e1i5pmia2"><div class="st-emotion-cache-1wivap2 e1i5pmia3"><div data-testid="stMarkdownContainer" class="st-emotion-cache-xujc5b e1nzilvr5"><p>Total Ducks Owned</p></div></div></label><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e1i5pmia1"><div class="st-emotion-cache-1wivap2 e1i5pmia3"> 133 </div></div></div></div></div></div></div><div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="157.7624969482422" data-testid="stVerticalBlock" class="st-emotion-cache-9xwmxx e1f1d6gn1"><div data-stale="false" width="157.7624969482422" class="element-container st-emotion-cache-az4wv8 e1f1d6gn3" data-testid="element-container"><div data-testid="stMetric"><label data-testid="stMetricLabel" visibility="0" class="st-emotion-cache-1tenn4l e1i5pmia2"><div class="st-emotion-cache-1wivap2 e1i5pmia3"><div data-testid="stMarkdownContainer" class="st-emotion-cache-xujc5b e1nzilvr5"><p>Ducks Bought Within Last Year</p></div></div></label><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e1i5pmia1"><div class="st-emotion-cache-1wivap2 e1i5pmia3"> 78 </div></div></div></div></div></div></div><div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="157.7624969482422" data-testid="stVerticalBlock" class="st-emotion-cache-9xwmxx e1f1d6gn1"><div data-stale="false" width="157.7624969482422" class="element-container st-emotion-cache-az4wv8 e1f1d6gn3" data-testid="element-container"><div data-testid="stMetric"><label data-testid="stMetricLabel" visibility="0" class="st-emotion-cache-1tenn4l e1i5pmia2"><div class="st-emotion-cache-1wivap2 e1i5pmia3"><div data-testid="stMarkdownContainer" class="st-emotion-cache-xujc5b e1nzilvr5"><p>Duck Collection Weight (g)</p></div></div></label><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e1i5pmia1"><div class="st-emotion-cache-1wivap2 e1i5pmia3"> 5209.2 </div></div></div></div></div></div></div><div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="157.7624969482422" data-testid="stVerticalBlock" class="st-emotion-cache-9xwmxx e1f1d6gn1"><div data-stale="false" width="157.7624969482422" class="element-container st-emotion-cache-az4wv8 e1f1d6gn3" data-testid="element-container"><div data-testid="stMetric"><label data-testid="stMetricLabel" visibility="0" class="st-emotion-cache-1tenn4l e1i5pmia2"><div class="st-emotion-cache-1wivap2 e1i5pmia3"><div data-testid="stMarkdownContainer" class="st-emotion-cache-xujc5b e1nzilvr5"><p>Unique Countries of Purchase</p></div></div></label><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e1i5pmia1"><div class="st-emotion-cache-1wivap2 e1i5pmia3"> 8 </div></div></div></div></div></div></div><div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="157.7624969482422" data-testid="stVerticalBlock" class="st-emotion-cache-9xwmxx e1f1d6gn1"><div data-stale="false" width="157.7624969482422" class="element-container st-emotion-cache-az4wv8 e1f1d6gn3" data-testid="element-container"><div data-testid="stMetric"><label data-testid="stMetricLabel" visibility="0" class="st-emotion-cache-1tenn4l e1i5pmia2"><div class="st-emotion-cache-1wivap2 e1i5pmia3"><div data-testid="stMarkdownContainer" class="st-emotion-cache-xujc5b e1nzilvr5"><p>Unique Cities of Purchase</p></div></div></label><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e1i5pmia1"><div class="st-emotion-cache-1wivap2 e1i5pmia3"> 40 </div></div></div></div></div></div></div></div>
# <div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="852.7999877929688" data-testid="stVerticalBlock" class="st-emotion-cache-pplk8x e1f1d6gn1"><div data-testid="stHorizontalBlock" class="st-emotion-cache-ocqkz7 e1f1d6gn4"><div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="157.7624969482422" data-testid="stVerticalBlock" class="st-emotion-cache-9xwmxx e1f1d6gn1"><div data-stale="false" width="157.7624969482422" class="element-container st-emotion-cache-az4wv8 e1f1d6gn3" data-testid="element-container"><div data-testid="stMetric"><label data-testid="stMetricLabel" visibility="0" class="st-emotion-cache-1tenn4l e1i5pmia2"><div class="st-emotion-cache-1wivap2 e1i5pmia3"><div data-testid="stMarkdownContainer" class="st-emotion-cache-xujc5b e1nzilvr5"><p>Total Ducks Owned</p></div></div></label><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e1i5pmia1"><div class="st-emotion-cache-1wivap2 e1i5pmia3"> 133 </div></div></div></div></div></div></div><div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="157.7624969482422" data-testid="stVerticalBlock" class="st-emotion-cache-9xwmxx e1f1d6gn1"><div data-stale="false" width="157.7624969482422" class="element-container st-emotion-cache-az4wv8 e1f1d6gn3" data-testid="element-container"><div data-testid="stMetric"><label data-testid="stMetricLabel" visibility="0" class="st-emotion-cache-1tenn4l e1i5pmia2"><div class="st-emotion-cache-1wivap2 e1i5pmia3"><div data-testid="stMarkdownContainer" class="st-emotion-cache-xujc5b e1nzilvr5"><p>Ducks Bought Within Last Year</p></div></div></label><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e1i5pmia1"><div class="st-emotion-cache-1wivap2 e1i5pmia3"> 78 </div></div></div></div></div></div></div><div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="157.7624969482422" data-testid="stVerticalBlock" class="st-emotion-cache-9xwmxx e1f1d6gn1"><div data-stale="false" width="157.7624969482422" class="element-container st-emotion-cache-az4wv8 e1f1d6gn3" data-testid="element-container"><div data-testid="stMetric"><label data-testid="stMetricLabel" visibility="0" class="st-emotion-cache-1tenn4l e1i5pmia2"><div class="st-emotion-cache-1wivap2 e1i5pmia3"><div data-testid="stMarkdownContainer" class="st-emotion-cache-xujc5b e1nzilvr5"><p>Duck Collection Weight (g)</p></div></div></label><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e1i5pmia1"><div class="st-emotion-cache-1wivap2 e1i5pmia3"> 5209.2 </div></div></div></div></div></div></div><div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="157.7624969482422" data-testid="stVerticalBlock" class="st-emotion-cache-9xwmxx e1f1d6gn1"><div data-stale="false" width="157.7624969482422" class="element-container st-emotion-cache-az4wv8 e1f1d6gn3" data-testid="element-container"><div data-testid="stMetric"><label data-testid="stMetricLabel" visibility="0" class="st-emotion-cache-1tenn4l e1i5pmia2"><div class="st-emotion-cache-1wivap2 e1i5pmia3"><div data-testid="stMarkdownContainer" class="st-emotion-cache-xujc5b e1nzilvr5"><p>Unique Countries of Purchase</p></div></div></label><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e1i5pmia1"><div class="st-emotion-cache-1wivap2 e1i5pmia3"> 8 </div></div></div></div></div></div></div><div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="157.7624969482422" data-testid="stVerticalBlock" class="st-emotion-cache-9xwmxx e1f1d6gn1"><div data-stale="false" width="157.7624969482422" class="element-container st-emotion-cache-az4wv8 e1f1d6gn3" data-testid="element-container"><div data-testid="stMetric"><label data-testid="stMetricLabel" visibility="0" class="st-emotion-cache-1tenn4l e1i5pmia2"><div class="st-emotion-cache-1wivap2 e1i5pmia3"><div data-testid="stMarkdownContainer" class="st-emotion-cache-xujc5b e1nzilvr5"><p>Unique Cities of Purchase</p></div></div></label><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e1i5pmia1"><div class="st-emotion-cache-1wivap2 e1i5pmia3"> 40 </div></div></div></div></div></div></div></div></div></div>
###################### KPI Calcs ##############################

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

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Ducks Owned",total_ducks)
    col2.metric("Ducks Bought Within Last Year",ducks_bought_last_year)
    col3.metric("Duck Collection Weight (g)",duck_weight)
    col4.metric("Unique Countries of Purchase",unique_countries)
    col5.metric("Unique Cities of Purchase",unique_cities)

# css='''
# [data-testid="stMetric"] {
#     color: #212529;
#     background-color: #f8f9fa;
#     width: 75%;
#     margin: auto;
#     padding: 1rem 1rem;
#     border-radius: 0.25rem
# }

# [data-testid="stMetric"] > div {
#     color: #212529;
#     background-color: #f8f9fa;
#     width: fit-content;
#     margin: auto;
# }


# [data-testid="stMetric"] label {
#     color: #212529;
#     background-color: #f8f9fa;
#     width: fit-content;
#     margin: auto;
# }
# '''

# st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)
# st.markdown('''
# <style>
# /*center metric label*/
# [data-testid="stMetricLabel"] > div:nth-child(1) {
#     justify-content: center;
# }

# /*center metric value*/
# [data-testid="stMetricValue"] > div:nth-child(1) {
#     justify-content: center;
# }
# </style>
# ''', unsafe_allow_html=True)

###################### General Data graphs ##############################




## pie chart showing purchase method of ducks

purchase_fig = px.pie(purchase_method_df, values='Quantity', names='Purchase_Method')
purchase_fig.update_layout(title_text="Purchase Method Distribution",
                           title_x=0.2,
                           paper_bgcolor="rgb(235,204,52)",
                           plot_bgcolor="rgb(206,212,218)",
                           font=dict(color="black")
                           )

# st.plotly_chart(purchase_fig, use_container_width=True)

owner_bar = px.bar(buyer_df,x="Buyer", y="Quantity")
owner_bar.update_layout(title_text="Rubber Duck Distribution by Purchaser", 
                        title_x=0.2,
                        xaxis_title="Purchaser", 
                        yaxis_title="Quantity",
                        paper_bgcolor="rgb(235,204,52)",
                        plot_bgcolor="rgb(206,212,218)",
                        font=dict(color="black")
                        )

# st.plotly_chart(owner_bar, use_container_width=True)

## 3d scatter of length, height, width

three_d_fig = px.scatter_3d(df, x='Length', 
                            y='Width', 
                            z="Height",
                            size='Avg_Weight',
                            color='Avg_Weight',
                            labels={'Avg_Weight':'Avg. Weight'}
                            )

three_d_fig.update_layout(title_text="Rubber Duck Length vs Width vs Height (cm)",
                          title_x=0.2,
                          paper_bgcolor="rgb(235,204,52)",
                          plot_bgcolor="rgb(255,0,0)",
                          font=dict(color="black")
                          )
camera = dict(
    eye=dict(x=0, y=2, z=1),
    # up=dict(x=1, y=1, z=0),
)

# camera = dict(
#     center=dict(x=0, y=0, z=0))

three_d_fig.update_layout(scene_camera=camera)

gen1,gen2,gen3 = st.columns(3)
gen1.plotly_chart(purchase_fig, use_container_width=True,theme=None)
gen2.plotly_chart(owner_bar, use_container_width=True,theme=None)
gen3.plotly_chart(three_d_fig, use_container_width=True,theme=None)

###################### Purchase and weight graphs ##############################

## bar plot showing number of ducks bought per year 

year_bar = px.bar(yearly_df,x="Year", y="Quantity")
year_bar.update_layout(title_text="Rubber Ducks Bought Per Year", 
                       title_x=0.3,
                       xaxis_title="Purchase Year",
                       yaxis_title="Quantity",
                       paper_bgcolor="rgba(0,0,0,0)"
                       )

# st.plotly_chart(year_bar, use_container_width=True)

## bar plot showing number of ducks bought per year, cumulative

year_bar_cumulative = px.line(weight_cum_df,x="Year", y="Quantity")
year_bar_cumulative.update_layout(title_text="Total Rubber Ducks Owned",
                                  title_x=0.3,
                                  xaxis_title="Purchase Year", 
                                  yaxis_title="Quantity",
                                  paper_bgcolor="rgba(0,0,0,0)"
                                  )

# st.plotly_chart(year_bar_cumulative, use_container_width=True)


## bar plot showing weight of ducks bought each year

weight_bar = px.bar(weight_df,x="Year", y="Total_Weight")
weight_bar.update_layout(title_text="Weight (g) of Annual Purchases",
                         title_x=0.3,
                         xaxis_title="Purchase Year",
                         yaxis_title="Weight (g)",
                         paper_bgcolor="rgba(0,0,0,0)"
                         )

# st.plotly_chart(weight_bar, use_container_width=True)


## bar plot showing weight of ducks bought each year, cumulative

weight_bar_cumulative = px.line(weight_cum_df,x="Year", y="Total_Weight")
weight_bar_cumulative.update_layout(title_text="Cumulative Collection Weight (g)",
                                    title_x=0.3,
                                    xaxis_title="Purchase Year", 
                                    yaxis_title="Cumulative Weight (g)",
                                    paper_bgcolor="rgba(0,0,0,0)"
                                    )

# st.plotly_chart(weight_bar_cumulative, use_container_width=True)

purchase1,purchase2 = st.columns(2)
purchase1.plotly_chart(year_bar, use_container_width=True,theme=None)
purchase2.plotly_chart(year_bar_cumulative, use_container_width=True,theme=None)

weight1,weight2 = st.columns(2)
weight1.plotly_chart(weight_bar, use_container_width=True,theme=None)
weight2.plotly_chart(weight_bar_cumulative, use_container_width=True,theme=None)


###################### Mapping graphs ##############################


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
country_fig.update_layout(title_text="Rubber Duck Purchase By Country",title_x=0.3,width=1000)

# st.plotly_chart(country_fig, use_container_width=True)

## choropleth showing duck purchase by US state

state_fig = px.choropleth(state_df,locations="Purchase_State", 
                          locationmode="USA-states", 
                          color="Quantity", 
                          scope="usa"
                        #   color_continuous_scale="YlGn"
                          )
state_fig.update_layout(title_text="Rubber Duck Purchase By State",title_x=0.3)
state_fig.add_trace(map_fig.data[0])

# st.plotly_chart(state_fig, use_container_width=True)


map1,map2 = st.columns(2)
map1.plotly_chart(country_fig, use_container_width=True,theme=None)
map2.plotly_chart(state_fig, use_container_width=True,theme=None)

###################### Duck info graphs ##############################


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
[data-testid="stMetric"] {
    color: #212529;
    background-color: #f8f9fa;
    width: 75%;
    margin: auto;
    padding: 1rem 1rem;
    border-radius: 0.25rem
}

[data-testid="stDataFrameResizable"] {
    align-content: center;
    align-items: center;
    width: 75%;
    margin: auto;
    padding: 1rem 1rem;
    border-radius: 0.25rem
}

[data-testid="stMetric"] > div {
    color: #212529;
    background-color: #f8f9fa;
    width: fit-content;
    margin: auto;
}


[data-testid="stMetric"] label {
    color: #212529;
    background-color: #f8f9fa;
    width: fit-content;
    margin: auto;
}

[data-testid="stVerticalBlock"] > [".st-emotion-cache-pplk8x e1f1d6gn1"] {
    border: 20px groove red;
}


# [data-testid="block-container"] {
#     color: #000000;
#     background-color: #f8f9fa;
#     width: fit-content;
#     margin: auto;
# }

# [data-testid="stMarkdownContainer"] > div > h1 {
#     color: #000000;
#     # background-color: #f8f9fa;
#     width: fit-content;
#     margin: auto;
# }

# [data-testid="stHorizontalBlock"] > div {
#     color: #000000;
#     background-color: #f8f9fa;
#     width: fit-content;
#     margin: auto;
# }



# [data-testid="element-container"] > div  {
#     # color: #EBCC34;
#     background-color: #EBCC34;
#     # width: fit-content;
#     # margin: auto;
# }    

# [data-testid="stMetric"] {
#     color: #212529;
#     background-color: #f8f9fa;
#     width: 75%;
#     margin: auto;
#     padding: 1rem 1rem;
#     border-radius: 0.25rem
# }

# [data-testid="stMetric"] > div {
#     color: #212529;
#     background-color: #f8f9fa;
#     width: fit-content;
#     margin: auto;
# }


# [data-testid="stMetric"] label {
#     color: #212529;
#     background-color: #f8f9fa;
#     width: fit-content;
#     margin: auto;
# }
}
'''
st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)


# <div data-testid="stHorizontalBlock" class="st-emotion-cache-ocqkz7 e1f1d6gn4"><div data-testid="column" class="st-emotion-cache-1r6slb0 e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="273.6000061035156" data-testid="stVerticalBlock" class="st-emotion-cache-2co4bz e1f1d6gn1"><div data-stale="false" width="273.6000061035156" class="element-container st-emotion-cache-f0kf11 e1f1d6gn3" data-testid="element-container"><div data-testid="stStyledFullScreenFrame" class="st-emotion-cache-9aoz2h e1vs0wn30"><button data-testid="StyledFullScreenButton" title="View fullscreen" class="st-emotion-cache-e370rw e1vs0wn31"><svg viewBox="0 0 8 8" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp51 st-emotion-cache-1pxazr7 ex0cdmw0"><path d="M0 0v4l1.5-1.5L3 4l1-1-1.5-1.5L4 0H0zm5 4L4 5l1.5 1.5L4 8h4V4L6.5 5.5 5 4z"></path></svg></button><div class="stPlotlyChart js-plotly-plot" style="position: relative; display: inline-block;"><div class="plot-container plotly"><div class="user-select-none svg-container" style="position: relative; width: 273.6px; height: 450px;"><svg class="main-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="273.6000061035156" height="450" style="background: rgb(235, 204, 52);"><defs id="defs-ac71b1"><g class="clips"></g><g class="gradients"></g><g class="patterns"></g></defs><g class="bglayer"></g><g class="draglayer"></g><g class="layer-below"><g class="imagelayer"></g><g class="shapelayer"></g></g><g class="cartesianlayer"></g><g class="polarlayer"></g><g class="smithlayer"></g><g class="ternarylayer"></g><g class="geolayer"></g><g class="funnelarealayer"></g><g class="pielayer"><g class="trace" stroke-linejoin="round" style="opacity: 1;"><g class="slice"><path class="surface" d="M112.5,215l0,-32.5a32.5,32.5 0 1 1 -32.47960203171076,33.65128270276675Z" style="pointer-events: all; fill: rgb(99, 110, 250); fill-opacity: 1; stroke-width: 0; stroke: rgb(68, 68, 68); stroke-opacity: 1;"></path><g class="slicetext"><text data-notex="1" class="slicetext" transform="translate(124.23942703356491,226.68111910211277)rotate(-46.01503759398497)" text-anchor="middle" data-unformatted="74.4%" data-math="N" x="0" y="0" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(255, 255, 255); fill-opacity: 1; white-space: pre;">74.4%</text></g></g><g class="slice"><path class="surface" d="M112.5,215l-27.20791054353218,-17.775815138978874a32.5,32.5 0 0 1 27.20791054353218,-14.724184861021126Z" style="pointer-events: all; fill: rgb(239, 85, 59); fill-opacity: 1; stroke-width: 0; stroke: rgb(68, 68, 68); stroke-opacity: 1;"></path><g class="slicetext"><text data-notex="1" class="slicetext" transform="translate(77.3397172050091,184.93870025405556)" text-anchor="middle" data-unformatted="15.8%" data-math="N" x="0" y="0" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre;">15.8%</text></g></g><g class="slice"><path class="surface" d="M112.5,215l-32.31657188172779,-3.448069287749389a32.5,32.5 0 0 1 5.10866133819561,-14.327745851229485Z" style="pointer-events: all; fill: rgb(0, 204, 150); fill-opacity: 1; stroke-width: 0; stroke: rgb(68, 68, 68); stroke-opacity: 1;"></path><g class="slicetext"><text data-notex="1" class="slicetext" transform="translate(62.195721100641435,202.25543759045635)" text-anchor="middle" data-unformatted="7.52%" data-math="N" x="0" y="0" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre;">7.52%</text></g><path class="textline" stroke-width="1.5" d="M81.88771362192745,204.08496803912726V197.85543749508892h-3.799999952316284" fill="none" style="stroke: rgb(0, 0, 0); stroke-opacity: 1;"></path></g><g class="slice"><path class="surface" d="M112.5,215l-32.497733348306035,-0.3838322842049931a32.5,32.5 0 0 1 0.18116146657824572,-3.0642370035443958Z" style="pointer-events: all; fill: rgb(171, 99, 250); fill-opacity: 1; stroke-width: 0; stroke: rgb(68, 68, 68); stroke-opacity: 1;"></path><g class="slicetext"><text data-notex="1" class="slicetext" transform="translate(63.34727438882905,217.4554373997215)" text-anchor="middle" data-unformatted="1.5%" data-math="N" x="0" y="0" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre;">1.5%</text></g></g><g class="slice"><path class="surface" d="M112.5,215l-32.47960203171076,1.1512827027667545a32.5,32.5 0 0 1 -0.018131316595273006,-1.5351149869717475Z" style="pointer-events: all; fill: rgb(255, 161, 90); fill-opacity: 1; stroke-width: 0; stroke: rgb(68, 68, 68); stroke-opacity: 1;"></path><g class="slicetext"><text data-notex="1" class="slicetext" transform="translate(57.32765579849877,232.65543720898663)" text-anchor="middle" data-unformatted="0.752%" data-math="N" x="0" y="0" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre;">0.752%</text></g><path class="textline" stroke-width="1.5" d="M80.00226665169396,215.383832284205V228.2554371136192h-3.799999952316284" fill="none" style="stroke: rgb(0, 0, 0); stroke-opacity: 1;"></path></g></g></g><g class="iciclelayer"></g><g class="treemaplayer"></g><g class="sunburstlayer"></g><g class="glimages"></g></svg><div class="gl-container"></div><svg class="main-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="273.6000061035156" height="450"><defs id="topdefs-ac71b1"><g class="clips"></g><clipPath id="legendac71b1"><rect width="116" height="105" x="0" y="0"></rect></clipPath></defs><g class="indicatorlayer"></g><g class="layer-above"><g class="imagelayer"></g><g class="shapelayer"></g></g><g class="selectionlayer"></g><g class="infolayer"><g class="legend" pointer-events="all" transform="translate(146.3,60)"><rect class="bg" shape-rendering="crispEdges" style="stroke: rgb(68, 68, 68); stroke-opacity: 1; fill: rgb(235, 204, 52); fill-opacity: 1; stroke-width: 0px;" width="116" height="105" x="0" y="0"></rect><g class="scrollbox" transform="" clip-path="url(#legendac71b1)"><g class="groups"><g class="traces" transform="translate(0,14.5)" style="opacity: 1;"><text class="legendtext" text-anchor="start" x="40" y="4.680000000000001" data-unformatted="Phyiscal Store" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre;">Phyiscal Store</text><g class="layers" style="opacity: 1;"><g class="legendfill"></g><g class="legendlines"></g><g class="legendsymbols"><g class="legendpoints"><path class="legendpie" d="M6,6H-6V-6H6Z" transform="translate(20,0)" style="fill: rgb(99, 110, 250); fill-opacity: 1; stroke-width: 0; stroke: rgb(68, 68, 68); stroke-opacity: 1;"></path></g></g></g><rect class="legendtoggle" pointer-events="all" x="0" y="-9.5" width="110.7203140258789" height="19" style="cursor: pointer; fill: rgb(0, 0, 0); fill-opacity: 0;"></rect></g><g class="traces" transform="translate(0,33.5)" style="opacity: 1;"><text class="legendtext" text-anchor="start" x="40" y="4.680000000000001" data-unformatted="Online" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre;">Online</text><g class="layers" style="opacity: 1;"><g class="legendfill"></g><g class="legendlines"></g><g class="legendsymbols"><g class="legendpoints"><path class="legendpie" d="M6,6H-6V-6H6Z" transform="translate(20,0)" style="fill: rgb(239, 85, 59); fill-opacity: 1; stroke-width: 0; stroke: rgb(68, 68, 68); stroke-opacity: 1;"></path></g></g></g><rect class="legendtoggle" pointer-events="all" x="0" y="-9.5" width="110.7203140258789" height="19" style="cursor: pointer; fill: rgb(0, 0, 0); fill-opacity: 0;"></rect></g><g class="traces" transform="translate(0,52.5)" style="opacity: 1;"><text class="legendtext" text-anchor="start" x="40" y="4.680000000000001" data-unformatted="Claw Machine" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre;">Claw Machine</text><g class="layers" style="opacity: 1;"><g class="legendfill"></g><g class="legendlines"></g><g class="legendsymbols"><g class="legendpoints"><path class="legendpie" d="M6,6H-6V-6H6Z" transform="translate(20,0)" style="fill: rgb(0, 204, 150); fill-opacity: 1; stroke-width: 0; stroke: rgb(68, 68, 68); stroke-opacity: 1;"></path></g></g></g><rect class="legendtoggle" pointer-events="all" x="0" y="-9.5" width="110.7203140258789" height="19" style="cursor: pointer; fill: rgb(0, 0, 0); fill-opacity: 0;"></rect></g><g class="traces" transform="translate(0,71.5)" style="opacity: 1;"><text class="legendtext" text-anchor="start" x="40" y="4.680000000000001" data-unformatted="Rescue" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre;">Rescue</text><g class="layers" style="opacity: 1;"><g class="legendfill"></g><g class="legendlines"></g><g class="legendsymbols"><g class="legendpoints"><path class="legendpie" d="M6,6H-6V-6H6Z" transform="translate(20,0)" style="fill: rgb(171, 99, 250); fill-opacity: 1; stroke-width: 0; stroke: rgb(68, 68, 68); stroke-opacity: 1;"></path></g></g></g><rect class="legendtoggle" pointer-events="all" x="0" y="-9.5" width="110.7203140258789" height="19" style="cursor: pointer; fill: rgb(0, 0, 0); fill-opacity: 0;"></rect></g><g class="traces" transform="translate(0,90.5)" style="opacity: 1;"><text class="legendtext" text-anchor="start" x="40" y="4.680000000000001" data-unformatted="Duck Game" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre;">Duck Game</text><g class="layers" style="opacity: 1;"><g class="legendfill"></g><g class="legendlines"></g><g class="legendsymbols"><g class="legendpoints"><path class="legendpie" d="M6,6H-6V-6H6Z" transform="translate(20,0)" style="fill: rgb(255, 161, 90); fill-opacity: 1; stroke-width: 0; stroke: rgb(68, 68, 68); stroke-opacity: 1;"></path></g></g></g><rect class="legendtoggle" pointer-events="all" x="0" y="-9.5" width="110.7203140258789" height="19" style="cursor: pointer; fill: rgb(0, 0, 0); fill-opacity: 0;"></rect></g></g></g><rect class="scrollbar" rx="20" ry="3" width="0" height="0" style="fill: rgb(128, 139, 164); fill-opacity: 1;" x="0" y="0"></rect></g><g class="g-gtitle"><text class="gtitle" x="82.08000183105469" y="30" text-anchor="start" dy="0em" data-unformatted="Purchase Method Distribution" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 17px; fill: rgb(0, 0, 0); opacity: 1; font-weight: normal; white-space: pre;">Purchase Method Distribution</text></g></g><g class="menulayer"></g><g class="zoomlayer"></g></svg><div class="modebar-container" style="position: absolute; top: 0px; right: 0px; width: 100%;"><div id="modebar-ac71b1" class="modebar modebar--hover ease-bg"><div class="modebar-group"><a rel="tooltip" class="modebar-btn" data-title="Download plot as a png" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m500 450c-83 0-150-67-150-150 0-83 67-150 150-150 83 0 150 67 150 150 0 83-67 150-150 150z m400 150h-120c-16 0-34 13-39 29l-31 93c-6 15-23 28-40 28h-340c-16 0-34-13-39-28l-31-94c-6-15-23-28-40-28h-120c-55 0-100-45-100-100v-450c0-55 45-100 100-100h800c55 0 100 45 100 100v450c0 55-45 100-100 100z m-400-550c-138 0-250 112-250 250 0 138 112 250 250 250 138 0 250-112 250-250 0-138-112-250-250-250z m365 380c-19 0-35 16-35 35 0 19 16 35 35 35 19 0 35-16 35-35 0-19-16-35-35-35z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a></div><div class="modebar-group"><a href="https://plotly.com/" target="_blank" data-title="Produced with Plotly.js (v2.26.1)" class="modebar-btn plotlyjsicon modebar-btn--logo"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 132 132" height="1em" width="1em"><defs> <style>  .cls-0{fill:#000;}  .cls-1{fill:#FFF;}  .cls-2{fill:#F26;}  .cls-3{fill:#D69;}  .cls-4{fill:#BAC;}  .cls-5{fill:#9EF;} </style></defs> <title>plotly-logomark</title> <g id="symbol">  <rect class="cls-0" x="0" y="0" width="132" height="132" rx="18" ry="18"></rect>  <circle class="cls-5" cx="102" cy="30" r="6"></circle>  <circle class="cls-4" cx="78" cy="30" r="6"></circle>  <circle class="cls-4" cx="78" cy="54" r="6"></circle>  <circle class="cls-3" cx="54" cy="30" r="6"></circle>  <circle class="cls-2" cx="30" cy="30" r="6"></circle>  <circle class="cls-2" cx="30" cy="54" r="6"></circle>  <path class="cls-1" d="M30,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,30,72Z"></path>  <path class="cls-1" d="M78,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,78,72Z"></path>  <path class="cls-1" d="M54,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,54,48Z"></path>  <path class="cls-1" d="M102,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,102,48Z"></path> </g></svg></a></div></div></div><svg class="main-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="273.6000061035156" height="450"><g class="hoverlayer"></g></svg></div></div></div></div></div></div></div></div><div data-testid="column" class="st-emotion-cache-1r6slb0 e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="273.6000061035156" data-testid="stVerticalBlock" class="st-emotion-cache-2co4bz e1f1d6gn1"><div data-stale="false" width="273.6000061035156" class="element-container st-emotion-cache-f0kf11 e1f1d6gn3" data-testid="element-container"><div data-testid="stStyledFullScreenFrame" class="st-emotion-cache-9aoz2h e1vs0wn30"><button data-testid="StyledFullScreenButton" title="View fullscreen" class="st-emotion-cache-e370rw e1vs0wn31"><svg viewBox="0 0 8 8" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp51 st-emotion-cache-1pxazr7 ex0cdmw0"><path d="M0 0v4l1.5-1.5L3 4l1-1-1.5-1.5L4 0H0zm5 4L4 5l1.5 1.5L4 8h4V4L6.5 5.5 5 4z"></path></svg></button><div class="stPlotlyChart js-plotly-plot" style="position: relative; display: inline-block;"><div class="plot-container plotly"><div class="user-select-none svg-container" style="position: relative; width: 273.6px; height: 450px;"><svg class="main-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="273.6000061035156" height="450" style="background: rgb(235, 204, 52);"><defs id="defs-3e787f"><g class="clips"><clipPath id="clip3e787fxyplot" class="plotclip"><rect width="114" height="310"></rect></clipPath><clipPath class="axesclip" id="clip3e787fx"><rect x="80" y="0" width="114" height="450"></rect></clipPath><clipPath class="axesclip" id="clip3e787fy"><rect x="0" y="60" width="273.6000061035156" height="310"></rect></clipPath><clipPath class="axesclip" id="clip3e787fxy"><rect x="80" y="60" width="114" height="310"></rect></clipPath></g><g class="gradients"></g><g class="patterns"></g></defs><g class="bglayer"><rect class="bg" x="80" y="60" width="114" height="310" style="fill: rgb(206, 212, 218); fill-opacity: 1; stroke-width: 0;"></rect></g><g class="draglayer cursor-crosshair"><g class="xy"><rect class="nsewdrag drag" data-subplot="xy" x="80" y="60" width="114" height="310" style="fill: transparent; stroke-width: 0; pointer-events: all;"></rect><rect class="nwdrag drag cursor-nw-resize" data-subplot="xy" x="60" y="40" width="20" height="20" style="fill: transparent; stroke-width: 0; pointer-events: all;"></rect><rect class="nedrag drag cursor-ne-resize" data-subplot="xy" x="194" y="40" width="20" height="20" style="fill: transparent; stroke-width: 0; pointer-events: all;"></rect><rect class="swdrag drag cursor-sw-resize" data-subplot="xy" x="60" y="370" width="20" height="20" style="fill: transparent; stroke-width: 0; pointer-events: all;"></rect><rect class="sedrag drag cursor-se-resize" data-subplot="xy" x="194" y="370" width="20" height="20" style="fill: transparent; stroke-width: 0; pointer-events: all;"></rect><rect class="ewdrag drag cursor-ew-resize" data-subplot="xy" x="91.4" y="370.5" width="91.2" height="20" style="fill: transparent; stroke-width: 0; pointer-events: all;"></rect><rect class="wdrag drag cursor-w-resize" data-subplot="xy" x="80" y="370.5" width="11.4" height="20" style="fill: transparent; stroke-width: 0; pointer-events: all;"></rect><rect class="edrag drag cursor-e-resize" data-subplot="xy" x="182.60000000000002" y="370.5" width="11.4" height="20" style="fill: transparent; stroke-width: 0; pointer-events: all;"></rect><rect class="nsdrag drag cursor-ns-resize" data-subplot="xy" x="59.5" y="91" width="20" height="248" style="fill: transparent; stroke-width: 0; pointer-events: all;"></rect><rect class="sdrag drag cursor-s-resize" data-subplot="xy" x="59.5" y="339" width="20" height="31" style="fill: transparent; stroke-width: 0; pointer-events: all;"></rect><rect class="ndrag drag cursor-n-resize" data-subplot="xy" x="59.5" y="60" width="20" height="31" style="fill: transparent; stroke-width: 0; pointer-events: all;"></rect></g></g><g class="layer-below"><g class="imagelayer"></g><g class="shapelayer"></g></g><g class="cartesianlayer"><g class="subplot xy"><g class="layer-subplot"><g class="shapelayer"></g><g class="imagelayer"></g></g><g class="minor-gridlayer"><g class="x"></g><g class="y"></g></g><g class="gridlayer"><g class="x"></g><g class="y"><path class="ygrid crisp" transform="translate(0,315.46000000000004)" d="M80,0h114" style="stroke: rgb(193, 199, 204); stroke-opacity: 1; stroke-width: 1px;"></path><path class="ygrid crisp" transform="translate(0,260.93)" d="M80,0h114" style="stroke: rgb(193, 199, 204); stroke-opacity: 1; stroke-width: 1px;"></path><path class="ygrid crisp" transform="translate(0,206.39)" d="M80,0h114" style="stroke: rgb(193, 199, 204); stroke-opacity: 1; stroke-width: 1px;"></path><path class="ygrid crisp" transform="translate(0,151.85)" d="M80,0h114" style="stroke: rgb(193, 199, 204); stroke-opacity: 1; stroke-width: 1px;"></path><path class="ygrid crisp" transform="translate(0,97.31)" d="M80,0h114" style="stroke: rgb(193, 199, 204); stroke-opacity: 1; stroke-width: 1px;"></path></g></g><g class="zerolinelayer"><path class="yzl zl crisp" transform="translate(0,370)" d="M80,0h114" style="stroke: rgb(68, 68, 68); stroke-opacity: 1; stroke-width: 1px;"></path></g><path class="xlines-below"></path><path class="ylines-below"></path><g class="overlines-below"></g><g class="xaxislayer-below"></g><g class="yaxislayer-below"></g><g class="overaxes-below"></g><g class="plot" transform="translate(80,60)" clip-path="url(#clip3e787fxyplot)"><g class="barlayer mlayer"><g class="trace bars" style="opacity: 1;"><g class="points"><g class="point"><path d="M1.42,310V307.27H12.83V310Z" style="vector-effect: non-scaling-stroke; opacity: 1; stroke-width: 0px; fill: rgb(99, 110, 250); fill-opacity: 1;"></path></g><g class="point"><path d="M15.68,310V307.27H27.08V310Z" style="vector-effect: non-scaling-stroke; opacity: 1; stroke-width: 0px; fill: rgb(99, 110, 250); fill-opacity: 1;"></path></g><g class="point"><path d="M29.93,310V307.27H41.33V310Z" style="vector-effect: non-scaling-stroke; opacity: 1; stroke-width: 0px; fill: rgb(99, 110, 250); fill-opacity: 1;"></path></g><g class="point"><path d="M44.18,310V304.55H55.58V310Z" style="vector-effect: non-scaling-stroke; opacity: 1; stroke-width: 0px; fill: rgb(99, 110, 250); fill-opacity: 1;"></path></g><g class="point"><path d="M58.43,310V304.55H69.83V310Z" style="vector-effect: non-scaling-stroke; opacity: 1; stroke-width: 0px; fill: rgb(99, 110, 250); fill-opacity: 1;"></path></g><g class="point"><path d="M72.68,310V293.64H84.07V310Z" style="vector-effect: non-scaling-stroke; opacity: 1; stroke-width: 0px; fill: rgb(99, 110, 250); fill-opacity: 1;"></path></g><g class="point"><path d="M86.93,310V277.28H98.32V310Z" style="vector-effect: non-scaling-stroke; opacity: 1; stroke-width: 0px; fill: rgb(99, 110, 250); fill-opacity: 1;"></path></g><g class="point"><path d="M101.18,310V15.5H112.57V310Z" style="vector-effect: non-scaling-stroke; opacity: 1; stroke-width: 0px; fill: rgb(99, 110, 250); fill-opacity: 1;"></path></g></g></g></g></g><g class="overplot"></g><path class="xlines-above crisp" d="M0,0" style="fill: none;"></path><path class="ylines-above crisp" d="M0,0" style="fill: none;"></path><g class="overlines-above"></g><g class="xaxislayer-above"><g class="xtick"><text text-anchor="start" x="0" y="383" data-unformatted="Gianna" data-math="N" transform="translate(87.13,0) rotate(90,0,377)" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;">Gianna</text></g><g class="xtick"><text text-anchor="start" x="0" y="383" data-unformatted="Larry" data-math="N" transform="translate(101.38,0) rotate(90,0,377)" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;">Larry</text></g><g class="xtick"><text text-anchor="start" x="0" y="383" data-unformatted="Parents" data-math="N" transform="translate(115.63,0) rotate(90,0,377)" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;">Parents</text></g><g class="xtick"><text text-anchor="start" x="0" y="383" data-unformatted="Marina" data-math="N" transform="translate(129.88,0) rotate(90,0,377)" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;">Marina</text></g><g class="xtick"><text text-anchor="start" x="0" y="383" data-unformatted="Yev" data-math="N" transform="translate(144.13,0) rotate(90,0,377)" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;">Yev</text></g><g class="xtick"><text text-anchor="start" x="0" y="383" data-unformatted="Diana" data-math="N" transform="translate(158.38,0) rotate(90,0,377)" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;">Diana</text></g><g class="xtick"><text text-anchor="start" x="0" y="383" data-unformatted="Julia" data-math="N" transform="translate(172.63,0) rotate(90,0,377)" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;">Julia</text></g><g class="xtick"><text text-anchor="start" x="0" y="383" data-unformatted="Allan" data-math="N" transform="translate(186.88,0) rotate(90,0,377)" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;">Allan</text></g></g><g class="yaxislayer-above"><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="0" data-math="N" transform="translate(0,370)" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;">0</text></g><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="20" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;" transform="translate(0,315.46000000000004)">20</text></g><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="40" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;" transform="translate(0,260.93)">40</text></g><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="60" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;" transform="translate(0,206.39)">60</text></g><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="80" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;" transform="translate(0,151.85)">80</text></g><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="100" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(0, 0, 0); fill-opacity: 1; white-space: pre; opacity: 1;" transform="translate(0,97.31)">100</text></g></g><g class="overaxes-above"></g></g></g><g class="polarlayer"></g><g class="smithlayer"></g><g class="ternarylayer"></g><g class="geolayer"></g><g class="funnelarealayer"></g><g class="pielayer"></g><g class="iciclelayer"></g><g class="treemaplayer"></g><g class="sunburstlayer"></g><g class="glimages"></g></svg><div class="gl-container"></div><svg class="main-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="273.6000061035156" height="450"><defs id="topdefs-3e787f"><g class="clips"></g></defs><g class="indicatorlayer"></g><g class="layer-above"><g class="imagelayer"></g><g class="shapelayer"></g></g><g class="selectionlayer"></g><g class="infolayer"><g class="g-gtitle"><text class="gtitle" x="82.08000183105469" y="30" text-anchor="start" dy="0em" data-unformatted="Rubber Duck Distribution by Purchaser" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 17px; fill: rgb(0, 0, 0); opacity: 1; font-weight: normal; white-space: pre;">Rubber Duck Distribution by Purchaser</text></g><g class="g-xtitle" transform="translate(0,9.02090072631836)"><text class="xtitle" x="137" y="422" text-anchor="middle" data-unformatted="Purchaser" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 14px; fill: rgb(0, 0, 0); opacity: 1; font-weight: normal; white-space: pre;">Purchaser</text></g><g class="g-ytitle"><text class="ytitle" transform="rotate(-90,42,215)" x="42" y="215" text-anchor="middle" data-unformatted="Quantity" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 14px; fill: rgb(0, 0, 0); opacity: 1; font-weight: normal; white-space: pre;">Quantity</text></g></g><g class="menulayer"></g><g class="zoomlayer"></g></svg><div class="modebar-container" style="position: absolute; top: 0px; right: 0px; width: 100%;"><div id="modebar-3e787f" class="modebar modebar--hover ease-bg"><div class="modebar-group"><a rel="tooltip" class="modebar-btn" data-title="Download plot as a png" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m500 450c-83 0-150-67-150-150 0-83 67-150 150-150 83 0 150 67 150 150 0 83-67 150-150 150z m400 150h-120c-16 0-34 13-39 29l-31 93c-6 15-23 28-40 28h-340c-16 0-34-13-39-28l-31-94c-6-15-23-28-40-28h-120c-55 0-100-45-100-100v-450c0-55 45-100 100-100h800c55 0 100 45 100 100v450c0 55-45 100-100 100z m-400-550c-138 0-250 112-250 250 0 138 112 250 250 250 138 0 250-112 250-250 0-138-112-250-250-250z m365 380c-19 0-35 16-35 35 0 19 16 35 35 35 19 0 35-16 35-35 0-19-16-35-35-35z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a></div><div class="modebar-group"><a rel="tooltip" class="modebar-btn active" data-title="Zoom" data-attr="dragmode" data-val="zoom" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m1000-25l-250 251c40 63 63 138 63 218 0 224-182 406-407 406-224 0-406-182-406-406s183-406 407-406c80 0 155 22 218 62l250-250 125 125z m-812 250l0 438 437 0 0-438-437 0z m62 375l313 0 0-312-313 0 0 312z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Pan" data-attr="dragmode" data-val="pan" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m1000 350l-187 188 0-125-250 0 0 250 125 0-188 187-187-187 125 0 0-250-250 0 0 125-188-188 186-187 0 125 252 0 0-250-125 0 187-188 188 188-125 0 0 250 250 0 0-126 187 188z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Box Select" data-attr="dragmode" data-val="select" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m0 850l0-143 143 0 0 143-143 0z m286 0l0-143 143 0 0 143-143 0z m285 0l0-143 143 0 0 143-143 0z m286 0l0-143 143 0 0 143-143 0z m-857-286l0-143 143 0 0 143-143 0z m857 0l0-143 143 0 0 143-143 0z m-857-285l0-143 143 0 0 143-143 0z m857 0l0-143 143 0 0 143-143 0z m-857-286l0-143 143 0 0 143-143 0z m286 0l0-143 143 0 0 143-143 0z m285 0l0-143 143 0 0 143-143 0z m286 0l0-143 143 0 0 143-143 0z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Lasso Select" data-attr="dragmode" data-val="lasso" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1031 1000" class="icon" height="1em" width="1em"><path d="m1018 538c-36 207-290 336-568 286-277-48-473-256-436-463 10-57 36-108 76-151-13-66 11-137 68-183 34-28 75-41 114-42l-55-70 0 0c-2-1-3-2-4-3-10-14-8-34 5-45 14-11 34-8 45 4 1 1 2 3 2 5l0 0 113 140c16 11 31 24 45 40 4 3 6 7 8 11 48-3 100 0 151 9 278 48 473 255 436 462z m-624-379c-80 14-149 48-197 96 42 42 109 47 156 9 33-26 47-66 41-105z m-187-74c-19 16-33 37-39 60 50-32 109-55 174-68-42-25-95-24-135 8z m360 75c-34-7-69-9-102-8 8 62-16 128-68 170-73 59-175 54-244-5-9 20-16 40-20 61-28 159 121 317 333 354s407-60 434-217c28-159-121-318-333-355z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a></div><div class="modebar-group"><a rel="tooltip" class="modebar-btn" data-title="Zoom in" data-attr="zoom" data-val="in" data-toggle="false" data-gravity="n"><svg viewBox="0 0 875 1000" class="icon" height="1em" width="1em"><path d="m1 787l0-875 875 0 0 875-875 0z m687-500l-187 0 0-187-125 0 0 187-188 0 0 125 188 0 0 187 125 0 0-187 187 0 0-125z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Zoom out" data-attr="zoom" data-val="out" data-toggle="false" data-gravity="n"><svg viewBox="0 0 875 1000" class="icon" height="1em" width="1em"><path d="m0 788l0-876 875 0 0 876-875 0z m688-500l-500 0 0 125 500 0 0-125z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Autoscale" data-attr="zoom" data-val="auto" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m250 850l-187 0-63 0 0-62 0-188 63 0 0 188 187 0 0 62z m688 0l-188 0 0-62 188 0 0-188 62 0 0 188 0 62-62 0z m-875-938l0 188-63 0 0-188 0-62 63 0 187 0 0 62-187 0z m875 188l0-188-188 0 0-62 188 0 62 0 0 62 0 188-62 0z m-125 188l-1 0-93-94-156 156 156 156 92-93 2 0 0 250-250 0 0-2 93-92-156-156-156 156 94 92 0 2-250 0 0-250 0 0 93 93 157-156-157-156-93 94 0 0 0-250 250 0 0 0-94 93 156 157 156-157-93-93 0 0 250 0 0 250z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Reset axes" data-attr="zoom" data-val="reset" data-toggle="false" data-gravity="n"><svg viewBox="0 0 928.6 1000" class="icon" height="1em" width="1em"><path d="m786 296v-267q0-15-11-26t-25-10h-214v214h-143v-214h-214q-15 0-25 10t-11 26v267q0 1 0 2t0 2l321 264 321-264q1-1 1-4z m124 39l-34-41q-5-5-12-6h-2q-7 0-12 3l-386 322-386-322q-7-4-13-4-7 2-12 7l-35 41q-4 5-3 13t6 12l401 334q18 15 42 15t43-15l136-114v109q0 8 5 13t13 5h107q8 0 13-5t5-13v-227l122-102q5-5 6-12t-4-13z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a></div><div class="modebar-group"><a href="https://plotly.com/" target="_blank" data-title="Produced with Plotly.js (v2.26.1)" class="modebar-btn plotlyjsicon modebar-btn--logo"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 132 132" height="1em" width="1em"><defs> <style>  .cls-0{fill:#000;}  .cls-1{fill:#FFF;}  .cls-2{fill:#F26;}  .cls-3{fill:#D69;}  .cls-4{fill:#BAC;}  .cls-5{fill:#9EF;} </style></defs> <title>plotly-logomark</title> <g id="symbol">  <rect class="cls-0" x="0" y="0" width="132" height="132" rx="18" ry="18"></rect>  <circle class="cls-5" cx="102" cy="30" r="6"></circle>  <circle class="cls-4" cx="78" cy="30" r="6"></circle>  <circle class="cls-4" cx="78" cy="54" r="6"></circle>  <circle class="cls-3" cx="54" cy="30" r="6"></circle>  <circle class="cls-2" cx="30" cy="30" r="6"></circle>  <circle class="cls-2" cx="30" cy="54" r="6"></circle>  <path class="cls-1" d="M30,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,30,72Z"></path>  <path class="cls-1" d="M78,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,78,72Z"></path>  <path class="cls-1" d="M54,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,54,48Z"></path>  <path class="cls-1" d="M102,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,102,48Z"></path> </g></svg></a></div></div></div><svg class="main-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="273.6000061035156" height="450"><g class="hoverlayer"></g></svg></div></div></div></div></div></div></div></div><div data-testid="column" class="st-emotion-cache-1r6slb0 e1f1d6gn2"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="273.6000061035156" data-testid="stVerticalBlock" class="st-emotion-cache-2co4bz e1f1d6gn1"><div data-stale="false" width="273.6000061035156" class="element-container st-emotion-cache-f0kf11 e1f1d6gn3" data-testid="element-container"><div data-testid="stStyledFullScreenFrame" class="st-emotion-cache-9aoz2h e1vs0wn30"><button data-testid="StyledFullScreenButton" title="View fullscreen" class="st-emotion-cache-e370rw e1vs0wn31"><svg viewBox="0 0 8 8" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp51 st-emotion-cache-1pxazr7 ex0cdmw0"><path d="M0 0v4l1.5-1.5L3 4l1-1-1.5-1.5L4 0H0zm5 4L4 5l1.5 1.5L4 8h4V4L6.5 5.5 5 4z"></path></svg></button><div class="stPlotlyChart js-plotly-plot" style="position: relative; display: inline-block;"><div class="plot-container plotly"><div class="user-select-none svg-container" style="position: relative; width: 273.6px; height: 450px;"><svg class="main-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="273.6000061035156" height="450" style="background: rgba(0, 0, 0, 0);"><defs id="defs-022822"><g class="clips"></g><g class="gradients"><linearGradient x1="0" x2="0" y1="1" y2="0" id="g022822-cbcoloraxis"><stop offset="0%" stop-color="rgb(13, 8, 135)" stop-opacity="1"></stop><stop offset="11.111111%" stop-color="rgb(70, 3, 159)" stop-opacity="1"></stop><stop offset="22.222222%" stop-color="rgb(114, 1, 168)" stop-opacity="1"></stop><stop offset="33.333333%" stop-color="rgb(156, 23, 158)" stop-opacity="1"></stop><stop offset="44.444444%" stop-color="rgb(189, 55, 134)" stop-opacity="1"></stop><stop offset="55.555556%" stop-color="rgb(216, 87, 107)" stop-opacity="1"></stop><stop offset="66.666667%" stop-color="rgb(237, 121, 83)" stop-opacity="1"></stop><stop offset="77.777778%" stop-color="rgb(251, 159, 58)" stop-opacity="1"></stop><stop offset="88.888889%" stop-color="rgb(253, 202, 38)" stop-opacity="1"></stop><stop offset="100%" stop-color="rgb(240, 249, 33)" stop-opacity="1"></stop></linearGradient></g><g class="patterns"></g></defs><g class="bglayer"></g><g class="draglayer"></g><g class="layer-below"><g class="imagelayer"></g><g class="shapelayer"></g></g><g class="cartesianlayer"></g><g class="polarlayer"></g><g class="smithlayer"></g><g class="ternarylayer"></g><g class="geolayer"></g><g class="funnelarealayer"></g><g class="pielayer"></g><g class="iciclelayer"></g><g class="treemaplayer"></g><g class="sunburstlayer"></g><g class="glimages"></g></svg><div class="gl-container"><div id="scene" style="position: absolute; left: 80px; top: 60px; height: 310px; width: 92px;"><svg viewBox="0 0 92 310" width="92" height="310" style="position: absolute; left: 0px; top: 0px; height: 100%; width: 100%; z-index: 20; pointer-events: none;"></svg><canvas width="184" height="620" style="position: absolute; left: 0px; top: 0px; width: 92px; height: 310px;"></canvas></div></div><svg class="main-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="273.6000061035156" height="450"><defs id="topdefs-022822"><g class="clips"></g></defs><g class="indicatorlayer"></g><g class="layer-above"><g class="imagelayer"></g><g class="shapelayer"></g></g><g class="selectionlayer"></g><g class="infolayer"><g class="cbcoloraxis colorbar" transform="translate(80,60)"><rect class="cbbg" x="93.5" y="0" width="88.10176086425781" height="311" style="fill: rgb(0, 0, 0); fill-opacity: 0; stroke: rgb(68, 68, 68); stroke-opacity: 1; stroke-width: 0;"></rect><g class="cbfills" transform="translate(0,33)"><rect class="cbfill gradient_filled" style="fill: url(&quot;#g022822-cbcoloraxis&quot;);" x="104" y="0" width="30" height="267"></rect></g><g class="cblines" transform="translate(0,33)"></g><g class="cbaxis crisp" transform="translate(0,-60)"><g class="ycbcoloraxistick"><text text-anchor="start" x="137.4" y="4.199999999999999" data-unformatted="50" data-math="N" transform="translate(0,281.0000003814697)" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(250, 250, 250); fill-opacity: 1; white-space: pre; opacity: 1;">50</text></g><g class="ycbcoloraxistick"><text text-anchor="start" x="137.4" y="4.199999999999999" data-unformatted="100" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(250, 250, 250); fill-opacity: 1; white-space: pre; opacity: 1;" transform="translate(0,201.84000038146974)">100</text></g><g class="ycbcoloraxistick"><text text-anchor="start" x="137.4" y="4.199999999999999" data-unformatted="150" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 12px; fill: rgb(250, 250, 250); fill-opacity: 1; white-space: pre; opacity: 1;" transform="translate(0,122.68000038146972)">150</text></g></g><g class="cbtitleunshift" transform="translate(-80,-60)"><g class="cbtitle" transform="translate(-0.5,-0.5)"><text class="ycbcoloraxistitle" x="183.84" y="83.5" text-anchor="start" data-unformatted="Avg. Weight" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 14px; fill: rgb(250, 250, 250); opacity: 1; font-weight: normal; white-space: pre;">Avg. Weight</text></g></g><rect class="cboutline" x="104" y="32.60000038146973" width="30" height="267.3999996185303" style="stroke: rgb(68, 68, 68); stroke-opacity: 1; fill: none; stroke-width: 1;"></rect></g><g class="g-gtitle"><text class="gtitle" x="82.08000183105469" y="30" text-anchor="start" dy="0em" data-unformatted="Rubber Duck Length vs Width vs Height (cm)" data-math="N" style="font-family: &quot;Source Sans Pro&quot;, sans-serif; font-size: 17px; fill: rgb(250, 250, 250); opacity: 1; font-weight: normal; white-space: pre;">Rubber Duck Length vs Width vs Height (cm)</text></g></g><g class="menulayer"></g><g class="zoomlayer"></g></svg><div class="modebar-container" style="position: absolute; top: 0px; right: 0px; width: 100%;"><div id="modebar-022822" class="modebar modebar--hover ease-bg"><div class="modebar-group"><a rel="tooltip" class="modebar-btn" data-title="Download plot as a png" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m500 450c-83 0-150-67-150-150 0-83 67-150 150-150 83 0 150 67 150 150 0 83-67 150-150 150z m400 150h-120c-16 0-34 13-39 29l-31 93c-6 15-23 28-40 28h-340c-16 0-34-13-39-28l-31-94c-6-15-23-28-40-28h-120c-55 0-100-45-100-100v-450c0-55 45-100 100-100h800c55 0 100 45 100 100v450c0 55-45 100-100 100z m-400-550c-138 0-250 112-250 250 0 138 112 250 250 250 138 0 250-112 250-250 0-138-112-250-250-250z m365 380c-19 0-35 16-35 35 0 19 16 35 35 35 19 0 35-16 35-35 0-19-16-35-35-35z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a></div><div class="modebar-group"><a rel="tooltip" class="modebar-btn" data-title="Zoom" data-attr="scene.dragmode" data-val="zoom" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m1000-25l-250 251c40 63 63 138 63 218 0 224-182 406-407 406-224 0-406-182-406-406s183-406 407-406c80 0 155 22 218 62l250-250 125 125z m-812 250l0 438 437 0 0-438-437 0z m62 375l313 0 0-312-313 0 0 312z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Pan" data-attr="scene.dragmode" data-val="pan" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m1000 350l-187 188 0-125-250 0 0 250 125 0-188 187-187-187 125 0 0-250-250 0 0 125-188-188 186-187 0 125 252 0 0-250-125 0 187-188 188 188-125 0 0 250 250 0 0-126 187 188z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Orbital rotation" data-attr="scene.dragmode" data-val="orbit" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m922 660c-5 4-9 7-14 11-359 263-580-31-580-31l-102 28 58-400c0 1 1 1 2 2 118 108 351 249 351 249s-62 27-100 42c88 83 222 183 347 122 16-8 30-17 44-27-2 1-4 2-6 4z m36-329c0 0 64 229-88 296-62 27-124 14-175-11 157-78 225-208 249-266 8-19 11-31 11-31 2 5 6 15 11 32-5-13-8-20-8-20z m-775-239c70-31 117-50 198-32-121 80-199 346-199 346l-96-15-58-12c0 0 55-226 155-287z m603 133l-317-139c0 0 4-4 19-14 7-5 24-15 24-15s-177-147-389 4c235-287 536-112 536-112l31-22 100 299-4-1z m-298-153c6-4 14-9 24-15 0 0-17 10-24 15z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn active" data-title="Turntable rotation" data-attr="scene.dragmode" data-val="turntable" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m833 5l-17 108v41l-130-65 130-66c0 0 0 38 0 39 0-1 36-14 39-25 4-15-6-22-16-30-15-12-39-16-56-20-90-22-187-23-279-23-261 0-341 34-353 59 3 60 228 110 228 110-140-8-351-35-351-116 0-120 293-142 474-142 155 0 477 22 477 142 0 50-74 79-163 96z m-374 94c-58-5-99-21-99-40 0-24 65-43 144-43 79 0 143 19 143 43 0 19-42 34-98 40v216h87l-132 135-133-135h88v-216z m167 515h-136v1c16 16 31 34 46 52l84 109v54h-230v-71h124v-1c-16-17-28-32-44-51l-89-114v-51h245v72z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a></div><div class="modebar-group"><a rel="tooltip" class="modebar-btn" data-title="Reset camera to default" data-attr="resetDefault" data-toggle="false" data-gravity="n"><svg viewBox="0 0 928.6 1000" class="icon" height="1em" width="1em"><path d="m786 296v-267q0-15-11-26t-25-10h-214v214h-143v-214h-214q-15 0-25 10t-11 26v267q0 1 0 2t0 2l321 264 321-264q1-1 1-4z m124 39l-34-41q-5-5-12-6h-2q-7 0-12 3l-386 322-386-322q-7-4-13-4-7 2-12 7l-35 41q-4 5-3 13t6 12l401 334q18 15 42 15t43-15l136-114v109q0 8 5 13t13 5h107q8 0 13-5t5-13v-227l122-102q5-5 6-12t-4-13z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Reset camera to last save" data-attr="resetLastSave" data-toggle="false" data-gravity="n"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m938 413l-188-125c0 37-17 71-44 94 64 38 107 107 107 187 0 121-98 219-219 219-121 0-219-98-219-219 0-61 25-117 66-156h-115c30 33 49 76 49 125 0 103-84 187-187 187s-188-84-188-187c0-57 26-107 65-141-38-22-65-62-65-109v-250c0-70 56-126 125-126h500c69 0 125 56 125 126l188-126c34 0 62 28 62 63v375c0 35-28 63-62 63z m-750 0c-69 0-125 56-125 125s56 125 125 125 125-56 125-125-56-125-125-125z m406-1c-87 0-157 70-157 157 0 86 70 156 157 156s156-70 156-156-70-157-156-157z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a></div><div class="modebar-group"><a href="https://plotly.com/" target="_blank" data-title="Produced with Plotly.js (v2.26.1)" class="modebar-btn plotlyjsicon modebar-btn--logo"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 132 132" height="1em" width="1em"><defs> <style>  .cls-0{fill:#000;}  .cls-1{fill:#FFF;}  .cls-2{fill:#F26;}  .cls-3{fill:#D69;}  .cls-4{fill:#BAC;}  .cls-5{fill:#9EF;} </style></defs> <title>plotly-logomark</title> <g id="symbol">  <rect class="cls-0" x="0" y="0" width="132" height="132" rx="18" ry="18"></rect>  <circle class="cls-5" cx="102" cy="30" r="6"></circle>  <circle class="cls-4" cx="78" cy="30" r="6"></circle>  <circle class="cls-4" cx="78" cy="54" r="6"></circle>  <circle class="cls-3" cx="54" cy="30" r="6"></circle>  <circle class="cls-2" cx="30" cy="30" r="6"></circle>  <circle class="cls-2" cx="30" cy="54" r="6"></circle>  <path class="cls-1" d="M30,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,30,72Z"></path>  <path class="cls-1" d="M78,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,78,72Z"></path>  <path class="cls-1" d="M54,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,54,48Z"></path>  <path class="cls-1" d="M102,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,102,48Z"></path> </g></svg></a></div></div></div><svg class="main-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="273.6000061035156" height="450"><g class="hoverlayer"></g></svg></div></div></div></div></div></div></div></div></div>

