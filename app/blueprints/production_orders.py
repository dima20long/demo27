"""Blueprint для заказов на производство."""
import uuid
from datetime import date
from flask import Blueprint, request, jsonify
from app.models import ProductionOrder, ProductionOrderItem
from app.extensions import db

production_orders_bp = Blueprint("production_orders", __name__)


@production_orders_bp.route("/", methods=["GET"])
def list_production_orders():
    """Список заказов на производство."""
    orders = db.session.execute(db.select(ProductionOrder)).scalars().all()
    return jsonify({
        "production_orders": [
            {
                "order_id": str(o.order_id),
                "order_number": o.order_number,
                "order_date": o.order_date.isoformat() if o.order_date else None,
                "subdivision": o.subdivision,
                "client_id": str(o.client_id) if o.client_id else None,
                "total_amount": float(o.total_amount) if o.total_amount else 0,
                "status": o.status,
                "created_at": o.created_at.isoformat() if o.created_at else None,
            }
            for o in orders
        ]
    }), 200


@production_orders_bp.route("/", methods=["POST"])
def create_production_order():
    """Создание заказа на производство."""
    data = request.get_json()
    required_fields = ["order_number", "order_date"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({
            "error": "Bad Request",
            "message": "Укажите order_number, order_date",
        }), 400

    order_date = date.fromisoformat(data["order_date"]) if isinstance(data["order_date"], str) else data["order_date"]

    client_uuid = None
    if data.get("client_id"):
        try:
            client_uuid = uuid.UUID(data["client_id"])
        except (ValueError, AttributeError):
            return jsonify({"error": "Bad Request", "message": "Неверный формат UUID"}), 400

    new_order = ProductionOrder(
        order_number=data["order_number"],
        order_date=order_date,
        subdivision=data.get("subdivision"),
        client_id=client_uuid,
        status=data.get("status", "Новый"),
    )
    db.session.add(new_order)
    db.session.flush()

    if "items" in data:
        for item_data in data["items"]:
            try:
                product_uuid = uuid.UUID(item_data["product_id"])
            except (ValueError, AttributeError):
                continue

            item = ProductionOrderItem(
                production_order=new_order,
                product_id=product_uuid,
                quantity=item_data.get("quantity", 1),
                completed_quantity=item_data.get("completed_quantity", 0),
                unit_price=item_data.get("unit_price", 0),
                total_price=item_data.get("total_price", 0),
            )
            db.session.add(item)

    db.session.commit()

    return jsonify({
        "message": "Заказ на производство создан",
        "order_id": str(new_order.order_id),
    }), 201


@production_orders_bp.route("/<order_id>", methods=["GET"])
def get_production_order(order_id):
    """Получение заказа на производство по ID."""
    try:
        order_uuid = uuid.UUID(order_id)
    except (ValueError, AttributeError):
        return jsonify({"error": "Bad Request", "message": "Неверный формат UUID"}), 400

    order = db.session.get(ProductionOrder, order_uuid)
    if not order:
        return jsonify({"error": "Not Found", "message": "Заказ на производство не найден"}), 404

    items = [
        {
            "order_item_id": str(i.order_item_id),
            "product_id": str(i.product_id),
            "quantity": float(i.quantity),
            "completed_quantity": float(i.completed_quantity),
            "unit_price": float(i.unit_price),
            "total_price": float(i.total_price),
        }
        for i in order.items
    ]

    return jsonify({
        "order_id": str(order.order_id),
        "order_number": order.order_number,
        "order_date": order.order_date.isoformat() if order.order_date else None,
        "subdivision": order.subdivision,
        "client_id": str(order.client_id) if order.client_id else None,
        "total_amount": float(order.total_amount) if order.total_amount else 0,
        "status": order.status,
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "items": items,
    }), 200


@production_orders_bp.route("/<order_id>", methods=["PUT"])
def update_production_order(order_id):
    """Обновление заказа на производство."""
    try:
        order_uuid = uuid.UUID(order_id)
    except (ValueError, AttributeError):
        return jsonify({"error": "Bad Request", "message": "Неверный формат UUID"}), 400

    order = db.session.get(ProductionOrder, order_uuid)
    if not order:
        return jsonify({"error": "Not Found", "message": "Заказ на производство не найден"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request", "message": "Нет данных"}), 400

    if "order_number" in data:
        order.order_number = data["order_number"]
    if "order_date" in data:
        od = data["order_date"]
        order.order_date = date.fromisoformat(od) if isinstance(od, str) else od
    if "subdivision" in data:
        order.subdivision = data["subdivision"]
    if "status" in data:
        order.status = data["status"]
    if "client_id" in data:
        if data["client_id"]:
            try:
                order.client_id = uuid.UUID(data["client_id"])
            except (ValueError, AttributeError):
                return jsonify({"error": "Bad Request", "message": "Неверный формат UUID"}), 400
        else:
            order.client_id = None

    db.session.commit()

    return jsonify({
        "message": "Заказ на производство обновлён",
        "order_id": str(order.order_id),
    }), 200


@production_orders_bp.route("/<order_id>", methods=["DELETE"])
def delete_production_order(order_id):
    """Удаление заказа на производство."""
    try:
        order_uuid = uuid.UUID(order_id)
    except (ValueError, AttributeError):
        return jsonify({"error": "Bad Request", "message": "Неверный формат UUID"}), 400

    order = db.session.get(ProductionOrder, order_uuid)
    if not order:
        return jsonify({"error": "Not Found", "message": "Заказ на производство не найден"}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": "Заказ на производство удалён"}), 200
