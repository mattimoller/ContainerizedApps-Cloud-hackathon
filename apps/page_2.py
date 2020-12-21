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
import random
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
idList = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
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
df['Dato'] = pd.to_datetime(df['Dato'], dayfirst=True, format='%d/%m/%y')

def create_employee_graph():
    fig = go.Figure(data=go.Scatter(x=df['Dato'], y=df['Ansatte']))
    fig.update_xaxes(title_text='Dato')
    fig.update_yaxes(title_text='Antall ansatte')
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
    df['Dato'] = pd.to_datetime(df['Dato'], dayfirst=True, format='%d/%m/%y')
    return df

df_counties_time = generate_county_timedata(fylker)

def generate_ansatte_df(counties, counties_IDlist):
    antall_ansatte = 1000
    Ansatt_ID = list(np.arange(1, antall_ansatte + 1, 1))
    Ansatt_ID = [str(ansatt) for ansatt in Ansatt_ID]
    df_ansatte = pd.DataFrame(columns = ['Fylke', 'Ansatt_ID', 'Alder', 'Kjoenn']) 
    for count, fylke in enumerate(counties):
        Ansatt_ID_fylke = [counties_IDlist[count] + '_'  + ansatt for ansatt in Ansatt_ID]
        Ansatt_alder = np.random.randint(low=25, high=72, size=(len(Ansatt_ID)), dtype='int')
        df_temp = pd.DataFrame({'Fylke': [fylke] * len(Ansatt_ID), 'Ansatt_ID': Ansatt_ID_fylke, 'Alder': Ansatt_alder, 'Kjoenn': random.choices(['Mann', 'Kvinne'], k=len(Ansatt_ID))})
        df_ansatte = df_ansatte.append(df_temp)

    return df_ansatte
df_ansatte = generate_ansatte_df(fylker, idList)

def generate_county_sykedata(Ansatt_IDList, num_entries=10000):
    startdate = datetime(2019, 1, 1)
    enddate = datetime(2020, 10, 1)
    datelist = []
    tempdate = startdate
    while tempdate <= enddate:
        datelist.append(tempdate)
        tempdate += relativedelta(months=+1)

    df_sykedata = pd.DataFrame({'Ansatt_ID': random.choices(Ansatt_IDList, k=num_entries), 'Lengde_fravaer': np.random.randint(low=1, high=25, size=num_entries, dtype='int'), 
                        'Dato': random.choices(datelist, k=num_entries)})
    df_sykedata['Dato'] = pd.to_datetime(df_sykedata['Dato'], dayfirst=True, format='%d/%m/%y')
    return df_sykedata

sykedata_df = generate_county_sykedata(list(df_ansatte['Ansatt_ID']))

sykedata_df = pd.merge(sykedata_df, df_ansatte, on='Ansatt_ID')
sykedata_df['Dato'] = pd.to_datetime(sykedata_df['Dato'], dayfirst=True, format='%d/%m/%y')
sykedata_monthly_df = sykedata_df.groupby(['Fylke', 'Dato'])['Lengde_fravaer'].sum().reset_index()
sykedata_monthly_df['Fravaer_prosent'] = 100*sykedata_monthly_df['Lengde_fravaer']/(1000*23)
sykedata_monthly_df['Month'] = [myDate.month for myDate in sykedata_monthly_df['Dato']]
sykedata_monthly_df['Year'] = [myDate.year for myDate in sykedata_monthly_df['Dato']]
sykedata_monthly_df['Month'] = sykedata_monthly_df['Month'].astype(str)
sykedata_monthly_df['Year'] = sykedata_monthly_df['Year'].astype(str)


def generate_syketimer_chart(sykedata_monthly_df):    
    fig = go.Figure()
    for fylke in fylker:
        df_temp = sykedata_monthly_df.loc[sykedata_monthly_df['Fylke'] == fylke]
        fig.add_trace(go.Scatter(x=df_temp['Dato'], y=df_temp['Lengde_fravaer'], name=fylke))
    fig.update_xaxes(title_text='Dato')
    fig.update_yaxes(title_text='Gjennomsnittlig fraværslengde')
    return fig

