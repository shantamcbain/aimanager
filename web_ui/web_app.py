from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from core.page_manager import PageManager, get_page_title, get_page_content
from core.user_manager.user_manager import user_manager
from utils.debug_utils import debug_print

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

# Initialize PageManager inside application context
with app.app_context():
    page_manager = PageManager()

# Debug print to check if app routes are being loaded
debug_print("Loading app routes...")

@app.route('/')
def index():
    debug_print("Index route called")
    # Use get_page instead of get_page_content since get_page_content is not a method of PageManager
    page_data = page_manager.get_page('index')
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
    # Use get_page instead of load_page_content since load_page_content is not defined
    page_data = page_manager.get_page(page_path)
    if page_data:
        title = get_page_title(page_data)
        content = get_page_content(page_data)
        return render_template('base.html', title=title, content=content)
    return render_template('404.html'), 404

@app.route('/pagemanagement', methods=['GET', 'POST'])
def manage_pages():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            title = request.form.get('title')
            content = request.form.get('content')
            new_id = page_manager.add_page(title, content)
            return jsonify({"message": f"Page added with ID: {new_id}"})
        elif action == 'modify':
            page_id = request.form.get('page_id')
            title = request.form.get('title')
            content = request.form.get('content')
            success = page_manager.modify_page(page_id, title, content)
            return jsonify({"message": f"Page modified: {'Success' if success else 'Failed'}"})
        elif action == 'delete':
            page_id = request.form.get('page_id')
            success = page_manager.delete_page(page_id)
            return jsonify({"message": f"Page deleted: {'Success' if success else 'Failed'}"})
    # GET request to show the page management interface
    pages = page_manager.list_pages()
    return render_template('manage_pages.html', pages=pages)

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