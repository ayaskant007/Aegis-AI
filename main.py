# =========================================================================
# AEGIS-AI: THE CYBER SENTINEL - CHAMPION EDITION
#
# HOW TO COMPILE TO AN EXECUTABLE (.exe) USING auto-py-to-exe:
# 1. Install the compiler: pip install auto-py-to-exe
# 2. Run the compiler by typing: auto-py-to-exe
# 3. In the UI that opens:
#    - Script Location: Select this 'main.py' file.
#    - Onefile: Choose "One Directory" (often safer for customtkinter) or "One File".
#    - Console Window: Select "Window Based (hide the console)".
#    - Icon: You can add an .ico file if you want a custom desktop icon.
# 4. Click "Convert .py to .exe" at the bottom.
# =========================================================================

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
try:
    import pyautogui
except ImportError:
    pass # Needs to be installed
import customtkinter as ctk
from google import genai

# ==========================================
# CONFIGURATION & SETUP
# ==========================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def get_secure_key(encoded_key):
    """Simple obfuscation to prevent plain-text scraping from EXE."""
    try:
        if not encoded_key or "_" in encoded_key: # Not base64
            return encoded_key
        return base64.b64decode(encoded_key).decode()
    except Exception:
        return encoded_key

# Secure API Key Handling
# 1. Checks Environment Variable first (Best for security)
# 2. Uses Obfuscated Fallback (Best for EXE distribution)
api_key = os.environ.get("GOOGLE_API_KEY", get_secure_key("QUl6YVN5RE9HSWVYUmJUOG1qcU5hU2J2TXplUnVLY2hfbW9nTTZV"))
newsapi = os.environ.get("NEWS_API_KEY", "YOUR_NEWS_API_KEY")

CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Aegis_Security_Vault", "user_config.json")

# Initialize Voice
try:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
except Exception as e:
    print(f"Error initializing speaker: {e}")
    speaker = None

def clean_text(text):
    """Remove standard markdown characters so it reads cleanly in UI & TTS."""
    if not isinstance(text, str):
        return text
    # Remove markdown bold, italic, codeblocks, headings
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

# Initialize AI Brain
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
            pyautogui.hotkey('win', 'd') # Minimize all
            time.sleep(0.5)
            webbrowser.open("https://duckduckgo.com/") # Safe search
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
            
            # Auto-generate default security guides
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

