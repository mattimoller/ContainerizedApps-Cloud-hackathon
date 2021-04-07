# -*- coding: utf-8 -*-
from datetime import datetime, date
import numpy as np
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
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
def create_general_df(fylker):
    df_world = pd.read_csv('assets/worldcities.csv')
    df_norway = df_world.loc[df_world['country'] == 'Norway']
    df_norway = df_norway.rename(columns={'population': 'Inbyggertall'})
    df_norway['Antall ansatte'] = (df_norway['Inbyggertall']*0.001).astype(int)
    df_norway['Sykefravær siste mnd (%)'] = np.random.randint(2, 20, size=(len(df_norway.index), 1))

    idList = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
    faste_ansatte = np.random.randint(low=500, high=2500, size=(len(fylker)), dtype='int')
    deltidsansatte = np.random.randint(low=20, high=100, size=(len(fylker)), dtype='int')
    ansatte = faste_ansatte + deltidsansatte
    kvinneandel = np.random.randint(low=30, high=70, size=(len(fylker)), dtype='int')
    oppsigelser = np.round(ansatte*random.randint(5, 15)/100, 0)
    nyansatte = np.round(ansatte*random.randint(5, 15)/100, 0)
    alder_avg = np.random.randint(low=38, high=59, size=(len(fylker)), dtype='int')
    sykfra = np.random.randint(low=2, high=20, size=(len(fylker)), dtype='int')
    antall_kurset = np.round(faste_ansatte*random.randint(30, 70)/100, 0)
    tilfredshet = np.random.randint(low=60, high=95, size=(len(fylker)), dtype='int')
    omdomme = np.random.randint(low=40, high=80, size=(len(fylker)), dtype='int')
    overtid = np.random.randint(low=5, high=20, size=(len(fylker)), dtype='int')

    return pd.DataFrame(
        {'Fylke': fylker, 'Sykefravær': sykfra, 'Faste_ansatte': faste_ansatte, 'Deltids_ansatte': deltidsansatte, 'Totalt_ansatte': ansatte, 'Kvinneandel': kvinneandel, 
        'Oppsigelser': oppsigelser, 'Nyansatte': nyansatte, 'Alder_avg': alder_avg, 'id': idList, 'Antall_kurset': antall_kurset, 'Ansattilfredshet': tilfredshet, 
        'Kundeomdømme': omdomme, 'Overtid': overtid})


df_counties = create_general_df(fylker)


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


def generate_county_timedata(counties):
    startdate = datetime(2017, 1, 1)
    enddate = datetime(2020, 10, 1)
    datelist = []
    tempdate = startdate
    while tempdate <= enddate:
        datelist.append(tempdate)
        tempdate += relativedelta(months=+1)
    c = 0
    df = pd.DataFrame(columns = ['Fylke', 'Dato', 'Sykefravær', 'Faste_ansatte', 'Deltids_ansatte', 'Totalt_ansatte', 'Kvinneandel', 'Oppsigelser', 'Nyansatte', 
        'Alder_avg', 'Antall_kurset', 'Ansattilfredshet', 'Kundeomdømme', 'Overtid']) 
    for fylke in counties:
        faste_ansatte = np.ones((len(datelist)))*750
        nye_ansatte = np.random.randint(low=0, high=15, size=len(datelist), dtype='int')
        oppsigelser = np.random.randint(low=0, high=10, size=len(datelist), dtype='int')
        for i in range(0, faste_ansatte.size):
            faste_ansatte[i] += np.sum(nye_ansatte[0:i])
            faste_ansatte[i] -= np.sum(oppsigelser[0:i])

        kvinneandel = np.random.randint(low=30, high=70, size=(len(datelist)), dtype='int')
        alder_avg = np.random.randint(low=38, high=59, size=(len(datelist)), dtype='int')
        sykefra = np.random.randint(low=2, high=20, size=(len(datelist)), dtype='int')
        antall_kurset = np.round(faste_ansatte*random.randint(30, 70)/100, 0)
        tilfredshet = np.random.randint(low=60, high=95, size=(len(datelist)), dtype='int')
        omdomme = np.random.randint(low=40, high=80, size=(len(datelist)), dtype='int')
        overtid = np.random.randint(low=5, high=20, size=(len(datelist)), dtype='int')
        fylkelist = [fylke] * len(datelist)
        df_temp = pd.DataFrame({'Fylke': fylkelist, 'Dato': datelist, 'Faste_ansatte': faste_ansatte, 'Kvinneadel': kvinneandel, 'Oppsigelser': oppsigelser, 'Alder_avg': alder_avg
                        , 'Ansattilfredshet': tilfredshet, 'Antall_kurset': antall_kurset, 'Sykefravær': sykefra, 'Kundeomdømme': omdomme, 'Overtid': overtid
                        , 'Nyansatte': nye_ansatte})
        df = df.append(df_temp)
    return df

