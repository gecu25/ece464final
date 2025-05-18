# enter holder
# enter ticker
# enter purchase info (# of shares, $$ price)

# sidebar: enter ticker & holder
# pulls up current stats

import dash
import dash_bootstrap_components as dbc
import plotly.express as plotly
import plotly.graph_objects as graph_objects
import pandas
import yfinance as yfi

from dash import Dash, html, dcc, Input, Output, State
from database import engine, SessionLocal, Base
from sqlalchemy import select
from datetime import date
from models import Stock, HistoryMixin

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

with SessionLocal() as session:
    prelim_retrieve_query = select(Stock.name)
    prelim_stock_options = session.execute(prelim_retrieve_query).all()
    prelim_stock_options = [ret.name for ret in prelim_stock_options]

app.layout = dbc.Container([
    dcc.Store(id="stock-options", data=[]),
    dbc.Row(
        dbc.Col([
            html.Br(),
            html.Br(),
            html.H1("Portfolio Dashboard"),
            html.Br(),
            html.P("ECE464 ✧ A simple database to check on manually entered stocks", className="initdescription"),
            html.Br(),
            dcc.Markdown(children="---"),
            html.Br()
        ], width=True)
    ),
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2("Add New Purchase Info"),
                    html.P("Please enter the ticker symbol and the individual share price for the purchase (in cents)."),
                    html.Br(),
                    dcc.Input(id="ticker-input", type="text", placeholder="Enter ticker symbol"),
                    dcc.Input(id="buy-input", type="text", placeholder="Enter single-unit price"),
                    html.Button("Add", id="add-record", n_clicks=0),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(id="cand-graph"),
                ], width=6
            ),
            dbc.Col(
                [
                html.H2("Selected Stock Stats"),
                html.P("Choose the stock you want to see an overview for!"),
                html.Br(),
                dcc.Dropdown(id="ind-stats-input", options=[], searchable=True),
                html.Br(),
                html.Br(),
                dcc.Graph(id="ind-graph"),
                ], width=6
            ),
        ]
    ),
    dbc.Row(
        dbc.Col([
            html.Br(),
            dcc.Markdown(children="---"),
            html.Br(),
            html.H2("Cumulative Stats"),
            html.Br(),
            dcc.Graph(id="cumul-graph")
        ], width=True)
    )
])

# for adding new entries
@app.callback(
    Input("add-record", "n_clicks"),
    State("ticker-input", "value"),
    State("buy-input", "value")
)
def add_stock(n, value1, value2):
    hold_cv = -1
    hold_update = False

    try:
        if n > 0 and value1 and value2:
            new_tick = yfi.Ticker(value1)
            new_historical = new_tick.history(period="max", interval="1d")
            hold_cv = int((new_historical["Close"].iloc[-1]) * 100)

            with SessionLocal() as session:
                new_stock = Stock(ticker=value1, name=new_tick.info["longName"], buyvalue=value2, currentvalue=hold_cv)
                session.add(new_stock)
                session.commit()

            tname_hold = "history-" + value1

            class HistoryTemp(HistoryMixin, Base):
                __tablename__ = tname_hold

            Base.metadata.create_all(bind=engine)

            for d, r in new_historical.iterrows():
                with SessionLocal() as session:
                    new_date = d
                    new_close = int(r["Close"] * 100)
                    new_rec = HistoryTemp(_date=new_date, ticker=value1, closevalue=new_close)
                    session.add(new_rec)
                    session.commit()
    except Exception as e:
        hold_update = True
        print(f"An error occurred: {e}")

    if hold_update:
        try:
            with SessionLocal() as session:
                updt_item = session.get(Stock, value1)
                updt_item.buyvalue = value2
                updt_item.currentvalue = hold_cv
                session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

# for refreshing the stock options list (background)
@app.callback(
    Output("stock-options", "data"),
    Input("add-record", "n_clicks")
)
def refresh_inventory(n):
    with SessionLocal() as session:
        retrieve_query = select(Stock.name)
        stock_options = session.execute(retrieve_query).all()
        stock_options = [ret.name for ret in stock_options]

    return stock_options

# for updating dropdown
@app.callback(
    Output("ind-stats-input", "options"),
    Input("stock-options", "data"),
    Input("add-record", "n_clicks")
)
def update_dropdown(stocklist, n):
    return [stock for stock in stocklist]

