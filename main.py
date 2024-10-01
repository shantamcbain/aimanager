import sys
import os
from PyQt6.QtWidgets import QApplication
from desktop_ui.ui import DesktopUI
from web_ui.web_app import app as flask_app
from flask_socketio import SocketIO
import logging
from utils.debug_utils import debug_print
from utils.server_thread import FlaskServerThread

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

socketio = SocketIO(flask_app)

def main():
    debug_print("Checking for web UI mode...")

    if len(sys.argv) > 1 and sys.argv[1] == '--web' or os.environ.get('RUN_WEB_UI', 'false').lower() == 'true':
        debug_print("Setting up Web UI...")
        try:
            socketio.run(flask_app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
        except Exception as e:
            logger.error(f"Error starting Flask server: {e}")
    else:
        debug_print("Setting up Desktop UI...")
        try:
            app = QApplication(sys.argv)
            # Create an instance of FlaskServerThread
            flask_thread = FlaskServerThread(flask_app, socketio)
            desktop_ui = DesktopUI(flask_app, socketio, flask_thread)
            desktop_ui.show()
            sys.exit(app.exec())
        except Exception as e:
            logger.error(f"Error in desktop UI: {e}")

if __name__ == "__main__":
    main()