df_counties_time = generate_county_timedata(fylker)
def create_employee_graph():
    fig = go.Figure()
    for fylke in fylker:
        df_temp = df_counties_time.loc[df_counties_time['Fylke'] == fylke]
        fig.add_trace(go.Scatter(x=df_temp['Dato'], y=df_temp['Faste_ansatte'], name=fylke))
    fig.update_xaxes(title_text='Dato')
    fig.update_yaxes(title_text='Antall faste ansatte')
    return fig

def create_ansatt_tilfredshet_graph():
    fig = go.Figure()
    for fylke in fylker:
        df_temp = df_counties_time.loc[df_counties_time['Fylke'] == fylke]
        fig.add_trace(go.Scatter(x=df_temp['Dato'], y=df_temp['Ansattilfredshet'], name=fylke))
    fig.update_xaxes(title_text='Dato')
    fig.update_yaxes(title_text='Ansatte som er fornøyd eller veldig fornøyd (%)')
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
                                        id='county-input1',
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
                    dbc.Col([dcc.Markdown('##### Antall ansatte: ' ), dcc.Markdown(children='', id='md-1-1'), dcc.Markdown(children='', id='md-1-2'), dcc.Markdown(children='', id='md-1-3')]),
                    dbc.Col([dcc.Markdown('##### Kvinneandel: ' ),dcc.Markdown(children='', id='md-2')]),

                ],
                style={'margin-top': '25px'}
                ),
                dbc.Row([
                    dbc.Col([dcc.Markdown('##### Sykefravær hittil i år: ' ),dcc.Markdown(children='', id='md-3')]),
                    dbc.Col([dcc.Markdown('##### Ansattes gjennomsnittsalder: ' ),dcc.Markdown(children='', id='md-6')]),

                ],
                style={'margin-top': '25px'}
                ),

              dbc.Row([
                    dbc.Col([dcc.Markdown('##### Nye ansatte hittil i år: ' ),dcc.Markdown(children='', id='md-4')]),
                    dbc.Col([dcc.Markdown('##### Oppsigelser hittil i år: ' ),dcc.Markdown(children='', id='md-5')]),

                ],
                style={'margin-top': '25px'}
                ),
                dbc.Row([
                    dbc.Col([dcc.Markdown('##### Ansattes tilfredshet: ' ),dcc.Markdown(children='', id='md-7')]),
                    dbc.Col([dcc.Markdown('##### Ansatte med kursing/utdanning: ' ),dcc.Markdown(children='', id='md-8')]),

                ],
                style={'margin-top': '25px'}
                ),

                dbc.Row([
                    dbc.Col([dcc.Markdown('##### Ansattes gjennomsnittlig overtidsjobbing: ' ),dcc.Markdown(children='', id='md-9')]),
                    dbc.Col([dcc.Markdown('##### Kundetilfredshet: ' ),dcc.Markdown(children='', id='md-10')]),

                ],
                style={'margin-top': '25px'}
                ),
            ],
            width=8
            )
            ],
            style={'margin-top': '25px'}
        ),
    
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Utvikling over tid",
                    className="text-center text-dark",
                ),
                #width={"size": 6, "offset": 3}
                style={'margin-top': '25px'}
            ),  
        ),
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
                width={'size': 3, 'offset': 1}
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
                width={'size': 3}
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Velg distrikt", style={'margin-right': '5px'}),
                        dcc.Dropdown(
                            options=[{'label': i, 'value': i} for i in fylker],
                            multi=True,
                            id='county-input2',
                            clearable=True
                        ),
                    ],
                    row=False,
                ),
                width={'size': 3}
            ), 
        ], 
        form=True,
        style={'margin-top': '50px'},
        ),

        dbc.Row([
            dbc.Col(children=[
                html.H6(children='Antall ansatte over tid'),
                dcc.Graph(figure=create_employee_graph()),
            ],
            ),
            dbc.Col(children=[
                html.H6(children='Ansattes tilfredshet'),
                dcc.Graph(figure=create_ansatt_tilfredshet_graph()),
            ],
            ),
        ],
        style={'margin-top': '25px'},
        className="text-center text-dark"), 
    ], fluid=True),
],
)

