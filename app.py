import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import os

app = dash.Dash()

server = app.server

app.layout = html.Div([
    
])


if __name__ == '__main__':
    app.run_server(debug=True)