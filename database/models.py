from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    expenses = relationship("Expense", back_populates="user")
    sales = relationship("Sale", back_populates="user")
    reports = relationship("FinancialReport", back_populates="user")

class Expense(Base):
    __tablename__ = 'expenses'
    
    expense_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text)
    
    user = relationship("User", back_populates="expenses")

class Inventory(Base):
    __tablename__ = 'inventory'
    
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String(100), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)
    
    sales_items = relationship("SaleItem", back_populates="inventory_item")

class Sale(Base):
    __tablename__ = 'sales'
    
    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    user = relationship("User", back_populates="sales")
    sale_items = relationship("SaleItem", back_populates="sale")

class SaleItem(Base):
    __tablename__ = 'sales_items'
    
    sale_item_id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey('sales.sale_id'))
    item_id = Column(Integer, ForeignKey('inventory.item_id'))
    quantity = Column(Integer, nullable=False)
    
    sale = relationship("Sale", back_populates="sale_items")
    inventory_item = relationship("Inventory", back_populates="sales_items")

class FinancialReport(Base):
    __tablename__ = 'financial_reports'
    
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    report_type = Column(String(50), nullable=False)
    generated_date = Column(Date, nullable=False)
    content = Column(Text, nullable=False)
    
    user = relationship("User", back_populates="reports")