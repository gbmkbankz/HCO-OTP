#!/usr/bin/env bash
set -e
echo "[*] Updating packages..."
pkg update -y
pkg upgrade -y

echo "[*] Installing python and git..."
pkg install -y python git

python -m pip install --upgrade pip
pip install flask python-dotenv

echo "[*] Done. Run: python3 main.py"
