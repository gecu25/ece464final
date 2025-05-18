# enter holder
# enter ticker
# enter purchase info (# of shares, $$ price)

# sidebar: enter ticker & holder
# pulls up current stats

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import psycopg2
import pandas

from dash import Dash, html, dcc, Input, Output, State
from database import engine, SessionLocal, Base
from models import Stock#, HistoryMixin
from insert_functions import scraper

session = SessionLocal()

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pandas.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col([
            html.Br(),
            html.Br(),
            html.H1("Portfolio Dashboard"),
            html.P("ECE464 ✧ A simple database to check on manually entered stocks", className="initdescription"),
            html.Br(),
            dcc.Markdown(children="---"),
            html.Br()
        ], width=True)
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2("Add New Purchase Info"), width=6
            ),
            dbc.Col(
                [
                    html.H2("Add New Purchase Info"),
                    html.P("Please enter the ticker symbol and the individual share price for the purchase."),
                    dcc.Input(id="ticker-input", type="text", placeholder="Enter ticker symbol"),
                    dcc.Input(id="buy-input", type="text", placeholder="Enter single-unit price"),
                    html.Button("Add", id="add-record", n_clicks=0)
                ], width=6
            ),
            dbc.Col(
                html.H2("Selected Stock Stats"), width=6
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
            dcc.Graph(
                id='life-exp-vs-gdp',
                figure=fig
            )
        ], width=True)
    )
])

@app.callback(
    Output("ticker-input", "value"),
    Input("add-record", "n_clicks"),
    State("ticker-input", "value"),
    State("buy-input", "value")
)
def add_stock(n, value1, value2):
    temp_scrape_data = scraper(value1)

    try:
        if n > 0 and value1 and value2:
            new_stock = Stock(ticker=value1, name=(temp_scrape_data[0]), buyvalue=value2, currentvalue=(temp_scrape_data[1]))
            session.add(new_stock)
            session.commit()
            return ""
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)