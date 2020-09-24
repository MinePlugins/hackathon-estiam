from app import db, ma
from marshmallow_sqlalchemy import ModelSchema, fields
from marshmallow_sqlalchemy.fields import Nested


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)


class RegionSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, convert_unicode=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    region = db.relationship("Region", backref="regions")


class CountrySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "region")
    region = ma.Nested(RegionSchema)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship("Country", backref="countrys")


class LocationSchema(ma.Schema):
    class Meta:
        fields = ("id", "address", "postal_code", "city", "state", "country")
    country = fields.Nested(lambda: CountrySchema)


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship("Location", backref="locations")
    warehouse = db.relationship("Inventory", back_populates="warehouse")


class WarehouseSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "location")
    location = fields.Nested(lambda: LocationSchema)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    hire_date = db.Column(db.TIMESTAMP, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'), index=True)
    manager = db.relationship(lambda: Employee, remote_side=id, backref='managers')


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "phone", "hire_date", "manager")
    manager = fields.Nested(lambda: EmployeeSchema)


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class ProductCategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    standard_cost = db.Column(db.Float)
    list_cost = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    category = db.relationship("ProductCategory", backref="category")
    order_item = db.relationship("OrderItem", back_populates="product")
    inventory = db.relationship("Inventory", back_populates="product")


class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "standard_cost", "category")
    category = fields.Nested(lambda: ProductCategorySchema)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    website = db.Column(db.String)
    credit_limit = db.Column(db.Float)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship("Location", backref="customer")
    contact = db.relationship("Contact", back_populates="customer")
    order = db.relationship("Order", back_populates="customer")

# CusomerSchema
class CustomerSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "address", "website", "credit_limit")

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship("Customer", back_populates="contact")

# ContactSchema
class ContactSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "phone", "customer")
    customer = fields.Nested(lambda: ContactSchema)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship("Customer", back_populates="order")
    salesman_id = db.Column(db.Integer, db.ForeignKey('employee.id'), index=True)
    salesman = db.relationship(Employee, backref='employee')
    order_date = db.Column(db.TIMESTAMP, nullable=False)
    status = db.Column(db.String, nullable=False)
    order_item = db.relationship("OrderItem", back_populates="order")

# OrderSchema
class OrderSchema(ma.Schema):
    class Meta:
        fields = ("id", "salesman", "order_date", "status")
    salesman = fields.Nested(lambda: OrderSchema) 

class OrderItem(db.Model):
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    product = db.relationship(Product, back_populates='order_item')
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    order = db.relationship(Order, back_populates='order_item')

# OrderItemSchema
class OrderItemSchema(ma.Schema):
    class Meta:
        fields = ("id", "quantity", "unit_price", "product", "order")

    product = fields.Nested(lambda: ProductSchema)
    order = fields.Nested(lambda: OrderSchema)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship(Product, back_populates='inventory')
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    warehouse = db.relationship(Warehouse, back_populates='warehouse')

# InventorySchema
class InventorySchema(ma.Schema):
    class Meta: 
        fields = ("id", "quantity")
