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
from apps.tables import time_columnDefs, defaultColDef

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
def load_time_data()->dict:
    query = """
    SELECT
        time_period,
        most_common_crime_type,
        overall_arrest_rate,
    FROM
        `dashapp-375513.Q4_crimes_by_time_period.crime_by_time_period`
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
                # Common Crimes by Time Period
                ---
                
                Which crime is the most common between?
                - 12am-6am cst
                - 6am-12pm cst
                - 12pm-6pm cst
                - 6pm-12pm cst
                
                What is the arrest rate for each period?

                ---

                ### Query to build this Dataset
                """,
                className='md')
            ])
    ]),
    dbc.Row(
        dbc.Col(
                dcc.Markdown(id='codeblock',
                children = """
                ```sql
                CREATE SCHEMA `dashapp-375513.Q4_crimes_by_time_period`
                OPTIONS (
                    description = "Which crime is the most common between 12am-6am cst 6am-12pm cst, 12pm-6pm cst and 6pm-12pm cst and what is the arrest rate for each period?",
                    location = 'us');
                CREATE OR REPLACE TABLE `dashapp-375513.Q4_crimes_by_time_period.crime_by_time_period` AS (
                WITH
                CTE AS (
                    WITH RAW AS (
                        SELECT
                            unique_key,
                            DATETIME(date, "America/Chicago") datetime_cst,
                            extract(hour from DATETIME(date, "America/Chicago")) as hour,
                            CASE 
                            WHEN extract(hour from DATETIME(date, "America/Chicago")) >= 18 THEN '6pm-12pm'
                            WHEN extract(hour from DATETIME(date, "America/Chicago")) >= 12 THEN '12pm-6pm'
                            WHEN extract(hour from DATETIME(date, "America/Chicago")) >= 6 THEN '6am-12pm'
                            WHEN extract(hour from DATETIME(date, "America/Chicago")) >= 0 THEN '12am-6am'
                            END AS time_period,
                            primary_type,
                            arrest,
                            ROW_NUMBER () OVER (PARTITION By case_number ORDER BY updated_on DESC) RN
                        FROM 
                            `bigquery-public-data.chicago_crime.crime`
                    )
                    SELECT
                        unique_key,
                        datetime_cst,
                        hour,
                        time_period,
                        primary_type,
                        arrest
                    FROM RAW
                    WHERE RN=1
                ),
                COUNT_CRIMES AS (
                    SELECT
                        primary_type,
                        time_period,
                        count(unique_key) as cnt_of_crimes
                    FROM CTE
                    GROUP BY 1, 2
                ),
                RANKED_CRIMES AS (
                    SELECT
                        primary_type,
                        time_period,
                        cnt_of_crimes,
                        RANK() OVER(PARTITION BY time_period ORDER BY cnt_of_crimes DESC) AS RC
                    FROM COUNT_CRIMES
                ),
                CRIMES AS (
                    SELECT 
                        time_period,
                        primary_type AS most_common_crime_type
                    FROM RANKED_CRIMES
                    WHERE RC = 1
                    ORDER BY 1
                ),
                ARREST_RATE AS (
                    SELECT
                        time_period,
                        CASE 
                        WHEN SUM(CAST(arrest AS INT)) = 0 THEN 0 
                        ELSE SAFE_DIVIDE(SUM(CAST(arrest AS INT)), COUNT(CAST(arrest AS INT)))
                        END AS overall_arrest_rate
                    FROM 
                        CTE
                    GROUP BY 1
                    )

                SELECT
                    c.time_period,
                    c.most_common_crime_type,
                    ar.overall_arrest_rate
                FROM CRIMES as c
                LEFT JOIN ARREST_RATE ar
                    ON c.time_period = ar.time_period
                ORDER BY 1
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
                ### Top Crimes by Time Period
                """,
                className='md'),
        width=5),
        dbc.Col(width=1)
    ]),
    dbc.Row([
        dbc.Col(
            [
            html.Br(),
            dag.AgGrid(
                id="datatable-time",
                rowData=load_time_data(),
                className="ag-theme-material",
                columnDefs=time_columnDefs,
                columnSize="sizeToFit",
                defaultColDef=defaultColDef,
                dashGridOptions={"undoRedoCellEditing": True, 
                "cellSelection": "single",
                "rowSelection": "single"},
                csvExportParams={"fileName": "top02_arrest_rate.csv", "columnSeparator": ","},
                style = {'width': '100%', 'color': 'grey'}
                ),
            dbc.Button(
                'Download', id='downloadTime', n_clicks=0,
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
                    ),
            ]
            )
    ]),
    html.Br(),
    dcc.Graph(id='graph-main1'),
    
]
)

# ---------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------

@app.callback(
    Output('datatable-time', 'exportDataAsCsv'),
    [Input('downloadTime', 'n_clicks')],
    prevent_initial_call=True,
    )
def update_prop_chart(n_clicks):
    if n_clicks:
        return True
    else:
        return False
