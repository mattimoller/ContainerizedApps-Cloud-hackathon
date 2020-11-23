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
from urllib.request import urlopen
from textwrap import dedent, indent
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
ansatte = np.random.randint(low=500, high=2500, size=(len(fylker)), dtype='int')
kvinneandel = np.random.randint(low=30, high=70, size=(len(fylker)), dtype='int')
oppsigelser = np.round(ansatte*random.randint(5, 15)/100, 0)
nyansatte = np.round(ansatte*random.randint(5, 15)/100, 0)
alder_avg = np.random.randint(low=38, high=59, size=(len(fylker)), dtype='int')
sykfra = np.random.randint(low=2, high=20, size=(len(fylker)), dtype='int')

df_counties = pd.DataFrame(
    {'Fylke': fylker, 'Sykefravær': sykfra, 'Antall ansatte': ansatte, 'Kvinneandel': kvinneandel, 'Oppsigelser': oppsigelser, 
        'Nyansatte': nyansatte, 'Alder_avg': alder_avg, 'id': idList})
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
                                            {'label': i, 'value': i} for i in df_counties.Fylke
                                        ],
                                        multi=False,
                                        id='county-input',
                                        clearable=True
                                    ),
                                ],
                            ),
                        width=6
                    ), 
                ),
                dbc.Row(
                    dbc.Col(html.H2(
                        children='',
                        id = 'fylke-header',
                        className="text-center text-dark",
                    ),),
                style={'margin-top': '25px'}
                ),
                dbc.Row([
                    dbc.Col([dcc.Markdown('##### Antall ansatte: ' ), dcc.Markdown(children='', id='md-1')]),
                    dbc.Col([dcc.Markdown('##### Kvinneandel: ' ),dcc.Markdown(children='', id='md-2')]),

                ],
                style={'margin-top': '25px'}
                ),
                dbc.Row([
                    dbc.Col([dcc.Markdown('##### Sykefravær: ' ),dcc.Markdown(children='', id='md-3')]),
                    dbc.Col([dcc.Markdown('##### Ansattes gjennomsnittsalder: ' ),dcc.Markdown(children='', id='md-6')]),

                ],
                style={'margin-top': '25px'}
                ),

              dbc.Row([
                    dbc.Col([dcc.Markdown('##### Ansatte hittil i år: ' ),dcc.Markdown(children='', id='md-4')]),
                    dbc.Col([dcc.Markdown('##### oppsigelser hittil i år: ' ),dcc.Markdown(children='', id='md-5')]),

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

@app.callback(
    Output('fylke-header', "children"),
    Output('md-1', "children"),
    Output('md-2', "children"),
    Output('md-3', "children"),
    Output('md-4', "children"),
    Output('md-5', "children"),
    Output('md-6', "children"),
    Input("county-input", "value"),
)
def update_county_markdown_info(search_value):
    df_filtered = df_counties
    if search_value != '' and search_value is not None:
        df_filtered = df_filtered.loc[df_filtered['Fylke'] == search_value]
        md1_var = int(df_filtered['Antall ansatte'])
        md2_var = int(df_filtered['Kvinneandel'])
        md3_var = int(df_filtered['Sykefravær'])
        md4_var = int(df_filtered['Nyansatte'])
        md5_var = int(df_filtered['Oppsigelser'])
        md6_var = int(df_filtered['Alder_avg'])
        md1 = f'{md1_var}'
        md2 = f'{md2_var}%'
        md3 = f'{md3_var}%'
        md4 = f'{md4_var}'
        md5 = f'{md5_var}'
        md6 = f'{md6_var}'
        fylke_head = 'Distrikt: ' + str(search_value)
        return [fylke_head, md1, md2, md3, md4, md5, md6]
    else:
        return['Distrikt:', '', '', '', '', '', '']

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port='8050')
