## imports

import datetime as dt
from datetime import date
import os
import requests

import dash
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output, State
from PIL import Image
import dash_bootstrap_components as dbc

## start up the app, and provide title and bootstrap ref
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.title="Analyducks"
server=app.server

## -------------------------------------------------------------------------------------------------
# data load

## read in excel dataset
df = pd.read_excel("data/data.xlsx", sheet_name="Ducks")

## convert date bought col to date, and extract year into a column
df['Date_Bought'] = pd.to_datetime(df['Date_Bought']).dt.date
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

yearly_df = df.groupby(["Year"]).agg({"Quantity":"sum"}).reset_index()

weight_df = df.groupby(["Year"]).agg({"Total_Weight":"sum"}).reset_index()

weight_cum_df = df.groupby(['Year']).sum().cumsum().reset_index()

## -------------------------------------------------------------------------------------------------
## figs

## bar plot showing ducks bought by purchaser

owner_bar = px.bar(buyer_df,x="Buyer", y="Quantity")
owner_bar.update_layout(title_text="Rubber Duck Distribution by Purchaser", 
                        title_x=0.5,
                        xaxis_title="Purchaser", 
                        yaxis_title="Quantity",
                        paper_bgcolor="rgba(0,0,0,0)"
                        )

## pie chart showing purchase method of ducks

purchase_fig = px.pie(purchase_method_df, values='Quantity', names='Purchase_Method')
purchase_fig.update_layout(title_text="Purchase Method Distribution",
                           title_x=0.5,
                           paper_bgcolor="rgba(0,0,0,0)"
                           )

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


## bar plot showing weight of ducks bought each year

weight_bar = px.bar(weight_df,x="Year", y="Total_Weight")
weight_bar.update_layout(title_text="Weight (g) of Annual Purchases",
                         title_x=0.5,
                         xaxis_title="Purchase Year",
                         yaxis_title="Weight (g)",
                         paper_bgcolor="rgba(0,0,0,0)"
                         )

## bar plot showing weight of ducks bought each year, cumulative

weight_bar_cumulative = px.bar(weight_cum_df,x="Year", y="Total_Weight")
weight_bar_cumulative.update_layout(title_text="Cumulative Collection Weight (g)",
                                    title_x=0.5,
                                    xaxis_title="Purchase Year", 
                                    yaxis_title="Cumulative Weight (g)",
                                    paper_bgcolor="rgba(0,0,0,0)"
                                    )

## bar plot showing number of ducks bought per year 

year_bar = px.bar(yearly_df,x="Year", y="Quantity")
year_bar.update_layout(title_text="Rubber Ducks Bought Per Year", 
                       title_x=0.5,
                       xaxis_title="Purchase Year",
                       yaxis_title="Quantity",
                       paper_bgcolor="rgba(0,0,0,0)"
                       )

## bar plot showing number of ducks bought per year, cumulative

year_bar_cumulative = px.bar(weight_cum_df,x="Year", y="Quantity")
year_bar_cumulative.update_layout(title_text="Total Rubber Ducks Owned",
                                  title_x=0.5,
                                  xaxis_title="Purchase Year", 
                                  yaxis_title="Quantity",
                                  paper_bgcolor="rgba(0,0,0,0)"
                                  )

map_fig = px.scatter_geo(df,
        lon = 'Longitude',
        lat = 'Latitude',
        hover_name="Name"      
        )

map_fig.update_traces(marker=dict(color="Red"))

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

## choropleth showing duck purchase by US state

state_fig = px.choropleth(state_df,locations="Purchase_State", 
                          locationmode="USA-states", 
                          color="Quantity", 
                          scope="usa"
                        #   color_continuous_scale="YlGn"
                          )
state_fig.update_layout(title_text="Rubber Duck Purchase By State",title_x=0.5)
state_fig.add_trace(map_fig.data[0])

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

## -------------------------------------------------------------------------------------------------
### App layout

app.layout = html.Div([
    html.Div([
        html.H1("Analyducks"),
        html.H4("A visual analysis of Allan K's rubber duck collection"),
        html.A("Click here to view my portfolio",href= "https://akstl1.github.io/")
    ],className="title"),
    html.Div([
        dbc.Card(
            dbc.CardBody(
                [
                    html.H2(total_ducks, className="card-title"),
                    html.H6("Total Ducks Owned", className="card-subtitle"),
                ]
        ),className='kpi'),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H2(ducks_bought_last_year, className="card-title"),
                    html.H6("Ducks Bought Within Last Year", className="card-subtitle"),
                ]
        ),className='kpi'),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H2(duck_weight, className="card-title"),
                    html.H6("Duck Collection Weight (g)", className="card-subtitle"),
                ]
        ),className='kpi'),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H2(unique_countries, className="card-title"),
                    html.H6("Unique Countries of Purchase", className="card-subtitle"),
                ]
        ),className='kpi'),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H2(unique_cities, className="card-title"),
                    html.H6("Unique Cities of Purchase", className="card-subtitle"),
                ]
        ),className='kpi')
    ],className='kpi-container'),
    html.Div([
              dcc.Graph(id='owner-bar',figure=owner_bar,className='graph1'),
              dcc.Graph(id='3d-scatter',figure=three_d_fig,className='graph1'),
              dcc.Graph(id='method-pie',figure=purchase_fig,className='graph1')
            ],className="graph-container"),
    html.Div([
              dcc.Graph(id='year-bar',figure=year_bar,className='graph2'), 
              dcc.Graph(id='year-bar-cumulative',figure=year_bar_cumulative,className='graph2'),
              dcc.Graph(id='weight-bar',figure=weight_bar,className='graph2'),
              dcc.Graph(id='weight-bar-cumulative',figure=weight_bar_cumulative,className='graph2')
            ],className="graph-container2"),
    html.Div([
                dcc.Graph(id='state-map',figure=state_fig,className="map"),
                dcc.Graph(id='country-map',figure=country_fig,className="map")
            ]),
    html.Div(dash_table.DataTable(
                id="table",
                data=df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df[["Name","Purchase_City","Purchase_Country","Date_Bought","About Me","Total_Weight","Height","Width","Length"]].columns],
                fixed_rows={'headers': True, 'data': 0 },
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                    },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth':'60px',
                    'width': '120px',
                    'lineHeight': '20px',
                    'color': 'black',
                    'backgroundColor': 'white'
                    },
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                    }]
    )),
    html.Br()
    
])

## -------------------------------------------------------------------------------------------------
# run app
if __name__=="__main__":
    app.run_server()