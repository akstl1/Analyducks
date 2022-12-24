import datetime as dt
from datetime import date
import os

import dash
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output, State
from PIL import Image
import dash_bootstrap_components as dbc

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server=app.server

## -------------------------------------------------------------------------------------------------
# data load

df = pd.read_excel("data/data.xlsx", sheet_name="Ducks")
df['Date_Bought'] = pd.to_datetime(df['Date_Bought']).dt.date
# df.Date_Bought = pd.DatetimeIndex(df.Date_Bought).strftime("%d-%m-%Y")
df['Year'] = pd.DatetimeIndex(df['Date_Bought']).year
df['Avg_Weight'] = np.round(df.Total_Weight/df.Quantity,2)
df2 = df.groupby(['Year']).sum().cumsum().reset_index()
## -------------------------------------------------------------------------------------------------
## figs

## year bar plot

owner_bar = px.bar(df,x="Buyer", y="Quantity")
owner_bar.update_layout(title_text="Rubber Duck Distribution by Purchaser", title_x=0.5,xaxis_title="Purchaser", yaxis_title="Quantity")


## weight bar plot

weight_bar = px.bar(df,x="Year", y="Avg_Weight")
weight_bar.update_layout(title_text="Weight (g) of Rubber Ducks Bought Per Year", title_x=0.5,xaxis_title="Purchase Year", yaxis_title="Weight (g)")

## weight bar plot cumulative

weight_bar_cumulative = px.bar(df2,x="Year", y="Total_Weight")
weight_bar_cumulative.update_layout(title_text="Cumulative Weight of Rubber Ducks Bought", title_x=0.5,xaxis_title="Purchase Year", yaxis_title="Cumulative Weight (g)")

## year bar plot

year_bar = px.bar(df,x="Year", y="Quantity")
year_bar.update_layout(title_text="Number of Rubber Ducks Bought Per Year", title_x=0.5,xaxis_title="Purchase Year", yaxis_title="Quantity Bought")

## year bar plot cumulative

year_bar_cumulative = px.bar(df2,x="Year", y="Quantity")
year_bar_cumulative.update_layout(title_text="Total Rubber Ducks Owned", title_x=0.5,xaxis_title="Purchase Year", yaxis_title="Quantity")

### height width scatter plot

height_width_fig = px.scatter(df, x="Height", y="Width")
height_width_fig.update_traces(marker=dict(color='rgba(0,0,0,0)'), showlegend=False)

# maxDim = df[["Height", "Weight"]].max().idxmax()
# maxi = df[maxDim].max()
min_weight = df["Avg_Weight"].min()
max_weight = df["Avg_Weight"].max()

for i, row in df.iterrows():
    # country = row['country'].replace(" ", "-")
    height_width_fig.add_layout_image(
        dict(
            source=Image.open(f"ducks/png/duck2.png"),
            xref="x",
            yref="y",
            xanchor="center",
            yanchor="middle",
            x=row["Height"],
            y=row["Width"],
            sizex=5*(row["Avg_Weight"] - min_weight) / (max_weight - min_weight),
            sizey=5*(row["Avg_Weight"] - min_weight) / (max_weight - min_weight),
            sizing="contain",
            opacity=0.8,
            layer="above"
        )
    )

height_width_fig.update_layout(title_text="Rubber Duck Height vs Width", title_x=0.5,xaxis_title="Height (cm)", yaxis_title="Width (cm)")


##

map_fig = go.Figure(data=go.Scattergeo(
        lon = df['Longitude'],
        lat = df['Latitude'],
        text = df['Name'],
        mode = 'markers'
        # marker_color = df['cnt'],
        ))
map_fig.update_layout(title_text="Rubber Duck Purchase Locations",title_x=0.5)

## kpis

duck_weight = df["Total_Weight"].sum()
total_ducks = df["Quantity"].sum()
unique_countries = df.Purchase_Country.nunique()
unique_cities = df.Purchase_City.nunique()
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
        html.H4("A visual analysis of my rubber duck collection")
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
    html.Div([dcc.Graph(id='height-scatter',figure=height_width_fig,className='graph'), 
              dcc.Graph(id='owner-bar',figure=owner_bar,className='graph')]),
    html.Div([dcc.Graph(id='year-bar',figure=year_bar,className='graph'), 
              dcc.Graph(id='year-bar-cumulative',figure=year_bar_cumulative,className='graph')]),
    html.Div([dcc.Graph(id='weight-bar',figure=weight_bar,className='graph'),
              dcc.Graph(id='weight-bar-cumulative',figure=weight_bar_cumulative,className='graph')]),
    html.Div([dcc.Graph(id='map',figure=map_fig)]),
    html.Div(dash_table.DataTable(
                id="table",
                data=df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df[["Name","Purchase_City","Date_Bought","Fun Fact","Total_Weight","Height","Width","Length"]].columns],
                fixed_rows={'headers': True, 'data': 0 },
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold',
                     'width':'20px'
                    },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'width': '50px',
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