import yfinance as yfi

my_stonks = [
    "HTZ",
    "AAPL",
    "NVDA",
    "GOOG"
]

for sym in my_stonks:
    temp_tick = yfi.Ticker(sym)
    temp_historical = temp_tick.history(period="max", interval="1d")
    print(temp_historical.columns.tolist())
    print(temp_historical)
    for d, r in temp_historical.iterrows():
        temp_date = d
        temp_close = int(r["Close"] * 100)
        print(sym)
        print(temp_date)
        print(temp_close)