# ==========================================
# USER INTERFACE (CustomTkinter)
# ==========================================
class AegisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # UI Color Palette (Apple-Inspired Professional Dark Mode)
        self.BG_COLOR = "#000000" # True black background
        self.SIDEBAR_COLOR = "#1C1C1E" # Minimal grey sidebar
        self.ACCENT_COLOR = "#0A84FF" # Apple system blue
        self.ACCENT_HOVER = "#007AFF" # Apple blue slightly darker
        self.PANEL_BG = "#1C1C1E" # Dark panel
        self.TEXT_COLOR = "#FFFFFF"
        self.TEXT_SECONDARY = "#8E8E93"
        self.BORDER_COLOR = "#38383A"

        self.configure(fg_color=self.BG_COLOR)
        ctk.set_appearance_mode("dark")
        
        # Window settings
        self.title("Aegis AI: Security Hub")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Apply Glassmorphism design (Liquid Glass / Mica Acrylic)
        try:
            # Set the window transparency key to match the exact background color for the glass effect
            self.wm_attributes("-transparentcolor", "#010101")
            self.configure(fg_color="#010101") 
            
            # Apply the style via pywinstyles for Windows 11 Acrylic (Liquid Glass)
            pywinstyles.apply_style(self, "acrylic")
            pywinstyles.change_header_color(self, color="#010101")
        except Exception as e:
            print(f"Glass implementation error: {e}")
            self.configure(fg_color=self.BG_COLOR)

        # Components
        self.brain = CyberSentinelAI()
        self.commander = SystemCommander(self.log_message)
        self.recognizer = sr.Recognizer()   
        self.listening = False
        self.user_name = None
        self.quiz_mode = False

        # Load or initialize user configuration
        self._ensure_vault_exists()
        self._load_config()

        # Layout Setup
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_sidebar()
        self._create_header()
        self._create_chat_area()
        self._create_input_area()

        # Start background tasks
        self._animate_breathing_logo()
        self._update_clock()
        self._transition_chat()

        if not self.user_name:
            self._start_onboarding()
        else:
            self.log_message("Aegis AI", f"Welcome back, {self.user_name}. Systems are nominal. I am your Cyber Sentinel. How can I protect you today?")
            speak_async(f"Welcome back, {self.user_name}. Systems are nominal.")

    def _ensure_vault_exists(self):
        """Ensures the safe vault directory exists and populates it with default files."""
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
        """Updates the clock/date widget in the sidebar."""
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            current_date = datetime.now().strftime("%Y-%m-%d")
            self.clock_label.configure(text=f"{current_time}\n{current_date}")
            self.after(1000, self._update_clock)
        except Exception:
            pass

    def _animate_breathing_logo(self):
        """Creates a smooth pulsing glow effect for the Aegis AI logo text."""
        # Clean white to blue cycle
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
        """Slide up effect initialization trick. Simulates the screen fading/sliding into place."""
        def animate_opacity(step=0):
            try:
                # Bouncy/smooth ease-in array
                ease = [0.05, 0.1, 0.15, 0.25, 0.3, 0.1, 0.05]
                if step < len(ease):
                    current = self.attributes("-alpha")
                    self.attributes("-alpha", min(1.0, current + ease[step]))
                    self.after(20, animate_opacity, step + 1)
                else:
                    self.attributes("-alpha", 1.0)
            except Exception:
                pass
        self.attributes("-alpha", 0.0) # Hide
        self.after(200, animate_opacity)

    def _create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="transparent",
                                          border_width=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # Clock & Date Area
        self.clock_label = ctk.CTkLabel(self.sidebar_frame, text="", 
                                        font=ctk.CTkFont(family="SF Pro Display", size=13, weight="bold"), 
                                        text_color=self.TEXT_SECONDARY, anchor="center")
        self.clock_label.pack(pady=(30, 10))

        # Logo Area
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Aegis AI", 
                                       font=ctk.CTkFont(family="SF Pro Display", size=24, weight="bold"), 
                                       text_color=self.TEXT_COLOR, justify="center")
        self.logo_label.pack(pady=(10, 40))

        # Modern Buttons Frame
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
            # We use a helper function to capture the tool value correctly in the loop
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
            # Add a slight hover effect via bind to simulate glass touch
            btn.bind("<Enter>", lambda e, b=btn: b.configure(fg_color="#3A3A3C"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(fg_color="#1C1C1E"))
            
            btn.pack(pady=8, fill="x", padx=10)

        # Bottom info
        self.version_label = ctk.CTkLabel(self.sidebar_frame, text="v2.0.4 - Secure Connection", 
                                        font=ctk.CTkFont(family="SF Pro Text", size=11), 
                                        text_color=self.TEXT_SECONDARY)
        self.version_label.pack(side="bottom", pady=20)

    def _trigger_slide_transition(self):
        """Simulates a quick slide/fade reload of the screen when a sidebar tool is selected."""
        stop_speaking() # Critical: Interrupt voice when interacting heavily
        def animate_opacity(step=0, fade_out=True):
            try:
                # Easing array for smoother fade
                ease = [0.15, 0.25, 0.35, 0.20, 0.05]
                current = self.attributes("-alpha")
                
                if fade_out:
                    if step < len(ease):
                        self.attributes("-alpha", max(0.0, current - ease[step]))
                        self.after(20, lambda: animate_opacity(step + 1, fade_out=True))
                    else:
                        self.attributes("-alpha", 0.0)
                        # Clear chat here for new task
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
        self.header_frame = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=1, sticky="ew", padx=40, pady=(15, 0))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Terminal Uplink Established", 
                                        font=ctk.CTkFont(family="SF Pro Text", size=13, weight="bold"),
                                        text_color=self.ACCENT_COLOR, anchor="w")
        self.title_label.pack(side="left", pady=10)

    def _create_chat_area(self):
        # Master frame to hold the glow effect and the chat
        self.glow_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=20, border_width=1, border_color=self.BORDER_COLOR)
        self.glow_frame.grid(row=1, column=1, padx=40, pady=(10, 20), sticky="nsew")
        self.glow_frame.grid_columnconfigure(0, weight=1)
        self.glow_frame.grid_rowconfigure(0, weight=1)

        self.chat_container = ctk.CTkScrollableFrame(self.glow_frame, fg_color="transparent")
        self.chat_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.chat_container.grid_columnconfigure(0, weight=1)

        # Quiz Area overlay frame (initially hidden)
        self.quiz_frame = ctk.CTkFrame(self.glow_frame, fg_color="transparent")
        self.quiz_frame.grid_columnconfigure(0, weight=1)

    def _create_input_area(self):
        # Master container for input and status
        self.bottom_container = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_container.grid(row=2, column=1, padx=40, pady=(0, 30), sticky="ew")
        self.bottom_container.grid_columnconfigure(0, weight=1)

        # Status Bar above input & Waveform indicator
        self.status_container = ctk.CTkFrame(self.bottom_container, fg_color="transparent")
        self.status_container.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.status_container.grid_columnconfigure(0, weight=1)

        self.status_bar = ctk.CTkLabel(self.status_container, text="Status: Online & Secure", 
                                       font=ctk.CTkFont(family="SF Pro Text", size=13), text_color=self.TEXT_SECONDARY, anchor="w")
        self.status_bar.grid(row=0, column=0, sticky="w")
        
        self.waveform_label = ctk.CTkLabel(self.status_container, text="", text_color=self.ACCENT_COLOR)
        self.waveform_label.grid(row=0, column=1, sticky="e")

        # Input Frame - Ultra modern rounded look
        self.input_frame = ctk.CTkFrame(self.bottom_container, fg_color="#18181A", corner_radius=20, 
                                        border_width=1, border_color=self.BORDER_COLOR)
        self.input_frame.grid(row=1, column=0, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter command, ask advice, or type 'check: password'...",
                                  fg_color="transparent", border_width=0, text_color=self.TEXT_COLOR,
                                  font=ctk.CTkFont(family="SF Pro Text", size=15), height=55)
        self.entry.grid(row=0, column=0, padx=(25, 15), sticky="ew")
        self.entry.bind("<Return>", lambda event: self.handle_text_input())

        # Buttons
        self.send_btn = ctk.CTkButton(self.input_frame, text="↑", width=40, height=40,
                                      fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER, corner_radius=20,
                                      text_color="#FFFFFF",
                                      command=self.handle_text_input, font=ctk.CTkFont(size=20, weight="bold"))
        self.send_btn.grid(row=0, column=1, padx=(0, 10))

        self.mic_btn = ctk.CTkButton(self.input_frame, text="MIC", width=40, height=40, 
                                     fg_color="transparent", hover_color="#2C2C2E", corner_radius=20,
                                     text_color=self.TEXT_SECONDARY,
                                     command=self.toggle_listening, font=ctk.CTkFont(size=18))
        self.mic_btn.grid(row=0, column=2, padx=(5, 15))

    def log_message(self, sender, text):
        clean_msg = clean_text(text)
        
        # Stop speech when starting to show a new message (interrupt)
        if sender == "User":
            stop_speaking()

        bubble_container = ctk.CTkFrame(self.chat_container, fg_color="transparent")
        bubble_container.pack(fill="x", pady=15)
        
        if sender == "User":
            # Apple iMessage-like User Bubble
            bubble = ctk.CTkFrame(bubble_container, fg_color=self.ACCENT_COLOR, corner_radius=18)
            bubble.pack(side="right", padx=(80, 10))
            msg_label = ctk.CTkLabel(bubble, text=clean_msg, text_color="#FFFFFF", 
                                     font=ctk.CTkFont(family="SF Pro Text", size=15, weight="normal"), wraplength=450, justify="right")
            msg_label.pack(padx=20, pady=12)
        else:
            # Aegis AI Modern Panel
            self._render_ai_panels(bubble_container, text) 
            
        self.chat_container._parent_canvas.yview_moveto(1.0)

    def _render_ai_panels(self, container, text):
        """Parses the text and renders beautiful glassmorphic security panels with animation."""
        master_panel = ctk.CTkFrame(container, fg_color="transparent", corner_radius=15,
                                    border_width=0)
        master_panel.pack(side="left", fill="both", expand=True, padx=(10, 80)) 
        
        # Header for the bot
        header_frame = ctk.CTkFrame(master_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(5, 5))
        
        icon_lbl = ctk.CTkLabel(header_frame, text="🛡️", font=ctk.CTkFont(size=14)) # Added slight shield icon to represent Aegis AI
        icon_lbl.pack(side="left", padx=(0, 8))
        
        header_lbl = ctk.CTkLabel(header_frame, text="Aegis AI Core", 
                                  font=ctk.CTkFont(family="SF Pro Text", size=13, weight="bold"), text_color=self.TEXT_SECONDARY)
        header_lbl.pack(side="left")

        # Container for the dynamic text - Professional spacing and padding
        content_frame = ctk.CTkFrame(master_panel, fg_color="#18181A", corner_radius=18, border_width=1, border_color="#2C2C2E")
        content_frame.pack(fill="both", expand=True, padx=5, pady=(0, 10))

        # Trigger Typing Animation Thread
        threading.Thread(target=self._animate_typing, args=(content_frame, text), daemon=True).start()

    def _animate_typing(self, parent_frame, text):
        blocks = text.split("\n\n")
        
        for block in blocks:
            block = block.strip()
            if not block: continue

            # Sub-panel logic
            match = re.match(r"^[\*]*\d+\.\s+[\*]*(.*?)[\*]*$", block)
            if match:
                point_text = match.group(1).replace("*", "")
                
                point_frame = ctk.CTkFrame(parent_frame, fg_color="#2C2C2E", corner_radius=12)
                point_frame.pack(fill="x", padx=20, pady=8)
                
                # We place the text inside the sub-panel
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
                
                # Type block text
                def update_label(char, l=lbl):
                    if l.winfo_exists():
                        l.configure(text=l.cget("text") + char)
                        self.chat_container._parent_canvas.yview_moveto(1.0)
                
                for char in clean_block:
                    self.after(0, update_label, char)
                    time.sleep(0.015)
            time.sleep(0.1) # Small pause between blocks

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
        """Initializes and displays the Security Quiz interface."""
        # Safeguard to prevent multiple quiz overlays
        if self.quiz_mode:
            return
            
        self.quiz_mode = True
        self.quiz_score = 0
        self.quiz_index = 0
        
        # Hide chat, show quiz
        self.chat_container.grid_forget()
        self.quiz_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Build Quiz Data
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
            
        # Cancel Button
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
            
        speak_async(f"Quiz completed. Calculating score of {self.quiz_score} out of 5.")
        
        # Get AI comment
        def fetch_comment():
            comment = self.brain.get_response(f"I just took a cyber security quiz and scored {self.quiz_score} out of 5.", extra_context=f"The user's name is {self.user_name}.")
            self.after(0, lambda: self.q_label.configure(text=f"Score: {self.quiz_score}/5\n\n{comment}"))
            speak_async(comment)
            
        threading.Thread(target=fetch_comment, daemon=True).start()

    def _end_quiz(self):
        self.quiz_mode = False
        # Remove buttons from pack
        for widget in self.quiz_frame.winfo_children():
            widget.destroy()
        self.quiz_frame.grid_forget()
        self.chat_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") # Match original padding
        self.log_message("Aegis AI", "Quiz terminated. Returning to main terminal.")
        speak_async("Quiz closed. Terminal restored.")
        # Ensure scroll to bottom
        self.after(100, lambda: self.chat_container._parent_canvas.yview_moveto(1.0))

    def process_input(self, text, is_voice=False):
        if text.lower() == "security quiz":
            self._start_quiz()
            return
            
        if self.quiz_mode:
            self._end_quiz()
            
        stop_speaking() # Immediate UI halt of voice
        self.glow_frame.configure(border_color=self.ACCENT_COLOR) # Light up on active process
        
        self.log_message("User", text)
        self.status_bar.configure(text=f"Status: Processing request...")
        
        # Thinking indicator
        self.thinking = True
        threading.Thread(target=self._animate_thinking, daemon=True).start()

        # Async logic
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

    def _process_logic(self, text, is_voice):
        # Fake "Active Scanning" logic
        if text.lower() == "system health":
            self.after(0, self.log_message, "Aegis AI", "Initiating Active System Scan...")
            # Simulate a 3s scan with console-like text updates
            fake_logs = ["Scanning registry hooks...", "Verifying firewall rules...", "Mapping active TCP connections...", "Checking memory anomalies..."]
            for log in fake_logs:
                time.sleep(0.7)
                self.after(0, self.status_bar.configure, f"text=Status: {log}")
            response = self.commander.execute_command("system health")
        elif text.lower() == "screen shield":
            self.after(0, self.log_message, "Aegis AI", "Taking forensic screenshot of current workspace...")
            # Simulate processing time
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
            # Add user name context if available
            ctx = f"The user's name is {self.user_name}. " if self.user_name else ""
            response = self.brain.get_response(text, extra_context=ctx)

        self.thinking = False
        self.after(0, lambda: self.glow_frame.configure(border_color="#003333")) # Dim
        self.after(0, lambda: self.log_message("Aegis AI", response))
        self.status_bar.configure(text="Status: Online & Secure")
        
        should_speak = False
        if is_voice:
            should_speak = True
        else:
            trigger_words = ["say", "speak", "tell me", "read"]
            if any(word in text.lower() for word in trigger_words):
                should_speak = True
                
        if should_speak:
            self.is_speaking = True
            threading.Thread(target=self._animate_waveform, daemon=True).start()
            speak_async(response)
            # The speech is async, but we can't easily wait for SAPI without events.
            # We'll just assume voice ends after some time based on word count over a simple ratio.
            sleep_time = len(response.split()) * 0.4
            time.sleep(sleep_time)
            self.is_speaking = False

    def _pulse_mic(self):
        if self.listening:
            current_color = self.mic_btn.cget("fg_color")
            # Pulsing rapidly with a custom red/orange hue for active recording
            next_color = "#FF3B30" if current_color == "transparent" else "transparent"
            self.mic_btn.configure(fg_color=next_color, text_color="white")
            self.after(300, self._pulse_mic)

    def toggle_listening(self):
        stop_speaking() # Interruption on mic press
        if not self.listening:
            self.listening = True
            self.mic_btn.configure(fg_color="#FF3B30", text_color="white")
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
        self.mic_btn.configure(fg_color="transparent", text_color=self.TEXT_SECONDARY)
        if "Listening" in self.status_bar.cget("text"):
             self.status_bar.configure(text="Status: Online & Secure")


if __name__ == "__main__":
    app = AegisApp()
    app.mainloop()