@app.callback(
    Output('fylke-header', "children"),
    Output('md-1-1', "children"),
    Output('md-1-2', "children"),
    Output('md-1-3', "children"),
    Output('md-2', "children"),
    Output('md-3', "children"),
    Output('md-4', "children"),
    Output('md-5', "children"),
    Output('md-6', "children"),
    Output('md-7', "children"),
    Output('md-8', "children"),
    Output('md-9', "children"),
    Output('md-10', "children"),
    Input("county-input1", "value"),
)
def update_county_markdown_info(search_value):
    df_filtered = df_counties
    if search_value != '' and search_value is not None:
        df_filtered = df_filtered.loc[df_filtered['Fylke'] == search_value]
        md1_1_var = int(df_filtered['Totalt_ansatte'])
        md1_2_var = int(df_filtered['Faste_ansatte'])
        md1_3_var = int(df_filtered['Deltids_ansatte'])
        md2_var = int(df_filtered['Kvinneandel'])
        md3_var = int(df_filtered['Sykefravær'])
        md4_var = int(df_filtered['Nyansatte'])
        md5_var = int(df_filtered['Oppsigelser'])
        md6_var = int(df_filtered['Alder_avg'])
        md7_var = int(df_filtered['Ansattilfredshet'])
        md8_var1 = int(df_filtered['Antall_kurset'])
        md8_var2 = int(100*df_filtered['Antall_kurset']/df_filtered['Faste_ansatte'])
        md9_var = int(df_filtered['Overtid'])
        md10_var = int(df_filtered['Kundeomdømme'])
        md1_1 = f'Totalt: {md1_1_var}'
        md1_2 = f'Faste ansatte: {md1_2_var}'
        md1_3 = f'Deltidsansatte: {md1_3_var}'
        md2 = f'{md2_var}%'
        md3 = f'{md3_var}%'
        md4 = f'{md4_var}'
        md5 = f'{md5_var}'
        md6 = f'{md6_var}'
        md7 = f'{md7_var}% av ansatte er "fornøyd" eller "veldig fornøyd"'
        md8 = f'{md8_var1} ({md8_var2}% av de faste ansatte)'
        md9 = f'{md9_var}% gjennomsnitt per ansatt'
        md10 = f'{md10_var}% av kundene er "fornøyd" eller "veldig fornøyd"'
        fylke_head = 'Distrikt: ' + str(search_value)
        return [fylke_head, md1_1, md1_2, md1_3, md2, md3, md4, md5, md6, md7, md8, md9, md10]
    else:
        return['Distrikt:', '', '', '', '', '', '', '', '', '', '', '', '']

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port='8050')
