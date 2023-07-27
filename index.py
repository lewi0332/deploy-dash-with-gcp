#!/usr/bin/env python3
"""
Main file to run the app. 

'python index.py' will run the app on your local machine.

Auther: Derrick Lewis
"""
import os
from dotenv import load_dotenv
from dash import  dcc, html
from dash.dependencies import Input, Output, State
import plotly.io as pio
import dash_bootstrap_components as dbc
from apps import page3
from plotly_theme_light import plotly_light
from main import server, app
from apps import home, page1, page2, page3

pio.templates["plotly_light"] = plotly_light
pio.templates.default = "plotly_light"
load_dotenv()


FOLDER = os.environ.get('FOLDER')

COMPANY_LOGO ="DELVE Logo Black.png"

# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
dropdown_disc = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem("Page3", href="/page1"),
        dbc.DropdownMenuItem("Page3", href="/page2"),
        dbc.DropdownMenuItem("Page2", href="/page3"),
        dbc.DropdownMenuItem("Individual Channel Behavior", href="/channel_behavior"),
        dbc.DropdownMenuItem("Optimization", href="/optimize"),
        dbc.DropdownMenuItem("Detailed Model Validation", href="/features_detail"),
    ],
    nav=True,
    in_navbar=True,
    label="Pages",
)

navbar = dbc.Navbar(
    dbc.Container([
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(src=app.get_asset_url(COMPANY_LOGO), height="50px"),
                         ),
                    dbc.Col(
                        dbc.NavbarBrand("Marketing Mix Model",
                            style={
                            # 'font-family': 'plain',
                            'color': 'grey',
                            'font-weight': 'light',
                            'font-size': '1.9rem',
                            'margin-top': '1rem',
                            'margin-left': '1rem'
                            }
                            )
                    )
                ],
                align="center",
                className="g-0"
            ),
            href="/home",
            style={'text-decoration':'none'}
            ),
        
        dbc.NavbarToggler(id="navbar-toggler2"),
        dbc.Collapse(
            dbc.Nav(
                # right align dropdown menu with ml-auto className
                [],
                className="ml-auto",
                navbar=True),
            id="navbar-collapse2",
            navbar=True,
        ),
        dbc.NavbarToggler(id="navbar-toggler3"),
        dbc.Collapse(
            dbc.Nav(
                # right align dropdown menu with ml-auto className
                [],
                className="ml-auto",
                navbar=True),
            id="navbar-collapse3",
            navbar=True,
        ),
        dbc.NavbarToggler(id="navbar-toggler4"),
        dbc.Collapse(
            dbc.Nav(
                # right align dropdown menu with ml-auto className
                [],
                className="ml-auto",
                navbar=True),
            id="navbar-collapse4",
            navbar=True,
        ),
        dbc.NavbarToggler(id="navbar-toggler5"),
        dbc.Collapse(
            dbc.Nav(
                # right align dropdown menu with ml-auto className
                [dropdown_disc],
                className="ml-auto",
                navbar=True),
            id="navbar-collapse5",
            navbar=True,
        ),
    ]),
    color="white",
    dark=False,
    className="mb-4",
)


def toggle_navbar_collapse(n, is_open):
    """Toggle navbar-collapse when clicking on navbar-toggler"""
    if n:
        return not is_open
    return is_open


for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    navbar,
    html.Div(id='page-content', style={
        'margin-right': '70px',
        'margin-left': '50px'
    }),
    html.Div(
        [
            dcc.Markdown(f"""
                        Model Updated on {FOLDER}
                        """,
                             style={
                                 'font-family': 'plain',
                                 'color': 'grey',
                                 'font-weight': 'light',
                                 'align': 'right'
                             }),
        ],
        id='footer', style={
        'margin-top': '250px',
        'margin-right': '70px',
        'margin-left': '50px',
        'float': 'right'
    })

] )


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    """
    This function is used to route the user to the correct page based on the url
    """
    print(pathname)
    if pathname == '/':
        return home.layout
    elif pathname == '/home':
        return home.layout
    elif pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    elif pathname == '/page3':
        return page3.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)