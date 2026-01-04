from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.models import db, Product, Category, Comment, Order, OrderItem, User, Wishlist
from app.decorators import role_required
from datetime import datetime, timedelta
from flask_login import current_user
from flask_mail import Message
from app import mail

product_manager = Blueprint('product_manager', __name__)

@product_manager.route('/product-manager')
@role_required('product_manager')
def dashboard():
    try:
        # Basic statistics
        total_products = Product.query.count()
        total_categories = Category.query.count()
        total_comments = Comment.query.count()
        total_orders = Order.query.count()
        
        # Product statistics
        approved_products = Product.query.filter_by(is_approved=True).count()
        pending_products = Product.query.filter_by(is_approved=False).count()
        out_of_stock = Product.query.filter(Product.stock == 0).count()
        low_stock = Product.query.filter(Product.stock < 10).count()
        
        # Category statistics
        products_per_category = db.session.query(
            Category.name,
            db.func.count(Product.id)
        ).join(Product).group_by(Category.id).all()
        
        # Comment statistics
        approved_comments = Comment.query.filter_by(is_approved=True).count()
        pending_comments = Comment.query.filter_by(is_approved=False).count()
        
        # Order statistics
        orders_by_status = db.session.query(
            Order.status,
            db.func.count(Order.id)
        ).group_by(Order.status).all()
        
        # Recent activity
        recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
        recent_comments = Comment.query.order_by(Comment.created_at.desc()).limit(5).all()
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        
        return render_template('product_manager/dashboard.html',
            total_products=total_products,
            total_categories=total_categories,
            total_comments=total_comments,
            total_orders=total_orders,
            approved_products=approved_products,
            pending_products=pending_products,
            out_of_stock=out_of_stock,
            low_stock=low_stock,
            products_per_category=products_per_category,
            approved_comments=approved_comments,
            pending_comments=pending_comments,
            orders_by_status=orders_by_status,
            recent_products=recent_products,
            recent_comments=recent_comments,
            recent_orders=recent_orders
        )
    except Exception as e:
        flash('Error loading dashboard statistics', 'error')
        return render_template('product_manager/dashboard.html')

@product_manager.route('/product-manager/products')
@role_required(['product_manager'])
def manage_products():
    # Show all products regardless of price
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('product_manager/products.html',
                         products=products,
                         categories=categories)

@product_manager.route('/product-manager/categories')
@role_required(['product_manager'])
def manage_categories():
    categories = Category.query.all()
    return render_template('product_manager/categories.html',
                         categories=categories)

@product_manager.route('/product-manager/comments')
@role_required(['product_manager'])
def manage_comments():
    comments = Comment.query.filter_by(approved=False).all()
    return render_template('product_manager/comments.html',
                         comments=comments)

@product_manager.route('/product-manager/deliveries')
@role_required(['product_manager'])
def manage_deliveries():
    orders = Order.query.all()
    return render_template('product_manager/deliveries.html',
                         orders=orders)

