from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.models import db, Product, Order, OrderItem, Return, User, Wishlist
from app.decorators import role_required
from flask_mail import Message
from app import mail
from datetime import datetime
from app.utils import send_email
from app.utils.pdf_generator import generate_invoice_pdf
import os
from flask import current_app

sales_manager = Blueprint('sales_manager', __name__)

@sales_manager.route('/sales-manager')
@role_required(['sales_manager'])
def dashboard():
    # Get statistics for the dashboard
    total_orders = Order.query.count()
    total_revenue = sum(float(order.total_price) for order in Order.query.filter_by(payment_status='completed').all())
    pending_returns = Return.query.filter_by(status='pending').count()
    total_products = Product.query.count()
    
    return render_template('sales_manager/dashboard.html',
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         pending_returns=pending_returns,
                         total_products=total_products)

@sales_manager.route('/sales-manager/products')
@role_required(['sales_manager'])
def manage_products():
    products = Product.query.all()
    return render_template('sales_manager/products.html',
                         products=products)

@sales_manager.route('/sales-manager/orders')
@role_required(['sales_manager'])
def manage_orders():
    orders = Order.query.all()
    return render_template('sales_manager/orders.html',
                         orders=orders)

@sales_manager.route('/sales-manager/returns')
@role_required(['sales_manager'])
def manage_returns():
    returns = Return.query.all()
    return render_template('sales_manager/returns.html',
                         returns=returns)

@sales_manager.route('/sales-manager/discounts')
@role_required(['sales_manager'])
def discounts():
    products = Product.query.filter(Product.price > 0).all()
    return render_template('sales_manager/discounts.html', products=products)

@sales_manager.route('/sales-manager/invoices')
@role_required(['sales_manager'])
def invoices():
    return render_template('sales_manager/invoices.html')

@sales_manager.route('/sales-manager/reports')
@role_required(['sales_manager'])
def reports():
    return render_template('sales_manager/reports.html')

