from sqlalchemy import Column, Integer, String
from db.db_connection import Base, engine

class UserInDB(Base):
    __tablename__ = "users"

    username    = Column(String, primary_key=True, unique=True)
    password    = Column(String)
    balance     = Column(Integer)

Base.metadata.create_all(bind=engine)
