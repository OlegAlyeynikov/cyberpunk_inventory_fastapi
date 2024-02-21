import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Float, Text, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from passlib.context import CryptContext

load_dotenv()
db_url = os.getenv("SQLALCHEMY_DATABASE_URL")
Base = declarative_base()
engine = create_engine(db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default='user')


class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    category = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
