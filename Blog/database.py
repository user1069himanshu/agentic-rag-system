from sqlalchemy import create_engine

#Creating Engine
SQLALCHEMY_DATABSE_URL='sqlite:///./blog.db'

engine = create_engine(SQLALCHEMY_DATABSE_URL, connect_args={'check_same_thread':False})

#Map Declration
from sqlalchemy.ext.declarative import declarative_base

#Create seassion
from sqlalchemy.orm import sessionmaker

sessionlocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()