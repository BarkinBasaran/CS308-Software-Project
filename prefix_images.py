from app import create_app, db
from app.models import Product

"""
Prefix existing image filenames in the database with '/static/product_images/' so that templates can load them correctly.
Usage: python prefix_images.py
"""
app = create_app()
with app.app_context():
    products = Product.query.filter(Product.image != None).all()
    count = 0
    for p in products:
        # Skip if already prefixed
        if not p.image.startswith('/static/product_images/'):
            old_path = p.image
            new_path = f"/static/product_images/{old_path}"
            p.image = new_path
            count += 1
            print(f"Updated product {p.id}: '{old_path}' -> '{new_path}'")
    if count > 0:
        db.session.commit()
        print(f"Completed prefixing for {count} products.")
    else:
        print("No images needed prefixing.") 