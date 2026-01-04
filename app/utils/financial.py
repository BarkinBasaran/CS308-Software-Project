from app.models import Order, OrderItem, Product
from datetime import datetime, timedelta
from sqlalchemy import func

def calculate_revenue(start_date, end_date):
    """Calculate total revenue for a given date range."""
    orders = Order.query.filter(
        Order.created_at.between(start_date, end_date),
        Order.status != 'cancelled'
    ).all()
    
    total_revenue = sum(order.total_price for order in orders)
    return total_revenue

def calculate_profit(start_date, end_date):
    """Calculate total profit for a given date range."""
    orders = Order.query.filter(
        Order.created_at.between(start_date, end_date),
        Order.status != 'cancelled'
    ).all()
    
    total_profit = 0
    for order in orders:
        for item in order.order_items:
            # Assuming product cost is 50% of sale price
            cost = float(item.unit_price) * 0.5
            profit = (float(item.unit_price) - cost) * item.quantity
            total_profit += profit
    
    return total_profit

def get_sales_trends(days=30):
    """Get daily sales trends for the last N days."""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    daily_sales = db.session.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_price).label('revenue'),
        func.count(Order.id).label('orders')
    ).filter(
        Order.created_at.between(start_date, end_date),
        Order.status != 'cancelled'
    ).group_by(
        func.date(Order.created_at)
    ).order_by(
        func.date(Order.created_at)
    ).all()
    
    return [
        {
            'date': sale.date.strftime('%Y-%m-%d'),
            'revenue': float(sale.revenue) if sale.revenue else 0,
            'orders': sale.orders
        }
        for sale in daily_sales
    ]

def get_top_products(limit=10):
    """Get top selling products by revenue."""
    top_products = db.session.query(
        Product,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.total_price).label('total_revenue')
    ).join(
        OrderItem
    ).join(
        Order
    ).filter(
        Order.status != 'cancelled'
    ).group_by(
        Product.id
    ).order_by(
        func.sum(OrderItem.total_price).desc()
    ).limit(limit).all()
    
    return [
        {
            'product': product,
            'total_quantity': total_quantity,
            'total_revenue': float(total_revenue)
        }
        for product, total_quantity, total_revenue in top_products
    ]

def get_product_performance(product_id, days=30):
    """Get performance metrics for a specific product."""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    performance = db.session.query(
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.total_price).label('total_revenue'),
        func.avg(OrderItem.unit_price).label('average_price')
    ).join(
        Order
    ).filter(
        OrderItem.product_id == product_id,
        Order.created_at.between(start_date, end_date),
        Order.status != 'cancelled'
    ).first()
    
    return {
        'total_quantity': performance.total_quantity or 0,
        'total_revenue': float(performance.total_revenue) if performance.total_revenue else 0,
        'average_price': float(performance.average_price) if performance.average_price else 0
    } 