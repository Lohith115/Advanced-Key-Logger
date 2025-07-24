<<<<<<< HEAD

# 🛡️ Advanced Python Keylogger (For Educational Use)

> **⚠️ Disclaimer:** This project is for **educational and ethical use only**. Do not use this on systems without explicit permission. Unauthorized access is illegal and unethical.

## 📌 Project Description

This is a stealth-based keylogger built in Python designed for cybersecurity learning and red team simulation. It captures:

- ✅ Keystrokes
- ✅ Clipboard content
- ✅ Screenshots (every 60 seconds)
- ✅ Email exfiltration of logs + screenshots
- ✅ Startup persistence (auto-start on Windows boot)

All data is silently stored in a hidden `AppData\MicrosoftLogs` folder and sent via Gmail using App Password authentication.

---

## ⚙️ Features

| Feature                 | Description |
|------------------------|-------------|
| 🔑 Keylogger           | Logs all user keystrokes in background |
| 📋 Clipboard Capture   | Captures all text copied to clipboard |
| 🖼️ Screenshots         | Takes a screenshot every 60 seconds |
| 📧 Gmail Exfiltration  | Emails logs + screenshots every 5 minutes |
| 🔁 Startup Persistence | Re-executes silently on boot via Startup folder |
| 🕵️ Hidden Execution    | No console window, disguised executable |

---

## 🧪 Testing Instructions

1. Create a Gmail account + enable 2FA
2. Generate an [App Password](https://myaccount.google.com/security)
3. Replace credentials in `main.py`:
   ```python
   ATTACKER_EMAIL = "your_email@gmail.com"
   APP_PASSWORD = "your_app_password"
   ```
4. Convert to `.exe`:
   ```bash
   pip install pyinstaller
   pyinstaller --noconsole --onefile main.py
   ```
5. Run the `.exe` on a test VM (like VirtualBox/Windows)

---

## 📁 Files

- `main.py` — Full source code of the keylogger
- `README.md` — Project documentation

---

## ❗Important Notes

- This tool is for **lab use only**
- Do **not** deploy on real systems without consent
- Helps learn about malware defense, threat modeling, and detection evasion

---

## 👨‍💻 Author

- Name: Lohith  
- Program: Masters in Cybersecurity  
- LinkedIn: www.linkedin.com/in/lohith-t-944909318

=======
# Advanced-Key-Logger
>>>>>>> 1f628c5017995a298f32318f9047b0dc071e0edf
