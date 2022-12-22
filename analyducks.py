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

app = dash.Dash()
server=app.server

data = {'col_1':['Webbed developer','Spy Museum',43134,'????????','Allan','????????',1,7,2,2],'col_2':['Cannes-ard','Paris',44743,'je ne sais quack','Yev','????????',1,1,6,5],'col_3':['Iron Duck','Israel',44682,'????????','Allan','????????',1,1,6,1],'col_4':['Andy Rodduck','NY US Open',42979,'Game, Set Quack!','Allan','????????',1,7,1,7],'col_5':['Mini Mallards','Big E',44805,'????????','Allan','????????',2,2,3,5],'col_6':['Flights of the Round Table','DC/Bethesda',43160,'????????','Allan','????????',12,6,2,1],'col_7':['????????','Fuse',44228,'????????','Allan','????????',1,1,5,2],'col_8':['Creeper','????????',47484,'????????','Allan','????????',1,5,2,2],'col_9':['Beak-a-boos','STL',44501,'????????','Diana','????????',6,6,6,7],'col_10':['Universiduck','????????',47484,'Carnegie Mallard University','??????','????????',1,1,4,1],'col_11':['Evel Ksqueakel??????????????','Burlington',44774,'????????','Allan','????????',1,2,3,2],'col_12':['????????','Plymouth musem',44136,'????????','Allan','????????',1,6,4,7],'col_13':['Bill Bean','Cruise Ship',43070,'????????','Allan','????????',1,3,2,1],'col_14':['Liberduck','NY Trip',43435,'????????','Allan','????????',1,4,7,4],'col_15':["Quack's Guard",'London',43617,'????????','Allan','????????',1,2,6,6],'col_16':['RagnoQuack','Israel',44682,'????????','Allan','????????',1,2,4,6],'col_17':['Starducks','ice cream marblehead',44378,'????????','Allan','????????',1,5,4,7],'col_18':['Billcelona Bunch','Spain',43252,'????????','Marina','????????',2,7,6,7],'col_19':['Duck Lord / Lord of the wings','Fuse',43977,'Wing of Power  one wing to rule them all','Allan','????????',1,1,5,6],'col_20':['AnaQuack Skyflocker','Israel',44682,'????????','Allan','????????',1,4,5,5],'col_21':['Orduck 66','Israel',44682,'????????','Allan','????????',1,6,7,5],'col_22':['Spyduck','Spy Museum',43134,'License to Bill. No Time to Fly.','Allan','????????',1,1,1,4],'col_23':['Neil Wingstrong','Cape Canaveral',43101,'Cape CaQuackeral','Allan','????????',1,1,4,6],'col_24':['Constable Quack','Montreal',44774,'Royal Mounted Fowlice','Julia','????????',1,5,5,5],'col_25':['Extruduck','Fuse',44455,'????????','Allan','????????',1,1,6,2],'col_26':['Quack-O-Lantern','Ballston',43374,'????????','Allan','????????',1,2,1,7],'col_27':['LeDuckhosen','Austria',43617,'????????','Parents','????????',1,1,4,2],'col_28':['????????','DCA',43617,'????????','Allan','????????',1,3,3,2],'col_29':['Orthoduck','Israel museum',44682,'????????','Allan','????????',1,7,2,5],'col_30':['Arquackologist','Israel',44682,'????????','Allan','????????',1,6,3,3],'col_31':['Froduck','Fuse',43977,'????????','Allan','????????',1,6,3,5],'col_32':['Punk Duck','NY Essex Pizza Salem',44805,"We're up all night to get ducky",'Allan','????????',1,6,1,6],'col_33':['Fireflighter','AEPi',42795,'????????','Allan','????????',1,3,2,4],'col_34':['James Pond','Spy Museum',43134,'????????','Allan','????????',1,7,1,7],'col_35':['Duckdive','???????',47484,'????????','???','????????',1,6,7,2],'col_36':['????????','???????',47484,'????????','???','????????',1,7,4,3],'col_37':['Disco Bill','???????',47484,'????????','???','????????',1,7,4,3],'col_38':['????????','????????',44872,'????????','Rescue','????????',1,2,3,4],'col_39':['????????','????????',44872,'????????','Rescue','????????',1,2,1,4],}


df = pd.DataFrame.from_dict(data, orient='index',columns=['Name', 'Location', 'Date Bought', 'Fact','Buyer','Phrase','Qty','Weight','Height','Width'])
df['Date Bought'] = pd.TimedeltaIndex(df['Date Bought'], unit='d') + dt.datetime(1899, 12, 30)
df['year'] = pd.DatetimeIndex(df['Date Bought']).year
df['total weight'] = df.Qty*df.Weight
df2 = df.groupby(['year']).sum().cumsum().reset_index()
print(df)
print(df2)

