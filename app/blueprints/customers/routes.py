from app.blueprints.customers import customers_bp
from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customer, db
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required
from sqlalchemy import select 

# login route
@customers_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = request.json
        email = credentials['email']
        password = credentials['password']
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting username and password'}), 400
    
    query = select(Customer).where(Customer.email == email) 
    user = db.session.execute(query).scalar_one_or_none() #Query user table for a user with this email

    if user and user.password == password: #if we have a user associated with the email, validate the password
        auth_token = encode_token(user.id)

        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'messages': "Invalid email or password"}), 401

#CREATE Customer ROUTE
@customers_bp.route('', methods=['POST']) #route servers as the trigger for the function below.
@limiter.limit("3 per hour")  #A client can only attempt to make 3 users per hour
def create_customer():
    try:
        data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 #Returning the error as a response so my client can see whats wrong.
    

    new_customer = Customer(**data) #Creating User object
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

#Read customers
@customers_bp.route('', methods=['GET']) #Endpoint to get user information
@cache.cached(timeout=60) #stores to a cache, so when you make any subsequent calls within 60 seconds, it will reach into the cache instead. So if you were to test these calls, the first one would be slower than the ones following.
def read_customers():
    customers = db.session.query(Customer).all()
    return customers_schema.jsonify(customers), 200

#Read Individual customer - Using a Dynamic Endpoint
@customers_bp.route('<int:customer_id>', methods=['GET'])
def read_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    return customer_schema.jsonify(customer), 200

#Search for a customer based on their email
@customers_bp.route('/search', methods=['GET'])
def search_email():
    email = request.args.get('email')  # Accessing the query parameters from the URL
    
    if email:
        customer = db.session.query(Customers).where(Customers.email.like(f'%{email}%')).all()
    
    return customers_schema.jsonify(customer), 200

#Delete a customer
@customers_bp.route('<int:customer_id>', methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted user {customer_id}"}), 200

#Update a customer
@customers_bp.route('<int:customer_id>', methods=['PUT'])
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id) #Query for our user to update

    if not customer: #Checking if I got a customer
        return jsonify({"message": "customer not found"}), 404  #if not return error message
    
    try:
        customer_data = customer_schema.load(request.json) #Validating updates
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in customer_data.items(): #Looping over attributes and values from user data dictionary
        setattr(customer, key, value) # setting Object, Attribute, Value to replace

    db.session.commit()
    return customer_schema.jsonify(customer), 200
