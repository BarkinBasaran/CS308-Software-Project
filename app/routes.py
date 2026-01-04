from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import db, User, Product, Comment, Rating, Wishlist, CartItem, Category, Address, CreditCard, Order, OrderItem
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from app import mail
from sqlalchemy.exc import IntegrityError
from app.logger import log_user_action
from functools import wraps
from decimal import Decimal
from io import BytesIO
from weasyprint import HTML
from sqlalchemy import func
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.context_processor
def inject_user():
    return dict(session=session)

# Home page routes
@main.route('/')
def index():
    return redirect(url_for('main.home'))

@main.route('/home')
def home():
    # Get featured products from database
    featured_products = Product.query.limit(4).all()
    
    # Prepare product data for template
    product_list = []
    for product in featured_products:
        # Use stored rating data
        total_ratings = product.total_reviews or 0
        average_rating = product.average_rating or 0.0
        
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'image': product.image if hasattr(product, 'image') else 'https://via.placeholder.com/400',
            'rating': average_rating,
            'total_reviews': total_ratings
        }
        product_list.append(product_data)
    
    return render_template('home.html', featured_products=product_list)

# User profile route
@main.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('User not found. Please login again.', 'error')
        return redirect(url_for('main.login'))

    # Son 3 siparişi ve ürünlerini çek
    recent_orders = (
        Order.query
        .filter_by(user_id=user.id)
        .order_by(Order.created_at.desc())
        .limit(3)
        .all()
    )
    # Her siparişin ilk 2 ürününü ekle
    for order in recent_orders:
        order.preview_items = order.order_items[:2]

    return render_template('profile.html', user=user, recent_orders=recent_orders)

@main.route('/products')
def products():
    # Get filter parameters
    category = request.args.get('category', 'All')
    price_range = request.args.get('price_range', 'All')
    sort_by = request.args.get('sort_by', 'name_asc')
    
    # Get user's wishlist items if logged in
    user_wishlist_ids = []
    if session.get('logged_in'):
        user_wishlist_ids = [w.product_id for w in Wishlist.query.filter_by(user_id=session['user_id']).all()]
    
    # Get all products from database (only those priced by sales managers)
    query = Product.query.filter(Product.price > 0)
    
    # Apply category filter
    if category != 'All':
        query = query.filter(Product.category_id == int(category))
    
    # Apply price range filter
    if price_range != 'All':
        if price_range == '0-100':
            query = query.filter(Product.price <= 100)
        elif price_range == '100-500':
            query = query.filter(Product.price > 100, Product.price <= 500)
        elif price_range == '500-1000':
            query = query.filter(Product.price > 500, Product.price <= 1000)
        elif price_range == '1000+':
            query = query.filter(Product.price > 1000)
    
    # Apply sorting
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'name_desc':
        query = query.order_by(Product.name.desc())
    elif sort_by == 'popularity':
        # Önce sales_count'a, eşitse average_rating'e göre sırala
        query = query.order_by(Product.sales_count.desc(), Product.average_rating.desc())
    else:  # name_asc
        query = query.order_by(Product.name.asc())
    
    products = query.all()
    
    # Get all categories for the dropdown
    categories = db.session.query(Category).all()
    
    # Calculate ratings for each product
    product_list = []
    for product in products:
        # Use stored rating data
        total_ratings = product.total_reviews or 0
        average_rating = product.average_rating or 0.0
        
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'model': product.model,
            'serial_number': product.serial_number,
            'warranty_status': product.warranty_status,
            'distributor_info': product.distributor_info,
            'price': float(product.price),
            'discounted_price': float(product.discounted_price) if product.discounted_price is not None else None,
            'discount_rate': product.discount_rate,
            'stock_quantity': product.quantity_in_stock,
            'image': product.image if hasattr(product, 'image') else 'https://via.placeholder.com/400',
            'rating': average_rating,
            'total_reviews': total_ratings,
            'in_wishlist': product.id in user_wishlist_ids
        }
        product_list.append(product_data)
    
    # Price range options
    price_ranges = [
        {'value': 'All', 'label': 'All Prices'},
        {'value': '0-100', 'label': '$0 - $100'},
        {'value': '100-500', 'label': '$100 - $500'},
        {'value': '500-1000', 'label': '$500 - $1000'},
        {'value': '1000+', 'label': '$1000+'}
    ]
    
    # Sort options
    sort_options = [
        {'value': 'name_asc', 'label': 'Name (A-Z)'},
        {'value': 'name_desc', 'label': 'Name (Z-A)'},
        {'value': 'price_asc', 'label': 'Price (Low to High)'},
        {'value': 'price_desc', 'label': 'Price (High to Low)'},
        {'value': 'popularity', 'label': 'Popularity (Most Sold)'}
    ]
    
    return render_template('products.html', 
                         products=product_list,
                         categories=categories,
                         price_ranges=price_ranges,
                         sort_options=sort_options,
                         selected_category=category,
                         selected_price_range=price_range,
                         selected_sort=sort_by)

