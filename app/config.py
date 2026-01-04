import os

class Config:
    SECRET_KEY = 'your-secret-key-here'  # In production, use a secure random key
    
    # MySQL configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'mysql')
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123321'
    MYSQL_DB = 'store_db'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Mail Ayarları
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'chipmasteremail@gmail.com'  # Change this
    MAIL_PASSWORD = 'vqnoplditfqbujje'  # Change this
    MAIL_DEFAULT_SENDER = 'chipmasteremail@gmail.com'

    INVOICE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'invoices')
