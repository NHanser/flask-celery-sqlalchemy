from datetime import datetime as dt

from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from flask_login import current_user
import numpy as np

def register_callbacks(dashapp):
    @dashapp.callback(
        Output('my-graph', 'figure'),
        Input('my-dropdown', 'value'),
        State('user-store', 'data'))
    def update_graph(selected_dropdown_value, data):
        x = np.linspace(0,7,100)
        if selected_dropdown_value == 'sin':
            y = np.sin(x)
        elif selected_dropdown_value == 'cos':
            y = np.cos(x)
        return {
            'data': [{
                'x': x,
                'y': y
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }

    @dashapp.callback(
        Output('user-store', 'data'),
        Input('my-dropdown', 'value'),
        State('user-store', 'data'))
    def cur_user(args, data):
        if current_user.is_authenticated:
            return current_user.email

    @dashapp.callback(Output('username', 'children'), Input('user-store', 'data'))
    def username(data):
        if data is None:
            return ''
        else:
            return f'Hello {data}'