import datetime as dt
import os
from datetime import timedelta

import dash
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output, State
from PIL import Image
import math

app = dash.Dash()
server=app.server

df = pd.read_excel("data/data.xlsx", sheet_name="Ducks")

df['Year'] = pd.DatetimeIndex(df['Date_Bought']).year
df['Avg_Weight'] = np.round(df.Total_Weight/df.Quantity,2)
df2 = df.groupby(['Year']).sum().cumsum().reset_index()
print(df)
print(df2)

# ------------------------------------------------------------------------------------------------
## figs

## year bar plot

owner_bar = px.bar(df,x="Buyer", y="Quantity")
owner_bar.update_layout(title_text="Rubber Duck Distribution by Purchase", title_x=0.5,xaxis_title="Purchaser", yaxis_title="Quantity")


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
        # text = df['text'],
        mode = 'markers'
        # marker_color = df['cnt'],
        ))

## kpis

# kpi_fig = go.Figure()

# kpi_fig.add_trace(go.Indicator(
#     mode = "number+delta",
#     value = 200,
#     domain = {'x': [0, 0.5], 'y': [0, 0.5]},
#     delta = {'reference': 400, 'relative': True, 'position' : "top"}))

### App layout

app.layout = html.Div([
    # html.Div(dcc.Graph(id='kpi', figure=kpi_fig)),
    html.Div([dcc.Graph(id='height-scatter',className="graph",figure=height_width_fig),
             dcc.Graph(id='owner-bar',figure=owner_bar)]),
    # html.Div(dcc.Graph(id='owner-bar',figure=owner_bar)),
    html.Div(dcc.Graph(id='year-bar',figure=year_bar)),
    html.Div(dcc.Graph(id='year-bar-cumulative',figure=year_bar_cumulative)),
    html.Div(dcc.Graph(id='weight-bar',figure=weight_bar)),
    html.Div(dcc.Graph(id='weight-bar-cumulative',figure=weight_bar_cumulative)),
    html.Div(dcc.Graph(id='map',figure=map_fig)),
    html.Div(dash_table.DataTable(
                id="table",
                data=df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns]
))
    
])

# ## -------------------------------------------------------------------------------------------------


# run app
if __name__=="__main__":
    app.run_server()