# API Endpoints
@sales_manager.route('/api/products/<int:product_id>/price', methods=['PUT'])
@role_required(['sales_manager'])
def api_set_product_price(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    if 'price' not in data:
        return jsonify({'success': False, 'error': 'Price is required'}), 400
    
    try:
        product.price = data['price']
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Product price updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@sales_manager.route('/api/discounts', methods=['POST'])
@role_required(['sales_manager'])
def api_create_discount():
    data = request.get_json()
    
    required_fields = ['product_ids', 'discount_rate', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
    
    try:
        # Update prices for all products
        products = Product.query.filter(Product.id.in_(data['product_ids'])).all()
        for product in products:
            original_price = float(product.price)
            discount_amount = original_price * (data['discount_rate'] / 100)
            discounted_price = original_price - discount_amount
            
            # İndirim bilgilerini güncelle
            product.discounted_price = discounted_price
            product.discount_rate = data['discount_rate']
        
        # Notify users who have these products in their wishlist
        for product in products:
            wishlist_users = User.query.join(Wishlist).filter(
                Wishlist.product_id == product.id
            ).all()
            
            for user in wishlist_users:
                msg = Message(
                    "Product in your wishlist is now on sale!",
                    recipients=[user.email]
                )
                original_price = float(product.price)
                discounted_price = float(product.discounted_price or 0)
                msg.body = f"""
                Hello {user.username},
                
                A product in your wishlist is now on sale!
                Product: {product.name}
                Original Price: ${original_price:.2f}
                New Price: ${discounted_price:.2f}
                Discount: {data['discount_rate']}%
                
                Visit our store to check it out!
                """
                mail.send(msg)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Discount applied successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@sales_manager.route('/api/discounts/remove/<int:product_id>', methods=['POST'])
@role_required(['sales_manager'])
def remove_discount(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        product.discounted_price = None
        product.discount_rate = None
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@sales_manager.route('/api/reports/revenue', methods=['GET'])
@role_required(['sales_manager'])
def api_get_revenue_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({'success': False, 'error': 'Start date and end date are required'}), 400
    
    try:
        orders = Order.query.filter(
            Order.created_at.between(start_date, end_date),
            Order.payment_status == 'completed'
        ).all()
        
        total_revenue = sum(float(order.total_price) for order in orders)
        total_cost = total_revenue * 0.5  # Assuming 50% cost as per requirements
        profit = total_revenue - total_cost
        
        return jsonify({
            'success': True,
            'report': {
                'start_date': start_date,
                'end_date': end_date,
                'total_orders': len(orders),
                'total_revenue': total_revenue,
                'total_cost': total_cost,
                'profit': profit
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sales_manager.route('/api/refunds/<int:order_id>', methods=['POST'])
@role_required(['sales_manager'])
def api_process_refund(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    if 'approved' not in data:
        return jsonify({'success': False, 'error': 'Approval status is required'}), 400
    
    if order.status != 'delivered':
        return jsonify({'success': False, 'error': 'Only delivered orders can be refunded'}), 400
    
    try:
        if data['approved']:
            # Get the return record
            return_id = data.get('return_id')
            if return_id:
                return_record = Return.query.get(return_id)
                if return_record:
                    return_record.status = 'approved'
                    return_record.refund_amount = order.total_price
                    return_record.refund_method = 'credit'
                    return_record.updated_at = datetime.utcnow()
            
            # Update order status
            order.status = 'refunded'
            
            # Return products to stock
            for item in order.order_items:
                product = Product.query.get(item.product_id)
                product.quantity_in_stock += item.quantity
            
            # Send email notification
            subject = f"Refund Approved - Order #{order.id}"
            body = f"""
            Hello {order.user.username},

            Your refund request for order #{order.id} has been approved.
            
            Order Details:
            - Order ID: {order.id}
            - Refund Amount: ${order.total_price}
            - Refund Method: {order.payment_method}
            
            The refunded amount will be processed to your original payment method within 3-5 business days.
            
            Thank you for shopping with us!
            """
            
            html = f"""
            <html>
                <body>
                    <h2>Hello {order.user.username},</h2>
                    <p>Your refund request for order #{order.id} has been approved.</p>
                    
                    <h3>Order Details:</h3>
                    <ul>
                        <li><strong>Order ID:</strong> {order.id}</li>
                        <li><strong>Refund Amount:</strong> ${order.total_price}</li>
                        <li><strong>Refund Method:</strong> {order.payment_method}</li>
                    </ul>
                    
                    <p>The refunded amount will be processed to your original payment method within 3-5 business days.</p>
                    <p>Thank you for shopping with us!</p>
                </body>
            </html>
            """
            
            send_email(subject, [order.user.email], body, html)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Refund processed successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@sales_manager.route('/api/returns/<int:return_id>/reject', methods=['POST'])
@role_required(['sales_manager'])
def api_reject_return(return_id):
    return_record = Return.query.get_or_404(return_id)
    
    if return_record.status != 'pending':
        return jsonify({'success': False, 'error': 'Only pending returns can be rejected'}), 400
    
    try:
        # Update return status
        return_record.status = 'rejected'
        return_record.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Send email notification
        user = User.query.get(return_record.user_id)
        order = Order.query.get(return_record.order_id)
        product = Product.query.get(return_record.product_id)
        
        subject = f"Return Request Rejected - Order #{order.id}"
        body = f"""
        Hello {user.username},

        Your return request for order #{order.id} has been rejected.
        
        Product: {product.name}
        Quantity: {return_record.quantity}
        Reason provided: {return_record.reason}
        
        If you have any questions, please contact our customer support.
        
        Thank you,
        ChipMaster Team
        """
        
        send_email(user.email, subject, body)
        
        return jsonify({
            'success': True,
            'message': 'Return request rejected successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@sales_manager.route('/api/invoices', methods=['GET'])
@role_required(['sales_manager'])
def api_get_invoices():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', type=int) or 20
    offset = request.args.get('offset', type=int) or 0
    try:
        query = Order.query
        if start_date and end_date:
            query = query.filter(Order.created_at.between(start_date, end_date))
        query = query.order_by(Order.created_at.desc())
        orders = query.offset(offset).limit(limit).all()
        invoices = []
        for order in orders:
            invoices.append({
                'order_id': order.id,
                'customer_id': order.user_id,
                'customer_name': order.user.username,
                'customer_email': order.user.email,
                'order_date': order.created_at.isoformat(),
                'total_price': float(order.total_price),
                'payment_status': order.payment_status,
                'delivery_status': order.status,
                'items': [{
                    'product_id': item.product_id,
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'unit_price': float(item.unit_price),
                    'total_price': float(item.total_price)
                } for item in order.order_items]
            })
        return jsonify({'success': True, 'invoices': invoices})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sales_manager.route('/api/invoices/<int:order_id>/pdf', methods=['GET'])
@role_required(['sales_manager'])
def api_generate_invoice_pdf(order_id):
    order = Order.query.get_or_404(order_id)
    try:
        # Save PDF using utility
        filename = f'invoice_{order.id}_{datetime.utcnow().strftime("%Y%m%d")}.pdf'
        filepath = os.path.join(current_app.config['INVOICE_FOLDER'], filename)
        generate_invoice_pdf(order, filepath)

        # Send email with PDF attachment (optional, can keep or remove)
        msg = Message(
            f"Invoice for Order #{order.id}",
            recipients=[order.user.email]
        )
        msg.body = f"""
        Hello {order.user.username},
        \nPlease find attached the invoice for your order #{order.id}.
        \nOrder Details:
        - Order ID: {order.id}
        - Order Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        - Total Amount: ${order.total_price}
        \nThank you for shopping with us!
        """
        with open(filepath, 'rb') as fp:
            msg.attach(filename, 'application/pdf', fp.read())
        mail.send(msg)

        from flask import send_file
        return send_file(filepath, mimetype='application/pdf', as_attachment=False)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sales_manager.route('/api/reports/profit-loss', methods=['GET'])
@role_required(['sales_manager'])
def api_get_profit_loss_report():
    period = request.args.get('period', 'monthly')
    try:
        query = Order.query.filter(Order.payment_status == 'completed')
        orders = query.all()
        # Calculate revenue and costs
        total_revenue = sum(float(order.total_price) for order in orders)
        total_cost = total_revenue * 0.5  # Assuming 50% cost
        profit = total_revenue - total_cost
        # Group by period for chart data
        from collections import defaultdict
        import calendar
        daily_data = defaultdict(lambda: {'revenue': 0, 'cost': 0, 'profit': 0, 'orders': 0})
        for order in orders:
            dt = order.created_at
            if period == 'yearly':
                key = str(dt.year)
            elif period == 'monthly':
                key = f"{dt.year}-{dt.month:02d}"
            elif period == 'weekly':
                key = f"{dt.year}-W{dt.isocalendar()[1]:02d}"
            else:
                key = dt.strftime('%Y-%m-%d')
            daily_data[key]['revenue'] += float(order.total_price)
            daily_data[key]['cost'] += float(order.total_price) * 0.5
            daily_data[key]['profit'] += float(order.total_price) * 0.5
            daily_data[key]['orders'] += 1
        # Sort keys
        sorted_keys = sorted(daily_data.keys())
        chart_data = [{
            'date': key,
            'revenue': daily_data[key]['revenue'],
            'cost': daily_data[key]['cost'],
            'profit': daily_data[key]['profit'],
            'orders': daily_data[key]['orders']
        } for key in sorted_keys]
        return jsonify({
            'success': True,
            'report': {
                'period': period,
                'total_orders': len(orders),
                'total_revenue': total_revenue,
                'total_cost': total_cost,
                'profit': profit,
                'chart_data': chart_data
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500 