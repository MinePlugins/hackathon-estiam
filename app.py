
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template
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
from sqlalchemy import func

app = Flask(__name__, static_folder="./static/build/static", template_folder="./static/build")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:undeuxtrois@192.168.10.176:5432/hack"
app.config.update({
    'SECRET_KEY': 'kdjfoijdzoxksdpdlpdskdoskdloskqq',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_OPENID_REALM': 'https://hack.cournut.ovh/oidc_callback'
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

@app.route('/', methods=['GET'])
@oidc.require_login
def index():
    return render_template('index.html')


@app.route('/<path:path>', methods=['GET'])
@oidc.require_login
def any_root_path(path):
    return render_template('index.html')


@app.route('/api/products')
@oidc.require_login
def get_products():
    products = Product.query.all()
    schema = ProductSchema(many=True)
    return schema.jsonify(products)


# Products route by id 
@app.route("/api/product/<id>")
@oidc.require_login
def get_productId(id):
    productId = Product.query.filter_by(id=id).first()
    schema = ProductSchema()
    if productId:
        return schema.jsonify(productId)
    else:
        return '<h1>Product ' + id + ' does not exist</h1>'


@app.route('/api/country_code/<code>')
@oidc.require_login
def get_country_by_code(code):
    country = pycountry.countries.get(alpha_2=code)
    print(country.name)
    data = Country.query.filter_by(name=country.name).first()
    print(data)
    schema = CountrySchema()
    return schema.jsonify(data)


# Product Count Query
@app.route("/api/product/count")
@oidc.require_login
def get_count_product():
    productCount = db.session.query(db.func.count(Product.id)).scalar()
    return jsonify(ProductsNumbers=productCount)


@app.route('/api/locations')
@oidc.require_login
def get_locations():
    locations = Location.query.all()
    schema = LocationSchema(many=True)
    return schema.jsonify(locations)


# Location route by id 
@app.route("/api/location/<id>")
@oidc.require_login
def get_locationId(id):
    locationId = Location.query.filter_by(id=id).first()
    schema = LocationSchema()
    if locationId:
        return schema.jsonify(locationId)
    else:
        return '<>Location ' + id + ' does not exist</>'


@app.route('/api/warehouses')
@oidc.require_login
def get_warehouses():
    warehouses = Warehouse.query.all()
    schema = WarehouseSchema(many=True)
    return schema.jsonify(warehouses)


@app.route("/api/warehouses/<country_id>")
def get_warehouse_by_country(country_id):
    loc = Location.query.filter_by(country_id=country_id).all()
    id_list = []
    for i in loc:
        id_list.append(i.id)
    warehouses = Warehouse.query.filter(Warehouse.location_id.in_(id_list)).all()
    schema = WarehouseSchema(many=True)
    return schema.jsonify(warehouses)

# Warehouse route by id 
@app.route("/api/warehouse/<id>")
@oidc.require_login
def get_warehouseId(id):
    warehouseId = Warehouse.query.filter_by(id=id).first()
    schema = WarehouseSchema()
    if warehouseId:
        return schema.jsonify(warehouseId)
    else:
        return '<h1>Warehouse ' + id + ' does not exist</h1>'


@app.route('/api/employees')
@oidc.require_login
def get_employees():
    employees = Employee.query.all()
    schema = EmployeeSchema(many=True)
    return schema.jsonify(employees)


# Employee route by id  
@app.route("/api/employee/<id>")
@oidc.require_login
def get_employeeId(id):
    employeeId = Employee.query.filter_by(id=id).first()
    schema = EmployeeSchema()
    if employeeId:
        return schema.jsonify(employeeId)
    else:
        return '<h1>Employee ' + id + ' does not exist</h1>'


# Employee Count Query
@app.route('/api/employee/count')
@oidc.require_login
def get_count_employee():
    employeeCount = db.session.query(db.func.count(Employee.id)).scalar()
    return jsonify(EmployeeNumbers = employeeCount)


@app.route('/api/regions')
@oidc.require_login
def get_regions():
    regions = Region.query.all()
    schema = RegionSchema(many=True)
    return schema.jsonify(regions)


# Region route by id 
@app.route("/api/region/<id>")
@oidc.require_login
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
@oidc.require_login
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
@oidc.require_login
def get_countries():
    countries = Country.query.all()
    schema = CountrySchema(many=True)
    return schema.jsonify(countries)


# Country route by id 
@app.route("/api/country/<id>")
@oidc.require_login
def get_countryId(id):
    countryId = Country.query.filter_by(id=id).first()
    schema = CountrySchema()
    if countryId:
        return schema.jsonify(countryId)
    else:
        return '<h1>CountryId ' + id + ' does not exist</h1>'


# Customer route 
@app.route('/api/customers')
@oidc.require_login
def get_customers():
    customers = Customer.query.all()
    schema = CustomerSchema(many=True)
    return schema.jsonify(customers)


# Customer route by id 
@app.route("/api/customer/<id>")
@oidc.require_login
def get_customerId(id):
    customerId = Customer.query.filter_by(id=id).first()
    schema = CustomerSchema()
    if customerId:
        return schema.jsonify(customerId)
    else:
        return '<h1>Customer ' + id + ' does not exist</h1>' 


# Customer Count Query 
@app.route('/api/customer/count')
@oidc.require_login
def get_count_customer():
    customerCount = db.session.query(db.func.count(Customer.id)).scalar()
    return jsonify(CustomersNumbers = customerCount)


# Contact route
@app.route('/api/contacts')
@oidc.require_login
def get_contacts():
    contacts = Contact.query.all()
    schema = ContactSchema(many=True)
    return schema.jsonify(contacts)


# Contact route by id
@app.route("/api/contact/<id>")
@oidc.require_login
def get_contactId(id):
    contactId = Contact.query.filter_by(id=id).first()
    schema = ContactSchema()
    if contactId:
        return schema.jsonify(contactId)
    else:
        return '<h1>Contact ' + id + ' does not exist</h1>' 


# Order route
@app.route('/api/orders')
@oidc.require_login
def get_orders():
    orders = Order.query.all()
    schema = OrderSchema(many=True)
    return schema.jsonify(orders)


# Order route by id 
@app.route("/api/order/<id>")
@oidc.require_login
def get_orderId(id):
    orderId = Order.query.filter_by(id=id).first()
    schema = OrderSchema()
    if orderId:
        return schema.jsonify(orderId)
    else:
        return '<h1>Order ' + id + ' does not exist</h1>'


# OrderItems route
@app.route('/api/orderItems')
@oidc.require_login
def get_orderItems():
    orderItems = OrderItem.query.all()


@app.route('/api/order_items/<country_id>')
def get_order_items_by_country(country_id):
    loc = Location.query.filter_by(country_id=country_id).all()
    id_list = []
    for i in loc:
        id_list.append(i.id)
    customer = Customer.query.filter(Customer.location_id.in_(id_list))
    id_list = []
    for i in customer:
        id_list.append(i.id)
    order = Order.query.filter(Order.customer_id.in_(id_list))
    id_list = []
    for i in order:
        id_list.append(i.id)
    orderItems = db.session.query(ProductCategory.name, func.sum(OrderItem.quantity)).join(OrderItem.product).join(Product.category)\
        .filter(OrderItem.order_id.in_(id_list))\
        .group_by(ProductCategory.name)\
        .all()

    # Renvoi un tab [] vide ??
    return jsonify(orderItems)

# OrderItems route
@app.route('/api/order_items')
def get_order_items():
    orderItems = db.session.query(func.date_trunc('year', Order.order_date),func.sum(OrderItem.quantity)).group_by(func.date_trunc('year', Order.order_date)).join(Order).all()
    schema = OrderItemSchema(many=True)
    # Renvoi un tab [] vide ??
    return jsonify(orderItems)


# OrderItem route by id 
@app.route("/api/orderItem/<id>")
@oidc.require_login
def get_orderItemId(id):
    orderItemId = OrderItem.query.filter_by(id=id).first()
    schema = OrderItemSchema()
    if orderItemId:
        return schema.jsonify(orderItemId)
    else:
        return '<h1>OrderItem ' + id + ' does not exist</h1>'


# Inventory route
@app.route('/api/inventorys')
@oidc.require_login
def get_inventorys():
    inventorys = Inventory.query.all()
    schema = InventorySchema(many=True)
    return schema.jsonify(inventorys)


# Invetory route by id 
@app.route("/api/inventory/<id>")
@oidc.require_login
def get_inventoryId(id):
    inventoryId = Inventory.query.filter_by(id=id).first()
    schema = InventorySchema()
    if inventoryId:
        return schema.jsonify(inventoryId)
    else:
        return '<h1>InventoryId ' + id + ' does not exist</h1>'


@app.route('/api/logout')
def logout():
    oidc.logout()
    return jsonify(message="You have been logged out")


@app.route('/generate_data')
@oidc.require_login
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
