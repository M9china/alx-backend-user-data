#!/usr/bin/env python3
""" User module
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """ User class
    """
    __tablename__ = 'users'

    email = Column(String(250), nullable=False)
    hashed_password = Column('password', String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    reset_token = (Column(String(250), nullable=True))
    session_id = Column(String(250), nullable=True)
