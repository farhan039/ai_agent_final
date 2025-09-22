import os
import subprocess
import sys
import venv

VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"

def create_venv():
    print("[INFO] Creating virtual environment...")
    venv.create(VENV_DIR, with_pip=True)

def install_requirements():
    print("[INFO] Installing dependencies...")
    subprocess.check_call([os.path.join(VENV_DIR, "Scripts", "pip.exe"), "install", "-r", REQUIREMENTS_FILE])

def run_server():
    print("[INFO] Starting FastAPI server at http://127.0.0.1:4000 ...")
    subprocess.call([os.path.join(VENV_DIR, "Scripts", "uvicorn.exe"), "main:app", "--reload", "--port", "4000"])

if __name__ == "__main__":
    if not os.path.exists(VENV_DIR):
        create_venv()
    pip_path = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    try:
        subprocess.check_call([pip_path, "show", "fastapi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        install_requirements()
    run_server()