@main.route('/product/<int:product_id>')
def product_details(product_id):
    # Get product from database
    product = Product.query.get_or_404(product_id)
    
    # Use stored rating data
    total_ratings = product.total_reviews or 0
    average_rating = product.average_rating or 0.0
    rating_distribution = {
        5: len([r for r in product.ratings if r.rating == 5]),
        4: len([r for r in product.ratings if r.rating == 4]),
        3: len([r for r in product.ratings if r.rating == 3]),
        2: len([r for r in product.ratings if r.rating == 2]),
        1: len([r for r in product.ratings if r.rating == 1])
    }
    # Build comments data with user and rating info
    comments_data = []
    raw_comments = Comment.query.filter_by(product_id=product_id, approved=True).all()
    for c in raw_comments:
        # find the rating associated with this user and product
        rating_obj = Rating.query.filter_by(user_id=c.user_id, product_id=product_id).first()
        comments_data.append({
            'username': c.user.username,
            'rating': rating_obj.rating if rating_obj else 0,
            'date': c.comment_date.strftime('%B %d, %Y'),
            'text': c.comment
        })
    
    # Check if product is in user's wishlist
    in_wishlist = False
    if session.get('user_id'):
        wishlist_item = Wishlist.query.filter_by(
            user_id=session['user_id'],
            product_id=product_id
        ).first()
        in_wishlist = wishlist_item is not None
    
    # Prepare product data for template
    product_data = {
        'id': product.id,
        'name': product.name,
        'model': product.model,
        'serial_number': product.serial_number,
        'description': product.description,
        'stock_quantity': product.quantity_in_stock,
        'price': float(product.price),
        'discounted_price': float(product.discounted_price) if product.discounted_price is not None else None,
        'discount_rate': product.discount_rate,
        'warranty_status': product.warranty_status,
        'distributor_info': product.distributor_info,
        'image_url': product.image if hasattr(product, 'image') else 'https://via.placeholder.com/400',
        'additional_images': [product.image if hasattr(product, 'image') else 'https://via.placeholder.com/400'] * 4,
        'average_rating': average_rating,
        'total_reviews': total_ratings,
        'rating_distribution': rating_distribution,
        'can_review': session.get('logged_in', False),
        'in_wishlist': in_wishlist,
        'comments': comments_data
    }
    
    return render_template('product_details.html', product=product_data)

# Cart routes
@main.route('/cart')
def cart():
    cart_items = []
    subtotal = 0
    
    if session.get('user_id'):
        # Kullanıcı giriş yapmışsa veritabanından sepet öğelerini al
        db_cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        
        for cart_item in db_cart_items:
            product = Product.query.get(cart_item.product_id)
            if product:
                # Fiyatı belirle: indirimli varsa onu kullan
                unit_price = float(product.discounted_price) if product.discounted_price is not None and product.discounted_price < product.price else float(product.price)
                item = {
                    'id': product.id,
                    'name': product.name,
                    'model': product.model,
                    'stock_quantity': product.quantity_in_stock,
                    'price': float(product.price),
                    'discounted_price': float(product.discounted_price) if product.discounted_price is not None else None,
                    'quantity': cart_item.quantity,
                    'image_url': product.image if hasattr(product, 'image') else 'https://via.placeholder.com/400'
                }
                cart_items.append(item)
                subtotal += unit_price * cart_item.quantity
    else:
        # Kullanıcı giriş yapmamışsa session'dan sepet öğelerini al
        if not session.get('cart_items'):
            session['cart_items'] = {}
        
        for product_id, quantity in session['cart_items'].items():
            product = Product.query.get(int(product_id))
            if product:
                unit_price = float(product.discounted_price) if product.discounted_price is not None and product.discounted_price < product.price else float(product.price)
                item = {
                    'id': product.id,
                    'name': product.name,
                    'model': product.model,
                    'stock_quantity': product.quantity_in_stock,
                    'price': float(product.price),
                    'discounted_price': float(product.discounted_price) if product.discounted_price is not None else None,
                    'quantity': quantity,
                    'image_url': product.image if hasattr(product, 'image') else 'https://via.placeholder.com/400'
                }
                cart_items.append(item)
                subtotal += unit_price * quantity
    
    if not cart_items:
        return render_template('cart.html', cart_items=None, subtotal=0, total=0)
    
    total = subtotal  # Add shipping cost if needed
    can_checkout = session.get('logged_in', False)
    return render_template('cart.html', 
                         cart_items=cart_items, 
                         subtotal=subtotal, 
                         total=total,
                         can_checkout=can_checkout)

