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
                # Explore Chicago Crime Statistics
                ---
                
                Below is a project to explore the publicly available Chicago Crime Statistics through 
                Google BigQuery.

                [Chicago Crime Statisics](https://cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console)
    
                The task is to create a `dataset` for each of 4 questions. The datasets were created in the
                bigquery console and then queried here to explore.

                As the core concept of the project is to show the ability to query the data, the full query used
                to create each dataset is shown on the respective page.

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
                    dbc.CardImg(src="/static/images/channel.png", top=True, style={'opacity': '0.05'}),
                    dbc.CardImgOverlay(
                    dbc.CardBody(
                        [
                            dcc.Markdown("""
                            ---
                            # Question  - 1
                            ---

                            Which beats are in the top and bottom 2% for arrest rate for residence crime in each district in 2020?
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
                ]
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
                                            
                                    What are the top 5 primary crime types in 2020 by comminity area?
                                    """,
                                    style={
                                        'font-family': 'plain',
                                        'color': 'grey',
                                        'font-weight': 'light'
                                        # 'font-size': '12px',
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
                        )
                    )
                ]
            ),
            ], width=5
            ),
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

                        What street in each ward had the most domestic crimes in 2020?
                        """,
                            style={
                                'font-family': 'plain',
                                'color': 'grey',
                                'font-weight': 'light'
                                }
                            ),
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
                            )
                        ]
                    ))
                ]
            ), width=5
            ),
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

                                Which crime is the most common between 12am-6am cst 6am-12pm cst, 12pm-6pm cst and 6pm-12pm cst and what is the arrest rate for each period?
                                """,
                                    style={
                                        'font-family': 'plain',
                                        'color': 'grey',
                                        'font-weight': 'light'
                                        }
                                    ),
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
                                )
                            ]
                        )
                    )
                ]
            ), 
            width=5
        )
        ]
    )
])
