import sys
import os
import subprocess
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

# Determine the base directory of your application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    debug_print("Checking for web UI mode...")

    # Check and install dependencies
    install_dependencies()

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
            flask_thread = FlaskServerThread(flask_app, socketio)

            # Pass the correct relative path to aimanager
            watch_path = os.path.join(BASE_DIR, 'aimanager')
            desktop_ui = DesktopUI(flask_app, socketio, flask_thread, watch_path)
            desktop_ui.show()
            sys.exit(app.exec())
        except Exception as e:
            logger.error(f"Error in desktop UI: {e}")


def install_dependencies():

    try:

        with open('requirements.txt', 'r') as file:

            packages = file.read().splitlines()



        for package in packages:

            try:

                subprocess.check_call([sys.executable, "-m", "pip", "install", package])

                print(f"Successfully installed {package}")

            except subprocess.CalledProcessError:

                print(f"Failed to install {package}")

    except FileNotFoundError:

        print("requirements.txt not found.")
if __name__ == "__main__":
    main()