# ------------------------------------------------------------------------------------------------

# ### calorie plot

# df['Daily_Green'] = df.Breakfast_Green+df.Lunch_Green+df.Dinner_Green+df.Snacks_Green
# df['Daily_Yellow'] = df.Breakfast_Yellow+df.Lunch_Yellow+df.Dinner_Yellow+df.Snacks_Yellow
# df['Daily_Red'] = df.Breakfast_Red+df.Lunch_Red+df.Dinner_Red+df.Snacks_Red

# cal_fig = go.Figure()
# cal_fig.add_trace(go.Bar(
#     y=df.Daily_Green,
#     x=df.Date,
#     name='Green',
#     text=df.Daily_Green,
#     marker=dict(
#         color='rgb(0,255,0)'
#     )
# ))
# cal_fig.add_trace(go.Bar(
#     y=df.Daily_Yellow,
#     x=df.Date,
#     name='Yellow',
#     text=df.Daily_Yellow,
#     marker=dict(
#         color='rgb(242,242,19)'
#     )
# ))
# cal_fig.add_trace(go.Bar(
#     y=df.Daily_Red,
#     x=df.Date,
#     name='Red',
#     text=df.Daily_Red,
#     marker=dict(
#         color='rgb(246, 78, 139)'
#     )
# ))
# cal_fig.update_layout(barmode='stack')
# cal_fig.update_layout(title_text='Daily Calorie and Calorie Density Breakdown', title_x=0.5)


# ### weight plot

# weight_fig = px.line(df, x="Date", y="Weight", title='Weight Over Time',markers=True)
# weight_fig.add_hline(y=155,line=dict(color='royalblue', width=4, dash='dot'))
# weight_fig.update_layout(yaxis_range=[150,180])
# weight_fig.update_layout(title_text="Weight Over Time", title_x=0.5)

# annotation = {
#     'xref': 'paper',
#     'yref': 'paper',
#     'x': 0.05,
#     'y': 0.27,
#     'text': 'Goal weight: 155 lb',
#     'showarrow': False,
#     'arrowhead': 0,
# }

# weight_fig.update_layout({'annotations': [annotation]})

## year bar plot

owner_bar = px.bar(df,x="Buyer", y="Qty")


## weight bar plot

weight_bar = px.bar(df,x="year", y="total weight")

## weight bar plot cumulative

weight_bar_cumulative = px.bar(df2,x="year", y="total weight")

## year bar plot

year_bar = px.bar(df,x="year", y="Qty")

## year bar plot cumulative

year_bar_cumulative = px.bar(df2,x="year", y="Qty")

### height width scatter plot

height_width_fig = px.scatter(df, x="Height", y="Width")
height_width_fig.update_traces(marker=dict(color='rgba(0,0,0,0)'), showlegend=False)

# maxDim = df[["Height", "Weight"]].max().idxmax()
# maxi = df[maxDim].max()
min_weight = df["Weight"].min()
max_weight = df["Weight"].max()

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
            sizex=(row["Weight"] - min_weight) / (max_weight - min_weight),
            sizey=(row["Weight"] - min_weight) / (max_weight - min_weight),
            sizing="contain",
            opacity=0.8,
            layer="above"
        )
    )



# height_weight_fig.update_layout(yaxis_range=[0,1500])
# height_weight_fig.update_layout(title_text="Steps", title_x=0.5)

# ### App layout

app.layout = html.Div([
    html.Div(dcc.Graph(id='height-scatter',className="graph",figure=height_width_fig)),
    html.Div(dcc.Graph(id='year-bar',figure=year_bar)),
    html.Div(dcc.Graph(id='year-bar-cumulative',figure=year_bar_cumulative)),
    html.Div(dcc.Graph(id='owner-bar',figure=owner_bar)),
    html.Div(dcc.Graph(id='weight-bar',figure=weight_bar)),
    html.Div(dcc.Graph(id='weight-bar-cumulative',figure=weight_bar_cumulative))
])

