# backend/app/routes.py
# ------------------------------------------------------------------------------
#  الاستيراد:
#  - Blueprint: لتنظيم مجموعة من الروابط (Routes) معاً.
#  - request: للوصول إلى البيانات المرسلة في الطلب (مثل JSON).
#  - jsonify: لتحويل قواميس بايثون (dictionaries) إلى استجابة JSON.
#  - services: الملف الذي يحتوي على منطق التعامل مع قاعدة البيانات.
# ------------------------------------------------------------------------------
from flask import Blueprint, request, jsonify
from . import services

# --- إعداد المخطط (Blueprint) ---
# نستخدم Blueprint لتجميع كل الروابط المتعلقة بالمنتجات تحت بادئة (prefix)

products_bp = Blueprint('products_bp', __name__, url_prefix='/api/products')

@products_bp.route('/', methods=['GET'])
def get_all_products():
    
    # الرابط: GET /api/products
    # الوظيفة: يستدعي دالة الخدمة لجلب كل المنتجات ويرجعها كـ JSON.
    
    products = services.get_all_products_service()
    if "error" in products:
        return jsonify(products), 500
    return jsonify(products)


@products_bp.route('/<int:item_id>', methods=['GET'])
def get_product(item_id):
    
    # الرابط: GET /api/products/<id>
    # الوظيفة: يستدعي دالة الخدمة لجلب منتج واحد بناءً على الـ ID.
    
    product = services.get_product_by_id_service(item_id)
    if "error" in product:
        return jsonify(product), 500
    if not product:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(product)


@products_bp.route('/', methods=['POST'])
def create_product():
    
    # الرابط: POST /api/products
    # الوظيفة: يأخذ بيانات المنتج الجديد من الطلب (request body) ويستدعي
    #          دالة الخدمة لإنشائه في قاعدة البيانات.
    
    data = request.get_json()
    # يمكن إضافة تحقق أكثر تفصيلاً هنا
    if not data:
        return jsonify({"message": "Request body is missing"}), 400
        
    new_product = services.create_product_service(data)
    if "error" in new_product:
        return jsonify(new_product), 500
    return jsonify(new_product), 201


@products_bp.route('/<int:item_id>/update_weight', methods=['POST'])
def update_product_weight(item_id):
    
    # الرابط: POST /api/products/<id>/update_weight
    # الوظيفة: يأخذ الوزن الإجمالي الجديد من الطلب ويستدعي دالة الخدمة لتحديثه.
    
    data = request.get_json()
    if not data or 'total_weight' not in data:
        return jsonify({"message": "'total_weight' is required in request body"}), 400
    
    # استدعاء دالة الخدمة الجديدة
    updated_product = services.update_product_weight_service(item_id, data['total_weight'])
    
    if "error" in updated_product:
        return jsonify(updated_product), 500
    if not updated_product:
         return jsonify({"message": "Product not found"}), 404

    return jsonify(updated_product)


@products_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_product(item_id):
    
    # الرابط: DELETE /api/products/<id>
    # الوظيفة: يستدعي دالة الخدمة لحذف المنتج المطابق للـ ID.
    
    result = services.delete_product_service(item_id)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

