import datetime
import enum
from uuid import uuid4

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum, Float, Text, MetaData
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class TypeOrder(enum.Enum):
    in_hall = 1
    with_myself = 2


class StatusOrder(enum.Enum):
    waiting_for_payment = 1
    paid = 2
    waiting_for_confirmation = 3
    confirmed = 4
    prepared = 5
    ready = 6
    waiting_for_the_courier = 7
    delivery = 8
    completed = 9


class Role(db.Model):
    __tablename__ = "role"
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __repr__(self):
        return f"{self.name}"


class Type(db.Model):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String(255))

    def __repr__(self):
        return f"{self.name}"


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))
    name = Column(String(32), nullable=False)
    surname = Column(String(32), nullable=False)
    patronymics = Column(String(32), nullable=False)

    phone = Column(String(20), nullable=False)
    email = Column(String(32), nullable=False)

    data_bith = Column(Date, nullable=True)
    role = relationship("Role")
    passport_series = Column(String(4), nullable=True)
    passport_number = Column(String(10), nullable=True)

    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, val):
        self.password_hash = generate_password_hash(val)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.surname} {self.name[0]}. {self.patronymics[0]}."


class Order(db.Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

    datatime_order = Column(DateTime, nullable=False, default=datetime.datetime.now())
    type_order = Column(Enum(TypeOrder), default=TypeOrder.in_hall)
    status_order = Column(Enum(StatusOrder), default=StatusOrder.waiting_for_confirmation)
    sweet_products = relationship("OrderToSweetProduct")
    address = Column(String, nullable=True)
    description = Column(Text, nullable=True)


class OrderToSweetProduct(db.Model):
    __tablename__ = "order_to_sweet_product"
    id_order = Column(ForeignKey("order.id"), primary_key=True)
    id_sweet_product = Column(ForeignKey("sweet_product.id"), primary_key=True)
    sweet_product = relationship("SweetProduct")
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return f"{self.sweet_product.name} {self.price}"


class SweetProduct(db.Model):
    __tablename__ = "sweet_product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))

    name = Column(String(32), nullable=False)

    type_id = Column(Integer, ForeignKey('type.id'), nullable=True)
    type = relationship("Type")

    price_sweet = Column(Float, nullable=False, default=0.0)
    weight_sweet = Column(Integer, nullable=False, default=0)
    description = Column(Text, nullable=True)
    image = Column(String, nullable=True, default="default.png")
    ingredients = relationship(
        "Ingredient", secondary="sweet_product_to_ingredient"
    )


class SweetProductToIngredient(db.Model):
    __tablename__ = "sweet_product_to_ingredient"
    id_sweet_product = Column(ForeignKey("sweet_product.id"), primary_key=True)
    id_ingredient = Column(ForeignKey("ingredient.id"), primary_key=True)


class Ingredient(db.Model):
    __tablename__ = "ingredient"
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(32), nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"{self.name}"


class Bakery(db.Model):
    __tablename__ = "bakery"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))

    name = Column(String(32), nullable=False)
    address = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"{self.name} ({self.address})"


class Table(db.Model):
    __tablename__ = "table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    description = Column(Text, nullable=True)
    bakery_id = Column(Integer, ForeignKey('bakery.id'), nullable=True)
    bakery = relationship("Bakery")

    def __repr__(self):
        return f"{self.name}"


class RegistrateTable(db.Model):
    __tablename__ = "registrate_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, unique=True, default=str(uuid4()))

    name = Column(String(32), nullable=False)
    surname = Column(String(32), nullable=False)
    patronymics = Column(String(32), nullable=False)

    phone = Column(String(20), nullable=False)
    table_id = Column(Integer, ForeignKey('table.id'), nullable=True, default=None)
    table = relationship("Table")

    bakery_id = Column(Integer, ForeignKey('bakery.id'), nullable=True)
    bakery = relationship("Bakery")

    data_registrate = Column(DateTime, nullable=True)

    order_id = Column(Integer, ForeignKey('order.id'), nullable=True, default=None)
    order = relationship("Order")
    status_registrate = Column(Enum(StatusOrder), default=StatusOrder.waiting_for_confirmation)

    start_time = Column(Integer, nullable=True, default=0)
    end_time = Column(Integer, nullable=True, default=0)



