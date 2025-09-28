from app.blueprints.service_tickets import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import ServiceTickets, Mechanic, Inventory, db

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

# add a single part to an existing Service Ticket
@service_tickets_bp.route("/<int:ticket_id>/add-part", methods=["POST"])
def add_part_to_ticket(ticket_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    data = request.get_json()
    part_id = data.get("part_id")
    if not part_id:
        return jsonify({"message": "part_id is required"}), 400

    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"message": "Part not found"}), 404

    if part not in ticket.parts:
        ticket.parts.append(part)
        db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200