import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import os
import pandas as pd
import pandas_datareader.data as pdr
import datetime

# test

app = dash.Dash()

server = app.server

# ETFのティッカー一覧を読み込み
tickers_data = pd.read_csv('ticker.csv',header=None)
ticlist = []
for tc in tickers_data.itertuples():
    ticlist.append({'label': tc[1], 'value': tc[1]})

# 投信一覧を読み込み
funds_data = pd.read_csv('fundf.csv',index_col=0)
fdlist = []
for fd in funds_data.itertuples():
    fdlist.append({'label': fd[1], 'value': fd[2]})

app.layout = html.Div([
    dcc.Dropdown(
    id="dropdown-ticker",
    options=ticlist,
    value=['QQQ'],
    clearable=False,
    multi=True
),
html.Button(id="submit-button", children="表示"),
dcc.Graph(id="price_graph"),
dcc.Dropdown(
    id="dropdown-fund",
    options=fdlist,
    value=[''],
    clearable=False,
    multi=True
),
html.Button(id="fund-button", children="表示"),
dcc.Graph(id="fund_graph")
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



@app.callback(
    Output("fund_graph", "figure"),
    [Input("fund-button", 'n_clicks')],
    [State("dropdown-fund", "value")]
)
def update_output(n_clicks,funds):
    # データ取得
    ticker = ['QQQ','SPY','VTI','GLD']
    start = datetime.date(2018, 1, 1)
    end = datetime.date(2020, 12, 31)
    url_base = "https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd={isin}"
    dl_base = "https://toushin-lib.fwg.ne.jp"
    #一つだけロードしベースとする
    # pd_data = pdr.DataReader(ticker[0], 'yahoo', start, end)
    # pd_data.drop(columns=['High', 'Low', 'Open', 'Close', 'Volume'], inplace=True)
    # pd_data.columns = ['base']

    for fc in funds:
        url = url_base.format(isin=fc)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        dl = soup.find_all('a',{"id":"download"})
        dl_url = dl_base+dl[0].get('href')
        res = requests.get(dl_url)
        saveFileName = isin + ".csv"
        with open(saveFileName, 'wb') as saveFile:
            saveFile.write(res.content)
        time.sleep(1)

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