# API Endpoints
@product_manager.route('/api/categories', methods=['GET', 'POST'])
@role_required(['product_manager'])
def api_categories():
    if request.method == 'GET':
        categories = Category.query.all()
        return jsonify({
            'success': True,
            'categories': [{
                'id': c.id,
                'name': c.name,
                'description': c.description
            } for c in categories]
        })
    
    # POST - Create new category
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'success': False, 'error': 'Category name is required'}), 400
    
    try:
        category = Category(
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(category)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Category created successfully',
            'category_id': category.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@product_manager.route('/api/categories/<int:category_id>', methods=['PUT', 'DELETE'])
@role_required(['product_manager'])
def api_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'PUT':
        data = request.get_json()
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        
        try:
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Category updated successfully'
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # DELETE
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Category deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@product_manager.route('/api/comments/<int:comment_id>', methods=['PUT'])
@role_required(['product_manager'])
def api_approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()
    
    if 'approved' not in data:
        return jsonify({'success': False, 'error': 'Approval status is required'}), 400
    
    try:
        comment.approved = data['approved']
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Comment status updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@product_manager.route('/api/orders/<int:order_id>/status', methods=['PUT'])
@role_required(['product_manager'])
def api_update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    if 'status' not in data or data['status'] not in ['processing', 'in_transit', 'delivered']:
        return jsonify({'success': False, 'error': 'Invalid status'}), 400
    
    try:
        order.status = data['status']
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Order status updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@product_manager.route('/api/products/<int:product_id>/approve', methods=['POST'])
@role_required('product_manager')
def approve_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    try:
        product.is_approved = True
        db.session.commit()
        
        # Notify sales managers about new product
        sales_managers = User.query.filter_by(role='sales_manager').all()
        for manager in sales_managers:
            msg = Message(
                "New Product Requires Pricing",
                recipients=[manager.email]
            )
            msg.body = f"""
            Hello {manager.username},
            
            A new product has been added and requires pricing:
            
            Product: {product.name}
            Category: {product.category.name}
            Description: {product.description}
            
            Please log in to set the price for this product.
            """
            
            html = f"""
            <html>
                <body>
                    <h2>Hello {manager.username},</h2>
                    <p>A new product has been added and requires pricing:</p>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                        <h3>{product.name}</h3>
                        <p><strong>Category:</strong> {product.category.name}</p>
                        <p><strong>Description:</strong> {product.description}</p>
                    </div>
                    
                    <p>Please log in to set the price for this product.</p>
                </body>
            </html>
            """
            
            msg.html = html
            mail.send(msg)
        
        return jsonify({
            'success': True,
            'message': 'Product approved successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while approving the product'
        }), 500

@product_manager.route('/api/products/<int:product_id>/reject', methods=['POST'])
@role_required('product_manager')
def reject_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    try:
        # Send notification to the user who added the product
        msg = Message(
            "Product Submission Rejected",
            recipients=[product.added_by.email]
        )
        msg.body = f"""
        Hello {product.added_by.username},
        
        Your product submission "{product.name}" has been reviewed and rejected.
        
        If you have any questions, please contact our product management team.
        """
        
        html = f"""
        <html>
            <body>
                <h2>Hello {product.added_by.username},</h2>
                <p>Your product submission "{product.name}" has been reviewed and rejected.</p>
                <p>If you have any questions, please contact our product management team.</p>
            </body>
        </html>
        """
        
        msg.html = html
        mail.send(msg)
        
        # Delete the product
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Product rejected and deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while rejecting the product'
        }), 500

@product_manager.route('/api/orders/<int:order_id>/deliver', methods=['POST'])
@role_required(['product_manager'])
def api_mark_order_delivered(order_id):
    order = Order.query.get_or_404(order_id)
    
    try:
        order.status = 'delivered'
        order.delivered_at = datetime.utcnow()
        order.can_be_returned_until = datetime.utcnow() + timedelta(days=30)
        
        # Update delivery status for all order items
        for item in order.order_items:
            product = Product.query.get(item.product_id)
            if product:
                # Update product stock
                product.quantity_in_stock -= item.quantity
                
                # Create delivery record
                delivery = Delivery(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    status='delivered',
                    delivered_at=datetime.utcnow()
                )
                db.session.add(delivery)
        
        # Send delivery confirmation email
        msg = Message(
            f"Your order #{order.id} has been delivered",
            recipients=[order.user.email]
        )
        msg.body = f"""
        Hello {order.user.username},
        
        Your order #{order.id} has been successfully delivered!
        
        Order Details:
        - Order ID: {order.id}
        - Delivery Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
        - Total Amount: ${order.total_price}
        
        You can now rate and review the products you received.
        
        Thank you for shopping with us!
        """
        mail.send(msg)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Order marked as delivered successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@product_manager.route('/api/comments/<int:comment_id>/verify-delivery', methods=['POST'])
