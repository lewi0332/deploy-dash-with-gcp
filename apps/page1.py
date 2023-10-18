"""


Author: Derrick Lewis
"""
import json
import pandas as pd
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
from main import app

pio.templates["plotly_light"] = plotly_light
pio.templates.default = "plotly_light"
load_dotenv()

client = bigquery.Client(project='dashapp-375513')

# Load custom GeoJSON file
with open('police_beats.geojson', mode='r', encoding='utf-8') as f:
    geojson_data = json.load(f)

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
                # Arrest Rates for Residence Crime
                ---
                
                Which beats are in the top and bottom 2% for arrest rate for residence crime in each district in 2020?
    
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
        width=5)
    ]),
    dbc.Row([
        dbc.Col(
            [
            html.Br(),
            dag.AgGrid(
                id="datatable-top",
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
                'Download', id='downloadTop', n_clicks=0,
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
        ),
        dbc.Col(width=1),
        dbc.Col(dcc.Graph(id='graph-main1'), width=6)
    ]),
    html.Br(),
    dbc.Row([
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
                id="datatable-bottom",
                rowData=load_bottom_data(),
                className="ag-theme-material",
                columnDefs=BOTTOMcolumnDefs,
                columnSize="sizeToFit",
                defaultColDef=defaultColDef,
                dashGridOptions={"undoRedoCellEditing": True,
                "cellSelection": "single",
                "rowSelection": "single"},
                csvExportParams={"fileName": "bottom02_arrest_rate.csv", "columnSeparator": ","},
                style = {'height': '800px', 'width': '100%', 'color': 'grey'}
                ),
            dbc.Button(
                'Download', id='downloadBottom', n_clicks=0,
                style={

                           'background-color': 'rgba(0, 203, 166, 0.7)',
                           'border': 'none',
                           'color': 'white',
                           'padding': '8px',
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
        dbc.Col(dcc.Graph(id='graph-main2'),
                width=6)
        ]),
    
]
)

# ---------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------

@app.callback(
    Output('datatable-top', 'exportDataAsCsv'),
    [Input('downloadTop', 'n_clicks')],
    prevent_initial_call=True,
    )
def downloadTop(n_clicks):
    if n_clicks:
        return True
    else:
        return False
    
@app.callback(
    Output('datatable-bottom', 'exportDataAsCsv'),
    [Input('downloadBottom', 'n_clicks')],
    prevent_initial_call=True,
    )
def downloadBottom(n_clicks):
    if n_clicks:
        return True
    else:
        return False
    
@app.callback(
    Output('graph-main1', 'figure'),
    [Input('datatable-top', 'rowData'),
    Input('datatable-top', 'cellClicked')],
    # prevent_initial_call=True,
    )
def update_figure(rowData, selectedRows):
    if selectedRows is None:
        markerlist = [.5] * len(rowData)
    else:
        markerlist = [.1] * len(rowData)
        markerlist[selectedRows['rowIndex']] = .5
    dff = pd.DataFrame(rowData)
    # Create choropleth map
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson_data,
            featureidkey='properties.beat_num',
            locations=dff['TOP_02_beat'].astype(str).str.zfill(4),
            z=dff['TOP_02_arrest_rate'],
            colorscale='Viridis',
            zmin=0,
            zmax=.4,
            marker_opacity=markerlist,
            marker_line_width=.1,
            text=dff['district'].astype(str),
            hovertemplate =
                "District: <b>%{text} </b><br>" +
                "Beat: <b>%{location} </b><br>" +
                "Arrest Rate: <b>%{z:.2%} </b><br><extra></extra>" 
        )
    )

    # Set map layout
    fig.update_layout(
        mapbox_style='carto-positron',
        mapbox_zoom=9.7,
        mapbox_center={'lat': 41.86, 'lon': -87.69
    },
    height=900,
    width=800
    )
    return fig

@app.callback(
    Output('graph-main2', 'figure'),
    [Input('datatable-bottom', 'rowData'),
    Input('datatable-bottom', 'cellClicked')],
    # prevent_initial_call=True,
    )
def update_figure(rowData, selectedRows):
    print(selectedRows)
    if selectedRows is None:
        markerlist = [.5] * len(rowData)
    else:
        markerlist = [.1] * len(rowData)
        markerlist[selectedRows['rowIndex']] = .5
    dff = pd.DataFrame(rowData)
    # Create choropleth map
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson_data,
            featureidkey='properties.beat_num',
            locations=dff['BOTTOM_02_beat'].astype(str).str.zfill(4),
            z=dff['BOTTOM_02_arrest_rate'],
            colorscale='Viridis',
            zmin=0,
            zmax=.4,
            marker_opacity=markerlist,
            marker_line_width=markerlist,
            text=dff['district'].astype(str),
            hovertemplate =
                "District: <b>%{text} </b><br>" +
                "Beat: <b>%{location} </b><br>" +
                "Arrest Rate: <b>%{z:.2%} </b><br><extra></extra>" 
        )
    )

    # Set map layout
    fig.update_layout(
        mapbox_style='carto-positron',
        mapbox_zoom=9.7,
        mapbox_center={'lat': 41.86, 'lon': -87.69
    },
    height=900,
    width=800
    )
    return fig