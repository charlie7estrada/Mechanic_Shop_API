from app.blueprints.mechanics import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Mechanic, db, ServiceTickets
from app.utils.util import encode_token, token_required
from sqlalchemy import select 
from sqlalchemy.exc import IntegrityError

# login route
@mechanics_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == email) 
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

@mechanics_bp.route('', methods=['POST'])
def create_mechanic():
    try:
        data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    

    new_mechanic = Mechanic(**data) #Creating User object
    db.session.add(new_mechanic)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "email is taken"}), 400
    return mechanic_schema.jsonify(new_mechanic), 201

@mechanics_bp.route('', methods=['GET'])
def read_mechanics():
    mechanics = db.session.query(Mechanic).all()
    return mechanics_schema.jsonify(mechanics), 200

@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def read_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"message": "mechanic not found"}), 404
    
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('<int:mechanic_id>', methods=['PUT'])
@token_required
def update_mechanic(mechanic_id=None, user_id=None):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic: 
        return jsonify({"message": "mechanic not found"}), 404 
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route('<int:mechanic_id>', methods=['DELETE'])
@token_required
def delete_mechanic(mechanic_id=None, user_id=None):
    mechanic = db.session.get(Mechanic, mechanic_id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted user {mechanic_id}"}), 200

@mechanics_bp.route("/my-tickets", methods=['GET'])
@token_required
def my_tickets(mechanic_id=None, user_id=None):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    if len(mechanic.tickets) <= 0:
        return jsonify({"message": "No tickets found for this mechanic"}), 404
    output = []
    for ticket in mechanic.tickets:
        print(ticket.id, ticket.service_desc, ticket.service_date)
        output.append({
            "id": ticket.id,
            "VIN": ticket.VIN,
            "service_date": ticket.service_date.isoformat() if ticket.service_date else None,
            "service_desc": ticket.service_desc,
            "customer_id": ticket.customer_id
        })
    return jsonify(output), 200