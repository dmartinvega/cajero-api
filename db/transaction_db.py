from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
import datetime
from db.db_connection import Base, engine

class TransactionInDB(Base):
    __tablename__ = "transactions"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    username        = Column(String, ForeignKey("users.username"))
    date            = Column(DateTime, default=datetime.datetime.utcnow)
    value           = Column(Integer)
    actual_balance  = Column(Integer)

Base.metadata.create_all(bind=engine)
