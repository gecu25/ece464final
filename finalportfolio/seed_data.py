import random
import yfinance as yfi

from database import SessionLocal, engine
from models import Base, Stock, HistoryMixin

def seed_data():
    session = SessionLocal()

    my_stonks = [
        "HTZ",
        "AAPL",
        "NVDA",
        "GOOG"
    ]

    for sym in my_stonks:
        temp_tick = yfi.Ticker(sym)
        temp_historical = temp_tick.history(period="max", interval="1d")

        temp_cv = int((temp_historical["Close"].iloc[-1]) * 100)

        temp_stock = Stock(ticker=sym, name=temp_tick.info["longName"], buyvalue=0, currentvalue=temp_cv)
        session.add(temp_stock)
        session.commit()

        name_hold = "history-" + sym

        class HistoryTemp(HistoryMixin, Base):
	        __tablename__ = name_hold

        Base.metadata.create_all(bind=engine)

        for d, r in temp_historical.iterrows():
            temp_date = d
            temp_close = int(r["Close"] * 100)
            start_rec = HistoryTemp(_date=temp_date, ticker=sym, closevalue=temp_close)
            session.add(start_rec)
            session.commit()

    session.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_data()