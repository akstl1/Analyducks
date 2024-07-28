## imports

import dash
from dash import html, dcc  #, callback # If you need callbacks, import it here.
import dash_bootstrap_components as dbc

def create_card_A(name,description):
    card_A = dbc.Card(
    [
        # dbc.CardImg(src=image, top=True,style={"border-top":"#2C2F36","border-top-left-radius":"2%","border-top-right-radius":"2%"}),
        dbc.CardBody(
            [
                html.H4(name, className="card-title"),
                html.P(
                    description,
                    className="card-text",
                )
            ]
        ),
    ],
    style={"margin-top":"2em", "margin-bottom":"1em"
        #    ,"margin-left":left,"margin-right":right
           },
    className="cardA"
)
    return card_A