def generate_onecounty_sykebarchart(sykedata_monthly_df, county='Oslo', year='2020'):
    sykedata_monthly_df = sykedata_monthly_df.loc[sykedata_monthly_df['Year'] == year]
    sykedata_monthly_df_onecounty = sykedata_monthly_df.loc[sykedata_monthly_df['Fylke'] == county]
    sykedata_monthly_otherCounties = sykedata_monthly_df.loc[sykedata_monthly_df['Fylke'] != county]
    sykedata_monthly_otherCounties = sykedata_monthly_otherCounties.groupby(['Year', 'Month'])['Fravaer_prosent'].mean().reset_index()


    trace1  = go.Scatter(
        mode='lines+markers',
        x = sykedata_monthly_otherCounties['Month'],
        y = sykedata_monthly_otherCounties['Fravaer_prosent'],
        name="Other counties average",
        marker_color='crimson'
    )

    trace2 = go.Bar(
        x = sykedata_monthly_df_onecounty['Month'],
        y = sykedata_monthly_df_onecounty['Fravaer_prosent'],
        name = county,
        yaxis='y2'
    )
    data = [trace1, trace2]

    layout = go.Layout(
        title_text='States_Name',
        yaxis=dict(
            range = [0, 10],
            side = 'right'
        ),
        yaxis2=dict(
            overlaying='y',
            anchor='y3',
        )
    )
    fig = go.Figure(data=data, layout=layout)
    return fig

def generate_sickleave_chart_allcounties(sykedata_monthly_df, year='2020'):
    sykedata_monthly_df = sykedata_monthly_df.loc[sykedata_monthly_df['Year'] >= str(int(year) - 1)]
    sykedata_yearly_df = sykedata_monthly_df.groupby(['Fylke', 'Year'])['Fravaer_prosent'].mean().reset_index()
    fig = px.bar(sykedata_yearly_df, x='Fylke', y='Fravaer_prosent', color='Year', barmode='group')
    return fig

def generate_county_sickleave_comparison(sykedata_monthly_df, county='Oslo'):
    sykedata_monthly_df = sykedata_monthly_df.loc[sykedata_monthly_df['Fylke'] == county]
    fig = px.bar(sykedata_monthly_df, x='Month', y='Fravaer_prosent', color='Year', barmode='group')
    return fig


layout=html.Div([
    dbc.Container([
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Sykefravær",
                    className="text-center text-dark",
                ),
                #width={"size": 6, "offset": 3}
                style={'margin-top': '25px'}
            ),  
        ),
        
        dbc.Row([
            dbc.Col(children=[
                html.H4(children='Sykefravær i alle distrkit så så langt i år'),
                dcc.Graph(figure=generate_sickleave_chart_allcounties(sykedata_monthly_df)),
            ],
            ),
            ],
            style={'margin-top': '25px'},
            className="text-center text-dark"
        ),

        dbc.Row(dbc.Col(
            dbc.Form([
                dbc.Row([
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("Velg år", className="mr-2"),
                                dcc.Dropdown(
                                    options=[
                                        {'label': '2020', 'value': '2020'},
                                        {'label': '2019', 'value': '2019'},
                                        {'label': '2018', 'value': '2018'},
                                        {'label': '2017', 'value': '2017'}
                                    ],
                                    #value=['MTL', 'NYC'],
                                    multi=False,
                                    id='year-input',
                                    clearable=True
                                ),
                            ],

                        ),
                        width={'size': 3}
                    ), 
                
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label("Velg distrikt", style={'margin-right': '5px'}),
                                dcc.Dropdown(
                                    options=[{'label': i, 'value': i} for i in fylker],
                                    multi=False,
                                    id='county-input',
                                    clearable=True
                                ),
                            ],
                            row=False,
                        ),
                        width={'size': 3}
                    ), 
                    
                    dbc.Button("Oppdater", color="primary", id="UpdateButton")
                ], 
                ),
            ],), 
            width={"size": 10, "offset": 1}
        ),
        style={'margin-top': '25px'}
        ),
                
            
        dbc.Row([
            dbc.Col(children=[
                html.H6(children='Sykedata for ett distrikt'),
                dcc.Graph(figure=generate_county_sickleave_comparison(sykedata_monthly_df, county='Rogaland'), id='county-yearcomparison'),
                ],
            ),
            ],
            style={'margin-top': '25px'},
            className="text-center text-dark"
        ),
        dbc.Row([
            dbc.Col(children=[
                html.H6(children='Sykedata for ett distrikt'),
                dcc.Graph(figure=generate_onecounty_sykebarchart(sykedata_monthly_df, county='Oslo', year='2020'), id='county-meancomparison'),
                ],
            ),
            ],
            style={'margin-top': '25px'},
            className="text-center text-dark"
        ),
    ], fluid=True),
],
)
@app.callback(
    Output('county-yearcomparison', 'figure'),
    Output('county-meancomparison', 'figure'),
    [Input('UpdateButton', 'n_clicks'),
    State('year-input', 'value'),
    State('county-input', 'value'),])
def update_plots(n_clicks, year_value, county_value,):
    if year_value is not None and county_value is not None:
        return [generate_county_sickleave_comparison(sykedata_monthly_df, county=county_value), generate_onecounty_sykebarchart(sykedata_monthly_df, county=county_value, year=year_value)]
    else:
        return [generate_county_sickleave_comparison(sykedata_monthly_df), generate_onecounty_sykebarchart(sykedata_monthly_df)]
        
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port='8050')
