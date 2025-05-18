from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import declared_attr, backref, relationship

from database import Base

class Stock(Base):
	__tablename__ = "stocks"

	ticker = Column(String, primary_key=True)
	name = Column(String)
	buyvalue = Column(Integer)
	currentvalue = Column(Integer)

class HistoryMixin(Base):
	__abstract__ = True
	_date = Column(DateTime, primary_key=True)
	closevalue = Column(Integer)

	@declared_attr
	def ticker(cls):
		return Column("ticker", ForeignKey("stocks.ticker"))

	@declared_attr
	def stock(cls):
		return relationship("Stock")