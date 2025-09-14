# Service_Ticket: Create the following routes to Create service tickets, assign mechanics, remove mechanics, and retrieve all service tickets.

#     POST '/': Pass in all the required information to create the service_ticket.
#     PUT '/<ticket_id>/assign-mechanic/<mechanic-id>: Adds a relationship between a service ticket and the mechanics. (Reminder: use your relationship attributes! They allow you the treat the relationship like a list, able to append a Mechanic to the mechanics list).
#     PUT '/<ticket_id>/remove-mechanic/<mechanic-id>: Removes the relationship from the service ticket and the mechanic.
#     GET '/': Retrieves all service tickets.

from app.blueprints.service_tickets import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import ServiceTickets, Mechanic, db

@service_tickets_bp.route('', methods=['POST'])
def create_service_ticket():
    try:
        data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    

    new_service_ticket = ServiceTickets(**data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201


@service_tickets_bp.route('<service_tickets_id>/assign-mechanic/<mechanic_id>', methods=['PUT'])
def assign_mechanic(service_tickets_id, mechanic_id):
    ticket = db.session.get(ServiceTickets, service_tickets_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket: #Checking if I got a service ticket
        return jsonify({"message": "service ticket not found"}), 404  
    if not mechanic:
        return jsonify({"message": "mechanic not found"}), 404
    
    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

@service_tickets_bp.route('<ticket_id>/assign-mechanic/<mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"message": "Service ticket not found"}), 404
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('', methods=['GET'])
def read_service_tickets():
    tickets = db.session.query(ServiceTickets).all()
    return service_tickets_schema.jsonify(tickets), 200

