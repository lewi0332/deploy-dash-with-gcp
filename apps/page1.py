"""
This module contains the code for the Optimize page of the Dash app.

The Optimize page allows the user to enter a proposed budget and 
see how that budget might effect sales. Then can create an optimized
budget based on the model's predictions.

Author: Derrick Lewis
"""
import plotly.graph_objects as go
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_ag_grid as dag
from google.cloud import bigquery
from dotenv import load_dotenv
from apps.tables import BOTTOMcolumnDefs, TOPcolumnDefs, defaultColDef

from plotly_theme_light import plotly_light

from apps.tables import (df_col_data_cond, opt_channel_col,
                         opt_channel_col_cond, tooltip_data_list)
from main import app

pio.templates["plotly_light"] = plotly_light
pio.templates.default = "plotly_light"
load_dotenv()

client = bigquery.Client(project='dashapp-375513')



# Table settings
CELL_PADDING = 5
DATA_PADDING = 5
TABLE_PADDING = 1
FONTSIZE = 12


# ---------------------------------------------------------------------
# Python functions
# ---------------------------------------------------------------------


# Build some function, perhaps load data from a database or file
def load_top_data():
    query = """
    SELECT
        district,
        TOP_02.beat AS TOP_02_beat,
        TOP_02.arrest_rate AS TOP_02_arrest_rate,
    FROM
        `dashapp-375513.Q1_ranked_residential_beats_per_district_2020.arrest_rates_per_beat_2020`,
        UNNEST(TOP_02) AS TOP_02
    """
    dff = client.query(query).to_dataframe()
    return dff.to_dict('records')

def load_bottom_data():
    query = """
    SELECT
        district,
        BOTTOM_02.beat AS BOTTOM_02_beat,
        BOTTOM_02.arrest_rate AS BOTTOM_02_arrest_rate,
    FROM
        `dashapp-375513.Q1_ranked_residential_beats_per_district_2020.arrest_rates_per_beat_2020`,
        UNNEST(BOTTOM_02) AS BOTTOM_02
    """
    dff = client.query(query).to_dataframe()
    return dff.to_dict('records')


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
                
                Insert some markdown here to explain the page.
    
                ---
                """,
                className='md')
            ])
    ]),
    dbc.Row(
        dbc.Col(
                dcc.Markdown(id='codeblock',
                children = """
                ```sql
                CREATE SCHEMA `dashapp-375513.Q1_ranked_residential_beats_per_district_2020` 
                OPTIONS (
                    description = "Which beats are in the top and bottom 2% for arrest rate for residence crime in each district in 2020?",
                    location = 'us');
                CREATE OR REPLACE TABLE
                `dashapp-375513.Q1_ranked_residential_beats_per_district_2020.arrest_rates_per_beat_2020` AS (
                WITH
                    CTE AS (
                    -- Duplicate Case numbers? I made some assumptions to de-dupe. I would verify in the real world.
                        WITH RAW AS (
                            SELECT
                                district,
                                beat,
                                CAST(arrest AS INT) AS arrest,
                                ROW_NUMBER () OVER (PARTITION BY case_number ORDER BY updated_on DESC) RN
                            FROM
                                `bigquery-public-data.chicago_crime.crime`
                            WHERE
                                location_description = 'RESIDENCE'
                                AND year = 2020 )
                            SELECT
                                district,
                                beat,
                                CASE
                                    WHEN SUM(arrest) = 0 THEN 0
                                ELSE
                                SAFE_DIVIDE(SUM(arrest), COUNT(arrest))
                                END AS arrest_rate
                            FROM RAW
                            WHERE RN=1
                            GROUP BY
                                1,
                                2 
                ),
                PERCS AS (
                    SELECT
                        district,
                        APPROX_QUANTILES(arrest_rate, 100)[OFFSET(98)] AS percentile_98,
                        APPROX_QUANTILES(arrest_rate, 100)[OFFSET(02)] AS percentile_02
                    FROM
                        CTE
                    GROUP BY
                        1 ),
                HIGHS AS (
                    SELECT
                        CTE.district,
                        ARRAY_AGG(STRUCT(CTE.beat, CTE.arrest_rate)) TOP_02
                    FROM
                        CTE
                    LEFT JOIN
                        PERCS
                    ON
                        CTE.district = PERCS.district
                    WHERE
                        CTE.arrest_rate >= PERCS.percentile_98
                    GROUP BY
                        1
                ),
                LOWS AS (
                    SELECT
                        CTE.district,
                        ARRAY_AGG(STRUCT(CTE.beat, CTE.arrest_rate)) BOTTOM_02
                    FROM
                        CTE
                    LEFT JOIN
                        PERCS
                    ON
                        CTE.district = PERCS.district
                    WHERE
                        CTE.arrest_rate <= PERCS.percentile_02
                    GROUP BY
                    1
                )
                SELECT
                    LOWS.district,
                    LOWS.BOTTOM_02,
                    HIGHS.TOP_02
                FROM
                    LOWS
                LEFT JOIN
                    HIGHS
                ON
                    LOWS.district = HIGHS.district
                ORDER BY
                    1
                );
                ```
                """,
                
                className='md')
            ),
        style={"maxHeight": "400px", "overflow": "scroll"}
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dcc.Markdown(
                children = """
                ---
                ### Top 2% Arrest Rate by District
                """,
                className='md'),
        width=5),
        dbc.Col(width=1),
        dbc.Col(
            dcc.Markdown(id='intro',
                children = """
                ---
                ### Bottom 2% Arrest Rate by District
                """,
                className='md')
        ),
    ]),
    dbc.Row([
        dbc.Col(
            [
            html.Br(),
            dag.AgGrid(
                id="datatable-main",
                rowData=load_top_data(),
                className="ag-theme-material",
                columnDefs=TOPcolumnDefs,
                columnSize="sizeToFit",
                defaultColDef=defaultColDef,
                dashGridOptions={"undoRedoCellEditing": True, 
                "cellSelection": "single",
                "rowSelection": "single"},
                csvExportParams={"fileName": "top02_arrest_rate.csv", "columnSeparator": ","},
                style = {'height': '800px', 'width': '100%', 'color': 'grey'}
                ),
            dbc.Button(
                'Download', id='submit-prop', n_clicks=0,
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
            ]
            ),
        dbc.Col(width=1),
        dbc.Col(
            [
            dbc.Col(
            [
            html.Br(),
            dag.AgGrid(
                id="datatable-main",
                rowData=load_bottom_data(),
                className="ag-theme-material",
                columnDefs=BOTTOMcolumnDefs,
                columnSize="sizeToFit",
                defaultColDef=defaultColDef,
                dashGridOptions={"undoRedoCellEditing": True,
                "cellSelection": "single",
                "rowSelection": "single"},
                csvExportParams={"fileName": "top02_arrest_rate.csv", "columnSeparator": ","},
                style = {'height': '800px', 'width': '100%', 'color': 'grey'}
                ),
            dbc.Button(
                'Download', id='submit-prop', n_clicks=0,
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
            ]
            )
            ])
                ]),
    html.Br(),
    dcc.Graph(id='graph-main1'),
    
]
)

# ---------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------

@app.callback(
    Output('datatable-main', 'exportDataAsCsv'),
    [Input('submit-prop', 'n_clicks')],
    prevent_initial_call=True,
    )
def update_prop_chart(n_clicks):
    if n_clicks:
        return True
    else:
        return False
