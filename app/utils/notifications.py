from flask_mail import Message
from app import mail
from app.models import Wishlist, User
from datetime import datetime

def notify_wishlist_users(product, old_price, new_price):
    """Notify users who have this product in their wishlist about the price change."""
    wishlist_items = Wishlist.query.filter_by(product_id=product.id).all()
    
    for item in wishlist_items:
        user = User.query.get(item.user_id)
        if user:
            discount_percentage = ((old_price - new_price) / old_price) * 100
            
            msg = Message(
                f"Price Drop Alert - {product.name}",
                recipients=[user.email]
            )
            
            msg.body = f"""
            Hello {user.username},
            
            Great news! A product in your wishlist has had a price drop!
            
            Product: {product.name}
            Old Price: ${old_price}
            New Price: ${new_price}
            Discount: {discount_percentage:.2f}%
            
            Don't miss this opportunity! The product might sell out quickly.
            
            Click here to view the product: [Product Link]
            
            Happy shopping!
            """
            
            html = f"""
            <html>
                <body>
                    <h2>Hello {user.username},</h2>
                    <p>Great news! A product in your wishlist has had a price drop!</p>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                        <h3>{product.name}</h3>
                        <p><strong>Old Price:</strong> <span style="text-decoration: line-through;">${old_price}</span></p>
                        <p><strong>New Price:</strong> <span style="color: #28a745; font-weight: bold;">${new_price}</span></p>
                        <p><strong>Discount:</strong> <span style="color: #28a745; font-weight: bold;">{discount_percentage:.2f}%</span></p>
                    </div>
                    
                    <p>Don't miss this opportunity! The product might sell out quickly.</p>
                    
                    <a href="[Product Link]" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">View Product</a>
                    
                    <p>Happy shopping!</p>
                </body>
            </html>
            """
            
            msg.html = html
            mail.send(msg) 