# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app import db, login_manager

from app.base.util import hash_pass

Base = declarative_base()

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)
    picker = Column(Boolean)
    supplier = Column(Boolean)
    bids = relationship('Bid')


    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None


user_bids = Table(
    'UserBids', Base.metadata,
    Column('user_id', Integer, ForeignKey('User.id')),
    Column('bid_id', Integer, ForeignKey('Bid.id'))
    )


class Bid(db.Model):

    __tablename__='Bid'

    id = Column(Integer, primary_key=True)
    bidder_id = Column(Integer, ForeignKey('User.id'))
    amount = Column(Float)
    pickup_id = Column(Integer, ForeignKey('Pickup.id'))
    pickup = relationship('Pickup')
    created = Column(DateTime)



class Pickup(db.Model):

    __tablename__='Pickup'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    pickup_by_date = Column(DateTime, nullable=False)
    winning_picker = Column(Integer, ForeignKey('User.id'))
    completed_picker = Column(Boolean)
    completed_supplier = Column(Boolean)
    auto_select_winner = Column(Boolean)
    picker_rating = Column(Integer)  # picker rating supplier
    supplier_rating = Column(Integer)


class Message(db.Model):
    __tablename__ = 'Message'
    id = Column(Integer, primary_key=True)
    sent_date = Column(DateTime, nullable=False)
    sender_id = None
    receiver_id = None
    contents = (Column, String)





