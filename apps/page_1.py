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
import random
import json
from urllib.request import urlopen
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#A5E1D2',
    'text': '#14555A',
    'dark-text': '#00343E',
    'light-background':  '#F2F2F5',
}

PAGE_SIZE = 5

df_world = pd.read_csv('assets/worldcities.csv')
df_norway = df_world.loc[df_world['country'] == 'Norway']
df_norway = df_norway.rename(columns={'population': 'Inbyggertall'})
df_norway['Antall ansatte'] = (df_norway['Inbyggertall']*0.001).astype(int)
df_norway['Sykefravær siste mnd (%)'] = np.random.randint(2, 20, size=(len(df_norway.index), 1))

fylker = ['Rogaland', 'Finnmark', 'Troms', 'Møre og Romsdal', 'Hordaland', 'Telemark', 'Vestfold', 'Østfold', 'Buskerud', 'Oslo', 'Akershus', 'Oppland', 'Hedmark', 'Nordland', 'Aust-Agder', 'Vest-Agder', 'Trøndelag', 'Sogn og Fjordane']
idList = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"]

sykfra = np.random.randint(
    low=2, high=20, size=(len(fylker)), dtype='int')
# all_trans = np.hstack((income, expenses * -1))
df_counties = pd.DataFrame(
    {'Fylke': fylker, 'Sykefravær': sykfra, 'id': idList})
with open('assets/gamle_fylker.json') as json_file:
    counties = json.load(json_file)

def generate_cities_map(df_norway):
    map_fig = px.scatter_mapbox(df_norway, lat="lat", lon="lng", hover_name="city", hover_data=["Antall ansatte", "Sykefravær siste mnd (%)"],
                        color_discrete_sequence=["#006458"], zoom=3, height=800, width=400)
    map_fig.update_layout(mapbox_style="open-street-map")
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return map_fig

def generate_counties_map(df_counties, geojson_file):
    fig = px.choropleth_mapbox(df_counties, geojson=geojson_file ,locations='id', color='Sykefravær',
                            color_continuous_scale="Viridis",
                            labels={'Fylke':'Fylke'},
                            mapbox_style='open-street-map',
                            center={"lat": 65.4305, "lon": 13.3951},
                            zoom=3,
                            height=600,
                            width=00,
                          )
    fig.update_geos(fitbounds="locations", visible=False, resolution=50, projection_type="conic equidistant")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(showlegend=False, marker_opacity=0.5)
    fig.update(layout_coloraxis_showscale=False)
    return fig

# If running in a single.page app use app.layout = html.Div()....., if running in multi-page app use layout = html.Div()
layout=html.Div([
    dbc.Container([
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Distriktsoversikt",
                    className="text-center text-dark",
                ),
                #width={"size": 6, "offset": 3}
                style={'margin-top': '25px'}
            ),  
        ),
        
                # Insert international transactions map and company structure
        dbc.Row([
            dbc.Col(dcc.Graph(figure=generate_counties_map(df_counties, counties)),width=4),
            dbc.Col([
                dbc.Row(
                    dbc.Col(
                            dbc.FormGroup(
                                [
                                    dbc.Label("Velg distrikt", className="mr-2"),
                                    dcc.Dropdown(
                                        options=[
                                            {'label': i, 'value': i} for i in df_norway.city
                                        ],
                                        multi=True,
                                        id='status-input',
                                        clearable=True
                                    ),
                                ],
                            ),
                        width=6
                    ), 
                ),
                dbc.Row(
                    dbc.Col(html.H2(
                        "Status: Sett inn butikk",
                        className="text-center text-dark",
                    ),),
                style={'margin-top': '25px'}
                ),
                dbc.Row([
                    dbc.Col(dcc.Markdown('''
                        Text placeholder 1

                    ''')),
                    dbc.Col(dcc.Markdown('''
                        Text placeholder 2

                    ''')),
                ],
                style={'margin-top': '25px'}
                ),

                dbc.Row([
                    dbc.Col(dcc.Markdown('''
                        Text placeholder 3

                    ''')),
                    dbc.Col(dcc.Markdown('''
                        Text placeholder 4

                    ''')),
                ],
                style={'margin-top': '25px'}
                ),
            ],
            width=8
            )
            ],
            style={'margin-top': '25px'}
        ),
    ], fluid=True),
],
)


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port='8050')