# Checkout route
@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        # Process order creation
        shipping_address_id = request.form.get('shipping_address')
        billing_address_id = shipping_address_id
        credit_card_id = request.form.get('credit_card')
        if not shipping_address_id or not credit_card_id:
            flash('Please select shipping address and payment method', 'error')
            return redirect(url_for('main.checkout'))

        # Retrieve cart items
        cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        if not cart_items:
            flash('Your cart is empty', 'error')
            return redirect(url_for('main.cart'))

        # Retrieve user selections
        shipping_address = Address.query.get(shipping_address_id)
        billing_address = Address.query.get(billing_address_id)
        credit_card = CreditCard.query.get(credit_card_id)
        if not all([shipping_address, billing_address, credit_card]):
            flash('Invalid address or payment method', 'error')
            return redirect(url_for('main.checkout'))

        # Calculate totals (using floats to avoid Decimal/float issues)
        subtotal = 0
        for cart_item in cart_items:
            product = cart_item.product if hasattr(cart_item, 'product') else Product.query.get(cart_item.product_id)
            unit_price = float(product.discounted_price) if product.discounted_price is not None and product.discounted_price < product.price else float(product.price)
            subtotal += unit_price * cart_item.quantity
        tax = subtotal * 0.18
        shipping_cost = 0 if subtotal > 100 else 10
        total = subtotal + tax + shipping_cost

        # Create the Order
        order = Order(
            user_id=session['user_id'],
            total_price=total,
            delivery_address=f"{shipping_address.full_name}, {shipping_address.street_address}, {shipping_address.city}, {shipping_address.state} {shipping_address.postal_code}",
            billing_address=f"{billing_address.full_name}, {billing_address.street_address}, {billing_address.city}, {billing_address.state} {billing_address.postal_code}",
            status='processing',
            payment_status='completed',
            payment_method=f"{credit_card.card_type} ending in {credit_card.last_four}"
        )
        db.session.add(order)

        # Create OrderItems and update stock
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.quantity_in_stock:
                db.session.rollback()
                flash(f'Not enough stock for {cart_item.product.name}', 'error')
                return redirect(url_for('main.checkout'))
            cart_item.product.quantity_in_stock -= cart_item.quantity
            # Satış sayısını artır
            cart_item.product.sales_count = (cart_item.product.sales_count or 0) + cart_item.quantity
            # Fiyatı belirle: indirimli varsa onu kullan
            unit_price = float(cart_item.product.discounted_price) if cart_item.product.discounted_price is not None and cart_item.product.discounted_price < cart_item.product.price else float(cart_item.product.price)
            order_item = OrderItem(
                order=order,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                unit_price=unit_price,
                total_price=cart_item.quantity * unit_price
            )
            db.session.add(order_item)

        # Clear the cart and commit
        CartItem.query.filter_by(user_id=session['user_id']).delete()
        
        # Send purchase confirmation email
        msg = Message(
            f"Order Confirmation - Order #{order.id}",
            recipients=[order.user.email]
        )
        msg.body = f"""
        Hello {order.user.username},
        
        Thank you for your purchase! Your order has been confirmed.
        
        Order Details:
        - Order ID: {order.id}
        - Order Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        - Total Amount: ${order.total_price}
        - Payment Method: {order.payment_method}
        - Delivery Address: {order.delivery_address}
        
        You can track your order status in your account dashboard.
        
        Thank you for shopping with us!
        """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset='UTF-8'>
          <title>Order Confirmation - ChipMaster</title>
          <style>
            body {{
              font-family: 'Poppins', Arial, sans-serif;
              background-color: #000;
              margin: 0;
              padding: 0;
              text-align: center;
              color: #ddd;
            }}
            .container {{
              max-width: 600px;
              margin: 50px auto;
              background: #111;
              padding: 25px;
              border-radius: 12px;
              box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.1);
              text-align: center;
            }}
            .logo {{
              font-size: 2.2rem;
              font-weight: 700;
              color: #ff5e62;
              margin-bottom: 15px;
            }}
            h1 {{
              font-size: 1.6rem;
              color: #fff;
              margin-bottom: 10px;
            }}
            p {{
              font-size: 1rem;
              color: #bbb;
              margin-bottom: 20px;
              line-height: 1.5;
            }}
            .order-details {{
              text-align: left;
              margin: 0 auto 20px auto;
              display: inline-block;
              color: #fff;
              background: #181818;
              border-radius: 8px;
              padding: 18px 28px;
            }}
            .order-details ul {{
              padding-left: 18px;
              margin: 0;
            }}
            .btn {{
              display: inline-block;
              padding: 12px 20px;
              margin: 20px 0;
              background: #ff5e62;
              color: white !important;
              text-decoration: none;
              font-size: 1rem;
              font-weight: bold;
              border-radius: 5px;
              transition: background 0.3s ease-in-out;
            }}
            .btn:hover {{
              background: #e94057;
              color: white !important;
            }}
            .footer {{
              margin-top: 20px;
              font-size: 0.85rem;
              color: #777;
            }}
          </style>
        </head>
        <body>
          <div class='container'>
            <div class='logo'>ChipMaster</div>
            <h1>Order Confirmation</h1>
            <p>Thank you for your purchase! Your order has been confirmed.</p>
            <div class='order-details'>
              <ul>
                <li><b>Order ID:</b> {order.id}</li>
                <li><b>Order Date:</b> {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}</li>
                <li><b>Total Amount:</b> ${order.total_price}</li>
                <li><b>Payment Method:</b> {order.payment_method}</li>
                <li><b>Delivery Address:</b> {order.delivery_address}</li>
              </ul>
            </div>
            <p>You can track your order status in your account dashboard.<br>Thank you for shopping with us!</p>
            <div class='footer'>
              <p>&copy; 2025 ChipMaster. All rights reserved.</p>
            </div>
          </div>
        </body>
        </html>
        """
        
        msg.html = html
        # Generate PDF attachment for order confirmation
        pdf_file = BytesIO()
        HTML(string=html).write_pdf(pdf_file)
        pdf_file.seek(0)
        msg.attach(f"order_{order.id}.pdf", "application/pdf", pdf_file.getvalue())
        mail.send(msg)
        
        db.session.commit()
        # Redirect to order success page with details
        return redirect(url_for('main.order_success', order_id=order.id))

    # GET request: retrieve cart items
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    if not cart_items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('main.cart'))
    # Get user's addresses and credit cards
    addresses = Address.query.filter_by(user_id=session['user_id']).all()
    credit_cards = CreditCard.query.filter_by(user_id=session['user_id']).all()
    
    # Prepare cart items with product information
    cart_items_with_products = []
    subtotal = 0
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        if product:
            unit_price = float(product.discounted_price) if product.discounted_price is not None and product.discounted_price < product.price else float(product.price)
            item = {
                'id': cart_item.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': float(product.price),
                    'discounted_price': float(product.discounted_price) if product.discounted_price is not None else None,
                    'discount_rate': product.discount_rate,
                    'image_url': product.image if hasattr(product, 'image') else 'https://via.placeholder.com/400'
                },
                'quantity': cart_item.quantity,
                'total': unit_price * cart_item.quantity
            }
            cart_items_with_products.append(item)
            subtotal += item['total']
    
    # Calculate totals (using float arithmetic)
    tax = subtotal * 0.18
    shipping_cost = 0 if subtotal > 100 else 10
    total = subtotal + tax + shipping_cost
    
    # Get current user
    user = User.query.filter_by(username=session.get('username')).first()
    
    return render_template('checkout.html',
                         cart_items=cart_items_with_products,
                         subtotal=subtotal,
                         tax=tax,
                         shipping_cost=shipping_cost,
                         total=total,
                         addresses=addresses,
                         credit_cards=credit_cards,
                         user=user)

# API routes
@main.route('/api/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Find product in database
    product = Product.query.get_or_404(product_id)
    
    if session.get('user_id'):
        # Kullanıcı giriş yapmışsa veritabanına ekle/güncelle
        cart_item = CartItem.query.filter_by(
            user_id=session['user_id'],
            product_id=product_id
        ).first()
        
        if cart_item:
            if cart_item.quantity < product.quantity_in_stock:
                cart_item.quantity += 1
                db.session.commit()
            else:
                return jsonify({'success': False, 'message': 'Not enough stock available'})
        else:
            cart_item = CartItem(
                user_id=session['user_id'],
                product_id=product_id,
                quantity=1
            )
            db.session.add(cart_item)
            db.session.commit()
    else:
        # Kullanıcı giriş yapmamışsa session'da sakla
        if 'cart_items' not in session:
            session['cart_items'] = {}
        
        product_id_str = str(product_id)
        
        if product_id_str in session['cart_items']:
            if session['cart_items'][product_id_str] < product.quantity_in_stock:
                session['cart_items'][product_id_str] += 1
            else:
                return jsonify({'success': False, 'message': 'Not enough stock available'})
        else:
            session['cart_items'][product_id_str] = 1
        
        session.modified = True
    
    return jsonify({'success': True})

@main.route('/api/cart/<int:item_id>', methods=['PUT', 'DELETE'])
def manage_cart_item(item_id):
    # Check if product exists
    product = Product.query.get_or_404(item_id)
    
    if request.method == 'DELETE':
        if session.get('user_id'):
            # Kullanıcı giriş yapmışsa veritabanından sil
            cart_item = CartItem.query.filter_by(
                user_id=session['user_id'],
                product_id=item_id
            ).first()
            if cart_item:
                db.session.delete(cart_item)
                db.session.commit()
                return jsonify({'success': True})
            return jsonify({'success': False, 'message': 'Item not found in cart'})
        else:
            # Kullanıcı giriş yapmamışsa session'dan sil
            if 'cart_items' in session:
                item_id_str = str(item_id)
                if item_id_str in session['cart_items']:
                    del session['cart_items'][item_id_str]
                    session.modified = True
                    return jsonify({'success': True})
            return jsonify({'success': False, 'message': 'Item not found in cart'})
    
    # Update quantity
    data = request.get_json()
    if not data or 'quantity' not in data:
        return jsonify({'success': False, 'message': 'No quantity specified'})
    
    quantity = int(data['quantity'])
    if quantity < 1:
        return jsonify({'success': False, 'message': 'Invalid quantity'})
    
    if quantity > product.quantity_in_stock:
        return jsonify({'success': False, 'message': 'Not enough stock available'})
    
    if session.get('user_id'):
        # Kullanıcı giriş yapmışsa veritabanını güncelle
        cart_item = CartItem.query.filter_by(
            user_id=session['user_id'],
            product_id=item_id
        ).first()
        if cart_item:
            cart_item.quantity = quantity
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Item not found in cart'})
    else:
        # Kullanıcı giriş yapmamışsa session'ı güncelle
        if 'cart_items' in session:
            item_id_str = str(item_id)
            if item_id_str in session['cart_items']:
                session['cart_items'][item_id_str] = quantity
                session.modified = True
                return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Item not found in cart'})

@main.route('/api/wishlist/<int:product_id>', methods=['POST'])
def toggle_wishlist(product_id):
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Please log in first'})
    
    # Check if product exists
    product = Product.query.get_or_404(product_id)
    
    # Check if product is already in wishlist
    wishlist = Wishlist.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).first()
    
    if wishlist:
        # Remove from wishlist
        db.session.delete(wishlist)
        db.session.commit()
        return jsonify({'success': True, 'in_wishlist': False})
    else:
        # Add to wishlist
        wishlist = Wishlist(
            user_id=session['user_id'],
            product_id=product_id
        )
        db.session.add(wishlist)
        db.session.commit()
        return jsonify({'success': True, 'in_wishlist': True})

@main.route('/api/reviews/<int:product_id>', methods=['POST'])
def submit_review(product_id):
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Please log in first'})
    
    # Check if product exists
    product = Product.query.get_or_404(product_id)
    
    data = request.get_json()
    rating_value = data.get('rating')
    comment_text = data.get('comment')
    
    if not rating_value or not comment_text:
        return jsonify({'success': False, 'message': 'Rating and comment are required'})
    
    # Create and add rating
    rating_obj = Rating(
        user_id=session['user_id'],
        product_id=product_id,
        rating=rating_value
    )
    db.session.add(rating_obj)
    
    # Create and add comment
    comment_obj = Comment(
        user_id=session['user_id'],
        product_id=product_id,
        comment=comment_text,
        approved=False  # Awaiting approval; not shown immediately
    )
    db.session.add(comment_obj)
    
    # Update product's stored rating and review count
    prev_total = product.total_reviews or 0
    prev_avg = product.average_rating or 0.0
    new_total = prev_total + 1
    new_avg = (prev_avg * prev_total + rating_value) / new_total
    product.total_reviews = new_total
    product.average_rating = new_avg
    db.session.add(product)
    
    db.session.commit()
    return jsonify({'success': True})

# Kullanıcı girişi
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        user = User.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.password, password):
            log_user_action('Failed login attempt', email)
            flash("Incorrect email or password", "error")
            return redirect(url_for('main.login'))

        # Merge session cart with user's cart
        if 'cart_items' in session and session['cart_items']:
            for product_id, quantity in session['cart_items'].items():
                product = Product.query.get(int(product_id))
                if not product:
                    continue
                cart_item = CartItem.query.filter_by(user_id=user.id, product_id=product.id).first()
                if cart_item:
                    # Eğer zaten varsa, miktarı arttır
                    cart_item.quantity += quantity
                else:
                    # Yoksa yeni CartItem oluştur
                    cart_item = CartItem(user_id=user.id, product_id=product.id, quantity=quantity)
                    db.session.add(cart_item)
            db.session.commit()
            session.pop('cart_items')

        # Store user info in session
        session['user_id'] = user.id
        session['email'] = user.email
        session['username'] = user.username
        session['logged_in'] = True
        session['role'] = user.role
        
        log_user_action('Successful login', email)
        flash("Login successful!", "success")
        # Redirect based on role
        if user.role == 'product_manager':
            return redirect(url_for('product_manager.dashboard'))
        elif user.role == 'sales_manager':
            return redirect(url_for('sales_manager.dashboard'))
        else:
            return redirect(url_for('main.home'))

    return render_template('login.html')

# Kullanıcı kaydı
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip()
        username = request.form['username'].strip()
        password = request.form['password']

        # E-posta zaten kayıtlı mı kontrol et
        if User.query.filter_by(email=email).first():
            log_user_action('Failed registration - email already exists', email)
            flash("This email is already registered. Please use a different one.", "error")
            return redirect(url_for('main.register'))

        # Kullanıcı adı zaten alınmış mı kontrol et
        if User.query.filter_by(username=username).first():
            log_user_action('Failed registration - username already taken', email)
            flash("This username is already taken. Please choose a different one.", "error")
            return redirect(url_for('main.register'))

        # Şifreyi hashleyerek veritabanına ekle
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(email=email, username=username, password=hashed_password)
        db.session.add(new_user)

        try:
            db.session.commit()
            log_user_action('Successful registration', email)
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('main.login'))
        except IntegrityError:
            db.session.rollback()
            log_user_action('Registration error - database integrity error', email)
            flash("An unexpected error occurred. Please try again.", "error")
            return redirect(url_for('main.register'))

    return render_template('register.html')

# Şifre sıfırlama isteği
@main.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if request.method == 'POST':
        email = request.form['forgot-email'].strip()
        user = User.query.filter_by(email=email).first()

        if user:
            try:
                token = user.get_reset_token()
                reset_url = url_for('main.reset_password', token=token, _external=True)

                msg = Message("Reset Your Password - ChipMaster", recipients=[email])
                msg.html = render_template('email_template.html', reset_url=reset_url)

                mail.send(msg)
                flash("Password reset instructions have been sent to your email.", "success")
            except Exception as e:
                flash("An error occurred while sending the email: " + str(e), "error")
        else:
            flash("No user found with that email address.", "error")

        return redirect(url_for('main.login'))

    return render_template('forgotpassword.html')

# Şifre sıfırlama işlemi
@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid or expired token.", "error")
        return redirect(url_for('main.forgotpassword'))

    if request.method == 'POST':
        new_password = request.form['password'].strip()
        user.password = generate_password_hash(new_password, method='scrypt')
        db.session.commit()
        flash("Your password has been updated. You can now log in.", "success")
        return redirect(url_for('main.login'))

    return render_template('reset_password.html')

# Logout route
@main.route('/logout')
def logout():
    if 'email' in session:
        log_user_action('User logged out', session['email'])
    session.clear()
    flash("You have been successfully logged out.", "success")
    return redirect(url_for('main.login'))

@main.route('/orders')
@login_required
def orders():
    # Get user's orders
    user_orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.created_at.desc()).all()
    
    # Calculate can_be_returned for each order
    for order in user_orders:
        order.can_be_returned = (
            order.status == 'delivered' and 
            order.created_at and 
            datetime.utcnow() - order.created_at <= timedelta(days=30)
        )
    
    return render_template('orders.html', orders=user_orders)

@main.route('/add_address', methods=['POST'])
@login_required
def add_address():
    full_name = request.form.get('full_name')
    street_address = request.form.get('street_address')
    city = request.form.get('city')
    state = request.form.get('state')
    postal_code = request.form.get('postal_code')
    
    if not all([full_name, street_address, city, state, postal_code]):
        flash('Please fill in all fields', 'error')
        return redirect(url_for('main.profile'))
    
    address = Address(
        user_id=session['user_id'],
        full_name=full_name,
        street_address=street_address,
        city=city,
        state=state,
        postal_code=postal_code
    )
    
    db.session.add(address)
    db.session.commit()
    
    flash('Address added successfully', 'success')
    return redirect(url_for('main.profile'))

@main.route('/add_card', methods=['POST'])
@login_required
def add_card():
    card_holder = request.form.get('card_holder')
    card_number = request.form.get('card_number')
    expiry_month = request.form.get('expiry_month')
    expiry_year = request.form.get('expiry_year')
    card_type = request.form.get('card_type')
    
    if not all([card_holder, card_number, expiry_month, expiry_year, card_type]):
        flash('Please fill in all fields', 'error')
        return redirect(url_for('main.profile'))
    
    # Get last 4 digits of card number
    last_four = card_number[-4:]
    
    card = CreditCard(
        user_id=session['user_id'],
        card_holder=card_holder,
        card_number=card_number,
        card_type=card_type,
        last_four=last_four,
        expiry_month=expiry_month,
        expiry_year=expiry_year
    )
    
    db.session.add(card)
    db.session.commit()
    
    flash('Card added successfully', 'success')
    return redirect(url_for('main.profile'))

@main.route('/api/address/<int:address_id>', methods=['DELETE'])
@login_required
def delete_address(address_id):
    address = Address.query.get_or_404(address_id)
    
    if address.user_id != session['user_id']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    db.session.delete(address)
    db.session.commit()
    
    return jsonify({'success': True})

@main.route('/api/card/<int:card_id>', methods=['DELETE'])
@login_required
def delete_card(card_id):
    card = CreditCard.query.get_or_404(card_id)
    
    if card.user_id != session['user_id']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    db.session.delete(card)
    db.session.commit()
    
    return jsonify({'success': True})

@main.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('main.login'))
    
    username = request.form.get('username')
    email = request.form.get('email')
    
    if username:
        user.username = username
    if email:
        user.email = email
    
    try:
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Username or email already exists.', 'error')
    
    return redirect(url_for('main.profile'))

@main.route('/api/address/add', methods=['POST'])
def api_add_address():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Please log in to add an address.'}), 401

    data = request.form
    required_fields = ['full_name', 'street_address', 'city', 'state', 'postal_code', 'address_type']
    
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    postal_code_str = data.get('postal_code', '').strip()
    if not postal_code_str.isdigit():
        flash('Postal code must be an integer value.', 'error')
        return redirect(url_for('main.profile'))

    try:
        address = Address(
            user_id=session['user_id'],
            full_name=data['full_name'],
            street_address=data['street_address'],
            city=data['city'],
            state=data['state'],
            country=data.get('country', 'Turkey'),
            postal_code=data['postal_code'],
            address_type=data['address_type']
        )
        db.session.add(address)
        db.session.commit()
        flash('Address added successfully!', 'success')
        return redirect(url_for('main.profile'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/change_password', methods=['POST'])
@login_required
def change_password():
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('main.login'))
    
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not all([current_password, new_password, confirm_password]):
        flash('Please fill in all fields', 'error')
        return redirect(url_for('main.profile'))
    
    if not check_password_hash(user.password, current_password):
        flash('Current password is incorrect', 'error')
        return redirect(url_for('main.profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('main.profile'))
    
    user.password = generate_password_hash(new_password, method='scrypt')
    db.session.commit()
    
    flash('Password changed successfully!', 'success')
    return redirect(url_for('main.profile'))

@main.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('main.login'))
    
    password = request.form.get('password')
    if not password:
        flash('Please enter your password', 'error')
        return redirect(url_for('main.profile'))
    
    if not check_password_hash(user.password, password):
        flash('Incorrect password', 'error')
        return redirect(url_for('main.profile'))
    
    try:
        # Delete all associated data
        Address.query.filter_by(user_id=user.id).delete()
        CreditCard.query.filter_by(user_id=user.id).delete()
        Wishlist.query.filter_by(user_id=user.id).delete()
        CartItem.query.filter_by(user_id=user.id).delete()
        Order.query.filter_by(user_id=user.id).delete()
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        # Clear the session
        session.clear()
        flash('Your account has been successfully deleted.', 'success')
        return redirect(url_for('main.home'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting your account.', 'error')
        return redirect(url_for('main.profile'))

# Place order endpoint
@main.route('/api/place-order', methods=['POST'])
@login_required
def place_order():
    data = request.get_json()
    
    if not data or not all([data.get('shipping_address_id'), 
                          data.get('billing_address_id'), 
                          data.get('card_id')]):
        return jsonify({
            'success': False,
            'message': 'Missing required fields'
        })
    
    try:
        # Get cart items
        cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        if not cart_items:
            return jsonify({
                'success': False,
                'message': 'Your cart is empty'
            })
        
        # Get addresses and card
        shipping_address = Address.query.get(data['shipping_address_id'])
        billing_address = Address.query.get(data['billing_address_id'])
        credit_card = CreditCard.query.get(data['card_id'])
        
        if not all([shipping_address, billing_address, credit_card]):
            return jsonify({
                'success': False,
                'message': 'Invalid address or credit card'
            })
        
        # Calculate totals (using floats to avoid Decimal/float issues)
        subtotal = 0
        for cart_item in cart_items:
            product = cart_item.product if hasattr(cart_item, 'product') else Product.query.get(cart_item.product_id)
            unit_price = float(product.discounted_price) if product.discounted_price is not None and product.discounted_price < product.price else float(product.price)
            subtotal += unit_price * cart_item.quantity
        tax = subtotal * 0.18
        shipping_cost = 0 if subtotal > 100 else 10
        total = subtotal + tax + shipping_cost
        
        # Create order
        order = Order(
            user_id=session['user_id'],
            total_price=total,
            delivery_address=f"{shipping_address.full_name}, {shipping_address.street_address}, {shipping_address.city}, {shipping_address.state} {shipping_address.postal_code}",
            billing_address=f"{billing_address.full_name}, {billing_address.street_address}, {billing_address.city}, {billing_address.state} {billing_address.postal_code}",
            status='processing',
            payment_status='completed',
            payment_method=f"{credit_card.card_type} ending in {credit_card.last_four}"
        )
        db.session.add(order)
        
        # Create order items and update stock
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.quantity_in_stock:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': f'Not enough stock for {cart_item.product.name}'
                })
            
            # Update product stock
            cart_item.product.quantity_in_stock -= cart_item.quantity
            # Satış sayısını artır
            cart_item.product.sales_count = (cart_item.product.sales_count or 0) + cart_item.quantity
            
            # Create order item
            # Fiyatı belirle: indirimli varsa onu kullan
            unit_price = float(cart_item.product.discounted_price) if cart_item.product.discounted_price is not None and cart_item.product.discounted_price < cart_item.product.price else float(cart_item.product.price)
            order_item = OrderItem(
                order=order,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                unit_price=unit_price,
                total_price=cart_item.quantity * unit_price
            )
            db.session.add(order_item)
        
        # Clear cart
        CartItem.query.filter_by(user_id=session['user_id']).delete()
        
        # Send purchase confirmation email
        msg = Message(
            f"Order Confirmation - Order #{order.id}",
            recipients=[order.user.email]
        )
        msg.body = f"""
        Hello {order.user.username},
        
        Thank you for your purchase! Your order has been confirmed.
        
        Order Details:
        - Order ID: {order.id}
        - Order Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        - Total Amount: ${order.total_price}
        - Payment Method: {order.payment_method}
        - Delivery Address: {order.delivery_address}
        
        You can track your order status in your account dashboard.
        
        Thank you for shopping with us!
        """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset='UTF-8'>
          <title>Order Confirmation - ChipMaster</title>
          <style>
            body {{
              font-family: 'Poppins', Arial, sans-serif;
              background-color: #000;
              margin: 0;
              padding: 0;
              text-align: center;
              color: #ddd;
            }}
            .container {{
              max-width: 600px;
              margin: 50px auto;
              background: #111;
              padding: 25px;
              border-radius: 12px;
              box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.1);
              text-align: center;
            }}
            .logo {{
              font-size: 2.2rem;
              font-weight: 700;
              color: #ff5e62;
              margin-bottom: 15px;
            }}
            h1 {{
              font-size: 1.6rem;
              color: #fff;
              margin-bottom: 10px;
            }}
            p {{
              font-size: 1rem;
              color: #bbb;
              margin-bottom: 20px;
              line-height: 1.5;
            }}
            .order-details {{
              text-align: left;
              margin: 0 auto 20px auto;
              display: inline-block;
              color: #fff;
              background: #181818;
              border-radius: 8px;
              padding: 18px 28px;
            }}
            .order-details ul {{
              padding-left: 18px;
              margin: 0;
            }}
            .btn {{
              display: inline-block;
              padding: 12px 20px;
              margin: 20px 0;
              background: #ff5e62;
              color: white !important;
              text-decoration: none;
              font-size: 1rem;
              font-weight: bold;
              border-radius: 5px;
              transition: background 0.3s ease-in-out;
            }}
            .btn:hover {{
              background: #e94057;
              color: white !important;
            }}
            .footer {{
              margin-top: 20px;
              font-size: 0.85rem;
              color: #777;
            }}
          </style>
        </head>
        <body>
          <div class='container'>
            <div class='logo'>ChipMaster</div>
            <h1>Order Confirmation</h1>
            <p>Thank you for your purchase! Your order has been confirmed.</p>
            <div class='order-details'>
              <ul>
                <li><b>Order ID:</b> {order.id}</li>
                <li><b>Order Date:</b> {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}</li>
                <li><b>Total Amount:</b> ${order.total_price}</li>
                <li><b>Payment Method:</b> {order.payment_method}</li>
                <li><b>Delivery Address:</b> {order.delivery_address}</li>
              </ul>
            </div>
            <p>You can track your order status in your account dashboard.<br>Thank you for shopping with us!</p>
            <div class='footer'>
              <p>&copy; 2025 ChipMaster. All rights reserved.</p>
            </div>
          </div>
        </body>
        </html>
        """
        
        msg.html = html
        # Generate PDF attachment for order confirmation
        pdf_file = BytesIO()
        HTML(string=html).write_pdf(pdf_file)
        pdf_file.seek(0)
        msg.attach(f"order_{order.id}.pdf", "application/pdf", pdf_file.getvalue())
        mail.send(msg)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order placed successfully!',
            'redirect_url': url_for('main.orders')
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your order'
        })

