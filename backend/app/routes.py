# app/routes.py
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import traceback
from app.openai_client import OpenAIClient
from app.rate_limiter import RateLimiter

def register_routes(app: Flask, socketio: SocketIO):
    """Register all application routes"""
    
    # --- CORS Configuration ---
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    rate_limiter = RateLimiter()
    openai_client = OpenAIClient()
    
    # --- Health Check Endpoints (Unchanged) ---
    @app.route('/healthz')
    def health_check():
        """Health check endpoint"""
        return 'OK', 200
    
    @app.route('/api/health')
    def api_health():
        """API health check with JSON response"""
        return jsonify({
            'status': 'healthy',
            'service': 'sander-kaatee-backend'
        })
        
    # --- HTTP Chat Endpoint (with Conversation History) ---
    @app.route('/api/chat', methods=['POST'])
    def handle_chat():
        """Handles a chat request with conversation history via HTTP POST."""
        try:
            client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            
            if not rate_limiter.is_allowed(client_ip):
                reset_time = rate_limiter.get_reset_time(client_ip)
                return jsonify({
                    'error': 'rate_limit',
                    'message': 'You have made too many requests. Please try again later.',
                    'reset_time': reset_time
                }), 429
                
            data = request.get_json()
            if not data or 'message' not in data:
                return jsonify({'error': 'Invalid request', 'message': 'Missing message field.'}), 400
                
            message_text = data['message'].strip()
            
            if not message_text:
                return jsonify({'error': 'Invalid request', 'message': 'Message cannot be empty.'}), 400

            # Get conversation history from request (optional)
            conversation_history = data.get('history', [])
            
            # Get response with conversation context
            response_content = openai_client.get_chat_response_with_history(
                message_text, 
                conversation_history
            )
            
            return jsonify({'content': response_content})

        except Exception as e:
            print(f"--- AN EXCEPTION OCCURRED IN /api/chat ---")
            traceback.print_exc()
            print(f"-----------------------------------------")
            return jsonify({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred on the server.'
            }), 500