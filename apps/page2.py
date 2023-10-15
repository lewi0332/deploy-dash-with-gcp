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
from apps.tables import crime_type_columnDefs, defaultColDef, crime_type_by_community_columnDefs

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

def load_primary_data()->dict:
    query = """
    SELECT
      rank_of_crime_type,
      primary_type,
      cnt_of_primary_typ_2020
    FROM
        `dashapp-375513.Q2_primary_crime_types.top_5_crime_types_2020`
    """
    dff = client.query(query).to_dataframe()
    return dff.to_dict('records')

def load_community_data(rank: int)->dict:
    query = """
    SELECT
        primary_type,
        com.value AS community_area,
        com.count AS cnt_of_primary_typ_2020,
        com.cnt_jan_2021 AS cnt_jan_2021,
    FROM
        `dashapp-375513.Q2_primary_crime_types.top_5_crime_types_2020`,
        UNNEST(communities) AS com
    WHERE rank_of_crime_type = {crime_rank}
    """
    dff = client.query(query.format(crime_rank=rank)).to_dataframe()
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
                # Primary Types of Crime
                ---
                
                What are the top 5 primary crime types in 2020?

                Provide the top 3 community areas for each type by occurrence in 2020?
                
                Finally, how many of those types of crime did the each of those community 
                areas have in January 2021?
    
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
                CREATE SCHEMA `dashapp-375513.Q2_primary_crime_types`
                OPTIONS (
                    description = "What are the top 5 primary crime types in 2020 also provide the top 3 community areas for each type by occurrence in 2020 and how many of those types of crime did the each of those community areas have in January 2021?",
                    location = 'us');

                CREATE OR REPLACE TABLE `dashapp-375513.Q2_primary_crime_types.top_5_crime_types_2020` AS (
                    WITH
                    RAW AS (
                        -- Duplicate Case numbers? I made some assumptions to de-dupe. I would verify in the real world.
                        SELECT
                            unique_key,
                            primary_type,
                            community_area,
                            ROW_NUMBER () OVER (PARTITION By case_number ORDER BY updated_on DESC) RN
                        FROM 
                            `bigquery-public-data.chicago_crime.crime`
                        WHERE
                            year = 2020
                    ),

                    TOPS AS (
                        SELECT
                            APPROX_TOP_COUNT(primary_type, 5) as primary_type
                        FROM RAW
                        WHERE RAW.RN = 1
                    ), 
                    TOP5 AS (
                        SELECT
                        RANK() OVER( ORDER BY pt.count DESC) AS rank_of_crime_type,
                        pt.value as primary_type,
                        pt.count as cnt_of_primary_typ_2020
                        FROM TOPS,
                        UNNEST(primary_type) as pt
                        ORDER by 3 DESC
                    ),
                    COMMUNITIES AS (
                        SELECT
                        TOP5.primary_type,
                        APPROX_TOP_COUNT(RAW.community_area, 3) AS top_community_area
                        FROM TOP5
                        LEFT JOIN RAW
                        ON TOP5.primary_type = RAW.primary_type
                        WHERE RAW.RN = 1
                        GROUP BY 1
                    ),
                    RAW_JAN AS (
                        SELECT
                            date,
                            unique_key,
                            primary_type,
                            community_area,
                            ROW_NUMBER () OVER (PARTITION By case_number ORDER BY updated_on DESC) RN
                        FROM 
                            `bigquery-public-data.chicago_crime.crime`
                        WHERE
                            date BETWEEN '2021-01-01' AND  '2021-01-31'
                    ),
                    JAN AS (
                        SELECT
                            RAW_JAN.primary_type,
                            tc.value community_area,
                            count(RAW_JAN.unique_key) cnt_jan_2021
                        FROM COMMUNITIES,
                            UNNEST(top_community_area) as tc
                        LEFT JOIN RAW_JAN
                            ON RAW_JAN.primary_type = COMMUNITIES.primary_type AND RAW_JAN.community_area = tc.value
                        WHERE RAW_JAN.RN = 1
                        GROUP BY 1, 2
                        ORDER BY 1, 2, 3
                    )
                    SELECT
                        rank_of_crime_type,
                        TOP5.primary_type,
                        cnt_of_primary_typ_2020,
                        ARRAY_AGG(STRUCT(tc.value, tc.count , JAN.cnt_jan_2021)) AS communities,
                    FROM TOP5
                    LEFT JOIN COMMUNITIES
                        ON COMMUNITIES.primary_type = TOP5.primary_type,
                        UNNEST(COMMUNITIES.top_community_area) as tc
                    LEFT JOIN JAN 
                        ON TOP5.primary_type = JAN.primary_type AND tc.value = JAN.community_area
                    GROUP BY 1,2,3
                    ORDER BY 1
                );
                ```
                """,
                
                className='md')
            ),
        style={"maxHeight": "400px", "overflow": "scroll"}
    ),
    html.Br(),
    dbc.Row(
        dbc.Col(
            dcc.Markdown(
                children = """
                ---
                ### Top 5 Primary Crime Types in 2020
                """,
                className='md'))
        ),
    dbc.Row([
        dbc.Col(
            [
            html.Br(),
            dag.AgGrid(
                id="datatable-community",
                rowData=load_primary_data(),
                className="ag-theme-material",
                columnDefs=crime_type_columnDefs,
                columnSize="sizeToFit",
                defaultColDef=defaultColDef,
                dashGridOptions={"undoRedoCellEditing": True, 
                "cellSelection": "single",
                "rowSelection": "single"},
                csvExportParams={"fileName": "top_primary_crime_type.csv", "columnSeparator": ","},
                style = {'width': '100%', 'color': 'grey'}
                ),
            dbc.Button(
                'Download', id='downloadCrimeType', n_clicks=0,
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
    dbc.Row([
        dbc.Col(
            dcc.Markdown(
                children = """
                ---
                ### Number 1 Crime type by Community Area
                """,
                className='md'),
        width=5),
        dbc.Col(width=1),
        dbc.Col(
            dcc.Markdown(id='intro',
                children = """
                ---
                ### Number 2 Crime type by Community Area
                """,
                className='md')
        ),
    ]),
    dbc.Row([
        dbc.Col(
            [
            html.Br(),
            dag.AgGrid(
                rowData=load_community_data(1),
                className="ag-theme-material",
                columnDefs=crime_type_by_community_columnDefs,
                columnSize="sizeToFit",
                defaultColDef=defaultColDef,
                dashGridOptions={"undoRedoCellEditing": True,
                "cellSelection": "single",
                "rowSelection": "single"},
                style = {'width': '100%', 'color': 'grey'}
                )
            ]
        ),
        dbc.Col(width=1),
        dbc.Col(
            [
            html.Br(),
            dag.AgGrid(
                rowData=load_community_data(2),
                className="ag-theme-material",
                columnDefs=crime_type_by_community_columnDefs,
                columnSize="sizeToFit",
                defaultColDef=defaultColDef,
                dashGridOptions={"undoRedoCellEditing": True,
                "cellSelection": "single",
                "rowSelection": "single"},
                style = {'width': '100%', 'color': 'grey'}
                )
            ]
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Markdown(
                children = """
                ---
                ### Number 3 Crime type by Community Area
                """,
                className='md'),
        width=5),
        dbc.Col(width=1),
        dbc.Col(
            dcc.Markdown(id='intro',
                children = """
                ---
                ### Number 4 Crime type by Community Area
                """,
                className='md')
        ),
    ]),
    dbc.Row([
        dbc.Col(
            [
            html.Br(),
            dag.AgGrid(
                rowData=load_community_data(3),
                className="ag-theme-material",
                columnDefs=crime_type_by_community_columnDefs,
                columnSize="sizeToFit",
                defaultColDef=defaultColDef,
                dashGridOptions={"undoRedoCellEditing": True,
                "cellSelection": "single",
                "rowSelection": "single"},
                style = {'width': '100%', 'color': 'grey'}
                )
            ]
        ),
        dbc.Col(width=1),
        dbc.Col(
            [
            html.Br(),
            dag.AgGrid(
                rowData=load_community_data(4),
                className="ag-theme-material",
                columnDefs=crime_type_by_community_columnDefs,
                columnSize="sizeToFit",
                defaultColDef=defaultColDef,
                dashGridOptions={"undoRedoCellEditing": True,
                "cellSelection": "single",
                "rowSelection": "single"},
                style = {'width': '100%', 'color': 'grey'}
                )
            ]
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Markdown(
                children = """
                ---
                ### Number 5 Crime type by Community Area
                """,
                className='md'),
        width=5),
        dbc.Col(width=1),
        dbc.Col(
        ),
    ]),
    dbc.Row([
        dbc.Col(
            [
            html.Br(),
            dag.AgGrid(
                rowData=load_community_data(5),
                className="ag-theme-material",
                columnDefs=crime_type_by_community_columnDefs,
                columnSize="sizeToFit",
                defaultColDef=defaultColDef,
                dashGridOptions={"undoRedoCellEditing": True,
                "cellSelection": "single",
                "rowSelection": "single"},
                style = {'width': '100%', 'color': 'grey'}
                )
            ]
        ),
        dbc.Col(width=1),
        dbc.Col(
        
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
    Output('datatable-community', 'exportDataAsCsv'),
    [Input('downloadCrimeType', 'n_clicks')],
    prevent_initial_call=True,
    )
def downloadCrimeType(n_clicks):
    if n_clicks:
        return True
    else:
        return False
