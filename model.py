from app import db, ma
from marshmallow_sqlalchemy import ModelSchema


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)


class RegionSchema(ModelSchema):
    class Meta:
        model = Region


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    region = db.relationship("Region", backref="regions")


class CountrySchema(ModelSchema):
    class Meta:
        model = Country


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship("Country", backref="countrys")


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship("Location", backref="locations")
    warehouse = db.relationship("Inventory", back_populates="warehouse")


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    hire_date = db.Column(db.TIMESTAMP, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'), index=True)
    manager = db.relationship(lambda: Employee, remote_side=id, backref='managers')


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    standard_cost = db.Column(db.Float)
    list_cost = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    category = db.relationship("ProductCategory", backref="categorys")
    order_item = db.relationship("OrderItem", back_populates="product")
    inventory = db.relationship("Inventory", back_populates="product")


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    website = db.Column(db.String)
    credit_limit = db.Column(db.Float)
    contact = db.relationship("Contact", back_populates="customer")
    order = db.relationship("Order", back_populates="customer")


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship("Customer", back_populates="contact")


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship("Customer", back_populates="order")
    salesman_id = db.Column(db.Integer, db.ForeignKey('employee.id'), index=True)
    salesman = db.relationship(Employee, backref='employee')
    order_date = db.Column(db.TIMESTAMP, nullable=False)
    status = db.Column(db.String, nullable=False)
    order_item = db.relationship("OrderItem", back_populates="order")


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship(Product, back_populates='order_item')
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship(Order, back_populates='order_item')


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship(Product, back_populates='inventory')
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    warehouse = db.relationship(Warehouse, back_populates='warehouse')
