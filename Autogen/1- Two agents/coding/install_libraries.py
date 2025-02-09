# filename: install_libraries.py
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "matplotlib"])