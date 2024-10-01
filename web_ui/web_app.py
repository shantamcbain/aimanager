from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json
from core.page_manager import load_page_content, get_page_title, get_page_content
from core.user_manager.user_manager import user_manager
from utils.debug_utils import debug_print

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

# Debug print to check if app routes are being loaded
debug_print("Loading app routes...")

@app.route('/')
def index():
    debug_print("Index route called")
    page_data = load_page_content('index')
    debug_print(f"Page data: {page_data}")
    if page_data:
        title = get_page_title(page_data)
        content = get_page_content(page_data)
        debug_print(f"Rendering with title: {title}")
        return render_template('base.html', title=title, content=content)
    debug_print("No page data found")
    return render_template('404.html'), 404

@app.route('/<path:page_path>', endpoint='dynamic_content_page')
def dynamic_content(page_path):
    debug_print(f"Requesting page: {page_path}")
    page_data = load_page_content(page_path)
    if page_data:
        title = get_page_title(page_data)
        content = get_page_content(page_data)
        return render_template('base.html', title=title, content=content)
    return render_template('404.html'), 404

@app.context_processor
def inject_user():
    return dict(current_user=user_manager.current_user)

@socketio.on('connect')
def handle_connect():
    debug_print(f"Client connected with session ID: {request.sid}")
    emit('connect_response', {'data': 'Connected'})

@socketio.on('message')
def handle_message(data):
    debug_print(f"Received message: {data}")
    emit('response', {'data': f'Server received: {data}'}, broadcast=True)

if __name__ == '__main__':
    debug_print("Starting Flask server with SocketIO...")
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)