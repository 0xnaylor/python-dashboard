import dash
import dash_bootstrap_components as dbc
from dash import html
import requests
import pandas as pd
from dash import dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash import dash_table
import plotly.graph_objects as go


app = dash.Dash(external_stylesheets = [ dbc.themes.FLATLY],)

url = "https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=2000"
response_world = requests.request("GET", url)

apiKey = 'b04bef671bddd0eabb09aa4f4f505edaf2be6086c30b52b910d19efb4fdabc5e'
r=requests.get(url, headers={'authorization': 'Apikey {apiKey}'})
json = r.json()
df = pd.DataFrame(json['Data']['Data'])

# plotly graph objects
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(pd.to_datetime(df.time,unit='s')), y=list(df.close), showlegend=False))
fig.update_layout(title_text="USDBTC Historic Price")

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

fig.add_scatter(x = [fig.data[0].x[-1]], y = [fig.data[0].y[-1]],
                     mode = 'markers + text',
                     marker = {'color':'blue', 'size':14},
                     showlegend = False,
                     text = [fig.data[0].y[-1]],
                     textposition='middle right')

# def zoom(layout, xrange):
#     in_view = df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
#     fig.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]

# fig.layout.on_change(zoom, 'xaxis.range')

fig.show()

# plotly express
# fig = px.line(df, x=pd.to_datetime(df['time'],unit='s'), y='close')
# fig.show()
