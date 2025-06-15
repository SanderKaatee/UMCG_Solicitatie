# app/__init__.py
from flask import Flask
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv

socketio = SocketIO()

def create_app():
    """Application factory pattern"""
    load_dotenv()
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Initialize SocketIO with CORS
    socketio.init_app(app, cors_allowed_origins="*", async_mode='eventlet')
    
    # Register routes
    from app.routes import register_routes
    register_routes(app, socketio)
    print("🔧 routes registered")

    return app