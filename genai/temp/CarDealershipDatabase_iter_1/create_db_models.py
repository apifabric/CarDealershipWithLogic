# using resolved_model gpt-4o-2024-08-06# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py

from sqlalchemy.dialects.sqlite import *


class Dealer(Base):
    """description: Represents an individual or company that sells cars."""
    __tablename__ = 'dealers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String)
    contact_number = Column(String)
    stock_limit = Column(Integer)
    inventory_total = Column(Integer)  # Sum of car stock inventory


class Car(Base):
    """description: Represents a car available in the dealership."""
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, autoincrement=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer)
    description = Column(String)
    dealer_id = Column(Integer, ForeignKey('dealers.id'))


class Inventory(Base):
    """description: Contains current stock details of cars in dealership inventory."""
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    stock_amount = Column(Integer, nullable=False)
    location = Column(String)


class Customer(Base):
    """description: Represents a customer of the dealership."""
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    unpaid_sales_count = Column(Integer)  # Count of unpaid sales


class Sale(Base):
    """description: Represents a sale transaction of a car to a customer."""
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    sale_date = Column(DateTime, default=datetime.utcnow)
    amount = Column(Integer, nullable=False)
    is_paid = Column(Boolean, default=False)


# end of model classes


try:
    
    
    
    
    # ALS/GenAI: Create an SQLite database
    
    engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    
    Base.metadata.create_all(engine)
    
    
    
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    
    
    # ALS/GenAI: Prepare for sample data
    
    
    
    session.commit()
    dealer1 = Dealer(name="City Auto", address="123 Main St.", contact_number="555-1234", stock_limit=50)
    dealer2 = Dealer(name="Town Motors", address="789 Elm St.", contact_number="555-6789", stock_limit=30)
    dealer3 = Dealer(name="Auto Plaza", address="456 Oak St.", contact_number="555-4567", stock_limit=40)
    dealer4 = Dealer(name="Village Cars", address="321 Pine St.", contact_number="555-9876", stock_limit=20)
    sale1 = Sale(car_id=1, customer_id=1, sale_date=date(2021, 6, 15), amount=25000, is_paid=False)
    sale2 = Sale(car_id=2, customer_id=2, sale_date=date(2021, 7, 18), amount=22000, is_paid=True)
    sale3 = Sale(car_id=3, customer_id=3, sale_date=date(2021, 8, 21), amount=35000, is_paid=False)
    sale4 = Sale(car_id=4, customer_id=1, sale_date=date(2021, 9, 25), amount=20000, is_paid=True)
    inventory1 = Inventory(car_id=1, stock_amount=5, location="Showroom A")
    inventory2 = Inventory(car_id=2, stock_amount=3, location="Showroom B")
    inventory3 = Inventory(car_id=3, stock_amount=2, location="Warehouse")
    inventory4 = Inventory(car_id=4, stock_amount=4, location="Showroom A")
    
    
    
    session.add_all([dealer1, dealer2, dealer3, dealer4, sale1, sale2, sale3, sale4, inventory1, inventory2, inventory3, inventory4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
