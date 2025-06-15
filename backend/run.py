# Keep this here. It's aggressive and good practice when debug issues occur.
import eventlet
eventlet.monkey_patch()

from app import create_app, socketio

# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    # The final, key change is to disable the problematic reloader
    socketio.run(app, debug=True, port=8001, use_reloader=False)