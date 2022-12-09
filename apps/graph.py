import dash_bootstrap_components as dbc
from dash import dash, Input, Output, State, html, dcc
import pymysql
import time
import pandas as pd
import plotly.graph_objects as go
from app import app

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id = 'torque-graph', figure = {}),
                            dcc.Interval(id = 'graph-update', n_intervals = 0, interval = 1000*1)
                        ])
                    ]),

                    dbc.Row([
                        dbc.Col([
                            html.Div('% Change: ', style = {'size':20})
                        ], width = 1, className = 'ms-5'),

                        dbc.Col([
                            html.P([
                                dcc.Graph(id = 'delta-indicator', figure = {}),
                                dcc.Interval(id = 'delta-update', n_intervals = 0, interval = 1000*1)
                            ], style = {'width':'12rem'})
                        ])
                    ]),
                ])
            ], style = {'width' : '145rem'}, className = 'm-5', color = 'secondary')
        ])
    ], justify='center')
], fluid = True)

# Delta indicator callback
@app.callback(
    Output('delta-indicator', 'figure'),
    Input('delta-update', 'n_intervals')
)
def update_delta(timer):
    for seconds in range(5):
        mydb2 = pymysql.connect(
            host="192.168.0.206",
            user="Emmanuel_Sim",
            password= "1221",
            database = "14octtraining"
        )
        cursor2 = mydb2.cursor()
        data = {
            "Torque":[],
            "Time":[]
            }
        cursor2.execute("SELECT * FROM s3_smart_drill_torque ORDER BY PID DESC LIMIT 30")
        # SELECT * FROM ( SELECT * FROM s3_smart_drill_torque ORDER BY PID DESC LIMIT 3 )Var1 ORDER BY time_stamp ASC

        tmp = cursor2.fetchall()
        mydb2.commit()

        for i in range(len(tmp)):
            data['Torque'].append(tmp[i][2])
            data['Time'].append(tmp[i][1])

        # mydb2.close()
        df1 = pd.DataFrame(data)
        df1['Time'] = pd.to_datetime(df1['Time'],format).apply(lambda x: x.time())
        df1=df1.iloc[::-1]
        mydb2.close()
    
    dff_rv = df1.iloc[::-1]
    day_start = dff_rv[dff_rv['Time'] == dff_rv['Time'].min()]['Torque'].values[0]
        
    day_end = dff_rv[dff_rv['Time'] == dff_rv['Time'].max()]['Torque'].values[0]


    fig = go.Figure(go.Indicator(
        mode = 'delta',
        value = day_end,
        delta = {'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font = {'size':13})
    fig.update_layout(height = 30, width = 80)
    fig.update_layout({
    'paper_bgcolor': 'rgba(0, 0, 0, 0)'
    })

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')

    return fig




@app.callback(
    Output('torque-graph', 'figure'),
    Input('graph-update', 'n_intervals')
)
def update_graph(n):
    for seconds in range(5):
        mydb2 = pymysql.connect(
            host="192.168.0.206",
            user="Emmanuel_Sim",
            password= "1221",
            database = "14octtraining"
        )
        cursor2 = mydb2.cursor()
        data = {
            "Torque":[],
            "Time":[]
            }
        cursor2.execute("SELECT * FROM s3_smart_drill_torque ORDER BY PID DESC LIMIT 50")
        # SELECT * FROM ( SELECT * FROM s3_smart_drill_torque ORDER BY PID DESC LIMIT 3 )Var1 ORDER BY time_stamp ASC

        tmp = cursor2.fetchall()
        mydb2.commit()

        for i in range(len(tmp)):
            data['Torque'].append(tmp[i][2])
            data['Time'].append(tmp[i][1])

        # mydb2.close()
        df1 = pd.DataFrame(data)
        df1['Time'] = pd.to_datetime(df1['Time'],format).apply(lambda x: x.time())
        df1=df1.iloc[::-1]
        mydb2.close()

    fig = go.Figure(data=go.Scatter(x= df1['Time'], y=df1['Torque'], mode='lines+markers'))
    #fig.add_trace(go.Scatter(y=data['Torque'], x=data['Time'], mode="lines+markers"), row=1, col=1)
    fig.update_layout(yaxis_range = [0,0.2], title = 'Smart Drill Torque Value')
    fig.update_xaxes(title = 'Time (s)')
    fig.update_yaxes(title = 'Torque (Nm)')
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0.1)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)'
    })
    return fig




# if __name__ == '__main__':
#     app.run_server(debug=False)