from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from opcua import Client

# Connect to main app.py file
# from app import app
# from app import server

from apps import navigationadv, graph, dashboard_layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
                
server = app.server


url = "opc.tcp://192.168.0.30:4840"
client = Client(url)

app.layout = html.Div([

    html.Div(navigationadv.navbar),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),   
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/graph':
        return graph.layout
    else:
        return dashboard_layout.layout


if __name__ == '__main__':
    app.run_server(debug=False, port = 3000)

client.disconnect()
client.session_timeout = 10000
