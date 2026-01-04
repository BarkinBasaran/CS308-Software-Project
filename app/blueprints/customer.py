from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from app.models import db, Product, Category, Comment, Rating, Wishlist, CartItem, Order, OrderItem, User, Return
from app.decorators import role_required
from datetime import datetime, timedelta
from flask_login import current_user, login_required as flask_login_required
from flask_mail import Message
from app import mail
import uuid
from app.routes import login_required as session_login_required

customer = Blueprint('customer', __name__)

@customer.route('/api/comments', methods=['POST'])
@session_login_required
def api_create_comment():
    data = request.get_json()
    
    required_fields = ['product_id', 'order_id', 'content', 'rating']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
    
    try:
        # Verify product is approved
        product = Product.query.get_or_404(data['product_id'])
        if not product.is_approved:
            return jsonify({'success': False, 'error': 'Product is not approved for comments'}), 403
        
        # Verify order is delivered
        order = Order.query.get_or_404(data['order_id'])
        if order.status != 'delivered':
            return jsonify({'success': False, 'error': 'Product must be delivered before commenting'}), 403
        
        # Check if comment already exists
        existing_comment = Comment.query.filter_by(
            user_id=current_user.id,
            product_id=data['product_id'],
            order_id=data['order_id']
        ).first()
        
        if existing_comment:
            return jsonify({'success': False, 'error': 'You have already commented on this product'}), 400
        
        # Create comment
        comment = Comment(
            user_id=current_user.id,
            product_id=data['product_id'],
            order_id=data['order_id'],
            content=data['content'],
            approved=False
        )
        
        # Create rating
        rating = Rating(
            user_id=current_user.id,
            product_id=data['product_id'],
            order_id=data['order_id'],
            rating=data['rating']
        )
        
        db.session.add(comment)
        db.session.add(rating)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Comment and rating submitted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@customer.route('/api/orders/<int:order_id>/cancel', methods=['POST'])
@session_login_required
def api_cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    if order.status != 'processing':
        return jsonify({'success': False, 'error': 'Only orders in processing status can be cancelled'}), 400
    
    try:
        # Return products to stock
        for item in order.order_items:
            product = Product.query.get(item.product_id)
            product.quantity_in_stock += item.quantity
        
        order.status = 'cancelled'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order cancelled successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@customer.route('/api/returns', methods=['POST'])
@session_login_required
def api_create_return():
    data = request.get_json()
    required_fields = ['order_id', 'product_id', 'quantity', 'reason']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
    try:
        # Kullanıcı kimliğini doğrula
        user_id = None
        
        # Flask-Login ile kimlik doğrulama
        if hasattr(current_user, 'id') and current_user.id is not None:
            user_id = current_user.id
        # Session tabanlı kimlik doğrulama kontrolü
        elif 'user_id' in session:
            user_id = session.get('user_id')
            
        # Kullanıcı kimliği bulunamadıysa
        if not user_id:
            return jsonify({'success': False, 'error': 'User not authenticated'}), 401
            
        order = Order.query.get_or_404(data['order_id'])
        if order.user_id != user_id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        if order.status != 'delivered':
            return jsonify({'success': False, 'error': 'Only delivered orders can be returned'}), 400
        # Prevent return if delivered more than 30 days ago
        if hasattr(order, 'delivered_at') and order.delivered_at:
            if datetime.utcnow() - order.delivered_at > timedelta(days=30):
                return jsonify({'success': False, 'error': 'Return period has expired for this order'}), 400
        # Find the order item for this product
        order_item = next((item for item in order.order_items if item.product_id == int(data['product_id'])), None)
        if not order_item:
            return jsonify({'success': False, 'error': 'Product not found in order'}), 400
        if int(data['quantity']) < 1 or int(data['quantity']) > order_item.quantity:
            return jsonify({'success': False, 'error': 'Invalid quantity'}), 400
        # Create return record
        ret = Return(
            user_id=user_id,
            order_id=order.id,
            product_id=data['product_id'],
            quantity=data['quantity'],
            reason=data['reason'],
            status='pending'
        )
        db.session.add(ret)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Return request submitted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@customer.route('/api/wishlist', methods=['GET'])
