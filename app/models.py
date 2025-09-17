from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, String, Table, Column

# create  base class for our models
class Base(DeclarativeBase):
    pass

#Instatiate your SQLAlchemy database:
db = SQLAlchemy(model_class = Base)

service_mechanics = db.Table(
    'service_mechanics',
    Base.metadata,
    db.Column('ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(15), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    #One to Many from customers to service tickets
    service_tickets: Mapped[list['ServiceTickets']] = relationship('ServiceTickets', back_populates='customer')

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(15), nullable=False, unique=True)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    tickets: Mapped[list['ServiceTickets']] = relationship('ServiceTickets', secondary=service_mechanics, back_populates='mechanics')

class ServiceTickets(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date: Mapped[date]
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    #Relationships
    customer: Mapped[Customer] = relationship('Customer', back_populates='service_tickets')
    mechanics: Mapped[list['Mechanic']] = relationship('Mechanic', secondary=service_mechanics, back_populates='tickets')


