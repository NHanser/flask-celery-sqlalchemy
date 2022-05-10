from dash import dcc
from dash import html
from flask import current_app as app

options = [{'label': 'sin', 'value': 'sin'}, {'label': 'cos', 'value': 'cos'}]
layout = html.Div(id='main', children=[
    html.H1(id='username'),
    html.H1('Dash demo'),
    dcc.Dropdown(
        id='my-dropdown',
        options=options,
        value=options[0]["value"]
    ),
    dcc.Graph(id='my-graph'),
    dcc.Store(id='user-store'),
], style={'width': '500'})