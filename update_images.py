from app import create_app, db
from app.models import Product
from app.logger import log_user_action

def update_product_image(product_id, image_filename):
    """Update the image field for a specific product."""
    app = create_app()
    with app.app_context():
        try:
            product = Product.query.get(product_id)
            if product:
                image_path = f"/static/product_images/{image_filename}"
                product.image = image_path
                db.session.commit()
                log_user_action(f"Updated product {product.name} with image {image_filename}")
            else:
                log_user_action(f"Product with ID {product_id} not found", level="warning")
        except Exception as e:
            log_user_action(f"Error updating product image: {str(e)}", level="error")
            db.session.rollback()

def list_products():
    """List all products in the database."""
    app = create_app()
    with app.app_context():
        try:
            products = Product.query.all()
            print("\nCurrent Products:")
            print("ID | Name | Image")
            print("-" * 50)
            for product in products:
                print(f"{product.id} | {product.name} | {product.image or 'No image'}")
        except Exception as e:
            log_user_action(f"Error listing products: {str(e)}", level="error")

def main():
    while True:
        print("\n1. List all products")
        print("2. Update product image")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            list_products()
        elif choice == "2":
            try:
                product_id = int(input("Enter product ID: "))
                image_filename = input("Enter image filename (e.g., product1.jpg): ")
                update_product_image(product_id, image_filename)
            except ValueError:
                print("Invalid product ID. Please enter a number.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 