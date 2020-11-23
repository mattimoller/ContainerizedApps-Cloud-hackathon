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
from app import app
import random
import json
from dateutil.relativedelta import relativedelta
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#A5E1D2',
    'text': '#14555A',
    'dark-text': '#00343E',
    'light-background':  '#F2F2F5',
}

PAGE_SIZE = 5
fylker = ['Rogaland', 'Finnmark', 'Troms', 'Møre og Romsdal', 'Hordaland', 'Telemark', 'Vestfold', 'Østfold', 'Buskerud', 'Oslo', 'Akershus', 'Oppland', 'Hedmark', 'Nordland', 'Aust-Agder', 'Vest-Agder', 'Trøndelag', 'Sogn og Fjordane']
startdate = datetime(2017, 1, 1)
enddate = datetime(2020, 10, 1)
datelist = []
tempdate = startdate
while tempdate <= enddate:
    datelist.append(tempdate)
    tempdate += relativedelta(months=+1)

ansatte = np.ones((1, len(datelist)) )*750
randomAdd = np.random.randint(low=-5, high=10, size=(len(datelist) - 1), dtype='int')
for i in range(0, ansatte.size):
    ansatte[0, i] += np.sum(randomAdd[0:i+1])
ansatte = ansatte.flatten()
kvinneandel = np.random.randint(low=30, high=70, size=(len(datelist)), dtype='int')
oppsigelser = np.round(ansatte*random.randint(5, 15)/100, 0)
alder_avg = np.random.randint(low=38, high=59, size=(len(datelist)), dtype='int')
sykfra = np.random.randint(low=2, high=20, size=(len(datelist)), dtype='int')

df = pd.DataFrame({'Dato': datelist, 'Ansatte': ansatte, 'Kvinneadel': kvinneandel, 'Oppsigelser': oppsigelser, 'Alder_avg': alder_avg})

def create_employee_graph():
    fig = go.Figure(data=go.Scatter(x=df['Dato'], y=df['Ansatte']))
    fig.update_xaxes(title_text='Dato')
    fig.update_yaxes(title_text='Antall ansatte')
    return fig
layout=html.Div([
    dbc.Container([
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Distriktsdetaljer",
                    className="text-center text-dark",
                ),
                #width={"size": 6, "offset": 3}
                style={'margin-top': '25px'}
            ),  
        ),
        
                # Insert international transactions map and company structure
        dbc.Row([
            dbc.Col(
                dbc.FormGroup([
                    dbc.Label('Startdato', html_for='dateStart', style={'margin-right': '5px'}),
                    dcc.DatePickerSingle(
                        id='dateStart', 
                        min_date_allowed=date(2017, 1, 1), 
                        max_date_allowed=date(2020, 10, 1),
                        initial_visible_month=date(2017, 10, 1),
                        clearable=True
                    )],
                row=False
                ), 
            ), 
            dbc.Col(
                dbc.FormGroup([
                    dbc.Label('Sluttdato:', html_for='dateEnd', style={'margin-right': '5px'}),
                    dcc.DatePickerSingle(
                        id='dateEnd', 
                        min_date_allowed=date(2017, 1, 1),
                        max_date_allowed=datetime.now().date(),
                        initial_visible_month=datetime.now().date(),
                        clearable=True,
                    )],
                    row=False
                ), 
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Velg distrikt", html_for='county-input', style={'margin-right': '5px'}),
                        dcc.Dropdown(
                            options=[{'label': i, 'value': i} for i in fylker],
                            multi=False,
                            id='county-input',
                            clearable=True
                        ),
                    ],
                    row=False,
                ),
            ), 
        ], 
        form=True,
        style={'margin-top': '25px'},
        ),
                
                
        dbc.Row([
            dbc.Col(children=[
                html.H6(children='Antall ansatte over tid'),
                dcc.Graph(figure=create_employee_graph()),
            ],
            ),
        ],
        style={'margin-top': '25px'},
        className="text-center text-dark"),
    ], fluid=True),
],
)



if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port='8050')
