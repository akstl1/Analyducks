## imports

import dash
from dash import html, dcc, register_page  #, callback # If you need callbacks, import it here.
import webbrowser
import numpy as np
import datetime as dt
from datetime import date
import os
from dash import dash_table
import dash_bootstrap_components as dbc



def duck_card(dt,ttle):

    card = dbc.Card(
            dbc.CardBody(
                [
                    html.H2(dt, className="card-title"),
                    html.H6(ttle, className="card-subtitle"),
                ]
        ),
        style={
            # 'display': 'inline-block',
            # 'width': '18%',
            # 'margin-left':'1%',
            # 'margin-right': '1%',
            # 'margin-bottom': '.5%',
            'text-align': 'center',
            'background-color':'white'
        }, className = "duckCard"
        )
        # ])
    return card