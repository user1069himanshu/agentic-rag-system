from .database import Base
from sqlalchemy import Column, Integer, String


#Defining what show be in the table

class Blog(Base):
    __tablename__ = 'blogs'
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String)
    body=Column(String)
