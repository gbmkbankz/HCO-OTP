# 🔥 HCO-OTP-Snag 🔥
A Termux-based educational tool that simulates an OTP phishing page for awareness purposes only.  
**This project is strictly for educational and ethical use to demonstrate security risks.**

---

[![Subscribe YouTube](https://img.shields.io/badge/YouTube-Hackers%20Colony-red?style=for-the-badge&logo=youtube)](https://youtube.com/@hackers_colony_tech?si=pvdCWZggTIuGb0ya)
[![Follow Instagram](https://img.shields.io/badge/Instagram-Hackers%20Colony-pink?style=for-the-badge&logo=instagram)](https://www.instagram.com/hackers_colony_official)
[![Join Telegram](https://img.shields.io/badge/Telegram-Hackers%20Colony-blue?style=for-the-badge&logo=telegram)](https://t.me/hackersColony)
[![Join Discord](https://img.shields.io/badge/Discord-Hackers%20Colony-purple?style=for-the-badge&logo=discord)](https://discord.gg/Xpq9nCGD)
[![Visit Website](https://img.shields.io/badge/Website-Hackers%20Colony-brightgreen?style=for-the-badge&logo=googlechrome)](https://hackerscolonyofficial.blogspot.com/?m=1)
[![Follow Facebook](https://img.shields.io/badge/Facebook-Hackers%20Colony-darkblue?style=for-the-badge&logo=facebook)](https://www.facebook.com/share/1AY25it2Em/)

---

## ⚠️ Disclaimer
This tool is for **educational purposes only**.  
The creator is not responsible for any misuse.  
Use it only in **authorized environments** to spread awareness about phishing attacks.

---

## 📌 Features
- Beautiful banner with countdown and YouTube redirect.
- Auto-subscribes prompt before tool usage.
- Creates a phishing-like OTP page for awareness.
- Logs entered OTPs into Termux.
- Works on **Android 15** with Termux.

---

## 📲 Step-by-Step Installation in Termux

```bash
# 1. Update & upgrade Termux
pkg update && pkg upgrade -y

# 2. Install dependencies
pkg install git python -y

# 3. Clone this repository
git clone https://github.com/<YOUR_GITHUB_USERNAME>/HCO-OTP-Snag.git

# 4. Enter the project folder
cd HCO-OTP-Snag

# 5. Install Python requirements
pip install -r requirements.txt

# 6. Run the tool
python otp_snag.py
```

---

## 🎯 How It Works
1. When launched, it displays the **HCO-OTP-Snag** banner.
2. Shows a **subscription countdown** and redirects to our YouTube channel.
3. Waits for the user to **come back after subscribing**.
4. Generates a phishing-like OTP input page (for awareness demo).
5. Logs the entered OTP in Termux for demonstration.

---

## 📸 Screenshot
![HCO OTP Snag Banner](screenshot.png)

---

## 🛡 Educational Purpose
This is made to **teach people** how OTP phishing works so they can avoid falling victim to it.

---

## 👨‍💻 Code by **Azhar**
