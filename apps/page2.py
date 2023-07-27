"""
This module contains the code for the Optimize page of the Dash app.

The Optimize page allows the user to enter a proposed budget and 
see how that budget might effect sales. Then can create an optimized
budget based on the model's predictions.

Author: Derrick Lewis
"""
import os

import dash_bootstrap_components as dbc
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv
from plotly.subplots import make_subplots

from plotly_theme_light import plotly_light

from apps.tables import (df_col_data_cond, opt_channel_col,
                         opt_channel_col_cond, tooltip_data_list)
from main import app

pio.templates["plotly_light"] = plotly_light
pio.templates.default = "plotly_light"
load_dotenv()


FOLDER = os.environ.get('FOLDER')


# Table settings
CELL_PADDING = 5
DATA_PADDING = 5
TABLE_PADDING = 1
FONTSIZE = 12


# ---------------------------------------------------------------------
# Python functions
# ---------------------------------------------------------------------


# Build some function, perhaps load data from a database or file




# ---------------------------------------------------------------------
# Create app layout
# ---------------------------------------------------------------------

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            [
                dcc.Markdown(id='intro',
                children = """
                ---
                # Markdown Area
                ---
                
                Inseert some markdown here to explain the page.
    
                
                ---
                """,
                className='md')
            ])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            [
            dbc.Button(
                'Calculate Proposed Budget', id='submit-prop', n_clicks=0,
                style={
                           'background-color': 'rgba(0, 203, 166, 0.7)',
                           'border': 'none',
                           'color': 'white',
                           'padding': '15px',
                           'margin-top': '5px',
                           'margin-bottom': '10px',
                           'text-align': 'center',
                           'text-decoration': 'none',
                           'font-size': '16px',
                           'border-radius': '26px'
                       }
                    ),
            ])
    ]),
    html.Br(),
    dcc.Graph(id='graph-main2'),
    
]
)

# ---------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------

@app.callback(
    [Output('graph-main2', 'figure')],
    [Input('submit-prop', 'n_clicks')])
def update_prop_chart(n_clicks, budget_data):
    if n_clicks == 0:
        return go.Figure()
    else:
        return go.Figure()
