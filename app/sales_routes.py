from flask import Blueprint, request, jsonify
from app.models import db, Product
from functools import wraps
from app.logger import log_user_action

sales = Blueprint('sales', __name__)

def sales_manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('role') == 'sales_manager':
            return jsonify({'error': 'Unauthorized access'}), 403
        return f(*args, **kwargs)
    return decorated_function

@sales.route('/set_price/<int:id>', methods=['PUT'])
@sales_manager_required
def set_price(id):
    product = Product.query.get_or_404(id)
    try:
        data = request.get_json()
        new_price = data.get('price')
        if new_price is None:
            return jsonify({'error': 'Price is required'}), 400
        product.price = new_price
        db.session.commit()
        log_user_action(session['user_id'], f'Set price for product {product.name} to {new_price}')
        return jsonify({'message': 'Price updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@sales.route('/set_discount/<int:id>', methods=['PUT'])
@sales_manager_required
def set_discount(id):
    product = Product.query.get_or_404(id)
    try:
        data = request.get_json()
        discount_percentage = data.get('discount_percentage')
        if discount_percentage is None:
            return jsonify({'error': 'Discount percentage is required'}), 400
        
        # Calculate discounted price
        original_price = float(product.price)
        discounted_price = original_price * (1 - discount_percentage / 100)
        product.price = discounted_price
        
        db.session.commit()
        log_user_action(session['user_id'], f'Set {discount_percentage}% discount for product {product.name}')
        return jsonify({
            'message': 'Discount applied successfully',
            'original_price': original_price,
            'discounted_price': discounted_price
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 