import os
import sys
import logging
import threading
import time
from flask import Flask
from flask_cors import CORS
import flask.cli
from colorama import Fore, Style, init


try:
    from routes import web
    from utils import run_cloudflare, run_ngrok
except ImportError:
    print(f"{Fore.RED}[!] Error: routes.py or utils.py not found!")
    sys.exit()

TOKEN_FILE = "TOKEN_NGROK.txt"

def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None

def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    print(f"{Fore.GREEN}[+] Token saved to {TOKEN_FILE}")

def edit_token():
    token = input(f"{Fore.CYAN}Enter your ngrok token: {Style.RESET_ALL}").strip()
    save_token(token)
    return token

init(autoreset=True)
flask.cli.show_server_banner = lambda *args: None
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

PORT = 7878
app = Flask(__name__)
CORS(app)
web(app) 

def start_flask():
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

print(Fore.CYAN + r"""
  ______         _____                
 |  ____|       / ____|               
 | |__ _____  _| |     __ _ _ __ ___  
 |  __/ _ \ \/ / |    / _` | '_ ` _ \ 
 | | |  __/>  <| |___| (_| | | | | | |
 |_|  \___/_/\_\\_____\__,_|_| |_| |_|
""")

token = get_token()

print(f"{Fore.YELLOW}[+]{Fore.WHITE} Select Tunnel Method:")
print(f"  {Fore.GREEN}1.{Fore.WHITE} Ngrok")
print(f"  {Fore.GREEN}2.{Fore.WHITE} Cloudflare")

try:
    choice = input(f"\n{Style.BRIGHT}choice > {Style.RESET_ALL}").strip()
    
    print(f"{Fore.YELLOW}[*] Starting Flask server on port {PORT}...")
    threading.Thread(target=start_flask, daemon=True).start()
    time.sleep(2)

    if choice == "1":
        if not token:
            print(f"{Fore.RED}[!] No ngrok token found.")
            token = edit_token()
        
        print(f"{Fore.YELLOW}[+]{Fore.WHITE} Ngrok Menu:")
        print(f"  {Fore.GREEN}1.{Fore.WHITE} Edit Token")
        print(f"  {Fore.GREEN}2.{Fore.WHITE} Start Ngrok")
        choice1 = input(f"\n{Style.BRIGHT}choice > {Style.RESET_ALL}").strip()
        
        if choice1 == "1":
            token = edit_token()
            run_ngrok(PORT, token)
        else:
            run_ngrok(PORT, token)

    elif choice == "2":
        run_cloudflare(PORT)
    else:
        print(f"{Fore.RED}[!] Invalid choice. Exiting...")
        sys.exit()

    print(f"{Fore.RED}{Style.BRIGHT}[*] Press Ctrl + C to stop\n")

    while True:
        time.sleep(10)

except KeyboardInterrupt:
    print(f"\n{Fore.RED}[!] Shutdown requested...")
    sys.exit()