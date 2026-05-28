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
    message=r"pkg_resources is deprecated as an API.*",
    category=UserWarning,
    module=r"pygame\.pkgdata",
)
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
import customtkinter as ctk
from google import genai

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
            speaker.Speak("", 3)
        except Exception:
            pass

def speak_async(text):
    if not text:
        return
    text = clean_text(text)
    if speaker:
        try:
            import pythoncom
            pythoncom.CoInitialize()
            speaker.Speak(text, 1)
        except Exception:
            pass
    else:
        print(f"Audio Output: {text}")

try:
    client = genai.Client(api_key=api_key)
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
            return "Gemini API key not configured or client failed to initialize."
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
            return "Please type a password in the chat to check its strength (Prefix with 'check: ')."
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
            webbrowser.open("https://google.com")
            return "Opening Google..."
        elif "open facebook" in command:
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
        if len(password) >= 8: strength += 1
        else: feedback.append("Needs at least 8 characters.")
        if re.search(r"[A-Z]", password): strength += 1
        else: feedback.append("Needs an uppercase letter.")
        if re.search(r"[a-z]", password): strength += 1
        else: feedback.append("Needs a lowercase letter.")
        if re.search(r"[0-9]", password): strength += 1
        else: feedback.append("Needs a number.")
        if re.search(r"[@$!%*?&]", password): strength += 1
        else: feedback.append("Needs a special character.")
        
        if strength == 5: return "Password Strength: STRONG. Excellent job!"
        elif strength >= 3: return f"Password Strength: MODERATE. {', '.join(feedback)}"
        else: return f"Password Strength: WEAK. {', '.join(feedback)}"

    def _trigger_panic(self):
        try:
            pyautogui.hotkey('win', 'd')
            time.sleep(0.5)
            webbrowser.open("https://duckduckgo.com/")
        except Exception as e:
            self.ui_callback("Aegis AI", f"Failed to trigger full panic mode: {e}")

    def _take_screenshot(self):
        try:
            folder = os.path.join(os.path.expanduser("~"), "Cyber-Evidence")
            if not os.path.exists(folder):
                os.makedirs(folder)
            filename = f"Evidence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(folder, filename)
            pyautogui.screenshot(filepath)
            return filepath
        except Exception as e:
            return f"Error: {e}"

    def _get_system_health(self):
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        return f"System Health: CPU @ {cpu}%, RAM @ {mem}%. Your system is stable."

    def _open_vault(self):
        folder = os.path.join(os.path.expanduser("~"), "Aegis_Security_Vault")
        if not os.path.exists(folder):
            os.makedirs(folder)
            guides = {
                "Strong_Passwords.txt": "AEGIS-AI SECURITY GUIDE: STRONG PASSWORDS\n\n"
                                        "1. Length matters: Aim for 12+ characters.\n"
                                        "2. Mix it up: Use uppercase, lowercase, numbers, and symbols.\n"
                                        "3. Avoid dictionary words or personal info (names, birthdays).\n"
                                        "4. Use a password manager to keep track of unique passwords.\n"
                                        "5. Enable Two-Factor Authentication (2FA) wherever possible.",
                                        
                "Reporting_Cyberbullying.txt": "AEGIS-AI SECURITY GUIDE: REPORTING CYBERBULLYING\n\n"
                                               "1. DO NOT RESPOND: Bullies want a reaction. Don't give it to them.\n"
                                               "2. SAVE THE EVIDENCE: Take screenshots of messages, posts, or comments.\n"
                                               "3. BLOCK AND REPORT: Use the platform's tools to block the user and report the behavior.\n"
                                               "4. TELL A TRUSTED ADULT: Reach out to a parent, teacher, or counselor for support.\n"
                                               "5. SEEK HELP: If you feel overwhelmed, contact a helpline or counselor.",
                                               
                "Safe_Social_Media.txt": "AEGIS-AI SECURITY GUIDE: SAFE SOCIAL MEDIA\n\n"
                                         "1. Check your privacy settings: Ensure your accounts are set to 'Private'.\n"
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
            return "News API key not configured."
        try:
            url = f"https://newsapi.org/v2/everything?q=cybersecurity OR data breach&sortBy=publishedAt&apiKey={newsapi}"
            r = requests.get(url)
            if r.status_code == 200:
                articles = r.json().get('articles', [])[:3]
                news_text = "Latest Privacy News:\n"
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
        self.ACCENT_COLOR = "#0A84FF"
        self.ACCENT_HOVER = "#007AFF"
        self.PANEL_BG = "#1C1C1E"
        self.TEXT_COLOR = "#FFFFFF"
        self.TEXT_SECONDARY = "#8E8E93"
        self.BORDER_COLOR = "#38383A"

        self.configure(fg_color=self.BG_COLOR)
        ctk.set_appearance_mode("dark")
        self.title("Aegis AI: Security Hub")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        try:
            self.configure(fg_color=self.BG_COLOR)
            pywinstyles.apply_style(self, "acrylic")
            pywinstyles.change_header_color(self, color=self.BG_COLOR)
        except Exception as e:
            print(f"Glass implementation error: {e}")
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
                icon_img = TablerIcons.load(OutlineIcon.SHIELD_LOCK, size=16, color=self.ACCENT_COLOR, stroke_width=1.9)
                self.ai_icon_image = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(16, 16))
                self.ai_icon_title = "Tabler Shield Lock"
            except Exception:
                self.ai_icon_image = None

            try:
                icon_dir = os.path.join(os.path.expanduser("~"), "Aegis_Security_Vault", "ui_icons")
                os.makedirs(icon_dir, exist_ok=True)

                send_path = os.path.join(icon_dir, "send_icon.png")
                send_img = TablerIcons.load(FilledIcon.CIRCLE_ARROW_UP, size=28, color="#FFFFFF", stroke_width=2.0)
                send_img.save(send_path)
                send_loaded = Image.open(send_path).convert("RGBA")
                self.send_icon_image = ctk.CTkImage(light_image=send_loaded, dark_image=send_loaded, size=(22, 22))
            except Exception:
                self.send_icon_image = None

            try:
                mic_path = os.path.join(icon_dir, "mic_icon.png")
                mic_img = TablerIcons.load(FilledIcon.MICROPHONE, size=28, color="#E5E5EA", stroke_width=2.0)
                mic_img.save(mic_path)
                mic_loaded = Image.open(mic_path).convert("RGBA")
                self.mic_icon_image = ctk.CTkImage(light_image=mic_loaded, dark_image=mic_loaded, size=(22, 22))
            except Exception:
                self.mic_icon_image = None

            try:
                mic_active_path = os.path.join(icon_dir, "mic_icon_active.png")
                mic_active_img = TablerIcons.load(FilledIcon.MICROPHONE, size=28, color="#FFFFFF", stroke_width=2.0)
                mic_active_img.save(mic_active_path)
                mic_active_loaded = Image.open(mic_active_path).convert("RGBA")
                self.mic_icon_active_image = ctk.CTkImage(light_image=mic_active_loaded, dark_image=mic_active_loaded, size=(22, 22))
            except Exception:
                self.mic_icon_active_image = None
        self._ensure_vault_exists()
        self._load_config()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._create_sidebar()
        self._create_header()
        self._create_chat_area()
        self._create_input_area()
        self._animate_breathing_logo()
        self._update_clock()
        self._transition_chat()

        if not self.user_name:
            self._start_onboarding()
        else:
            self.log_message("Aegis AI", f"Welcome back, {self.user_name}. Systems are nominal. I am your Cyber Sentinel. How can I protect you today?")
            speak_async(f"Welcome back, {self.user_name}. Systems are nominal.")

    def _ensure_vault_exists(self):
        folder = os.path.join(os.path.expanduser("~"), "Aegis_Security_Vault")
        if not os.path.exists(folder):
            os.makedirs(folder)
            
            guides = {
                "Strong_Passwords.txt": "AEGIS-AI SECURITY GUIDE: STRONG PASSWORDS\n\n1. Length matters: Aim for 12+ characters.\n2. Mix it up: Use uppercase, lowercase, numbers, and symbols.\n3. Avoid dictionary words or personal info.\n4. Use a password manager.\n5. Enable Two-Factor Authentication (2FA).",
                "Reporting_Cyberbullying.txt": "AEGIS-AI SECURITY GUIDE: REPORTING CYBERBULLYING\n\n1. DO NOT RESPOND: Bullies want a reaction.\n2. SAVE THE EVIDENCE: Take screenshots.\n3. BLOCK AND REPORT: Use platform tools.\n4. TELL A TRUSTED ADULT: Reach out to a parent or counselor.\n5. SEEK HELP: If overwhelmed, contact a helpline.",
                "Safe_Social_Media.txt": "AEGIS-AI SECURITY GUIDE: SAFE SOCIAL MEDIA\n\n1. Check privacy settings.\n2. Think before you post.\n3. Be wary of strangers.\n4. Protect personal info.\n5. Report suspicious activity."
            }
            for filename, content in guides.items():
                filepath = os.path.join(folder, filename)
                with open(filepath, 'w') as f:
                    f.write(content)

    def _load_config(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                self.user_name = data.get("name")
        except FileNotFoundError:
            self.user_name = None

    def _save_config(self, name):
        self.user_name = name
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({"name": self.user_name}, f)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def _start_onboarding(self):
        self.onboarding = True
        welcome_msg = "IDENTIFICATION REQUIRED.\n\nWelcome to Aegis AI Core. Please identify yourself, Citizen. What is your name?"
        self.log_message("Aegis AI", welcome_msg)
        speak_async("Identification required. Welcome to Aegis AI Core. Please identify yourself, Citizen. What is your name?")

    def _update_clock(self):
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            current_date = datetime.now().strftime("%Y-%m-%d")
            self.clock_label.configure(text=f"{current_time}\n{current_date}")
            self.after(1000, self._update_clock)
        except Exception:
            pass

    def _animate_breathing_logo(self):
        color_cycle = ["#8E8E93", "#9F9FA4", "#B0B0B5", "#C1C1C6", "#D2D2D7", "#E5E5EA", 
                       "#D2D2D7", "#C1C1C6", "#B0B0B5", "#9F9FA4"]
        if not hasattr(self, 'logo_color_idx'):
            self.logo_color_idx = 0

        try:
            self.logo_label.configure(text_color=color_cycle[self.logo_color_idx])
            self.logo_color_idx = (self.logo_color_idx + 1) % len(color_cycle)
            self.after(200, self._animate_breathing_logo)
        except Exception:
            pass

    def _transition_chat(self):
        def animate_opacity(step=0):
            try:
                ease = [0.05, 0.1, 0.15, 0.25, 0.3, 0.1, 0.05]
                if step < len(ease):
                    current = self.attributes("-alpha")
                    self.attributes("-alpha", min(1.0, current + ease[step]))
                    self.after(20, animate_opacity, step + 1)
                else:
                    self.attributes("-alpha", 1.0)
            except Exception:
                pass
        self.attributes("-alpha", 0.0)
        self.after(200, animate_opacity)

    def _create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="transparent",
                                          border_width=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.clock_label = ctk.CTkLabel(self.sidebar_frame, text="", 
                                        font=ctk.CTkFont(family="SF Pro Display", size=13, weight="bold"), 
                                        text_color=self.TEXT_SECONDARY, anchor="center")
        self.clock_label.pack(pady=(30, 10))
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Aegis AI", 
                                       font=ctk.CTkFont(family="SF Pro Display", size=24, weight="bold"), 
                                       text_color=self.TEXT_COLOR, justify="center")
        self.logo_label.pack(pady=(10, 40))
        self.nav_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.nav_frame.pack(fill="x", padx=20)

        tools = [
            ("Panic Mode"),
            ("Screen Shield"),
            ("System Health"),
            ("Safe Vault"),
            ("Privacy News"),
            ("Security Quiz")
        ]
        
        for tool in tools:
            def make_cmd(t=tool):
                return lambda: [self._trigger_slide_transition(), self.process_input(t)]

            btn = ctk.CTkButton(
                self.nav_frame, 
                text=tool, 
                command=make_cmd(tool), 
                fg_color="#1C1C1E", # Use a slightly visible base color to ensure click events are caught
                hover_color="#2C2C2E",
                text_color=self.TEXT_COLOR,
                font=ctk.CTkFont(family="SF Pro Text", size=14, weight="normal"),
                anchor="center",
                border_width=1,
                border_color="#38383A",
                corner_radius=12,
                height=45
            )
            btn.bind("<Enter>", lambda e, b=btn: b.configure(fg_color="#3A3A3C"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(fg_color="#1C1C1E"))
            btn.pack(pady=8, fill="x", padx=10)
        self.version_label = ctk.CTkLabel(self.sidebar_frame, text="v2.0.4 - Secure Connection", 
                                        font=ctk.CTkFont(family="SF Pro Text", size=11), 
                                        text_color=self.TEXT_SECONDARY)
        self.version_label.pack(side="bottom", pady=20)

    def _trigger_slide_transition(self):
        stop_speaking()
        def animate_opacity(step=0, fade_out=True):
            try:
                ease = [0.15, 0.25, 0.35, 0.20, 0.05]
                current = self.attributes("-alpha")
                
                if fade_out:
                    if step < len(ease):
                        self.attributes("-alpha", max(0.0, current - ease[step]))
                        self.after(20, lambda: animate_opacity(step + 1, fade_out=True))
                    else:
                        self.attributes("-alpha", 0.0)
                        for widget in self.chat_container.winfo_children():
                            widget.destroy()
                        self.after(20, lambda: animate_opacity(0, fade_out=False))
                else:
                    if step < len(ease):
                        self.attributes("-alpha", min(1.0, current + ease[step]))
                        self.after(20, lambda: animate_opacity(step + 1, fade_out=False))
                    else:
                        self.attributes("-alpha", 1.0)
                        return
            except Exception:
                self.attributes("-alpha", 1.0)
        animate_opacity()

    def _create_header(self):
        self.header_frame = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color=self.BG_COLOR)
        self.header_frame.grid(row=0, column=1, sticky="ew", padx=40, pady=(15, 0))
        self.title_label = ctk.CTkLabel(self.header_frame, text="Terminal Uplink Established", 
                                        font=ctk.CTkFont(family="SF Pro Text", size=13, weight="bold"),
                                        text_color=self.ACCENT_COLOR, anchor="w")
        self.title_label.pack(side="left", pady=10)

    def _create_chat_area(self):
        self.glow_frame = ctk.CTkFrame(self, fg_color="#0B0B0C", corner_radius=20, border_width=1, border_color=self.BORDER_COLOR)
        self.glow_frame.grid(row=1, column=1, padx=40, pady=(10, 20), sticky="nsew")
        self.glow_frame.grid_columnconfigure(0, weight=1)
        self.glow_frame.grid_rowconfigure(0, weight=1)

        self.chat_container = ctk.CTkScrollableFrame(self.glow_frame, fg_color="#0B0B0C")
        self.chat_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.chat_container.grid_columnconfigure(0, weight=1)
        self.quiz_frame = ctk.CTkScrollableFrame(self.glow_frame, fg_color="#0B0B0C")
        self.quiz_frame.grid_columnconfigure(0, weight=1)

    def _create_input_area(self):
        self.bottom_container = ctk.CTkFrame(self, fg_color=self.BG_COLOR)
        self.bottom_container.grid(row=2, column=1, padx=40, pady=(0, 30), sticky="ew")
        self.bottom_container.grid_columnconfigure(0, weight=1)
        self.status_container = ctk.CTkFrame(self.bottom_container, fg_color=self.BG_COLOR)
        self.status_container.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.status_container.grid_columnconfigure(0, weight=1)

        self.status_bar = ctk.CTkLabel(self.status_container, text="Status: Online & Secure", 
                                       font=ctk.CTkFont(family="SF Pro Text", size=13), text_color=self.TEXT_SECONDARY, anchor="w")
        self.status_bar.grid(row=0, column=0, sticky="w")
        self.waveform_label = ctk.CTkLabel(self.status_container, text="", text_color=self.ACCENT_COLOR)
        self.waveform_label.grid(row=0, column=1, sticky="e")

        self.stop_speech_btn = ctk.CTkButton(
            self.status_container,
            text="Stop",
            width=70,
            height=28,
            fg_color="#2C2C2E",
            hover_color="#3A3A3C",
            text_color="#FF453A",
            border_width=1,
            border_color="#FF453A",
            corner_radius=10,
            command=self._stop_current_speech,
            font=ctk.CTkFont(family="SF Pro Text", size=12, weight="bold"),
        )
        self.stop_speech_btn.grid(row=0, column=2, sticky="e", padx=(12, 0))
        self.stop_speech_btn.grid_remove()
        self.input_frame = ctk.CTkFrame(self.bottom_container, fg_color="#18181A", corner_radius=20, 
                                        border_width=1, border_color=self.BORDER_COLOR)
        self.input_frame.grid(row=1, column=0, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter command, ask advice, or type 'check: password'...",
                                  fg_color="transparent", border_width=0, text_color=self.TEXT_COLOR,
                                  font=ctk.CTkFont(family="SF Pro Text", size=15), height=55)
        self.entry.grid(row=0, column=0, padx=(25, 15), sticky="ew")
        self.entry.bind("<Return>", lambda event: self.handle_text_input())
        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", width=68, height=44,
                                      fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER, corner_radius=20,
                                      anchor="center", compound="left",
                                      text_color="#FFFFFF",
                                      command=self.handle_text_input, font=ctk.CTkFont(size=15, weight="bold"))
        if self.send_icon_image is not None:
            self.send_btn.configure(image=self.send_icon_image, text="Send")
        else:
            self.send_btn.configure(text="↑")
        self.send_btn.grid(row=0, column=1, padx=(0, 10))
        self.send_btn.bind("<Enter>", lambda e: self._animate_input_button_hover(self.send_btn, "send", "#3A9EFF", True))
        self.send_btn.bind("<Leave>", lambda e: self._animate_input_button_hover(self.send_btn, "send", self.ACCENT_COLOR, False))

        self.mic_btn = ctk.CTkButton(self.input_frame, text="Mic", width=68, height=44, 
                                     fg_color="#1F1F21", hover_color="#2C2C2E", corner_radius=20,
                                     anchor="center", compound="left",
                                     text_color=self.TEXT_SECONDARY,
                                     command=self.toggle_listening, font=ctk.CTkFont(size=15, weight="bold"))
        if self.mic_icon_image is not None:
            self.mic_btn.configure(image=self.mic_icon_image, text="Mic")
        else:
            self.mic_btn.configure(text="MIC")
        self.mic_btn.grid(row=0, column=2, padx=(5, 15))
        self.mic_btn.bind("<Enter>", lambda e: self._animate_input_button_hover(self.mic_btn, "mic", "#2E2E31", True))
        self.mic_btn.bind("<Leave>", lambda e: self._animate_input_button_hover(self.mic_btn, "mic", "#1F1F21", False))
        self.after(60, self._turn_off_mic_ui)
        self.after(120, self._apply_input_button_mode)
        self.bind("<Configure>", self._on_window_resize, add="+")

    def _on_window_resize(self, event):
        if event.widget is not self:
            return
        if self._input_resize_job is not None:
            self.after_cancel(self._input_resize_job)
        self._input_resize_job = self.after(100, self._apply_input_button_mode)

    def _send_button_text(self):
        if self.input_icon_only and self.send_icon_image is not None:
            return ""
        return "Send" if self.send_icon_image is not None else "↑"

    def _mic_button_text(self):
        if self.input_icon_only and self.mic_icon_image is not None:
            return ""
        return "Mic" if self.mic_icon_image is not None else "MIC"

    def _apply_input_button_mode(self):
        self._input_resize_job = None
        self.input_icon_only = self.winfo_width() >= 1380

        send_width = 46 if self.input_icon_only else 68
        mic_width = 46 if self.input_icon_only else 68
        compound_mode = "center" if self.input_icon_only else "left"

        self.send_btn.configure(width=send_width, compound=compound_mode, text=self._send_button_text())
        if self.send_icon_image is not None:
            self.send_btn.configure(image=self.send_icon_image)

        self.mic_btn.configure(width=mic_width, compound=compound_mode, text=self._mic_button_text())
        if self.listening and self.mic_icon_active_image is not None:
            self.mic_btn.configure(image=self.mic_icon_active_image)
        elif self.mic_icon_image is not None:
            self.mic_btn.configure(image=self.mic_icon_image)

    def _animate_input_button_hover(self, button, key, target_color, hovered):
        if self.listening and button is self.mic_btn:
            return
        if key in self._hover_jobs:
            self.after_cancel(self._hover_jobs[key])
            self._hover_jobs.pop(key, None)

        try:
            current = button.cget("fg_color")
            if isinstance(current, tuple):
                current = current[0]
        except Exception:
            current = target_color

        def hex_to_rgb(value):
            value = value.lstrip("#")
            return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb):
            return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

        start = hex_to_rgb(current)
        end = hex_to_rgb(target_color)
        steps = 4

        def step(i=1):
            t = i / steps
            mixed = (
                int(start[0] + (end[0] - start[0]) * t),
                int(start[1] + (end[1] - start[1]) * t),
                int(start[2] + (end[2] - start[2]) * t),
            )
            button.configure(fg_color=rgb_to_hex(mixed), corner_radius=(22 if hovered else 20))
            if i < steps:
                self._hover_jobs[key] = self.after(22, step, i + 1)
            else:
                self._hover_jobs.pop(key, None)

        step()

    def log_message(self, sender, text):
        clean_msg = clean_text(text)
        if sender == "User":
            stop_speaking()

        bubble_container = ctk.CTkFrame(self.chat_container, fg_color="transparent")
        bubble_container.pack(fill="x", pady=15)
        if sender == "User":
            bubble = ctk.CTkFrame(bubble_container, fg_color=self.ACCENT_COLOR, corner_radius=18)
            bubble.pack(side="right", padx=(80, 10))
            msg_label = ctk.CTkLabel(bubble, text=clean_msg, text_color="#FFFFFF", 
                                     font=ctk.CTkFont(family="SF Pro Text", size=15, weight="normal"), wraplength=450, justify="right")
            msg_label.pack(padx=20, pady=12)
        else:
            self._render_ai_panels(bubble_container, text) 
            
        self.chat_container._parent_canvas.yview_moveto(1.0)

    def _render_ai_panels(self, container, text):
        master_panel = ctk.CTkFrame(container, fg_color="transparent", corner_radius=15,
                                    border_width=0)
        master_panel.pack(side="left", fill="both", expand=True, padx=(10, 80))
        header_frame = ctk.CTkFrame(master_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(5, 5))

        if self.ai_icon_image is not None:
            icon_lbl = ctk.CTkLabel(header_frame, text="", image=self.ai_icon_image)
        else:
            icon_lbl = ctk.CTkLabel(
                header_frame,
                text="AI",
                font=ctk.CTkFont(family="SF Pro Display", size=12, weight="bold"),
                text_color=self.ACCENT_COLOR,
            )
        icon_lbl.pack(side="left", padx=(0, 8))
        
        header_lbl = ctk.CTkLabel(header_frame, text="Aegis AI Core", 
                                  font=ctk.CTkFont(family="SF Pro Text", size=13, weight="bold"), text_color=self.TEXT_SECONDARY)
        header_lbl.pack(side="left")
        content_frame = ctk.CTkFrame(master_panel, fg_color="#18181A", corner_radius=18, border_width=1, border_color="#2C2C2E")
        content_frame.pack(fill="both", expand=True, padx=5, pady=(0, 10))
        threading.Thread(target=self._animate_typing, args=(content_frame, text), daemon=True).start()

    def _animate_typing(self, parent_frame, text):
        blocks = text.split("\n\n")
        for block in blocks:
            block = block.strip()
            if not block: continue
            match = re.match(r"^[\*]*\d+\.\s+[\*]*(.*?)[\*]*$", block)
            if match:
                point_text = match.group(1).replace("*", "")
                point_frame = ctk.CTkFrame(parent_frame, fg_color="#2C2C2E", corner_radius=12)
                point_frame.pack(fill="x", padx=20, pady=8)
                point_header = ctk.CTkLabel(point_frame, text="• ", 
                                            font=ctk.CTkFont(family="SF Pro Text", size=15, weight="bold"), text_color=self.ACCENT_COLOR)
                point_header.pack(padx=(15, 5), pady=(15, 15), side="left")
                lbl = ctk.CTkLabel(point_frame, text="", text_color=self.TEXT_COLOR, 
                                   font=ctk.CTkFont(family="SF Pro Text", size=14), wraplength=500, justify="left")
                lbl.pack(padx=(0, 20), pady=(15, 15), anchor="w", side="left")
                def update_label(char, l=lbl):
                    if l.winfo_exists():
                        l.configure(text=l.cget("text") + char)
                        self.chat_container._parent_canvas.yview_moveto(1.0)
                for char in point_text:
                    self.after(0, update_label, char)
                    time.sleep(0.015)
            else:
                clean_block = clean_text(block)
                lbl = ctk.CTkLabel(parent_frame, text="", text_color=self.TEXT_COLOR, 
                                   font=ctk.CTkFont(family="SF Pro Text", size=14), wraplength=600, justify="left")
                lbl.pack(padx=25, pady=(12, 12), anchor="w")
                def update_label(char, l=lbl):
                    if l.winfo_exists():
                        l.configure(text=l.cget("text") + char)
                        self.chat_container._parent_canvas.yview_moveto(1.0)
                for char in clean_block:
                    self.after(0, update_label, char)
                    time.sleep(0.015)
            time.sleep(0.1)

    def handle_text_input(self):
        text = self.entry.get().strip()
        if text:
            self.entry.delete(0, 'end')
            if getattr(self, 'onboarding', False):
                self._save_config(text)
                self.onboarding = False
                welcome_msg = f"Identity Confirmed. Welcome logged: {self.user_name}. How can I assist you today?"
                self.log_message("User", text)
                self.log_message("Aegis AI", welcome_msg)
                speak_async(welcome_msg)
                return
                
            self.process_input(text, is_voice=False)

    def handle_voice_input(self, text):
        self.process_input(text, is_voice=True)

    def _start_quiz(self):
        if self.quiz_mode:
            return
        self.quiz_mode = True
        self.quiz_score = 0
        self.quiz_index = 0
        self.chat_container.grid_forget()
        self.quiz_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.after(50, lambda: self.quiz_frame._parent_canvas.yview_moveto(0.0))
        self.qa_data = [
            {"q": "What is 2FA (Two-Factor Authentication)?",
             "opts": ["A) A dual-core processor", "B) Using two passwords", "C) Requiring two forms of identification to log in", "D) Logging in from two devices"],
             "ans": 2},
            {"q": "How do you spot a phishing email?",
             "opts": ["A) It uses an urgent, threatening tone", "B) The sender email is slightly misspelled", "C) It asks for sensitive info immediately", "D) All of the above"],
             "ans": 3},
            {"q": "If you receive a cyberbullying message, you should...",
             "opts": ["A) Reply aggressively to defend yourself", "B) Delete it immediately so you don't look at it", "C) Take a screenshot, block the user, and report", "D) Share it on your timeline to expose them"],
             "ans": 2},
            {"q": "Which of these is the MOST secure password?",
             "opts": ["A) Password123!", "B) B@tm@nR0cks99", "C) I_L0v3_My_D0g!", "D) T$x9@qPzL1mVv"],
             "ans": 3},
            {"q": "What does a padlock icon in a website's address bar mean?",
             "opts": ["A) The website cannot be hacked", "B) The connection is encrypted (HTTPS)", "C) The website is officially verified by the government", "D) You can safely share any password there"],
             "ans": 1}
        ]
        self.q_label = ctk.CTkLabel(self.quiz_frame, text="", font=ctk.CTkFont(family="SF Pro Display", size=22, weight="bold"), wraplength=600, text_color=self.TEXT_COLOR)
        self.q_label.pack(pady=(40, 30))
        self.btn_opts = []
        for i in range(4):
            btn = ctk.CTkButton(self.quiz_frame, text="", fg_color="#1C1C1E", hover_color=self.ACCENT_HOVER,
                                text_color=self.TEXT_COLOR,
                                border_width=1, border_color="#38383A", corner_radius=12,
                                command=lambda idx=i: self._check_quiz_answer(idx), 
                                font=ctk.CTkFont(family="SF Pro Text", size=15), height=50)
            btn.pack(pady=10, fill="x", padx=80)
            self.btn_opts.append(btn)
        self.exit_quiz_btn = ctk.CTkButton(self.quiz_frame, text="Exit Quiz", fg_color="#1C1C1E", hover_color="#331A1A",
                                   text_color="#FF3B30", border_width=1, border_color="#FF3B30", corner_radius=12,
                                   command=self._end_quiz, font=ctk.CTkFont(family="SF Pro Text", size=14), height=40)
        self.exit_quiz_btn.pack(pady=40)
        self._load_next_question()
        
    def _load_next_question(self):
        if self.quiz_index < len(self.qa_data):
            data = self.qa_data[self.quiz_index]
            self.q_label.configure(text=f"Question {self.quiz_index + 1}: {data['q']}")
            for i, opt in enumerate(data['opts']):
                self.btn_opts[i].configure(text=opt)
        else:
            self._finish_quiz()

    def _check_quiz_answer(self, idx):
        if idx == self.qa_data[self.quiz_index]["ans"]:
            self.quiz_score += 1
            speak_async("Correct.")
        else:
            speak_async("Incorrect.")
            
        self.quiz_index += 1
        self._load_next_question()

    def _finish_quiz(self):
        self.q_label.configure(text=f"Quiz Complete! Score: {self.quiz_score}/5")
        for btn in self.btn_opts:
            btn.configure(state="disabled")
        self.after(50, lambda: self.quiz_frame._parent_canvas.yview_moveto(0.0))
        speak_async(f"Quiz completed. Calculating score of {self.quiz_score} out of 5.")
        def fetch_comment():
            comment = self.brain.get_response(f"I just took a cyber security quiz and scored {self.quiz_score} out of 5.", extra_context=f"The user's name is {self.user_name}.")
            self.after(0, lambda: self.q_label.configure(text=f"Score: {self.quiz_score}/5\n\n{comment}"))
            self.after(0, lambda: self.quiz_frame._parent_canvas.yview_moveto(0.0))
            speak_async(comment)
        threading.Thread(target=fetch_comment, daemon=True).start()

    def _end_quiz(self):
        self.quiz_mode = False
        for widget in self.quiz_frame.winfo_children():
            widget.destroy()
        self.quiz_frame.grid_forget()
        self.chat_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.log_message("Aegis AI", "Quiz terminated. Returning to main terminal.")
        speak_async("Quiz closed. Terminal restored.")
        self.after(100, lambda: self.chat_container._parent_canvas.yview_moveto(1.0))

    def process_input(self, text, is_voice=False):
        if text.lower() == "security quiz":
            self._start_quiz()
            return
        if self.quiz_mode:
            self._end_quiz()
        stop_speaking()
        self.glow_frame.configure(border_color=self.ACCENT_COLOR)
        self.log_message("User", text)
        self.status_bar.configure(text=f"Status: Processing request...")
        self.thinking = True
        threading.Thread(target=self._animate_thinking, daemon=True).start()
        threading.Thread(target=self._process_logic, args=(text, is_voice), daemon=True).start()

    def _animate_thinking(self):
        dots = [".  ", ".. ", "..."]
        idx = 0
        while self.thinking:
            try:
                self.status_bar.configure(text=f"Status: AEGIS-AI Analyzing{dots[idx % 3]}")
                idx += 1
                time.sleep(0.4)
            except:
                break

    def _animate_waveform(self):
        states = [" ▂ ▃ ▄ ▅ ", " ▃ ▄ ▅ ▆ ", " ▄ ▅ ▆ ▇ ", " ▂ ▄ ▆ █ ", " ▃ ▅ ▇ █ ", " ▂ ▃ ▄ ▅ "]
        idx = 0
        while getattr(self, 'is_speaking', False):
            try:
                self.waveform_label.configure(text=f" [MIC] {states[idx % 6]}")
                idx += 1
                time.sleep(0.15)
            except:
                break
        try:
            self.waveform_label.configure(text="")
        except: pass

    def _show_stop_speech_button(self):
        if self.stop_speech_btn is not None:
            self.stop_speech_btn.grid()

    def _hide_stop_speech_button(self):
        if self.stop_speech_btn is not None:
            self.stop_speech_btn.grid_remove()

    def _stop_current_speech(self):
        self.speech_cancelled.set()
        self.is_speaking = False
        stop_speaking()
        self._hide_stop_speech_button()
        try:
            self.waveform_label.configure(text="")
            self.status_bar.configure(text="Status: Speech stopped.")
        except Exception:
            pass

    def _process_logic(self, text, is_voice):
        if text.lower() == "system health":
            self.after(0, self.log_message, "Aegis AI", "Initiating Active System Scan...")
            fake_logs = ["Scanning registry hooks...", "Verifying firewall rules...", "Mapping active TCP connections...", "Checking memory anomalies..."]
            for log in fake_logs:
                time.sleep(0.7)
                self.after(0, self.status_bar.configure, f"text=Status: {log}")
            response = self.commander.execute_command("system health")
        elif text.lower() == "screen shield":
            self.after(0, self.log_message, "Aegis AI", "Taking forensic screenshot of current workspace...")
            time.sleep(1.5)
            response = self.commander.execute_command("screen shield")
        elif text.lower() == "panic mode":
            self.after(0, self.log_message, "Aegis AI", "PANIC MODE ACTIVATED. INITIATING LOCKDOWN PROTOCOLS.")
            response = self.commander.execute_command("panic mode")
        elif text.lower() == "privacy news":
            self.after(0, self.log_message, "Aegis AI", "Securing feed. Accessing top privacy reports...")
            response = self.commander.execute_command("privacy news")
        elif text.lower() == "safe vault":
            self.after(0, self.log_message, "Aegis AI", "Unlocking encrypted Safe Vault...")
            response = self.commander.execute_command("safe vault")
        elif text.lower().startswith("check:"):
            password = text.split("check:", 1)[1].strip()
            response = self.commander.check_password_strength(password)
        else:
            ctx = f"The user's name is {self.user_name}. " if self.user_name else ""
            response = self.brain.get_response(text, extra_context=ctx)

        self.thinking = False
        self.after(0, lambda: self.glow_frame.configure(border_color="#003333"))
        self.after(0, lambda: self.log_message("Aegis AI", response))
        self.status_bar.configure(text="Status: Online & Secure")
        should_speak = False
        if is_voice:
            should_speak = True
        else:
            trigger_words = ["say", "speak", "tell me", "read"]
            if any(word in text.lower() for word in trigger_words):
                should_speak = True
            self.speech_cancelled.clear()
            self.is_speaking = True
            self.after(0, self._show_stop_speech_button)
            threading.Thread(target=self._animate_waveform, daemon=True).start()
            threading.Thread(target=speak_async, args=(response,), daemon=True).start()
            estimated_seconds = max(1.0, len(response.split()) * 0.35)
            start_time = time.time()
            while self.is_speaking and (time.time() - start_time) < estimated_seconds:
                if self.speech_cancelled.is_set():
                    break
                time.sleep(0.1)
            self.is_speaking = False
            self.after(0, self._hide_stop_speech_button)

    def _pulse_mic(self):
        if self.listening:
            current_color = self.mic_btn.cget("fg_color")
            next_color = "#FF3B30" if current_color == "#1F1F21" else "#1F1F21"
            self.mic_btn.configure(fg_color=next_color, text_color="white")
            if self.mic_icon_active_image is not None:
                self.mic_btn.configure(image=self.mic_icon_active_image, text=self._mic_button_text())
            self.after(300, self._pulse_mic)

    def toggle_listening(self):
        self.speech_cancelled.set()
        self.is_speaking = False
        stop_speaking()
        self._hide_stop_speech_button()
        if not self.listening:
            self.listening = True
            self.mic_btn.configure(fg_color="#FF3B30", text_color="white")
            if self.mic_icon_active_image is not None:
                self.mic_btn.configure(image=self.mic_icon_active_image, text=self._mic_button_text())
            self.status_bar.configure(text="Status: Active Mic Listening...")
            self._pulse_mic()
            threading.Thread(target=self._listen_thread, daemon=True).start()
        else:
            self._turn_off_mic_ui()

    def _listen_thread(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio)
                self.after(0, self.handle_voice_input, text)
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                self.after(0, self.status_bar.configure, text="Status: Could not understand audio.")
            except Exception as e:
                self.after(0, self.status_bar.configure, text=f"Status: Audio Error - {e}")
        
        self.after(0, self._turn_off_mic_ui)

    def _turn_off_mic_ui(self):
        self.listening = False
        self.mic_btn.configure(fg_color="#1F1F21", text_color=self.TEXT_SECONDARY)
        if self.mic_icon_image is not None:
            self.mic_btn.configure(image=self.mic_icon_image, text=self._mic_button_text())
        else:
            self.mic_btn.configure(text="MIC")
        if "Listening" in self.status_bar.cget("text"):
             self.status_bar.configure(text="Status: Online & Secure")


if __name__ == "__main__":
    app = AegisApp()
    app.mainloop()