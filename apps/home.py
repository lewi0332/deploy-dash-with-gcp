import os
from dash import html, dcc
import dash_bootstrap_components as dbc
from main import app
from dotenv import load_dotenv

load_dotenv()


FOLDER = os.environ.get('FOLDER')

# Dummy page to get started.
layout = dbc.Container([
    dbc.Row(
        [
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardImg(src="/static/images/home.png", top=True, style={'opacity': '0.2'}),
                    dbc.CardBody(
                        [
                            dcc.Markdown("""
                        ---
                        # Example Card - 1
                        ---

                        Add something here
                        """,
                             style={
                                 'font-family': 'plain',
                                 'color': 'grey',
                                 'font-weight': 'light'
                             }),
                            html.Br(),
                            dbc.Button(
                                'View Page',
                                href='/model',
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
                        ],
                    )
                ],
                style={"width": "18rem"},
            ),
            width=4
        ),
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardImg(src="/static/images/channel.png", top=True, style={'opacity': '0.2'}),
                    dbc.CardBody(
                        [
                            dcc.Markdown("""
                                ---
                                # Example Card - 2
                                ---

                                Add something here
                                """,
                                style={
                                    'font-family': 'plain',
                                    'color': 'grey',
                                    'font-weight': 'light'
                                }),
                            html.Br(),
                            dbc.Button(
                                'View Page', 
                                href='/channel_behavior',
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
                        ],
                    )
                ], 
                style={"width": "18rem"},
            ),
            ], width=4),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardImg(src="/static/images/optimise.png", top=True, style={'opacity': '0.2'}),
                    dbc.CardBody(
                        [
                            dcc.Markdown("""
                        ---
                        # Example Card - 3
                        ---

                        Add something here
                        """,
                            style={
                                'font-family': 'plain',
                                'color': 'grey',
                                'font-weight': 'light'
                                }
                            ),
                            html.Br(),
                            dbc.Button(
                                'View Page', 
                                href='/optimize',
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
                            html.Br()
                        ]
                    )
                ], style={"width": "18rem"},
            ), width=4)
        ]
    ),
])
