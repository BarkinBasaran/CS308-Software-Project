import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db

app = create_app()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "mysql+pymysql://root:123321@localhost:3306/store_db"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='localhost', port=3060)

