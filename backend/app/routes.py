# backend/app/routes.py
from .models import InventoryReading
from flask import Blueprint, jsonify, request, render_template
from flask import redirect, url_for
# استيراد الدالة الجديدة predict_stock_needs
from .services import get_all_products_service, get_product_by_id_service, create_product_service, update_product_weight_service, delete_product_service, predict_stock_needs 
from .services import process_sensor_reading
from datetime import datetime
products_bp = Blueprint('products', __name__)
@products_bp.route("/", methods=["GET"])
def home():
    return render_template("login.html")

@products_bp.route("/dashboard", methods=["GET"])
def dashboard_page():
    return render_template("products.html")
# ------------------------------------------------------------------
# الـ Routes الحالية (CRUD Operations)
# ------------------------------------------------------------------

@products_bp.route('/api/products', methods=['GET'])
def get_all_products():
    products = get_all_products_service()
    if "error" in products:
        return jsonify({"message": "Error fetching products", "error": products["error"]}), 500
    return jsonify(products), 200

@products_bp.route('/api/products/<int:item_id>', methods=['GET'])
def get_product_by_id(item_id):
    product = get_product_by_id_service(item_id)
    if "error" in product:
        return jsonify({"message": "Error fetching product", "error": product["error"]}), 500
    if product is None:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(product), 200

@products_bp.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = create_product_service(data)
    if "error" in new_product:
        return jsonify({"message": "Error creating product", "error": new_product["error"]}), 500
    return jsonify(new_product), 201

@products_bp.route('/api/products/<int:item_id>', methods=['PUT'])
def update_product_weight(item_id):
    data = request.get_json()
    new_total_weight = data.get('total_weight')
    
    updated_product = update_product_weight_service(item_id, new_total_weight)
    
    if "error" in updated_product:
        return jsonify({"message": "Error updating product", "error": updated_product["error"]}), 500
    if updated_product is None:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(updated_product), 200

@products_bp.route('/api/products/<int:item_id>', methods=['DELETE'])
def delete_product(item_id):
    result = delete_product_service(item_id)
    if "error" in result:
        return jsonify({"message": "Error deleting product", "error": result["error"]}), 500
    if "Product not found" in result["message"]:
        return jsonify(result), 404
    return jsonify(result), 200

# ------------------------------------------------------------------
# الـ Route الجديدة للذكاء الاصطناعي (Predictive Analytics)
# ------------------------------------------------------------------
@products_bp.route('/api/predict/<int:item_id>', methods=['GET'])
def get_predictions(item_id):
    try:
        days = request.args.get('days', default=7, type=int)

        result, code = predict_stock_needs(item_id, days)
        return jsonify(result), code

    except Exception as e:
        return jsonify({"message": "An error occurred while getting predictions", "error": str(e)}), 500

# @products_bp.route('/api/sensor-readings', methods=['POST'])
# def receive_sensor_readings():
#     """
#     POST /api/sensor-readings
#     يستقبل بيانات المحاكي/الحساسات مثل: rfid, weight, timestamp
#     """
#     data = request.get_json(silent=True) or {}

#     rfid = data.get("rfid")
#     weight = data.get("weight")
#     timestamp = data.get("timestamp") or datetime.utcnow().isoformat()

#     # تحقق بسيط (مهم عشان المشرفة + يمنع قيم فاضية)
#     if rfid is None or weight is None:
#         return jsonify({
#             "message": "Missing required fields",
#             "required": ["rfid", "weight"],
#             "received": data
#         }), 400

#     payload = {
#         "rfid": str(rfid),
#         "weight": float(weight),
#         "timestamp": timestamp
#     }

#     # مؤقتًا نطبع للتأكد أن الربط شغال 100%
#     print("✅ Sensor Reading Received:", payload)

#     return jsonify({
#         "message": "Sensor reading received successfully",
#         "data": payload
#     }), 200

@products_bp.route('/api/sensor-readings', methods=['POST'])
def receive_sensor_readings():
    data = request.get_json(silent=True) or {}
    rfid = data.get("rfid")
    weight = data.get("weight")
    timestamp = data.get("timestamp") or datetime.utcnow().isoformat()

    if rfid is None or weight is None:
        return jsonify({
            "message": "Missing required fields",
            "required": ["rfid", "weight"],
            "received": data
        }), 400

    result, code = process_sensor_reading(str(rfid), float(weight), timestamp)
    return jsonify(result), code

@products_bp.route('/api/readings/<int:item_id>', methods=['GET'])
def get_item_readings(item_id):
    try:
        readings = InventoryReading.query.filter_by(item_id=item_id)\
                    .order_by(InventoryReading.timestamp.asc()).all()

        return jsonify([r.to_dict() for r in readings]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500