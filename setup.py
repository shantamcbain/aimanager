import subprocess
import sys
import os
import venv


def create_venv(venv_path):
    if not os.path.exists(os.path.join(venv_path, 'bin', 'python')):
        print("Creating virtual environment...")
        venv.create(venv_path, with_pip=True)
        print("Virtual environment created.")
    return os.path.join(venv_path, 'bin', 'python')


def install_requirements(venv_python):
    try:
        subprocess.check_call([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All dependencies installed successfully.")
        return True
    except Exception as e:
        print(f"Failed to install dependencies. Error: {e}")
        return False


def run_main(venv_python):
    try:
        subprocess.run([venv_python, "web_app.py"])
    except Exception as e:
        print(f"Failed to run main script. Error: {e}")


if __name__ == "__main__":
    venv_path = os.path.join(os.path.dirname(__file__), 'venv')
    venv_python = create_venv(venv_path)

    if install_requirements(venv_python):
        print("Now running the main application...")
        run_main(venv_python)


def setup_flask():
    return None


def setup_qt():
    return None