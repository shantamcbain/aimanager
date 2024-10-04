import os
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QToolBar
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from core.user_manager import user_manager
from core.user_manager.user_manager import current_user
from web_ui.web_app import app as flask_app
from utils.debug_utils import debug_print
from utils.server_thread import FlaskServerThread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#debug_print(f"Debug: Username is {username}")
logger = logging.getLogger(__name__)

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if event.is_directory:
            return
        self.callback(event.src_path)


class DesktopUI(QMainWindow):
    def __init__(self, flask_app, socketio, flask_thread, watch_path):
        super().__init__()
        self.flask_app = flask_app
        self.socketio = socketio
        self.flask_thread = flask_thread
        self.flask_thread.error.connect(self.show_error)
        self.flask_thread.finished.connect(self.server_finished)

        # Setup file observer
        self.observer = Observer()
        self.event_handler = FileChangeHandler(self.refresh_ide)

        # Check if the path exists before setting up the observer
        if os.path.exists(watch_path):
            self.observer.schedule(self.event_handler, path=watch_path, recursive=True)
            self.observer.start()
        else:
            logger.error(f"The directory {watch_path} does not exist.")

        self.initUI()


        
    def closeEvent(self, event):
        self.observer.stop()
        self.observer.join()
        event.accept()
        
    def refresh_ide(self, file_path):
        debug_print(f"File changed: {file_path}")
        # Add logic to refresh PyCharm file view
        # Placeholder for actual implementation. For example, using command line to trigger PyCharm refresh
        os.system("refresh-ide-command")  # Replace with the actual command as per your OS/IDE

    def initUI(self):
        self.setWindowTitle('AI Developer UI')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # Welcome label
        label = QLabel(f"Welcome, {current_user().username}")
        label = QLabel(f"Welcome, {current_user().username}")

        self.main_layout.addWidget(label)

        # Status label
        self.status_label = QLabel("Status: Idle", self)
        self.main_layout.addWidget(self.status_label)

        # Launch Web UI button
        self.launch_web_ui_button = QPushButton("Launch Web UI", self)
        self.launch_web_ui_button.clicked.connect(self.start_server)
        self.main_layout.addWidget(self.launch_web_ui_button)

        # Stop Web UI button
        self.stop_web_ui_button = QPushButton("Stop Web UI", self)
        self.stop_web_ui_button.clicked.connect(self.stop_server)
        self.stop_web_ui_button.setEnabled(False)
        self.main_layout.addWidget(self.stop_web_ui_button)

        # Add WebView for displaying web content
        self.web_view = QWebEngineView()
        self.main_layout.addWidget(self.web_view)

    def start_server(self):
        if self.flask_thread.isRunning():
            debug_print("Flask server already running.")
            return

        self.flask_thread.start()
        self.status_label.setText("Status: Web UI Running")
        self.launch_web_ui_button.setEnabled(False)
        self.stop_web_ui_button.setEnabled(True)
        debug_print("Flask server started.")

        # Load content when server starts
        self.load_web_content()

    def stop_server(self):
        if self.flask_thread.isRunning():
            self.flask_thread.terminate()
            self.status_label.setText("Status: Stopping Web UI...")
            self.stop_web_ui_button.setEnabled(False)
            self.launch_web_ui_button.setEnabled(True)
            debug_print("Flask server termination requested.")

    def server_finished(self):
        debug_print("Flask server has finished.")
        self.status_label.setText("Status: Idle")
        self.launch_web_ui_button.setEnabled(True)
        self.stop_web_ui_button.setEnabled(False)

    def show_error(self, error):
        debug_print(f"Error occurred: {error}")

    def load_web_content(self):
        # Here you would load the content from your Flask app
        # For simplicity, we'll load a static URL, but you should load dynamic content
        self.web_view.load(QUrl("http://localhost:5000"))  # Assuming your Flask server runs on port 5000
