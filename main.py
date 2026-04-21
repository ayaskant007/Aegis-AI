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

newsapi = "YOUR_NEWS_API_KEY"
api_key = "AIzaSyDOGIeXRbT8mjqNaSbvMzeRuKch_mogM6U"

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
            speaker.Speak("", 3)
        except Exception:
            pass

def speak_async(text):
    if not text:
        return
    text = clean_text(text)
    if speaker:
        try:
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
            "You are Aegis-AI: The Cyber Sentinel, a specialized guardian protecting students online. "
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
            return f"Error connecting to Aegis-AI Brain: {e}"


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
            self.ui_callback(f"Failed to trigger full panic mode: {e}")

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

        # UI Color Palette (Neo-Futuristic)
        self.BG_COLOR = "#0c0c0d"
        self.SIDEBAR_COLOR = "#1a1d2e"
        self.CYAN_ACCENT = "#00fbff"
        self.CYAN_HOVER = "#00a3a6"
        self.PANEL_BG = "#151821"
        self.TEXT_COLOR = "#e0e0e0"

        self.configure(fg_color=self.BG_COLOR)
        ctk.set_appearance_mode("dark")
        
        # Window settings
        self.title("Aegis-AI: Security Hub")
        self.geometry("1100x750")
        self.minsize(950, 600)

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
            self.log_message("Aegis-AI", f"Welcome back, {self.user_name}. Systems are nominal. I am your Cyber Sentinel. How can I protect you today?")
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
        welcome_msg = "IDENTIFICATION REQUIRED.\n\nWelcome to Aegis-AI Core. Please identify yourself, Citizen. What is your name?"
        self.log_message("Aegis-AI", welcome_msg)
        speak_async("Identification required. Welcome to Aegis-AI Core. Please identify yourself, Citizen. What is your name?")

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
        """Creates a smooth pulsing glow effect for the Aegis-AI logo text."""
        # Cyan color cycling arrays
        color_cycle = ["#005555", "#008888", "#00aaaa", "#00bbbb", "#00d4d4", "#00fbff", 
                       "#00d4d4", "#00bbbb", "#00aaaa", "#008888"]
        if not hasattr(self, 'logo_color_idx'):
            self.logo_color_idx = 0

        try:
            self.logo_label.configure(text_color=color_cycle[self.logo_color_idx])
            self.logo_color_idx = (self.logo_color_idx + 1) % len(color_cycle)
            self.after(120, self._animate_breathing_logo)
        except Exception:
            pass

    def _transition_chat(self):
        """Slide up effect initialization trick. Simulates the screen fading/sliding into place."""
        def animate_opacity(current=0.0):
            try:
                if current <= 1.0:
                    self.attributes("-alpha", current)
                    self.after(20, animate_opacity, current + 0.05)
            except Exception:
                pass
        self.attributes("-alpha", 0.0) # Hide
        self.after(200, animate_opacity)

    def _create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color=self.SIDEBAR_COLOR,
                                          border_width=1, border_color=self.CYAN_ACCENT)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # Clock & Date Array
        self.clock_label = ctk.CTkLabel(self.sidebar_frame, text="", 
                                        font=ctk.CTkFont(family="Inter", size=14, weight="bold"), 
                                        text_color="#888888", anchor="center")
        self.clock_label.grid(row=0, column=0, pady=(15, 0), sticky="ew")

        # Logo Area
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="🛡️ AEGIS-AI\nCORE", 
                                       font=ctk.CTkFont(family="Montserrat", size=24, weight="bold"), 
                                       text_color=self.CYAN_ACCENT, justify="center")
        self.logo_label.grid(row=1, column=0, padx=20, pady=(15, 30))

        # Modern Buttons
        tools = [
            ("🚨", "Panic Mode"),
            ("📸", "Screen Shield"),
            ("💻", "System Health"),
            ("📁", "Safe Vault"),
            ("📰", "Privacy News"),
            ("🎓", "Security Quiz")
        ]
        
        for i, (icon, tool) in enumerate(tools, 2):
            btn = ctk.CTkButton(
                self.sidebar_frame, 
                text=f"{icon}   {tool}", 
                # Add transition trigger
                command=lambda t=tool: [self._trigger_slide_transition(), self.process_input(t)], 
                fg_color="transparent", 
                hover_color="#2a304d", # Subtle hover
                text_color=self.TEXT_COLOR,
                font=ctk.CTkFont(family="Inter", size=15, weight="normal"),
                anchor="w",
                border_width=1,
                border_color="#2a304d",
                corner_radius=8,
                height=45
            )
            btn.grid(row=i, column=0, padx=25, pady=8, sticky="ew")

    def _trigger_slide_transition(self):
        """Simulates a quick slide/fade reload of the screen when a sidebar tool is selected."""
        stop_speaking() # Critical: Interrupt voice when interacting heavily
        def animate_opacity(current=1.0, fade_out=True):
            try:
                if fade_out:
                    current -= 0.15
                    if current <= 0:
                        current = 0
                        fade_out = False
                        # Clear chat here for new task
                        for widget in self.chat_container.winfo_children():
                            widget.destroy()
                else:
                    current += 0.15
                    if current >= 1.0:
                        current = 1.0
                        self.attributes("-alpha", current)
                        return
                
                self.attributes("-alpha", current)
                self.after(20, lambda: animate_opacity(current, fade_out))
            except Exception:
                pass
            
        animate_opacity()

    def _create_header(self):
        self.header_frame = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=1, sticky="ew", padx=20, pady=(10, 0))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="ACTIVE TERMINAL", 
                                        font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
                                        text_color="#555555", anchor="w")
        self.title_label.pack(side="left", pady=10)

    def _create_chat_area(self):
        # We will use this master frame to hold the glow effect and the chat
        self.glow_frame = ctk.CTkFrame(self, fg_color="#080808", border_width=2, border_color="#003333", corner_radius=15)
        self.glow_frame.grid(row=1, column=1, padx=30, pady=10, sticky="nsew")
        self.glow_frame.grid_columnconfigure(0, weight=1)
        self.glow_frame.grid_rowconfigure(0, weight=1)

        self.chat_container = ctk.CTkScrollableFrame(self.glow_frame, fg_color="transparent")
        self.chat_container.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.chat_container.grid_columnconfigure(0, weight=1)

        # Quiz Area overlay frame (initially hidden)
        self.quiz_frame = ctk.CTkFrame(self.glow_frame, fg_color="transparent")
        self.quiz_frame.grid_columnconfigure(0, weight=1)

    def _create_input_area(self):
        # Master container for input and status
        self.bottom_container = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_container.grid(row=2, column=1, padx=30, pady=(10, 20), sticky="ew")
        self.bottom_container.grid_columnconfigure(0, weight=1)

        # Status Bar above input & Waveform indicator
        self.status_container = ctk.CTkFrame(self.bottom_container, fg_color="transparent")
        self.status_container.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 5))
        self.status_container.grid_columnconfigure(0, weight=1)

        self.status_bar = ctk.CTkLabel(self.status_container, text="Status: Online & Secure", 
                                       font=ctk.CTkFont(family="Inter", size=12), text_color="#777777", anchor="w")
        self.status_bar.grid(row=0, column=0, sticky="w")
        
        self.waveform_label = ctk.CTkLabel(self.status_container, text="", text_color=self.CYAN_ACCENT)
        self.waveform_label.grid(row=0, column=1, sticky="e")

        # Input Frame (Grouped console look)
        self.input_frame = ctk.CTkFrame(self.bottom_container, fg_color=self.PANEL_BG, corner_radius=20, 
                                        border_width=1, border_color="#333333")
        self.input_frame.grid(row=1, column=0, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter command, ask for advice, or type 'check: password'...",
                                  fg_color="transparent", border_width=0, text_color="white",
                                  font=ctk.CTkFont(family="Inter", size=14), height=50)
        self.entry.grid(row=0, column=0, padx=(20, 10), sticky="ew")
        self.entry.bind("<Return>", lambda event: self.handle_text_input())

        # Buttons
        self.send_btn = ctk.CTkButton(self.input_frame, text="📤", width=45, height=40,
                                      fg_color="#1f538d", hover_color=self.CYAN_HOVER, corner_radius=15,
                                      command=self.handle_text_input, font=ctk.CTkFont(size=18))
        self.send_btn.grid(row=0, column=1, padx=(0, 10))

        self.mic_btn = ctk.CTkButton(self.input_frame, text="🎤", width=45, height=40, 
                                     fg_color="#2b2b2b", hover_color="#444444", corner_radius=15,
                                     text_color=self.CYAN_ACCENT,
                                     command=self.toggle_listening, font=ctk.CTkFont(size=18))
        self.mic_btn.grid(row=0, column=2, padx=(0, 10))

    def log_message(self, sender, text):
        clean_msg = clean_text(text)
        
        # Stop speech when starting to show a new message (interrupt)
        if sender == "User":
            stop_speaking()

        bubble_container = ctk.CTkFrame(self.chat_container, fg_color="transparent")
        bubble_container.grid(sticky="ew", pady=10)
        bubble_container.grid_columnconfigure(0, weight=1)
        bubble_container.grid_columnconfigure(1, weight=1)
        
        if sender == "User":
            # Premium User Bubble - Bottom-Right missing corner look via styling limits
            bubble = ctk.CTkFrame(bubble_container, fg_color="#1f538d", corner_radius=18)
            bubble.grid(row=0, column=1, sticky="e", padx=(80, 10))
            msg_label = ctk.CTkLabel(bubble, text=clean_msg, text_color="white", 
                                     font=ctk.CTkFont(family="Inter", size=15), wraplength=450, justify="right")
            msg_label.pack(padx=20, pady=15)
        else:
            # Aegis-AI Premium Structured Panels with Typing Animation
            self._render_ai_panels(bubble_container, text) 
            
        self.chat_container._parent_canvas.yview_moveto(1.0)

    def _render_ai_panels(self, container, text):
        """Parses the text and renders beautiful glassmorphic security panels with animation."""
        master_panel = ctk.CTkFrame(container, fg_color=self.PANEL_BG, corner_radius=12,
                                    border_width=1, border_color=self.CYAN_ACCENT)
        master_panel.pack(side="left", padx=(10, 80)) # Align left
        
        # Header for the bot
        header_lbl = ctk.CTkLabel(master_panel, text="AEGIS-AI | RESPONSE", 
                                  font=ctk.CTkFont(family="Montserrat", size=11, weight="bold"), text_color=self.CYAN_ACCENT)
        header_lbl.pack(padx=20, pady=(15, 5), anchor="w")

        # Container for the dynamic text
        content_frame = ctk.CTkFrame(master_panel, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

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
                
                point_frame = ctk.CTkFrame(parent_frame, fg_color="#1e2233", corner_radius=8)
                point_frame.pack(fill="x", padx=20, pady=8)
                
                point_header = ctk.CTkLabel(point_frame, text=f"🔹 ", 
                                            font=ctk.CTkFont(family="Inter", size=15, weight="bold"), text_color="#00fbff")
                point_header.pack(padx=15, pady=(12, 5), anchor="w", side="left")

                # Type header text
                def update_header(char):
                    point_header.configure(text=point_header.cget("text") + char)
                    self.chat_container._parent_canvas.yview_moveto(1.0)
                
                for char in point_text:
                    self.after(0, update_header, char)
                    time.sleep(0.015)
                
            else:
                clean_block = clean_text(block)
                lbl = ctk.CTkLabel(parent_frame, text="", text_color=self.TEXT_COLOR, 
                                   font=ctk.CTkFont(family="Inter", size=14), wraplength=550, justify="left")
                lbl.pack(padx=20, pady=(5, 10), anchor="w")
                
                # Type block text
                def update_label(char):
                    lbl.configure(text=lbl.cget("text") + char)
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
                self.log_message("Aegis-AI", welcome_msg)
                speak_async(welcome_msg)
                return
                
            self.process_input(text, is_voice=False)

    def handle_voice_input(self, text):
        self.process_input(text, is_voice=True)

    def _start_quiz(self):
        """Initializes and displays the Security Quiz interface."""
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
        
        self.q_label = ctk.CTkLabel(self.quiz_frame, text="", font=ctk.CTkFont(size=20, weight="bold"), wraplength=600)
        self.q_label.pack(pady=(40, 20))
        
        self.btn_opts = []
        for i in range(4):
            btn = ctk.CTkButton(self.quiz_frame, text="", fg_color="#1f538d", hover_color="#00fbff",
                                command=lambda idx=i: self._check_quiz_answer(idx), 
                                font=ctk.CTkFont(size=16), height=50)
            btn.pack(pady=10, fill="x", padx=100)
            self.btn_opts.append(btn)
            
        # Cancel Button
        cancel_btn = ctk.CTkButton(self.quiz_frame, text="Exit Quiz", fg_color="#ff4444", hover_color="#cc0000",
                                   command=self._end_quiz)
        cancel_btn.pack(pady=30)
        
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
        self.chat_container.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.log_message("Aegis-AI", "Quiz terminated. Returning to main terminal.")
        speak_async("Quiz closed. Terminal restored.")

    def process_input(self, text, is_voice=False):
        if text.lower() == "security quiz":
            self._start_quiz()
            return
            
        if self.quiz_mode:
            self._end_quiz()
            
        stop_speaking() # Immediate UI halt of voice
        self.glow_frame.configure(border_color="#00fbff") # Light up on active process
        
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
                self.waveform_label.configure(text=f" 🔊 {states[idx % 6]}")
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
            self.after(0, self.log_message, "Aegis-AI", "🔄 Initiating Active System Scan...")
            # Simulate a 3s scan with console-like text updates
            fake_logs = ["Scanning registry hooks...", "Verifying firewall rules...", "Mapping active TCP connections...", "Checking memory anomalies..."]
            for log in fake_logs:
                time.sleep(0.7)
                self.after(0, self.status_bar.configure, f"text=Status: {log}")
            response = self.commander.system_health()
        elif text.lower() == "screen shield":
            self.after(0, self.log_message, "Aegis-AI", "📸 Taking forensic screenshot of current workspace...")
            # Simulate processing time
            time.sleep(1.5)
            response = self.commander.screen_shield()
        elif text.lower() == "panic mode":
            self.after(0, self.log_message, "Aegis-AI", "🚨 PANIC MODE ACTIVATED. INITIATING LOCKDOWN PROTOCOLS. 🚨")
            response = self.commander.panic_mode()
        elif text.lower() == "privacy news":
            self.after(0, self.log_message, "Aegis-AI", "📰 Securing feed. Accessing top privacy reports...")
            response = self.commander.privacy_news()
        elif text.lower() == "safe vault":
            self.after(0, self.log_message, "Aegis-AI", "📁 Unlocking encrytped Safe Vault...")
            response = self.commander.safe_vault()
        elif text.lower().startswith("check:"):
            password = text.split("check:", 1)[1].strip()
            response = self.commander.check_password_strength(password)
        else:
            # Add user name context if available
            ctx = f"The user's name is {self.user_name}. " if self.user_name else ""
            response = self.brain.get_response(text, extra_context=ctx)

        self.thinking = False
        self.after(0, lambda: self.glow_frame.configure(border_color="#003333")) # Dim
        self.after(0, lambda: self.log_message("Aegis-AI", response))
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
            next_color = "#ff4444" if current_color == self.PANEL_BG else self.PANEL_BG
            self.mic_btn.configure(fg_color=next_color, text_color="white")
            self.after(300, self._pulse_mic)

    def toggle_listening(self):
        stop_speaking() # Interruption on mic press
        if not self.listening:
            self.listening = True
            self.mic_btn.configure(fg_color="#ff4444", text_color="white")
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
        self.mic_btn.configure(fg_color="#2b2b2b", text_color=self.CYAN_ACCENT)
        if "Listening" in self.status_bar.cget("text"):
             self.status_bar.configure(text="Status: Online & Secure")


if __name__ == "__main__":
    app = AegisApp()
    app.mainloop()