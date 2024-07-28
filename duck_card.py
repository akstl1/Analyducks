## imports

import dash
from dash import html, dcc  #, callback # If you need callbacks, import it here.
import dash_bootstrap_components as dbc

def create_card_A(name,about, city, country, date, weight, height, width, length):
    card_A = dbc.Card(
    [
        # dbc.CardImg(src=image, top=True,style={"border-top":"#2C2F36","border-top-left-radius":"2%","border-top-right-radius":"2%"}),
        dbc.CardBody(
            [
                html.H4(name, className="card-title"),
                html.P("About Me: "+str(about), className="card-text"),
                html.P("Purchase Location: "+city+", "+country, className="card-text"),
                html.P("Purchase Date: "+str(date), className="card-text"),
                html.P("Weight: "+str(weight)+"g", className="card-text"),
                html.P("H x W x L: "+str(height)+"cm x "+str(weight)+"cm x "+str(length)+"cm", className="card-text")
            ]
        ),
    ],
    style={"margin-top":"2em", "margin-bottom":"1em"
        #    ,"margin-left":left,"margin-right":right
           },
    className="cardA"
)
    return card_A