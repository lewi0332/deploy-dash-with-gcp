"""

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
from apps.tables import defaultColDef, top_streets_columnDefs

from plotly_theme_light import plotly_light

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
def load_top_streets():
    query = """
    SELECT
        ward,
        street,
        domestic_crimes
    FROM
        `dashapp-375513.Q3_domestic_crimes_by_strt_by_ward.top_streets_by_ward`
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
                # Top Streets for Domestic Crimes by Ward
                ---
                
                What street in each ward had the most domestic crimes in 2020?What street in each ward had the most domestic crimes in 2020?

                ---

                ### Query to Build this Dataset
                """,
                className='md')
            ])
    ]),
    dbc.Row(
        dbc.Col(
                dcc.Markdown(id='codeblock',
                children = """
                ```sql
                CREATE SCHEMA `dashapp-375513.Q3_domestic_crimes_by_strt_by_ward`
                OPTIONS (
                    description = "What street in each ward had the most domestic crimes in 2020?",
                    location = 'us');

                CREATE OR REPLACE TABLE `dashapp-375513.Q3_domestic_crimes_by_strt_by_ward.top_streets_by_ward` AS (
                WITH
                    RAW AS (
                        SELECT
                            unique_key,
                            TRIM(SUBSTR(block, 7)) as street,
                            ward,
                            ROW_NUMBER () OVER (PARTITION By case_number ORDER BY updated_on DESC) RN
                        FROM 
                            `bigquery-public-data.chicago_crime.crime`
                        WHERE
                            domestic=true
                            AND year = 2020
                            AND ward IS NOT NULL
                    ),
                    STREETS AS (
                        SELECT
                        ward,
                        street,
                        count(unique_key) as domestic_crimes,
                        FROM RAW
                        WHERE RN = 1
                        GROUP BY 1, 2
                    ),
                    STREET_row AS (
                        SELECT
                            ward,
                            street,
                            domestic_crimes,
                            RANK() OVER (PARTITION BY ward ORDER BY domestic_crimes DESC) as street_rank
                        FROM STREETS
                        ORDER BY 1
                    )
                    SELECT
                        STREET_row.ward,
                        STREET_row.street,
                        STREET_row.domestic_crimes
                    FROM STREET_row
                    WHERE street_rank = 1
                    ORDER BY 1, 2
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
                ### Top Streets for Domestic Crimes by Ward
                """,
                className='md'),
        width=5),
        dbc.Col(width=1),
        dbc.Col(),
    ]),
    dbc.Row([
        dbc.Col(
            [
            html.Br(),
            dag.AgGrid(
                id="datatable-streets",
                rowData=load_top_streets(),
                className="ag-theme-material",
                columnDefs=top_streets_columnDefs,
                columnSize="sizeToFit",
                defaultColDef=defaultColDef,
                dashGridOptions={"undoRedoCellEditing": True, 
                "cellSelection": "single",
                "rowSelection": "single"},
                csvExportParams={"fileName": "top02_arrest_rate.csv", "columnSeparator": ","},
                style = {'height': '800px', 'width': '100%', 'color': 'grey'}
                ),
            dbc.Button(
                'Download', id='topStreets', n_clicks=0,
                style={
                           'background-color': 'rgba(0, 203, 166, 0.7)',
                           'border': 'none',
                           'color': 'white',
                           'padding': '8px',
                           'margin-top': '10px',
                           'margin-bottom': '10px',
                           'text-align': 'center',
                           'text-decoration': 'none',
                           'font-size': '16px',
                           'border-radius': '26px'
                       }
            )
            ]
        )
    ]),
    html.Br(),
    dcc.Graph(id='graph-main1')
])

# ---------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------

@app.callback(
    Output('datatable-streets', 'exportDataAsCsv'),
    [Input('topStreets', 'n_clicks')],
    prevent_initial_call=True,
    )
def topStreets(n_clicks):
    if n_clicks:
        return True
    else:
        return False