# for updating single stock graph
@app.callback(
    Output("ind-graph", "figure"),
    Input("ind-stats-input", "value"),
    Input("add-record", "n_clicks")
)
def update_single_stats(drop1, n):
    with SessionLocal() as session:
        sing_tick = session.execute(select(Stock.ticker).where(Stock.name == drop1)).all()
        sing_tick = [ret.ticker for ret in sing_tick]
        sing_tick = sing_tick[0]

        sing_base = session.execute(select(Stock.buyvalue).where(Stock.name == drop1)).all()
        sing_base = [ret.buyvalue for ret in sing_base]
        sing_base = float(sing_base[0]) / 100

    sing_yfi_tick = yfi.Ticker(sing_tick)
    df1 = sing_yfi_tick.history(period="max", interval="1d")
    df1 = df1.drop(columns=["Open", "High", "Low", "Volume", "Dividends", "Stock Splits"])
    df1 = df1.reset_index()

    sing_fig = plotly.scatter(df1, x="Date", y="Close")
    sing_fig.update_xaxes(title="Closing Date")
    sing_fig.update_yaxes(title="Closing Price, USD", type='linear')
    sing_fig.update_layout(margin={'l': 75, 'b': 75, 't': 30, 'r': 50}, hovermode='closest')
    sing_fig.update_layout(
        font_family="Courier New",
        font_color="#34312d",
        plot_bgcolor="#E5DFFF"
    )
    sing_fig.update_layout(shapes=[dict(type="line", x0=min(df1["Date"]), y0=sing_base, x1=max(df1["Date"]), y1=sing_base, line=dict(color="red", width=2))])

    return sing_fig

# for updating candlestick graph
@app.callback(
    Output("cand-graph", "figure"),
    Input("ind-stats-input", "value"),
    Input("add-record", "n_clicks")
)
def update_cand_stats(drop2, n):
    with SessionLocal() as session:
        cand_tick = session.execute(select(Stock.ticker).where(Stock.name == drop2)).all()
        cand_tick = [ret.ticker for ret in cand_tick]
        cand_tick = cand_tick[0]

    cand_yfi_tick = yfi.Ticker(cand_tick)
    df2 = cand_yfi_tick.history(period="max", interval="1d")
    df2 = df2.reset_index()

    cand_fig = graph_objects.Figure(data=[graph_objects.Candlestick(x=df2["Date"],
                                                      open=df2["Open"],
                                                      high=df2["High"],
                                                      low=df2["Low"],
                                                      close=df2["Close"])])
    cand_fig.update_layout(margin={'l': 75, 'b': 50, 't': 50, 'r': 25}, hovermode='closest')
    cand_fig.update_layout(
        font_family="Courier New",
        font_color="#34312d",
        plot_bgcolor="#E5DFFF"
    )
    cand_fig.update_xaxes(title="Record Date")
    cand_fig.update_yaxes(title="Price, USD", type='linear')

    return cand_fig

# for updating cumulative price graph
@app.callback(
    Output("cumul-graph", "figure"),
    Input("add-record", "n_clicks"),
    Input("stock-options", "data"),
)
def update_cumulative(n, stock_list):
    cumul_fig = graph_objects.Figure()
    cumul_fig.update_xaxes(title="Closing Date")
    cumul_fig.update_yaxes(title="Closing Price, USD", type='linear')
    cumul_fig.update_layout(
        font_family="Courier New",
        font_color="#34312d",
        plot_bgcolor="#E5DFFF"
    )
    cumul_fig.update_layout(margin={'l': 100, 'b': 100, 't': 50, 'r': 100}, hovermode='closest')

    with SessionLocal() as session:
        for stk in stock_list:
            cumul_tick = session.execute(select(Stock.ticker).where(Stock.name == stk)).all()
            cumul_tick = [ret.ticker for ret in cumul_tick]
            cumul_tick = cumul_tick[0]

            cumul_yfi_tick = yfi.Ticker(cumul_tick)
            df3 = cumul_yfi_tick.history(period="max", interval="1d")
            df3 = df3.drop(columns=["Open", "High", "Low", "Volume", "Dividends", "Stock Splits"])
            df3 = df3.reset_index()

            cumul_fig.add_trace(graph_objects.Scatter(x=df3["Date"], y=df3["Close"], mode="lines", name=cumul_tick))

    return cumul_fig

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)