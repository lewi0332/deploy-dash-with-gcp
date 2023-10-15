import os
from dash import html, dcc
import dash_bootstrap_components as dbc
from main import app
from dotenv import load_dotenv

load_dotenv()


# Dummy page to get started.
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
                """
                ),
            ]
        )
    ]),
    dbc.Row(
        [
        dbc.Col(width=1),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardImg(src="/static/images/channel.png", top=True, style={'opacity': '0.05', 'width': '100%'}),
                    dbc.CardImgOverlay(
                    dbc.CardBody(
                        [
                            dcc.Markdown("""
                        ---
                        # Question  - 1
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
                                href='/Q1',
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
                    )
                ],
            ),
            width=5
        ),
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardImg(src="/static/images/channel.png", top=True, style={'opacity': '0.05'}),
                    dbc.CardImgOverlay(
                    dbc.CardBody(
                        [
                            dcc.Markdown("""
                                ---
                                # Question  - 2
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
                                href='/Q2',
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
                    ))
                ], 
            ),
            ], width=5),
        ]
    ),
    html.Br(),
    html.Br(),
    dbc.Row(
        [
        dbc.Col(width=1),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardImg(src="/static/images/channel.png", top=True, style={'opacity': '0.05'}),
                    dbc.CardImgOverlay(
                        dbc.CardBody(
                        [
                            dcc.Markdown("""
                        ---
                        # Question - 3
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
                                href='/Q3',
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
                    ))
                ],
            ), width=5),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardImg(src="/static/images/channel.png", top=True, style={'opacity': '0.05'}),
                    dbc.CardImgOverlay(
                        dbc.CardBody(
                        [
                            dcc.Markdown("""
                        ---
                        # Question - 4
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
                                href='/Q4',
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
                    ))
                ],
            ), width=5)
        ]
    ),
])