@main.route('/order-success/<int:order_id>')
@login_required
def order_success(order_id):
    # Show a success page with order details and allow ratings for purchased products
    order = Order.query.get_or_404(order_id)
    # Prepare items for rating only when order is delivered
    items = []
    if order.status == 'delivered':
        for order_item in order.order_items:
            product = Product.query.get(order_item.product_id)
            # Check if current user already rated this product
            existing_rating = Rating.query.filter_by(
                user_id=session['user_id'], product_id=product.id
            ).first()
            items.append({
                'id': product.id,
                'name': product.name,
                'image': product.image if product.image else 'https://via.placeholder.com/150',
                'can_rate': existing_rating is None
            })
    return render_template('order_success.html', order=order, items=items)

@main.route('/api/orders/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns the order
    if order.user_id != session['user_id']:
        return jsonify({
            'success': False,
            'message': 'Unauthorized'
        }), 403
    
    # Check if order can be cancelled
    if order.status != 'processing':
        return jsonify({
            'success': False,
            'message': 'Order can only be cancelled while in processing status'
        }), 400
    
    try:
        # Update order status
        order.status = 'cancelled'
        
        # Restore product stock
        for item in order.order_items:
            product = Product.query.get(item.product_id)
            product.quantity_in_stock += item.quantity
        
        # Send cancellation email
        msg = Message(
            f"Order Cancelled - Order #{order.id}",
            recipients=[order.user.email]
        )
        msg.body = f"""
        Hello {order.user.username},
        
        Your order #{order.id} has been cancelled.
        
        Order Details:
        - Order ID: {order.id}
        - Order Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        - Total Amount: ${order.total_price}
        - Payment Method: {order.payment_method}
        
        The refund will be processed according to your original payment method.
        Please allow 3-5 business days for the amount to reflect in your account.
        
        If you have any questions, please contact our customer support.
        """
        
        html = f"""
        <html>
            <body>
                <h2>Hello {order.user.username},</h2>
                <p>Your order #{order.id} has been cancelled.</p>
                
                <h3>Order Details:</h3>
                <ul>
                    <li><strong>Order ID:</strong> {order.id}</li>
                    <li><strong>Order Date:</strong> {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}</li>
                    <li><strong>Total Amount:</strong> ${order.total_price}</li>
                    <li><strong>Payment Method:</strong> {order.payment_method}</li>
                </ul>
                
                <p>The refund will be processed according to your original payment method.</p>
                <p>Please allow 3-5 business days for the amount to reflect in your account.</p>
                
                <p>If you have any questions, please contact our customer support.</p>
            </body>
        </html>
        """
        
        msg.html = html
        # Generate PDF attachment for order cancellation
        pdf_file = BytesIO()
        HTML(string=html).write_pdf(pdf_file)
        pdf_file.seek(0)
        msg.attach(f"order_{order.id}_cancellation.pdf", "application/pdf", pdf_file.getvalue())
        mail.send(msg)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order cancelled successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while cancelling the order'
        }), 500

@main.route('/wishlist')
@login_required
def wishlist():
    user = User.query.get(session['user_id'])
    wishlist_items = Wishlist.query.filter_by(user_id=user.id).all()
    products = [Product.query.get(item.product_id) for item in wishlist_items]
    return render_template('wishlist.html', products=products)