@role_required(['product_manager'])
def api_verify_delivery(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    try:
        comment.is_delivered = True
        comment.delivery_verified_at = datetime.utcnow()
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Delivery verified successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@product_manager.route('/api/products/<int:product_id>/stock', methods=['PUT'])
@role_required(['product_manager'])
def api_update_stock(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    if 'quantity' not in data:
        return jsonify({'success': False, 'error': 'Quantity is required'}), 400
    
    try:
        product.quantity_in_stock = data['quantity']
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Stock updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@product_manager.route('/api/deliveries', methods=['GET'])
@role_required(['product_manager'])
def api_get_deliveries():
    try:
        # Get all undelivered orders
        orders = Order.query.filter(Order.status != 'delivered').all()
        
        deliveries = []
        for order in orders:
            for item in order.order_items:
                deliveries.append({
                    'order_id': order.id,
                    'customer_id': order.user_id,
                    'customer_name': order.user.username,
                    'product_id': item.product_id,
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'total_price': float(item.total_price),
                    'delivery_address': order.delivery_address,
                    'status': order.status,
                    'created_at': order.created_at.isoformat()
                })
        
        return jsonify({
            'success': True,
            'deliveries': deliveries
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@product_manager.route('/api/inventory', methods=['GET'])
@role_required(['product_manager'])
def api_get_inventory():
    try:
        products = Product.query.all()
        return jsonify({
            'success': True,
            'inventory': [{
                'id': p.id,
                'name': p.name,
                'category': p.category.name if p.category else None,
                'quantity_in_stock': p.quantity_in_stock,
                'price': float(p.price),
                'is_approved': p.is_approved,
                'last_updated': p.updated_at.isoformat() if p.updated_at else None
            } for p in products]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@product_manager.route('/api/deliveries/<int:order_id>/complete', methods=['POST'])
@role_required(['product_manager'])
def api_complete_delivery(order_id):
    order = Order.query.get_or_404(order_id)
    
    try:
        # Update order status
        order.status = 'delivered'
        order.delivered_at = datetime.utcnow()
        order.can_be_returned_until = datetime.utcnow() + timedelta(days=30)
        
        # Update stock
        for item in order.order_items:
            product = Product.query.get(item.product_id)
            if product:
                product.quantity_in_stock -= item.quantity
        
        # Create delivery records
        for item in order.order_items:
            delivery = Delivery(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                status='delivered',
                delivered_at=datetime.utcnow()
            )
            db.session.add(delivery)
        
        # Send delivery confirmation email
        msg = Message(
            f"Your order #{order.id} has been delivered",
            recipients=[order.user.email]
        )
        msg.body = f"""
        Hello {order.user.username},
        
        Your order #{order.id} has been successfully delivered!
        
        Order Details:
        - Order ID: {order.id}
        - Delivery Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
        - Total Amount: ${order.total_price}
        
        You can now rate and review the products you received.
        
        Thank you for shopping with us!
        """
        mail.send(msg)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Delivery marked as completed successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@product_manager.route('/api/comments/<int:comment_id>/approve', methods=['POST'])
@role_required('product_manager')
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    try:
        comment.approved = True
        db.session.commit()
        
        # Send notification to user
        msg = Message(
            "Your Comment Has Been Approved",
            recipients=[comment.user.email]
        )
        msg.body = f"""
        Hello {comment.user.username},
        
        Your comment on {comment.product.name} has been approved and is now visible to other users.
        
        Thank you for your contribution!
        """
        
        html = f"""
        <html>
            <body>
                <h2>Hello {comment.user.username},</h2>
                <p>Your comment on {comment.product.name} has been approved and is now visible to other users.</p>
                <p>Thank you for your contribution!</p>
            </body>
        </html>
        """
        
        msg.html = html
        mail.send(msg)
        
        return jsonify({
            'success': True,
            'message': 'Comment approved successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while approving the comment'
        }), 500

@product_manager.route('/api/comments/<int:comment_id>/reject', methods=['POST'])
@role_required('product_manager')
def reject_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    try:
        # Send notification to user
        msg = Message(
            "Your Comment Has Been Rejected",
            recipients=[comment.user.email]
        )
        msg.body = f"""
        Hello {comment.user.username},
        
        Your comment on {comment.product.name} has been reviewed and rejected.
        
        If you have any questions, please contact our customer support.
        """
        
        html = f"""
        <html>
            <body>
                <h2>Hello {comment.user.username},</h2>
                <p>Your comment on {comment.product.name} has been reviewed and rejected.</p>
                <p>If you have any questions, please contact our customer support.</p>
            </body>
        </html>
        """
        
        msg.html = html
        mail.send(msg)
        
        # Delete the comment
        db.session.delete(comment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Comment rejected and deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while rejecting the comment'
        }), 500

@product_manager.route('/api/comments/<int:comment_id>/delete', methods=['POST'])
@role_required('product_manager')
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    try:
        # Send notification to user
        msg = Message(
            "Your Comment Has Been Deleted",
            recipients=[comment.user.email]
        )
        msg.body = f"""
        Hello {comment.user.username},
        
        Your comment on {comment.product.name} has been deleted by a product manager.
        
        If you have any questions, please contact our customer support.
        """
        
        html = f"""
        <html>
            <body>
                <h2>Hello {comment.user.username},</h2>
                <p>Your comment on {comment.product.name} has been deleted by a product manager.</p>
                <p>If you have any questions, please contact our customer support.</p>
            </body>
        </html>
        """
        
        msg.html = html
        mail.send(msg)
        
        # Delete the comment
        db.session.delete(comment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Comment deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while deleting the comment'
        }), 500

@product_manager.route('/api/products', methods=['POST'])
@role_required(['product_manager'])
def api_create_product():
    data = request.get_json()
    required_fields = ['name', 'category_id', 'quantity']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'{field} is required'}), 400
    try:
        product = Product(
            name=data['name'],
            category_id=data['category_id'],
            description=data.get('description'),
            quantity_in_stock=data['quantity'],
            image=data.get('image'),
            model=data.get('model'),
            serial_number=data.get('serial_number')
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'success': True, 'product_id': product.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@product_manager.route('/api/products/<int:product_id>', methods=['DELETE'])
@role_required(['product_manager'])
def api_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Product deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 