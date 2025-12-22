# backend/app/routes.py

from flask import Blueprint, jsonify, request
# استيراد الدالة الجديدة predict_stock_needs
from .services import get_all_products_service, get_product_by_id_service, create_product_service, update_product_weight_service, delete_product_service, predict_stock_needs 
from flask_login import login_required, current_user

products_bp = Blueprint('products', __name__)

# ------------------------------------------------------------------
# الـ Routes الحالية (CRUD Operations)
# ------------------------------------------------------------------


@products_bp.route("/api/products", methods=["GET"])
@login_required
def get_all_products():
    products = get_all_products_service(user_id=current_user.id)
    return jsonify(products), 200


@products_bp.route('/api/products/<int:item_id>', methods=['GET'])
def get_product_by_id(item_id):
    product = get_product_by_id_service(item_id)
    if "error" in product:
        return jsonify({"message": "Error fetching product", "error": product["error"]}), 500
    if product is None:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(product), 200

@products_bp.route("/api/products", methods=["POST"])
@login_required
def create_product():
    data = request.get_json(silent=True) or {}
    new_product = create_product_service(data, user_id=current_user.id)
    return jsonify(new_product), 201


@products_bp.route('/api/products/<int:item_id>', methods=['PUT'])
def update_product_weight(item_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    new_total_weight = data.get('total_weight')
    if new_total_weight is None:
        return jsonify({"message": "total_weight is required"}), 400


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
    """
    الرابط: GET /api/predict/<item_id>
    الوظيفة: يستدعي دالة الخدمة للتنبؤ بالطلب على منتج معين.
    """
    try:
        # يمكن تمرير عدد الأيام المراد التنبؤ بها من خلال query parameter
        days = request.args.get('days', default=7, type=int) 
        
        predictions = predict_stock_needs(item_id, days)
        
        if "error" in predictions:
            return jsonify({"message": "Prediction failed", "details": predictions["error"]}), 500
            
        return jsonify(predictions), 200
    
    except Exception as e:
        return jsonify({"message": "An error occurred while getting predictions", "error": str(e)}), 500

# Test
@products_bp.route('/api/products/test', methods=['POST'])
def create_product_test():
    data = request.get_json(silent=True) or {}

    return jsonify({
        "message": "Test route works 🎉",
        "received_data": data
    }), 201