# app.layout = html.Div([
#         # create a div to store each graph
#         html.Div([html.H1('Physical Health Dashboard')],style={'text-align':'center'}),
#         html.Div([
#         dcc.DatePickerRange(id='my-date-range-picker',
#     start_date=start_date,
#     end_date=end_date,
#     calendar_orientation='vertical',
#     min_date_allowed = min_date,
#     max_date_allowed = max_date
# )
#         ], style={'text-align':'center'}),
#         html.Div([dcc.Graph(id='weight-graph',figure=weight_fig)]),
#         html.Div([dcc.Graph(id='cal-graph',figure=cal_fig)]),
#         html.Div([dcc.Graph(id='exercise-graph',figure=exercise_fig)]),
#         html.Div([dcc.Graph(id='pct-graph',figure=pct_fig)]),
#         html.Div([
#             dcc.Input(
#                 id='adding-rows-name',
#                 placeholder='Enter a column name...',
#                 value='',
#                 style={'padding': 10}
#             ),
#             html.Button('Add Column', id='adding-columns-button', n_clicks=0)
#         ], style={'height': 50}),
#         dcc.Interval(id='interval_pg', interval=86400000*7, n_intervals=0),  # activated once/week or when page refreshed
#         html.Div(id='postgres_datatable'),
#         html.Button('Add Row', id='editing-rows-button', n_clicks=0),
#         html.Button('Save to PostgreSQL', id='save_to_postgres', n_clicks=0),

#         # Create notification when saving to excel
#         html.Div(id='placeholder', children=[]),
#         dcc.Store(id="store", data=0),
#         dcc.Interval(id='interval', interval=86400000*7),
#         html.Div([html.H1('-')], style={'opacity':'0'})
# ])


# ## -------------------------------------------------------------------------------------------------

# @app.callback(Output('height-scatter','figure'))
# def height_scatter():
#     exercise_fig = px.scatter(df, x="Height", y="Weight")
#     return exercise_fig


# @app.callback(Output('postgres_datatable', 'children'),
#               [Input('interval_pg', 'n_intervals')],
#               [Input(component_id='my-date-range-picker',component_property='start_date')],
#                [Input(component_id='my-date-range-picker',component_property='end_date')])
# def populate_datatable(n_intervals,start_date,end_date):
#     start_date = dt.datetime.strptime(start_date,'%Y-%m-%d').date()
#     end_date = dt.datetime.strptime(end_date,'%Y-%m-%d').date()
#     df = pd.read_sql_table('nutrition_table', con=db.engine)
#     df.Date = df.Date.apply(lambda x:dt.datetime.strptime(x,'%Y-%m-%d').date())
#     df = df[(df.Date>=start_date) & (df.Date<=end_date)]
#     return [
#         dash_table.DataTable(
#             id='our-table',
#             columns=[{
#                          'name': str(x),
#                          'id': str(x),
#                          'deletable': False,
#                      } if x == 'Date'
#                      else {
#                 'name': str(x),
#                 'id': str(x),
#                 'deletable': True,
#             }
#                      for x in df.columns],
#             data=df.to_dict('records'),
#             editable=True,
#             row_deletable=True,
#             filter_action="native",
#             sort_action="native",  # give user capability to sort columns
#             sort_mode="single",  # sort across 'multi' or 'single' columns
#             page_action='none',  # render all of the data at once. No paging.
#             style_table={'height': '300px', 'overflowY': 'auto'},
#             style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'}
#             # style_cell_conditional=[
#             #     {
#             #         'if': {'column_id': c},
#             #         'textAlign': 'right'
#             #     } for c in ['Date']
#             # ]

#         ),
#     ]

# @app.callback(
#     Output('our-table', 'columns'),
#     [Input('adding-columns-button', 'n_clicks')],
#     [State('adding-rows-name', 'value'),
#      State('our-table', 'columns')],
#     prevent_initial_call=True)
# def add_columns(n_clicks, value, existing_columns):
#     if n_clicks > 0:
#         existing_columns.append({
#             'name': value, 'id': value,
#             'renamable': True, 'deletable': True
#         })
#     return existing_columns


# @app.callback(
#     Output('our-table', 'data'),
#     [Input('editing-rows-button', 'n_clicks')],
#     [State('our-table', 'data'),
#      State('our-table', 'columns')],
#     prevent_initial_call=True)
# def add_row(n_clicks, rows, columns):
#     if n_clicks > 0:
#         rows.append({c['id']: '' for c in columns})
#     return rows

# @app.callback(
#     [Output('placeholder', 'children'),
#      Output("store", "data")],
#     [Input('save_to_postgres', 'n_clicks'),
#      Input("interval", "n_intervals")
#      ],
#     [State('our-table', 'data'),
#      State('store', 'data')],
#     prevent_initial_call=True)
# def df_to_csv(n_clicks, n_intervals, dataset, s):
#     output = html.Plaintext("The data has been saved to your PostgreSQL database.",
#                             style={'color': 'green', 'font-weight': 'bold', 'font-size': 'large'})
#     no_output = html.Plaintext("", style={'margin': "0px"})

