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
)  # Just learned how to use this!!!! Used AI to learn about DEV_NULL etc.

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


api_key = os.environ.get("GOOGLE_API_KEY", get_secure_key(
    "QUl6YVN5QWlIb2Nhdi1pZm5kUnRnSEMzeFZiaDdrcXdUOTJsbkZV"))
newsapi = os.environ.get("NEWS_API_KEY", get_secure_key(
    "NWMwY2MzMmJmOTBjNGFkNmE5NjRmNzY5NWZhNGU1Y2I"))

CONFIG_FILE = os.path.join(os.path.expanduser(
    "~"), "Aegis_Security_Vault", "user_config.json")

try:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
except Exception as e:
    print(f"Error initializing speaker: {e}")
    speaker = None


def clean_text(text):
    if not isinstance(text, str):
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

        def check_password_strength(self, password):
            strength = 0
            feedback = []
            if len(password) >= 8:
                strength += 1
            else:
                feedback.append("Needs at least 8 characters.")
            if re.search(r"[A-Z]", password):
                strength += 1
            else:
                feedback.append("Needs an uppercase letter.")
            if re.search(r"[a-z]", password):
                strength += 1
            else:
                feedback.append("Needs a number.")
            if re.search(r"[@$!%*?&]", password):
                strength += 1
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
                    self.ui_callback(
                        "Aegis AI", f"Panic Mode failed to trigger: {e}")

            def _take_screenshot(self):
                try:
                    folder = os.path.join(
                        os.path.expanduser("~"), "Cyber-Evidence")
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
                folder = os.path.join(os.path.expanduser("~")), "Aegis_Security_Vault")
                    if not os.path.exists(folder):
                    os.makedirs(folder)
                    guides= {
                "Strong_Passwords.txt": "Aegis AI SECURITY GUIDE: STRONG PASSWORDS\n\n"
                "1. Length Matters: Aim for 12+ characters.\n"
                "2. Mix it up: Use uppercase, lowercase, numbers, and symbols.\n"
                "3. Avoid dictionary words or personal info (names, birthdays). \n"
                "4. Use a password manager to keep track of unique passwords.\n"
                "5. Enable Two-Factor Authentication (2FA) wherever possible.",

                "Reporting_Cyberbullying.txt": "Aegis AI SECURITY GUIDE: REPORTING CYBERBULLYING\n\n"
                "1. DO NOT RESPOND: Bullies want a reaction. Don't give it to them.\n"
                "2. SAVE THE EVIDENCE: Take screenshots of messages, posts, or comments. \n"
                "3. BLOCK AND REPORT: Use the platform's tools to block the user and report the behavior.\n"
                "4. TELL A TRUSTED ADULT: Reach out to a parent, teacher, or counselor for support."
                "5. SEEK HELP: If you feel overwhelmed, contact a helpline or counselor.",

                "Safe_Social_Media.txt": "Aegis AI SECURITY GUIDE: SAFE SOCIAL MEDIA\n\n"
                "1. Check your privacy settings: Ensure your accounts are set to \"Private\""
                "2. Think before you post: Once it's online, it's hard to take back.\n"
                "3. Be wary of strangers: Don't accept requests from people you don't know in real life.\n"
                "4. Protect personal info: Never share your address, phone number, or school name publicly.\n"
                "5. Report suspicious activity: If something feels off, report it immediately."
                }

                for filename, content in guides.items():
                    filepath = os.path.join(folder, filename)
                    with open(filepath, 'w') as f:
                        f.write(content)

            os.startfile(folder) if os.name == 'nt' else None

        def _get_privacy_news(self):
            if newsapi == "YOUR_NEWS_API_KEY":
                return "News API Key not configured."
            try:
                url = f"https://newsapi.org/v2/everything?q=cybersecurity OR data breach&sortBy=publishedAt&apiKey={newsapi}"
                r = requests.get(url)
                if r.status_code == 200:
                    articles = r.json().get('articles', [])[:3]
                    news_text = "Latest privacy news:\n"
                    for i, article in enumerate(articles, 1):
                        news_text += f"{i}. {article['title']}\n"
                    return news_text
                else:
                    return "Failed to fetch news."
            except Exception as e:
                return f"Error fetching news: {e}"

class AegisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.BG_COLOR = "#000000"
        self.SIDEBAR_COLOR = "#1C1C1E"
        self.ACCENT_COLOR = "#007AFF"
        self.PANEL_BG = "#1C1C1E"
        self.TEXT_COLOR = "#FFFFFF"
        self.TEXT_SECONDARY = "#8E8E93"
        self.BORDER_COLOR = "#38383A"

        self.configure(fg_color=self.BG_COLOR)
        ctk.set_appearance_mode("dark")
        self.title("Aegis AI")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        try:
            self.configure(fg_color=self.BG_COLOR)
            pywinstyles.apply_style(self, "acrylic")
            pywinstyles.change_header_color(self, color=self.BG_COLOR)
        except Exception as e:
            print(f"Glass Implementation error: {e}")
            self.configure(fg_color=self.BG_COLOR)
            self.brain = CyberSentinelAI()
            self.commander = SystemCommander(self.log_message)
            self.recognizer = sr.Recognizer()
            self.listening = False
            self.user_name = None
            self.quiz_mode = False
            self.is_speaking = False
            self.speech_cancelled = threading.Event()
            self.stop_speech_btn = None
            self.ai_icon_image = None
            self.send_icon_image = None
            self.mic_icon_image = None
            self.mic_icon_active_image = None
            self.input_icon_only = False
            self._input_resize_job = None
            self._hover_jobs = {}
            self.ai_icon_title = "Aegis AI"
            if TablerIcons is not None and OutlineIcon is not None and FilledIcon is not None:
                try:
                    icon_img = TablerIcons.load(OutlineIcon.SHIELD_LOCK, size = 16, color=self.ACCENT_COLOR, stroke_width=1.9)
                    self.ai_icon_image = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size =(16,16))
                    self.ai_icon_title = "Tabler Shield Lock"
                except Exception:
                    self.ai_icon_image = None

                try:
                    icon_dir = os.path.join(os.path.expanduser("~"), "Aegis_Security_Vault", "ui_icons")
                    os.makedirs(icon_dir, exist_ok=True)

                    send_path = os.path.join(icon_dir, "send_icon.png")
                    send_img = TablerIcons.load(FilledIcon.CIRCLE_ARROW_UP, size=28, color="#FFFFFF", stroke_width=2.0)
                    send_loaded = Image.open(send_path).convert("RGBA")
                    self.send_icon_image = ctk.CTkImage(light_image=send_loaded, dark_image=send_loaded, size=(22,22))
                except Exception:
                    self.send_icon_image = None

                try:
                    mic_path = os.path.join(icon_dir, "mic_icon.png")
                    mic_img = TablerIcons.load(FilledIcon.MICROPHONE, size=28, color="#E5E5EA", stoke_width=2.0)
                    mic_img.save(mic_path)
                    mic_loaded = Image.open(mic_path).convert("RGBA")
                    self.mic_icon_image = ctk.CTkImage(light_image=mic_loaded, dark_image=mic_loaded, size=(22,22))
                except Exception:
                    self.mic_icon_image = None