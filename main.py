import speech_recognition as sr
import win32com.client
import webbrowser
import time
import requests
import threading
import os
import re
import json
import psutil
from datetime import datetime
import pywinstyles
import ctypes
import base64
import subprocess
import sys
import warnings
from PIL import Image

warnings.filterwarnings(
    "ignore",
    message=r"pkg_resources is deprecated as an API.*"
    category=UserWarning
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
try:
    from pytablericons import TablerIcons, OutlineIcon, FilledIcon
except ImportError:
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pytablericons", "pillow"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        from pytablericons import TablerIcons, OutlineIcon, FilledIcon
    except Exception:
        TablerIcons = None
        OutlineIcon = None
        FilledIcon = None
try:
    import pyautogui
except ImportError:
    pass
import customtkinter as ctk
from google import genai

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def get_secure_key(encoded_key)