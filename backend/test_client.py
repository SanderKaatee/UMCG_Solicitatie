import socketio
import time

# Create a standard Socket.IO client
sio = socketio.Client()

# Define event handlers for the client
@sio.event(namespace='/ws/chat')
def connect():
    print("✅ Connected to /ws/chat")
    sio.emit('message',
             {'id': 'test-from-cmd',
              'message': 'Hello from the Python test client!'},
             namespace='/ws/chat')

@sio.event
def connect_error(data):
    print("❌ The connection failed!", data)

@sio.event
def disconnect():
    print("👋 I'm disconnected from the server!")

# This will catch messages sent FROM the server
# It's the client-side equivalent of the server's @socketio.on('message')
@sio.on('message', namespace='/ws/chat')
def on_message(data):
    print(f"📩 Server sent a message: {data}")

if __name__ == '__main__':
    # Make sure your Flask server (run.py) is running first!
    try:
        print("--- Attempting to connect to ws://localhost:8001/ws/chat ---")
        sio.connect('ws://localhost:8001', namespaces=['/ws/chat'])
        
        # Wait for a bit to see incoming messages
        print("\n--- Waiting for 10 seconds to receive messages from the server... ---")
        sio.sleep(10)
        
        # Disconnect after we're done
        sio.disconnect()
        print("\n--- Test complete. ---")
        
    except socketio.exceptions.ConnectionError as e:
        print(f"❌ Could not connect to the server. Is it running? Error: {e}")