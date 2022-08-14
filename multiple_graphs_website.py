# -*- coding: utf-8 -*-
# importing libraries 
import plotly.graph_objects as go       # plotly graph objects
from plotly.subplots import make_subplots       # plotly.subplots make subplots
import pandas as pd             # pandas
import numpy as np          # numpy
import dash         # Dash
import dash_core_components as dcc      # dash core components dcc 
import dash_html_components as html      # dash core component html
import requests         # requests
from datetime import datetime , timedelta
from dash.dependencies import Output , Input
from data_analysis import DataAnalysis
import main
import pickle
import sys



# initialialize app ###############################################################

app = dash.Dash(__name__, title="SatEmLat")
server = app.server

app.layout = html.Div([
            html.Div([
                html.Img(src="/assets/favicon.ico", style={'height':'10%', 'width':'10%'})
            ], className = 'row'),
            html.Div([
                html.Div([
                    dcc.Graph(id = 'fig_1' ,),
                    dcc.Interval(id = 'fig_1_update' ,interval=2500 , n_intervals = 0)
                ], className = 'six columns'),
                html.Div([
                    dcc.Graph(id = 'fig_2' ),
                    dcc.Interval(id = 'fig_2_update', interval= 2500, n_intervals = 0)
                ], className = 'six columns')
            ], className = 'row'),
            html.Div([
                html.Div([
                    dcc.Graph(id = 'fig_3'),
                    dcc.Interval(id='fig_3_update' , interval = 2500 , n_intervals = 0)
                ], className = 'four columns'),
                html.Div([
                    dcc.Graph(id = 'fig_4'),
                    dcc.Interval(id = 'fig_4_update' , interval = 2500 , n_intervals = 0)
                ] , className = 'four columns'),
                html.Div([
                    dcc.Graph(id = 'fig_5'),
                    dcc.Interval(id = 'fig_5_update' , interval = 2500 , n_intervals = 0)
                ], className = 'four columns')
            ], className = 'row'),
            html.Div([
                html.Div([
                    dcc.Graph(id = 'fig_6'),
                    dcc.Interval(id= 'fig_6_update' , interval = 2500 , n_intervals= 0)
                ], className ='four columns'),
                html.Div([
                    dcc.Graph(id = 'fig_7'),
                    dcc.Interval(id = 'fig_7_update' , interval = 2500 , n_intervals=0)
                ], className = 'four columns'),
                html.Div([
                    dcc.Graph(id = 'fig_8' ),
                    dcc.Interval(id = 'fig_8_update' , interval = 2500 , n_intervals= 0)
                ], className = 'four columns')
            ], className = 'row'),
        ], style = {
        'backgroundColor' : "#ffffff"
        } , className = 'container-fluid')

PLOT_POINTS = 200

def calcVelocityAcceleration(gfz, alt, t):
    velocity = -1 * np.diff(alt) / np.diff(t)
    time = (np.array(t)[:-1] + np.array(t)[1:]) / 2
    aceleration = 0
    return velocity, time, aceleration

@app.callback([Output('fig_1' , 'figure'),
                Output('fig_2' , 'figure'),
                Output('fig_3', 'figure'),
                Output('fig_4' , 'figure'),
                Output('fig_5' , 'figure'),
                Output('fig_6' , 'figure'),
                Output('fig_7' , 'figure'),
                Output('fig_8' , 'figure')],
                [Input('fig_1_update' , 'n_intervals')])
