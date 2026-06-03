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
    stderr=subprocess.DEVNULL,
) # Just learned how to use this!!!! Used AI to learn about DEV_NULL etc.

try:
    from pytablericons import TablerIcons, OutlineIcon, FilledIcon
except ImportError:
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pytablericons", "pillow"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
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
            "You are Aegis AI: The Cyber Sentinel, a specialized guardian protecting students online. "
            "Provide empathetic, accurate, and structured advice about cyber safety, privacy, "
            "phishing, online bullying, and digital wellbeing. "
            "Keep responses concise and supportive. Command from the user: "
        )

def get_response(self, user_input, extra_context=""):
    if not client:
        return "Gemini API key is not configured or client failed to initialize. Please reboot the app or contact @ayaskant007 on Github."
    try:
        prompt = self.prompter + extra_context + " " + user_input
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error connecting to Aegis AI Brain: {e}"

class SystemCommander:
    def __init__(self, ui_callback):
        self.ui_callback = ui_callback

    def execute_command(self, command):
        command = command.lower()
        if "panic mode" in command:
            self._trigger_panic()
            return "Panic Mode Activated! All windows minimized and Safe Search opened."
        elif "password strength" in command:
            return "Please type a password in the chat to check its strength (Prefix with \"check: \")."
        elif "screen shield" in command:
            filepath = self._take_screenshot()
            return f"Screen Shield activated! Evidence saved to {filepath}"
        elif "system health" in command:
            return self._get_system_health()
        elif "safe vault" in command:
            self._open_vault()
            return "Safe Vault directory opened."
        elif "privacy news" in command:
            return self._get_privacy_news()
        elif "open google" in command:
            webbrowser.open("https://facebook.com")
            return "Opening Facebook..."
        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube..."
        else:
            return None
        
        def check_password_strength(self,password):
            strength = 0
            feedback = []
            if len(password) >= 8: 
                strength +=1
            else:
                feedback.append("Needs at least 8 characters.")
            if re.search(r"[A-Z]", password): 
                strength +=1
            else:
                feedback.append("Needs an uppercase letter.")
            if re.search(r"[a-z]", password): 
                strength +=1
            else:
                feedback.append("Needs a number.")
            if re.search(r"[@$!%*?&]", password): 
                strength+=1
            else:
                feedback.append("Needs a special character.")

            if strength == 5:
                return f"Password Strength: STRONG. Excellent job!!"
            elif strength >= 3:
                return f"Password Strength: MODERATE. {', '.join(feedback)}"

            def _trigger_panic(self):
                try:
                    pyautogui.hotkey('win', 'd')
                    time.sleep(0.5)
                    webbrowser.open("https://duckduckgo.com/")
                except Exception as e:
                    self.ui_callback("Aegis AI", f"Panic Mode failed to trigger: {e}")

            def _take_screenshot(self):
                try:
                    folder = os.path.join(os.path.expanduser("~"), "Cyber-Evidence")
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                        filename = f"Evidence_{datetime.now().strftime('%Y$m$d_%H%M%S')}.png"
                        filepath = os.path.join(folder, filename)
                        pyautogui.screenshot(filepath)
                        return filepath
                except Exception as e:
                    return f"Error: {e}"

            def _get_system_health(self):
                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtal_memory().percent
                return f"System Health: CPU @ {cpu}%, RAM @ {mem}%. Your system is stable."

            def _open_vault(self):
                folder            
        