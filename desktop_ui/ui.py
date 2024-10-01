#deskto_ui/ui.py
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from core.user_manager import user_manager
from web_ui.web_app import app as flask_app
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from core.user_manager import user_manager
from core.user_manager.user_manager import current_user
from utils.debug_utils import debug_print
from utils.server_thread import FlaskServerThread
debug_print(f"Debug: Username is {current_user().username}")
class DesktopUI(QMainWindow):
    def __init__(self, flask_app, socketio, flask_thread):
        super().__init__()
        self.flask_app = flask_app
        self.socketio = socketio
        self.flask_thread = flask_thread
        self.flask_thread.error.connect(self.show_error)
        self.flask_thread.finished.connect(self.server_finished)
        self.initUI()

    def initUI(self):
        # Setup main window
        self.setWindowTitle('AI Developer UI')
        self.setGeometry(100, 100, 800, 600)
        label = QLabel(f"Welcome, {current_user().username}")


        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        # Add the label to the main layout

        self.main_layout.addWidget(label)

        # Add status label
        self.status_label = QLabel("Status: Idle", self)
        self.main_layout.addWidget(self.status_label)

        # Add button to launch web UI
        self.launch_web_ui_button = QPushButton("Launch Web UI", self)
        self.launch_web_ui_button.clicked.connect(self.start_server)
        self.main_layout.addWidget(self.launch_web_ui_button)

        # Add button to stop web UI
        self.stop_web_ui_button = QPushButton("Stop Web UI", self)
        self.stop_web_ui_button.clicked.connect(self.stop_server)
        self.stop_web_ui_button.setEnabled(False)
        self.main_layout.addWidget(self.stop_web_ui_button)

    def start_server(self):
        debug_print("Attempting to start Flask server with web_app routes...")
        if self.flask_thread.isRunning():
            debug_print("Flask server already running.")
            return
        self.flask_thread.start()
        self.status_label.setText("Status: Web UI Running")
        self.launch_web_ui_button.setEnabled(False)
        self.stop_web_ui_button.setEnabled(True)
        debug_print("Flask server started with web_app routes.")

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
        # Here you might want to show a message box or log the errorrom core.user_manager.user_manager import current_user
from utils.debug_utils import debug_print
from utils.server_thread import FlaskServerThread
debug_print(f"Debug: Username is {current_user().username}")
class DesktopUI(QMainWindow):
    def __init__(self, flask_app, socketio, flask_thread):
        super().__init__()
        self.flask_app = flask_app
        self.socketio = socketio
        self.flask_thread = flask_thread
        self.flask_thread.error.connect(self.show_error)
        self.flask_thread.finished.connect(self.server_finished)
        self.initUI()

    def initUI(self):
        # Setup main window
        self.setWindowTitle('AI Developer UI')
        self.setGeometry(100, 100, 800, 600)
        label = QLabel(f"Welcome, {current_user().username}")


        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        # Add the label to the main layout

        self.main_layout.addWidget(label)

        # Add status label
        self.status_label = QLabel("Status: Idle", self)
        self.main_layout.addWidget(self.status_label)

        # Add button to launch web UI
        self.launch_web_ui_button = QPushButton("Launch Web UI", self)
        self.launch_web_ui_button.clicked.connect(self.start_server)
        self.main_layout.addWidget(self.launch_web_ui_button)

        # Add button to stop web UI
        self.stop_web_ui_button = QPushButton("Stop Web UI", self)
        self.stop_web_ui_button.clicked.connect(self.stop_server)
        self.stop_web_ui_button.setEnabled(False)
        self.main_layout.addWidget(self.stop_web_ui_button)

    def start_server(self):
        debug_print("Attempting to start Flask server...")  # Changed to debug_print for consistency
        if self.flask_thread.isRunning():  # Changed to check if thread is running
            debug_print("Flask server already running.")
            return

        # Start the Flask server thread
        self.flask_thread.start()  # Corrected to start the thread, not call start_server
        self.status_label.setText("Status: Web UI Running")
        self.launch_web_ui_button.setEnabled(False)
        self.stop_web_ui_button.setEnabled(True)
        debug_print("Flask server started.")

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
        # Here you might want to show a message box or log the error