def update_data(n):
    try:
        with open("temp.txt", "rb") as t:
            DATA = pickle.load(t)
    except:
        sys.exit()

    DATA.clean()

    print(DATA)
    sep = DATA.val_read()
    time = list(map(float, sep[0]))
    mpu_temp = list(map(float, sep[1]))
    accel = list(map(float, sep[2]))
    airQuality = list(map(lambda x: 100-x/1023*100, map(float, sep[3])))
    press = list(map(float, sep[4]))
    temp = list(map(float, sep[5]))
    alt = list(map(float, sep[6]))
    co = list(map(float, sep[7]))
    humidity = list(map(float, sep[8]))
    uv = list(map(float, sep[9]))

    velocity, tVel, acceleration = calcVelocityAcceleration(list(map(lambda x: x/9.8, accel)), alt, time)

    if len(sep[0]) > PLOT_POINTS:
        time = time[-PLOT_POINTS:]
        mpu_temp = mpu_temp[-PLOT_POINTS:]
        accel = accel[-PLOT_POINTS:]
        airQuality = airQuality[-PLOT_POINTS:]
        press = press[-PLOT_POINTS:]
        temp = temp[-PLOT_POINTS:]
        alt = alt[-PLOT_POINTS:]
        co = co[-PLOT_POINTS:]
        humidity = humidity[-PLOT_POINTS:]
        velocity = velocity[-PLOT_POINTS:]
        tVel = tVel[-PLOT_POINTS:]

    ####################### Creating the figure #############################
    
    ################################## creating fig 1 ##########################################
    
    fig_1 = go.Figure(
        data=    go.Scatter(
            x = time,
            y = temp,
            mode = 'lines',
            name = 'Temperature/Time'
        ))
    fig_1.update_layout(title = 'TEMPERATURE/TIME' , paper_bgcolor ="#ffffff" , plot_bgcolor="#ffffff" , font = dict(color = '#3c3b6f') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_1.update_xaxes(showgrid = False , zeroline = False ,showline=False )
    fig_1.update_yaxes(showgrid = False , zeroline = False , showline = False )

    ################################## creating fig 2 ##########################################

    fig_2 = go.Figure(
        data=    go.Scatter(
            x = time,
            y = alt,
            mode = 'lines',
            name = 'Altitude/Time'
        ))
    fig_2.update_layout(title = 'ALTITUDE/TIME' , paper_bgcolor ="#ffffff" , plot_bgcolor="#ffffff" , font = dict(color = '#3c3b6f') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_2.update_xaxes(showgrid = False , zeroline = False ,showline=False )
    fig_2.update_yaxes(showgrid = False , zeroline = False , showline = False )

    ################################## creating fig 3 ##########################################

    fig_3 = go.Figure(
        data=    go.Scatter(
            x = time,
            y = co,
            mode = 'lines',
            name = 'CO2/Time'
        ))
    fig_3.update_layout(title = 'CO2/Time' , paper_bgcolor ="#ffffff" , plot_bgcolor="#ffffff" , font = dict(color = '#3c3b6f') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_3.update_xaxes(showgrid = False , zeroline = False ,showline=False )
    fig_3.update_yaxes(showgrid = False , zeroline = False , showline = False )

    ################################## creating fig 4 ##########################################

    fig_4 = go.Figure(
        data=    go.Scatter(
            x = time,
            y = humidity,
            mode = 'lines',
            name = 'Humidity/Time'
        ))
    fig_4.update_layout(title = 'Humidity/Time' , paper_bgcolor ="#ffffff" , plot_bgcolor="#ffffff" , font = dict(color = '#3c3b6f') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_4.update_xaxes(showgrid = False , zeroline = False ,showline=False )
    fig_4.update_yaxes(showgrid = False , zeroline = False , showline = False )

    ################################## creating fig 5 ##########################################

    fig_5 = go.Figure(
        data=    go.Scatter(
            x = alt,
            y = temp,
            mode = 'markers',
            name = 'Temperature/Altitude'
        ))
    fig_5.update_layout(title = 'Temperature/Altitude' , paper_bgcolor ="#ffffff" , plot_bgcolor="#ffffff" , font = dict(color = '#3c3b6f') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_5.update_xaxes(showgrid = False , zeroline = False ,showline=False )
    fig_5.update_yaxes(showgrid = False , zeroline = False , showline = False )

    ################################## creating fig 6 ##########################################
    
    fig_6 = go.Figure(
        data=    go.Scatter(
            x = tVel,
            y = velocity,
            mode = 'lines',
            name = 'Velocity/Time'
        ))
    fig_6.update_layout(title = 'Velocity/Time' , paper_bgcolor ="#ffffff" , plot_bgcolor="#ffffff" , font = dict(color = '#3c3b6f') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_6.update_xaxes(showgrid = False , zeroline = False ,showline=False )
    fig_6.update_yaxes(showgrid = False , zeroline = False , showline = False )

    ################################## creating fig 7 ##########################################

    fig_7 = go.Figure( 
                data = go.Scatter(
                x = time,
                y = airQuality,
                mode = 'lines',
                name = 'Air Quality/Time'
            ))
    fig_7.update_layout(title = 'AirQuality/Time' , paper_bgcolor ="#ffffff" , plot_bgcolor="#ffffff" , font = dict(color = '#3c3b6f') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_7.update_xaxes(showgrid = False , zeroline = False ,showline=False )
    fig_7.update_yaxes(showgrid = False , zeroline = False , showline = False )

    ################################## creating fig 8 ##########################################
    
    fig_8 = go.Figure(
        data=    go.Scatter(
            x = press,
            y = alt,
            mode = 'markers',
            name = 'Altitude/Pressure'
        ))
    fig_8.update_layout(title = 'Altitude/Pressure' , paper_bgcolor ="#ffffff" , plot_bgcolor="#ffffff" , font = dict(color = '#3c3b6f') ,legend_orientation='h', legend = dict(x = 0.1 , y = -0.05))
    fig_8.update_xaxes(showgrid = False , zeroline = False ,showline=False )
    fig_8.update_yaxes(showgrid = False , zeroline = False , showline = False )

    return [fig_1, fig_2, fig_3, fig_4, fig_5, fig_6, fig_7, fig_8]


app.run_server(debug=False)