@session_login_required
def api_get_wishlist():
    try:
        wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            'success': True,
            'wishlist': [{
                'id': item.id,
                'product_id': item.product_id,
                'product_name': item.product.name,
                'price': float(item.product.price),
                'image': item.product.image,
                'added_at': item.added_at.isoformat()
            } for item in wishlist_items]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@customer.route('/api/wishlist/<int:product_id>', methods=['POST'])
@session_login_required
def api_toggle_wishlist(product_id):
    try:
        # Check if product exists and is approved
        product = Product.query.get_or_404(product_id)
        if not product.is_approved:
            return jsonify({'success': False, 'error': 'Product is not approved'}), 403
        
        # Check if already in wishlist
        wishlist_item = Wishlist.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if wishlist_item:
            # Remove from wishlist
            db.session.delete(wishlist_item)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Product removed from wishlist',
                'in_wishlist': False
            })
        else:
            # Add to wishlist
            wishlist_item = Wishlist(
                user_id=current_user.id,
                product_id=product_id
            )
            db.session.add(wishlist_item)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Product added to wishlist',
                'in_wishlist': True
            })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@customer.route('/api/products/search', methods=['GET'])
def api_search_products():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    sort_by = request.args.get('sort_by', 'name')
    sort_order = request.args.get('sort_order', 'asc')
    in_stock = request.args.get('in_stock', 'true').lower() == 'true'
    
    try:
        # Base query for approved products
        products_query = Product.query.filter(Product.is_approved == True)
        
        # Search in name and description
        if query:
            products_query = products_query.filter(
                db.or_(
                    Product.name.ilike(f'%{query}%'),
                    Product.description.ilike(f'%{query}%'),
                    Product.model.ilike(f'%{query}%')
                )
            )
        
        # Filter by category
        if category:
            products_query = products_query.join(Category).filter(Category.name == category)
        
        # Filter by price range
        if min_price:
            products_query = products_query.filter(Product.price >= float(min_price))
        if max_price:
            products_query = products_query.filter(Product.price <= float(max_price))
        
        # Filter by stock availability
        if in_stock:
            products_query = products_query.filter(Product.quantity_in_stock > 0)
        
        # Sorting
        if sort_by == 'price':
            products_query = products_query.order_by(
                Product.price.asc() if sort_order == 'asc' else Product.price.desc()
            )
        elif sort_by == 'popularity':
            products_query = products_query.order_by(
                Product.total_reviews.asc() if sort_order == 'asc' else Product.total_reviews.desc()
            )
        elif sort_by == 'rating':
            products_query = products_query.order_by(
                Product.average_rating.asc() if sort_order == 'asc' else Product.average_rating.desc()
            )
        else:  # default sort by name
            products_query = products_query.order_by(
                Product.name.asc() if sort_order == 'asc' else Product.name.desc()
            )
        
        products = products_query.all()
        
        return jsonify({
            'success': True,
            'products': [{
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'price': float(p.price),
                'quantity_in_stock': p.quantity_in_stock,
                'average_rating': p.average_rating,
                'total_reviews': p.total_reviews,
                'category': p.category.name if p.category else None,
                'model': p.model,
                'warranty_status': p.warranty_status,
                'image': p.image
            } for p in products]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@customer.route('/api/orders/<int:order_id>/status', methods=['GET'])
@session_login_required
def api_get_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        # Get delivery status for each item
        delivery_status = []
        for delivery in order.deliveries:
            delivery_status.append({
                'product_id': delivery.product_id,
                'product_name': delivery.product.name,
                'quantity': delivery.quantity,
                'status': delivery.status,
                'delivered_at': delivery.delivered_at.isoformat() if delivery.delivered_at else None
            })
        
        # Calculate estimated delivery date
        estimated_delivery = None
        if order.status == 'processing':
            estimated_delivery = (datetime.utcnow() + timedelta(days=3)).isoformat()
        elif order.status == 'in_transit':
            estimated_delivery = (datetime.utcnow() + timedelta(days=1)).isoformat()
        
        return jsonify({
            'success': True,
            'order': {
                'id': order.id,
                'status': order.status,
                'created_at': order.created_at.isoformat(),
                'total_price': float(order.total_price),
                'payment_status': order.payment_status,
                'delivery_status': delivery_status,
                'estimated_delivery': estimated_delivery,
                'can_be_cancelled': order.status == 'processing',
                'can_be_returned': order.status == 'delivered' and 
                                 datetime.utcnow() <= order.can_be_returned_until
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@customer.route('/api/orders/history', methods=['GET'])
@session_login_required
def api_order_history():
    try:
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
        return jsonify({
            'success': True,
            'orders': [{
                'id': order.id,
                'status': order.status,
                'created_at': order.created_at.isoformat(),
                'total_price': float(order.total_price),
                'items': [{
                    'product_id': item.product_id,
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'unit_price': float(item.unit_price),
                    'total_price': float(item.total_price)
                } for item in order.order_items]
            } for order in orders]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@customer.route('/api/products/<int:product_id>', methods=['GET'])
def api_product_details(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'success': True,
            'product': {
                'id': product.id,
                'name': product.name,
                'model': product.model,
                'serial_number': product.serial_number,
                'description': product.description,
                'quantity_in_stock': product.quantity_in_stock,
                'price': float(product.price),
                'warranty_status': product.warranty_status,
                'distributor_info': product.distributor_info,
                'image': product.image,
                'category': product.category.name if product.category else None,
                'average_rating': product.average_rating,
                'total_reviews': product.total_reviews,
                'is_approved': product.is_approved
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@customer.route('/api/cart', methods=['GET'])
def api_get_cart():
    try:
        # Get cart items from session if not logged in
        if not current_user.is_authenticated:
            cart_items = CartItem.query.filter_by(session_id=session.get('session_id')).all()
        else:
            cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        return jsonify({
            'success': True,
            'cart': [{
                'id': item.id,
                'product_id': item.product_id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': float(item.product.price),
                'total_price': float(item.product.price * item.quantity),
                'image': item.product.image,
                'stock': item.product.quantity_in_stock
            } for item in cart_items]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@customer.route('/api/cart', methods=['POST'])
def api_add_to_cart():
    data = request.get_json()
    if not data or 'product_id' not in data or 'quantity' not in data:
        return jsonify({'success': False, 'error': 'Product ID and quantity are required'}), 400
    
    try:
        product = Product.query.get_or_404(data['product_id'])
        
        # Check if product is in stock
        if product.quantity_in_stock < data['quantity']:
            return jsonify({'success': False, 'error': 'Not enough stock available'}), 400
        
        # Check if product is approved
        if not product.is_approved:
            return jsonify({'success': False, 'error': 'Product is not approved for sale'}), 400
        
        # Create or get session ID for anonymous users
        if not current_user.is_authenticated:
            if 'session_id' not in session:
                session['session_id'] = str(uuid.uuid4())
            user_id = None
            session_id = session['session_id']
        else:
            user_id = current_user.id
            session_id = None
        
        # Check if product already in cart
        cart_item = CartItem.query.filter_by(
            user_id=user_id,
            session_id=session_id,
            product_id=data['product_id']
        ).first()
        
        if cart_item:
            # Update quantity
            cart_item.quantity += data['quantity']
        else:
            # Create new cart item
            cart_item = CartItem(
                user_id=user_id,
                session_id=session_id,
                product_id=data['product_id'],
                quantity=data['quantity']
            )
            db.session.add(cart_item)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Product added to cart successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@customer.route('/api/cart/<int:item_id>', methods=['PUT', 'DELETE'])
def api_manage_cart_item(item_id):
    try:
        cart_item = CartItem.query.get_or_404(item_id)
        
        # Verify ownership
        if current_user.is_authenticated:
            if cart_item.user_id != current_user.id:
                return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        else:
            if cart_item.session_id != session.get('session_id'):
                return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        if request.method == 'PUT':
            data = request.get_json()
            if 'quantity' not in data:
                return jsonify({'success': False, 'error': 'Quantity is required'}), 400
            
            # Check stock
            if cart_item.product.quantity_in_stock < data['quantity']:
                return jsonify({'success': False, 'error': 'Not enough stock available'}), 400
            
            cart_item.quantity = data['quantity']
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Cart item updated successfully'
            })
        
        # DELETE
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Cart item removed successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 