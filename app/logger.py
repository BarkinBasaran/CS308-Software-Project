import logging
import os
from logging.handlers import RotatingFileHandler
from flask import current_app

def setup_logger(app):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Set up file handler
    file_handler = RotatingFileHandler(
        'logs/chipmaster.log',
        maxBytes=10240,  # 10KB
        backupCount=10
    )
    
    # Set up formatter
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    
    # Set log level
    file_handler.setLevel(logging.INFO)
    
    # Add handler to app logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
    # Log application startup
    app.logger.info('ChipMaster startup')

def log_user_action(action, user_email=None, details=None):
    """Helper function to log user actions"""
    if user_email:
        current_app.logger.info(f'User {user_email}: {action}')
    else:
        current_app.logger.info(f'System: {action}')
    
    if details:
        current_app.logger.info(f'Details: {details}') 