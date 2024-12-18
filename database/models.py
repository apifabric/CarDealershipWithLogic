# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 18, 2024 18:18:19
# Database: sqlite:////tmp/tmp.laBEUJJ4k5/CarDealershipDatabase_iter_1/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Customer(SAFRSBaseX, Base):
    """
    description: Represents a customer of the dealership.
    """
    __tablename__ = 'customers'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    unpaid_sales_count = Column(Integer)

    # parent relationships (access parent)

    # child relationships (access children)
    SaleList : Mapped[List["Sale"]] = relationship(back_populates="customer")



class Dealer(SAFRSBaseX, Base):
    """
    description: Represents an individual or company that sells cars.
    """
    __tablename__ = 'dealers'
    _s_collection_name = 'Dealer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)
    contact_number = Column(String)
    stock_limit = Column(Integer)
    inventory_total = Column(Integer)

    # parent relationships (access parent)

    # child relationships (access children)
    CarList : Mapped[List["Car"]] = relationship(back_populates="dealer")



class Car(SAFRSBaseX, Base):
    """
    description: Represents a car available in the dealership.
    """
    __tablename__ = 'cars'
    _s_collection_name = 'Car'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer)
    description = Column(String)
    dealer_id = Column(ForeignKey('dealers.id'))

    # parent relationships (access parent)
    dealer : Mapped["Dealer"] = relationship(back_populates=("CarList"))

    # child relationships (access children)
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="car")
    SaleList : Mapped[List["Sale"]] = relationship(back_populates="car")



class Inventory(SAFRSBaseX, Base):
    """
    description: Contains current stock details of cars in dealership inventory.
    """
    __tablename__ = 'inventory'
    _s_collection_name = 'Inventory'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    car_id = Column(ForeignKey('cars.id'))
    stock_amount = Column(Integer, nullable=False)
    location = Column(String)

    # parent relationships (access parent)
    car : Mapped["Car"] = relationship(back_populates=("InventoryList"))

    # child relationships (access children)



class Sale(SAFRSBaseX, Base):
    """
    description: Represents a sale transaction of a car to a customer.
    """
    __tablename__ = 'sales'
    _s_collection_name = 'Sale'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    car_id = Column(ForeignKey('cars.id'))
    customer_id = Column(ForeignKey('customers.id'))
    sale_date = Column(DateTime)
    amount = Column(Integer, nullable=False)
    is_paid = Column(Boolean)

    # parent relationships (access parent)
    car : Mapped["Car"] = relationship(back_populates=("SaleList"))
    customer : Mapped["Customer"] = relationship(back_populates=("SaleList"))

    # child relationships (access children)
