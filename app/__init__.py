from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from app.config import Config
from app.logger import setup_logger
from flask_login import LoginManager
import os

import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)
    print("DATABASE_URL from env:", os.environ.get('DATABASE_URL'))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "mysql+pymysql://root:123321@localhost:3306/store_db"
    print("SQLALCHEMY_DATABASE_URI after setting:", app.config['SQLALCHEMY_DATABASE_URI'])
    db.init_app(app)
    mail.init_app(app)
    
    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Set up logging
    setup_logger(app)
    
    # Ensure invoice folder exists
    invoice_folder = app.config.get('INVOICE_FOLDER')
    if invoice_folder:
        os.makedirs(invoice_folder, exist_ok=True)
    
    from app.routes import main
    app.register_blueprint(main)
    from app.blueprints.product_manager import product_manager as product_manager_bp
    app.register_blueprint(product_manager_bp)
    from app.blueprints.sales_manager import sales_manager as sales_manager_bp
    app.register_blueprint(sales_manager_bp)
    from app.blueprints.customer import customer as customer_bp
    app.register_blueprint(customer_bp)
    return app