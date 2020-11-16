# -*- coding: utf-8 -*-
from igraph import Graph, EdgeSeq
from datetime import datetime, timedelta, date
import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import sys
from app import app

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#A5E1D2',
    'text': '#14555A',
    'dark-text': '#00343E',
    'light-background':  '#F2F2F5',
}

PAGE_SIZE = 5
df = pd.DataFrame({
    'VarselID': ['A270520200001', 'A120520200001', 'A010420200001', 'A280220190001'],
    'KundeID': ['01017988333', '01017988333', '0204797722', '0204797722'],
    'Kundenavn': ['Peder Ås', 'Peder Ås', 'Dagligvarer AS', 'Dagligvarer AS'],
    'Forretningsområde': ['PM', 'PM', 'BM', 'BM'],
    'Prioritering': ['B', 'C', 'A', 'A'],
    'Dato': ['27/05/20', '12/05/20', '01/04/20', '28/02/19'],
    'Regel': ['R01 - Unormal nedbetaling på lån', ' R04 - Avvik fra kundens oppgitte internasjonale transaksjonsmønster', 'R06 - Kontantinnskudd og transaksjoner til skatteparadis'
        , 'R18 - Avvik fra kundesegment'],
    'Varseltekst': ['Kunden har et lån på 2 700 000 NOK, hvor 40% av lånet ble nedbetalt i én transaksjon fra en tredjepart som ikke er disponent på lånet'
                    , 'Kunden har oppgitt en månedlig frekvens av 2 transaksjoner til utlandet med totalsum på 100 000 NOK. Kunden har den foregående måneden hatt 7 transaksjoner til utlandet for en samlet sum på 7 000 000 NOK'
                    , 'Kunden har den siste uken hatt 100 000 NOK i kontantinnskudd, og deretter sendt 110 000 NOK til skatteparadisen(e) Caymand Islands, Bermuda'
                    , 'Kunden i segmentet "Små og mellomstore daglivarebutikker" har følgende avvik fra sitt segment: manglende lønnsutbetalinger, få kredittere varekjøp, høyt volum av nettbankbetalinger'
                    ],
    'Status': ['Åpen', 'Under utredning', 'Lukket', 'Sendt Økokrim'],
})
df['Dato'] = pd.to_datetime(df['Dato'], dayfirst=True, format='%d/%m/%y')


def generate_store_map():
    df_world = pd.read_csv('assets/worldcities.csv')
    df_norway = df_world.loc[df_world['country'] == 'Norway']
    map_fig = px.scatter_mapbox(df_norway, lat="lat", lon="lng", hover_name="city", hover_data=["population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    map_fig.update_layout(mapbox_style="open-street-map")
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return map_fig

# If running in a single.page app use app.layout = html.Div()....., if running in multi-page app use layout = html.Div()
layout=html.Div([
    dbc.Container([
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Varseloversikt",
                    className="text-center text-dark",
                )
                #width={"size": 6, "offset": 3}
            ),  
        ),

        dbc.Row(dbc.Col(
            dbc.Form([
                dbc.Row([
                    dbc.Col(
                        dbc.FormGroup([
                            dbc.Label('Startdato', html_for='dateStart', style={'margin-right': '5px'}),
                            dcc.DatePickerSingle(
                                id='dateStart', 
                                min_date_allowed=date(2015, 1, 1), 
                                max_date_allowed=datetime.now().date(),
                                initial_visible_month=date(2020, 1, 1),
                                clearable=True
                            )],
                        row=False
                        ), 
                        width=3
                    ), 
                    dbc.Col(
                        dbc.FormGroup([
                            dbc.Label('Sluttdato:', html_for='dateEnd', style={'margin-right': '5px'}),
                            dcc.DatePickerSingle(
                                id='dateEnd', 
                                min_date_allowed=date(2015, 1, 1),
                                max_date_allowed=datetime.now().date(),
                                initial_visible_month=datetime.now().date(),
                                clearable=True,
                            )],
                            row=False
                        ), 
                        width=3
                    )
                ]), 
                dbc.Row([
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("KundeID", className="mr-2"),
                                dbc.Input(type="text", id='CustID-input', placeholder="Skriv inn KundeID"),
                            ],
                        ),
                    width=3,
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("Forretningsområde", className="mr-2"),
                                dbc.Input(type="text",  placeholder="Skriv inn forretningsområde", id='FO-input', className="mr-2"),
                            ],

                        ),
                    width=3
                    ),

                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("VarselID", className="mr-2"),
                                dbc.Input(type="text",  placeholder="Skriv inn varselID", id='varselID-input', className="mr-2"),
                            ],

                        ),
                    width=3
                    ),

                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("Varselstatus", className="mr-2"),
                                dcc.Dropdown(
                                    options=[
                                        {'label': 'Åpen', 'value': 'Åpen'},
                                        {'label': 'Under utredning', 'value': 'Under utredning'},
                                        {'label': 'Lukket', 'value': 'Lukket'},
                                        {'label': 'Sendt Økokrim', 'value': 'Sendt Økokrim'}
                                    ],
                                    #value=['MTL', 'NYC'],
                                    multi=True,
                                    id='status-input',
                                    clearable=True
                                ),
                            ],

                        ),
                    width=3
                    ), 
                ]),
            
            dbc.Button("Søk", color="primary", id="SearchButton")
            
            ],), 
            width={"size": 10, "offset": 1}
            ),
            style={'margin-top': '25px'}
        ),
        
                # Insert international transactions map and company structure
        dbc.Row([
            dbc.Col([html.H6(children='International transactions'), dcc.Graph(figure=generate_store_map())],
                     width=10),
            ],
            style={'background-color': '#d7dce0', 'margin-top': '25px'}
        ),
    ], fluid=True),
],
)


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port='8050')
