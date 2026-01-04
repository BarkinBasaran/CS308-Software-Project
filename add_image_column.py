from app import create_app, db
from app.models import Product
from app.logger import log

app = create_app()

def add_image_column():
    with app.app_context():
        try:
            # Check if the column already exists
            columns = [column.name for column in Product.__table__.columns]
            if 'image' not in columns:
                log.info("Adding image column to products table...")
                # Add the image column
                with db.engine.connect() as connection:
                    connection.execute('ALTER TABLE products ADD COLUMN image VARCHAR(255);')
                db.session.commit()
                log.info("Image column added successfully")
            else:
                log.info("Image column already exists in products table")
        except Exception as e:
            log.error(f"Error adding image column: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    add_image_column() 