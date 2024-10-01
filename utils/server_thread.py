from PyQt6.QtCore import QThread, pyqtSignal
from flask import Flask
from flask_socketio import SocketIO

class FlaskServerThread(QThread):
    error = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, flask_app, socketio):
        super().__init__()
        self.flask_app = flask_app
        self.socketio = socketio

    def run(self):
        try:
            self.socketio.run(self.flask_app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
        except Exception as e:
            self.error.emit(f"Error starting Flask server: {str(e)}")
        finally:
            self.finished.emit()