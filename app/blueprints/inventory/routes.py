from app.blueprints.inventory import inventory_bp
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import Inventory, db
from .schemas import inventory_schema, inventories_schema

# Create a new inventory item
@inventory_bp.route('', methods=["POST"])
def create_inventory_item():
    try:
        data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_item = Inventory(**data)
    db.session.add(new_item)
    db.session.commit()
    return inventory_schema.jsonify(new_item), 201


# Read all inventory items
@inventory_bp.route('', methods=["GET"])
def get_inventory_items():
    items = db.session.query(Inventory).all()
    return inventories_schema.jsonify(items), 200


# Read single inventory item
@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({"message": "Item not found"}), 404
    return inventory_schema.jsonify(item), 200


# Update inventory item
@inventory_bp.route("/<int:item_id>", methods=["PUT"])
def update_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    try:
        data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in data.items():
        setattr(item, key, value)

    db.session.commit()
    return inventory_schema.jsonify(item), 200


# Delete inventory item
@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted item {item_id}"}), 200