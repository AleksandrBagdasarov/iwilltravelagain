from sqlalchemy import Column, String, Integer, Float, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()


class StartUrls(Base):
    __tablename__ = 'start_urls'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(1024), nullable=False)


class Activities(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    category = Column(String(64), nullable=False)
    location = Column(String(64), nullable=False)
    web_site = Column(String(1024), nullable=True)
    start_urls_id = Column(Integer)