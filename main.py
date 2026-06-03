from google import genai
import customtkinter as ctk
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
) # Just learned how to use this!!!!

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

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def get_secure_key(encoded_key):
    try:
        if not encoded_key:
            return encoded_key
        padding = "=" * (-len(encoded_key) % 4)
        return base64.urlsafe_b64decode(encoded_key + padding).decode()
    except Exception:
        return encoded_key


api_key = os.environ.get("GOOGLE_API_KEY", get_secure_key("QUl6YVN5QWlIb2Nhdi1pZm5kUnRnSEMzeFZiaDdrcXdUOTJsbkZV"))
newsapi = os.environ.get("NEWS_API_KEY", get_secure_key("NWMwY2MzMmJmOTBjNGFkNmE5NjRmNzY5NWZhNGU1Y2I"))

CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Aegis_Security_Vault", "user_config.json")

try:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
except Exception as e:
    print(f"Error initializing speaker: {e}")
    speaker = None

def clean_text(text):
    if not isinstance(text,str):
        return text
    text = re.sub(r'[*_`]', '', text)
    text = re.sub(r'#+\s?', '', text)
    return text.strip()

def stop_speaking():
    if speaker:
        try:
            import pythoncom
            pythoncom.CoInitialize()
            speaker.speak("", 3)
        except Exception:
            pass

def speak_async(text):
    if not text:
        return
    text = clean_text(text)
    if speaker:
        try:
            import pythoncom
            speaker.Speak(text, 1)
        except Exception:
            client = None

class CyberSentinelAI:
    def __init__(self):
        self.prompter = (
            "You are Aegis AI"
        )
