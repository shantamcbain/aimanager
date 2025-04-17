from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from core.page_manager import PageManager, get_page_title, get_page_content
from core.user_manager.user_manager import user_manager, current_user
from utils.debug_utils import debug_print

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

# Initialize PageManager inside application context
with app.app_context():
    page_manager = PageManager()

debug_print("Loading app routes...")

# Context processor to make current_user available globally to templates
@app.context_processor
def inject_user():
    return dict(current_user=current_user())

@app.route('/')
def index():
    page_data = page_manager.get_page('index')
    if page_data:
        header = get_page_title(page_data)
        content = get_page_content(page_data)
        description = page_data.get('description', '')
        keywords = page_data.get('keywords', [])
        javascript = page_data.get('javascript', '')
        # Assuming pagedisplayname is a field in your page_data
        pagedisplayname = page_data.get('pagedisplayname', 'Home')  # Default to 'Home' if not found
        return render_template('base.html', header=header, content=content, description=description,
                              keywords=keywords, javascript=javascript, pagedisplayname=pagedisplayname)
    return render_template('404.html'), 404

@app.route('/<path:page_path>')
def dynamic_content(page_path):
    page_data = page_manager.get_page(page_path)
    if page_data:
        header = get_page_title(page_data)
        content = get_page_content(page_data)
        description = page_data.get('description', '')
        keywords = page_data.get('keywords', [])
        javascript = page_data.get('javascript', '')
        pagedisplayname = page_data.get('pagedisplayname', page_path.capitalize())  # Default to capitalized page path
        return render_template('base.html', header=header, content=content, description=description,
                              keywords=keywords, javascript=javascript, pagedisplayname=pagedisplayname)
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

@app.route('/pagemanagement/<int:page_id>', methods=['GET', 'POST'])
def manage_page(page_id):
    page = page_manager.get_page(page_id)
    if not page:
        return "Page not found", 404

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        success = page_manager.modify_page(page_id, title, content)
        return jsonify({"message": f"Page modified: {'Success' if success else 'Failed'}"})

    # Render specific page management template for GET requests
    return render_template('manage_page.html', page=page)

# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app, debug=True)