#     input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

#     if input_triggered == "save_to_postgres":
#         s = 6
#         pg = pd.DataFrame(dataset)
#         pg.to_sql("nutrition_table", con=db.engine, if_exists='replace', index=False)
#         return output, s
#     elif input_triggered == 'interval' and s > 0:
#         s = s - 1
#         if s > 0:
#             return output, s
#         else:
#             return no_output, s
#     elif s == 0:
#         return no_output, s



# @app.callback(Output(component_id='cal-graph', component_property='figure'),
#               Output(component_id='weight-graph', component_property='figure'),
#               Output(component_id='exercise-graph', component_property='figure'),
#               Output(component_id='pct-graph', component_property='figure'),
#               [Input(component_id='my-date-range-picker',component_property='start_date')],
#                [Input(component_id='my-date-range-picker',component_property='end_date')])
# def update_cal_graph(start_date,end_date):

#     start_date = dt.datetime.strptime(start_date,'%Y-%m-%d').date()
#     end_date = dt.datetime.strptime(end_date,'%Y-%m-%d').date()

#     # df = pd.read_excel('./data_df.xlsx', 'df',converters = {'Date':dt.datetime.date}).fillna(0)

#     df = pd.read_sql_table('nutrition_table', con=db.engine).fillna(0)
#     df.Date = df.Date.apply(lambda x:dt.datetime.strptime(x,'%Y-%m-%d').date())
#     for col in df.columns:
#         if col=="Weight":
#             df[col] = df[col].astype('float')
#         elif col!="Date":
#             df[col] = df[col].astype('int')
#     # print('start',start_date,type(start_date),'end',end_date,type(end_date),'dates',df.Date[0],type(df.Date[0]))
#     df = df[(df.Date>=start_date) & (df.Date<=end_date)]
#     df['Daily_Green'] = df.Breakfast_Green+df.Lunch_Green+df.Dinner_Green+df.Snacks_Green
#     df['Daily_Yellow'] = df.Breakfast_Yellow+df.Lunch_Yellow+df.Dinner_Yellow+df.Snacks_Yellow
#     df['Daily_Red'] = df.Breakfast_Red+df.Lunch_Red+df.Dinner_Red+df.Snacks_Red

#     cal_fig = go.Figure()
#     cal_fig.add_trace(go.Bar(
#         y=df.Daily_Green,
#         x=df.Date,
#         name='Green',
#         text=df.Daily_Green,
#         marker=dict(
#             color='rgb(0,255,0)'
#         )
#     ))
#     cal_fig.add_trace(go.Bar(
#         y=df.Daily_Yellow,
#         x=df.Date,
#         name='Yellow',
#         text=df.Daily_Yellow,
#         marker=dict(
#             color='rgb(242,242,19)'
#         )
#     ))
#     cal_fig.add_trace(go.Bar(
#         y=df.Daily_Red,
#         x=df.Date,
#         name='Red',
#         text=df.Daily_Red,
#         marker=dict(
#             color='rgb(246, 78, 139)'
#         )
#     ))
#     cal_fig.update_layout(barmode='stack')
#     cal_fig.update_layout(title_text='Daily Calorie and Calorie Density Breakdown', title_x=0.5)
#     cal_fig.update_xaxes(fixedrange=True,tickformat="%m/%d/%Y")
#     # cal_fig.update_xaxes(dtick=86400000)
#     cal_fig.update_layout(xaxis=dict(tickformat="%m/%d/%Y"))



#     ### weight plot

#     weight_fig = px.line(df, x="Date", y="Weight", title='Weight Over Time',markers=True)
#     weight_fig.add_hline(y=155,line=dict(color='royalblue', width=4, dash='dot'))
#     weight_fig.update_layout(yaxis_range=[150,180])
#     weight_fig.update_layout(title_text="Weight Over Time", title_x=0.5)

#     annotation = {
#         'xref': 'paper',
#         'yref': 'paper',
#         'x': 0.05,
#         'y': 0.27,
#         'text': 'Goal weight: 155 lb',
#         'showarrow': False,
#         'arrowhead': 0,
#     }

#     weight_fig.update_layout({'annotations': [annotation]})
#     # weight_fig.update_xaxes(dtick=86400000)
#     weight_fig.update_layout(xaxis=dict(tickformat="%m/%d/%Y"))

#     ### exercise plot

