
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_marshmallow import Marshmallow
from faker import Faker
from collections import namedtuple
from flask_oidc import OpenIDConnect
from flask_cors import CORS
import gettext
import pycountry
import random
import json
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:undeuxtrois@lol.cournut.ovh:5432/hack"
app.config.update({
    'SECRET_KEY': 'kdjfoijdzoxksdpdlpdskdoskdloskqq',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_OPENID_REALM': 'http://localhost:5000/oidc_callback'
})
oidc = OpenIDConnect(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
fake = Faker()
from model import *

db.create_all()

def convert(dictionary):
    return namedtuple('GenericDict', dictionary.keys())(**dictionary)



@app.route('/')
def hello_world():
    if oidc.user_loggedin:
        return ('Hello, %s, <a href="/private">See private</a> '
                '<a href="/logout">Log out</a>') % \
            oidc.user_getfield('email')
    else:
        return 'Welcome anonymous, <a href="/private">Log in</a>'


@app.route('/api/products')
def get_products():
    products = Product.query.all()
    schema = ProductSchema(many=True)
    return schema.jsonify(products)


# test products route by id 
@app.route("/api/product/<id>")
def get_productId(id):
    productId = Product.query.filter_by(id=id).first()
    schema = ProductSchema()
    if productId:
        return schema.jsonify(productId)
    else:
        return '<h1>Product ' + id + ' does not exist</h1>'

@app.route('/api/country_code/<code>')
def get_country_by_code(code):
    country = pycountry.countries.get(alpha_2=code)
    print(country.name)
    data = Country.query.filter_by(name=country.name).first()
    print(data)
    schema = CountrySchema()
    return schema.jsonify(data)


@app.route('/api/locations')
def get_locations():
    locations = Location.query.all()
    schema = LocationSchema(many=True)
    return schema.jsonify(locations)

# test location route by id 
@app.route("/api/location/<id>")
def get_locationId(id):
    locationId = Location.query.filter_by(id=id).first()
    schema = LocationSchema()
    if locationId:
        return schema.jsonify(locationId)
    else:
        return '<h1>Location ' + id + ' does not exist</h1>'


@app.route('/api/warehouses')
def get_warehouses():
    warehouses = Warehouse.query.all()
    schema = WarehouseSchema(many=True)
    return schema.jsonify(warehouses)

# test warehouse route by id 
@app.route("/api/warehouse/<id>")
def get_warehouseId(id):
    warehouseId = Warehouse.query.filter_by(id=id).first()
    schema = WarehouseSchema()
    if warehouseId:
        return schema.jsonify(warehouseId)
    else:
        return '<h1>Warehouse ' + id + ' does not exist</h1>'

@app.route('/api/employees')
def get_employees():
    employees = Employee.query.all()
    schema = EmployeeSchema(many=True)
    return schema.jsonify(employees)

# test employee route by id  
@app.route("/api/employee/<id>")
def get_employeeId(id):
    employeeId = Employee.query.filter_by(id=id).first()
    schema = EmployeeSchema()
    if employeeId:
        return schema.jsonify(employeeId)
    else:
        return '<h1>Employee ' + id + ' does not exist</h1>'

@app.route('/api/regions')
def get_regions():
    regions = Region.query.all()
    schema = RegionSchema(many=True)
    return schema.jsonify(regions)

# test Region route by id 
@app.route("/api/region/<id>")
def get_regionId(id):
    regionId = Region.query.filter_by(id=id).first()
    schema = RegionSchema()
    if regionId:
        return schema.jsonify(regionId)
    else:
        return '<h1>Region ' + id + ' does not exist</h1>'

def search_in_list(pays, list):
    for i,v in enumerate(list):
        if pays in v:
            return i

    return False


@app.route('/api/global_income')
def get_global_income():
    order_item = OrderItem.query.all()
    list_pays = []
    for i in order_item:

        ca = 0
        for a in i.order.order_item:
            ca += (a.quantity*a.unit_price)
        val = search_in_list(i.order.customer.location.country.name, list_pays)
        if not val and val is not 0:
            list_pays.append([i.order.customer.location.country.name, ca])
        else:
            list_pays[val][1] += ca
    return jsonify(list_pays)


@app.route('/api/countries')
def get_countries():
    countries = Country.query.all()
    schema = CountrySchema(many=True)
    return schema.jsonify(countries)

# test Country route by id 
@app.route("/api/country/<id>")
def get_countryId(id):
    countryId = Country.query.filter_by(id=id).first()
    schema = CountrySchema()
    if countryId:
        return schema.jsonify(countryId)
    else:
        return '<h1>CountryId ' + id + ' does not exist</h1>'

#Customer route 
@app.route('/api/customers')
def get_customers():
    customers = Customer.query.all()
    schema = CustomerSchema(many=True)
    return schema.jsonify(customers)

# test Customer route by id 
@app.route("/api/customer/<id>")
def get_customerId(id):
    customerId = Customer.query.filter_by(id=id).first()
    schema = CustomerSchema()
    if customerId:
        return schema.jsonify(customerId)
    else:
        return '<h1>Customer ' + id + ' does not exist</h1>' 

# Contact route
@app.route('/api/contacts')
def get_contacts():
    contacts = Contact.query.all()
    schema = ContactSchema(many=True)
    return schema.jsonify(contacts)

# test contact route by id
@app.route("/api/contact/<id>")
def get_contactId(id):
    contactId = Contact.query.filter_by(id=id).first()
    schema = ContactSchema()
    if contactId:
        return schema.jsonify(contactId)
    else:
        return '<h1>Contact ' + id + ' does not exist</h1>' 

# Order route
@app.route('/api/orders')
def get_orders():
    orders = Order.query.all()
    schema = OrderSchema(many=True)
    return schema.jsonify(orders)

# test Order route by id 
@app.route("/api/order/<id>")
def get_orderId(id):
    orderId = Order.query.filter_by(id=id).first()
    schema = OrderSchema()
    if orderId:
        return schema.jsonify(orderId)
    else:
        return '<h1>Order ' + id + ' does not exist</h1>'

# OrderItems route
@app.route('/api/orderItems')
def get_orderItems():
    orderItems = OrderItem.query.all()
    schema = OrderItemSchema(many=True)
    # Renvoi un tab [] vide ??
    return schema.jsonify(orderItems)

# test OrderItem route by id 
@app.route("/api/orderItem/<id>")
def get_orderItemId(id):
    orderItemId = OrderItem.query.filter_by(id=id).first()
    schema = OrderItemSchema()
    if orderItemId:
        return schema.jsonify(orderItemId)
    else:
        return '<h1>OrderItem ' + id + ' does not exist</h1>'

# Inventory route
@app.route('/api/inventorys')
def get_inventorys():
    inventorys = Inventory.query.all()
    schema = InventorySchema(many=True)
    return schema.jsonify(inventorys)

# test Invetory route by id 
@app.route("/api/inventory/<id>")
def get_inventoryId(id):
    inventoryId = Inventory.query.filter_by(id=id).first()
    schema = InventorySchema()
    if inventoryId:
        return schema.jsonify(inventoryId)
    else:
        return '<h1>InventoryId ' + id + ' does not exist</h1>'

@app.route('/private')
@oidc.require_login
def hello_me():
    info = oidc.user_getinfo(['email', 'clientId'])
    return ('Hello, %s (%s)! <a href="/">Return</a>' %
            (info.get('email'), info.get('clientId')))


@app.route('/logout')
def logout():
    oidc.logout()
    return 'Hi, you have been logged out! <a href="/">Return</a>'


@app.route('/generate_data')
def generate():

    try:
        for i in range(10):
            user = Employee(
                            first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            email=fake.email(),
                            phone=fake.phone_number(),
                            hire_date=fake.date(),
                            )

            db.session.add(user)
            db.session.commit()
    except Exception as e:
        pass

    try:
        for i in range(10):
            country = Country.query.order_by(func.random()).first()

            loc = Location(
                address=fake.address(),
                postal_code=fake.postcode(),
                city=fake.city(),
                state=fake.state(),
                country=country
            )
            db.session.add(loc)
            db.session.commit()
    except Exception as e:
        pass
    try:
        for i in range(100):
            print("CUSTOMER")
            loc = Location.query.order_by(func.random()).first()

            customer = Customer(
                name=fake.name(),
                address=fake.address(),
                website="google.fr",
                credit_limit=fake.pyfloat(positive=True),
                location=loc

            )
            db.session.add(customer)
            contact = Contact(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.phone_number(),
                customer=customer,

            )
            db.session.add(contact)
            db.session.commit()
    except Exception as e:
        print(e)
    try:
        for i in range(10):
            loc = Location.query.order_by(func.random()).first()

            ware = Warehouse(
                name=fake.word(),
                location=loc
            )
            db.session.add(ware)
            db.session.commit()
    except Exception as e:
        pass

    try:
        for i in range(10):
            ware = Warehouse.query.order_by(func.random()).first()
            pro = Product.query.order_by(func.random()).first()

            inv = Inventory(
                quantity=fake.pyint(),
                warehouse=ware,
                product=pro,
            )
            db.session.add(inv)
            db.session.commit()
    except Exception as e:
        print(e)
    try:
        for i in range(10):
            cust = Customer.query.order_by(func.random()).first()
            emp = Employee.query.order_by(func.random()).first()

            inv = Order(
                customer=cust,
                salesman=emp,
                order_date=fake.iso8601(),
                status="Ended",
            )
            db.session.add(inv)
            db.session.commit()
    except Exception as e:
        print(e)
    try:
        for i in range(10):
            productcategory = ProductCategory(name=fake.word())
            db.session.add(productcategory)
            db.session.commit()
    except Exception as e:
        print(e)
    try:
        for i in range(10):
            category = ProductCategory.query.order_by(func.random()).first()
            product = Product(
                name=fake.word(),
                description=fake.text(),
                standard_cost=fake.pyfloat(positive=True),
                list_cost=fake.pyfloat(positive=True),
                category=category
            )
            db.session.add(product)
            db.session.commit()
    except Exception as e:
        print(e)
    try:
        eu = Region(name="Europe")
        asia = Region(name="Asia")
        usa = Region(name="Americas")
        africa = Region(name="Middle East and Africa")
        db.session.add(eu)
        db.session.add(asia)
        db.session.add(usa)
        db.session.add(africa)
        for i in ['France', 'Belgique', 'Suisse', 'Allemagne']:
            db.session.add(Country(name=i, region=eu))
            db.session.commit()
    except Exception as e:
        print(e)
    return jsonify(status="ok")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
