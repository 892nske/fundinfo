import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import os
import pandas as pd
import pandas_datareader.data as pdr
import datetime

app = dash.Dash()

server = app.server

tickers_data = pd.read_csv('ticker.csv',header=None)
ticlist = []
for tc in tickers_data.itertuples():
    ticlist.append({'label': tc[1], 'value': tc[1]})

app.layout = html.Div([
    dcc.Dropdown(
    id="dropdown-ticker",
    options=ticlist,
    value=['QQQ'],
    clearable=False,
    multi=True
),
html.Button(id="submit-button", children="表示"),
dcc.Graph(id="price_graph")
])

@app.callback(
    Output("price_graph", "figure"),
    [Input("submit-button", 'n_clicks')],
    [State("dropdown-ticker", "value")]
)
def update_output(n_clicks,ticker):
    # データ取得
    # ticker = ['QQQ','SPY','VTI','GLD']
    start = datetime.date(2018, 1, 1)
    end = datetime.date(2020, 12, 31)
    #一つだけロードしベースとする
    pd_data = pdr.DataReader(ticker[0], 'yahoo', start, end)
    pd_data.drop(columns=['High', 'Low', 'Open', 'Close', 'Volume'], inplace=True)
    pd_data.columns = ['base']

    for tic in ticker:
        pdv = pdr.DataReader(tic, 'yahoo', start, end)
        pdv.drop(columns=['High', 'Low', 'Open', 'Close', 'Volume'], inplace=True)
        pdv.columns = [tic]
        pd_data = pd_data.join(pdv, how='inner')

    pd_data.drop(columns=['base'], inplace=True)
    pd_ratio = pd_data/pd_data.iloc[0,:]
    pd_ratio['日付'] = pd_ratio.index

    # グラフの記述
    fig = go.Figure(layout=go.Layout(
                title = '価格推移',
                height = 800, 
                width = 1500,
                xaxis = dict(title="年月"),
                yaxis = dict(title="価格")
            )
        )
    
    # 価格グラフ
    for tc in ticker:
        fig.add_traces(go.Scatter(
            x = pd_ratio['日付'],
            y = pd_ratio[tc],
            mode='lines',
            name=tc,
            # marker_color='rgba(255, 182, 193, .9)'
        ))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)