#     exercise_fig = px.line(df, x="Date", y="Steps",markers=True)
#     exercise_fig.update_layout(yaxis_range=[0,25000])
#     exercise_fig.update_layout(title_text="Steps", title_x=0.5)
#     exercise_fig.add_hline(y=10000,line=dict(color='royalblue', width=4, dash='dot'))
#     annotation = {
#         'xref': 'paper',
#         'yref': 'paper',
#         'x': 0.05,
#         'y': 0.45,
#         'text': 'Goal steps: 10,000',
#         'showarrow': False,
#         'arrowhead': 0,
#     }

#     exercise_fig.update_layout({'annotations': [annotation]})
#     # exercise_fig.update_xaxes(dtick=86400000)
#     exercise_fig.update_layout(xaxis=dict(tickformat="%m/%d/%Y"))

#     ### calorie breakdown chart

#     breakfast_total = sum(df.Breakfast_Green+df.Breakfast_Yellow+df.Breakfast_Red)
#     if breakfast_total:
#         breakfast_green_pct = 100*sum(df.Breakfast_Green)/breakfast_total
#         breakfast_yellow_pct = 100*sum(df.Breakfast_Yellow)/breakfast_total
#         breakfast_red_pct = 100*sum(df.Breakfast_Red)/breakfast_total
#     else:
#         breakfast_green_pct,breakfast_yellow_pct,breakfast_red_pct =0,0,0

#     lunch_total = sum(df.Lunch_Green+df.Lunch_Yellow+df.Lunch_Red)
#     if lunch_total:
#         lunch_green_pct = 100*sum(df.Lunch_Green)/lunch_total
#         lunch_yellow_pct = 100*sum(df.Lunch_Yellow)/lunch_total
#         lunch_red_pct = 100*sum(df.Lunch_Red)/lunch_total
#     else:
#         lunch_green_pct,lunch_yellow_pct,lunch_red_pct=0,0,0

#     dinner_total = sum(df.Dinner_Green+df.Dinner_Yellow+df.Dinner_Red)
#     if dinner_total:
#         dinner_green_pct = 100*sum(df.Dinner_Green)/dinner_total
#         dinner_yellow_pct = 100*sum(df.Dinner_Yellow)/dinner_total
#         dinner_red_pct = 100* sum(df.Dinner_Red)/dinner_total
#     else:
#         dinner_green_pct,dinner_yellow_pct,dinner_red_pct=0,0,0

#     snack_total = sum(df.Snacks_Green+df.Snacks_Yellow+df.Snacks_Red)
#     if snack_total:
#         snacks_green_pct = 100*sum(df.Snacks_Green)/snack_total
#         snacks_yellow_pct = 100*sum(df.Snacks_Yellow)/snack_total
#         snacks_red_pct = 100*sum(df.Snacks_Red)/snack_total
#     else:
#         snacks_green_pct,snacks_yellow_pct,snacks_red_pct=0,0,0

#     d2= {'Green': [breakfast_green_pct,lunch_green_pct,dinner_green_pct,snacks_green_pct],
#          'Yellow': [breakfast_yellow_pct,lunch_yellow_pct,dinner_yellow_pct,snacks_yellow_pct],
#          'Red':[breakfast_red_pct,lunch_red_pct,dinner_red_pct, snacks_red_pct]

#                       }

#     d = pd.DataFrame(data=d2, index=['Breakfast','Lunch','Dinner','Snacks']).round(2)
#     pct_fig = go.Figure()
#     pct_fig.add_trace(go.Bar(
#         y=d.index,
#         x=d.Green,
#         name='Green',
#         orientation='h',
#         text=d.Green,
#         marker=dict(
#             color='rgb(0,255,0)'
#         )
#     ))
#     pct_fig.add_trace(go.Bar(
#         y=d.index,
#         x=d.Yellow,
#         name='Yellow',
#         orientation='h',
#         text=d.Yellow,
#         marker=dict(
#             color='rgb(242,242,19)'
#         )
#     ))
#     pct_fig.add_trace(go.Bar(
#         y=d.index,
#         x=d.Red,
#         name='Red',
#         orientation='h',
#         text=d.Red,
#         marker=dict(
#             color='rgb(246, 78, 139)'
#         )
#     ))
#     pct_fig.update_layout(barmode='stack')
#     pct_fig.update_layout(title_text="Calorie Density Breakdown by Meal (%)", title_x=0.5)

#     return cal_fig,weight_fig,exercise_fig,pct_fig


# run app
if __name__=="__main__":
    app.run_server()
