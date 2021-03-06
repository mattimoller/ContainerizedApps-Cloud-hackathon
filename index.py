import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
from app import app

from apps import page_1, page_2
# import all pages in the app


colors = {
    'background': '#A5E1D2',
    'text': '#14555A',
    'dark-text': '#00343E',
    'light-background':  '#F2F2F5',
}

PAGE_SIZE = 5

# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Distriktsoversikt", href="/page_1", style={'fontSize': 13}),
        dbc.DropdownMenuItem("Sykefravær oversikt", href="/page_2", style={'fontSize': 13}),
    ],
    nav = True,
    in_navbar = True,
    label = "Velg side",
    style={'fontSize': 13}
)
navbar = dbc.Navbar(
    dbc.Container([
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src="/assets/BearingPoint_201x_logo.svg.png", height="40px")),
                    dbc.Col(dbc.NavbarBrand("HR-Dashboard", className="ml-2", style={"textAlign": "center", 'fontSize': 25, 'color': '#002025'})),
                ],
                no_gutters=True,
                style={"textAlign": "center"}
            ),
            href="/page_1",
            style={"textAlign": "center", 'fontSize': 25}
        ),
        dbc.NavbarToggler(id="navbar-toggler2"),
        dbc.Collapse(
            dbc.Nav(
                # right align dropdown menu with ml-auto className
                [dropdown], className="ml-auto", navbar=True, style={'fontSize': 13}
            ),
            id="navbar-collapse2",
            navbar=True,
        ),
    ]),
    color="#989898",
    #dark=True,
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar


app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    navbar,
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page_1':
        return page_1.layout
    elif pathname == '/page_2':
        return page_2.layout
    else:
        return page_1.layout

if __name__ == '__main__':
    # For local hosting, use <app.run_server(debug=True)>
    # For AWS hosting use <app.run_server(host='0.0.0.0', port=8050, debug=True)>
    app.run_server(host='0.0.0.0', port=8050, debug=True)
    # app.run_server(debug=True)