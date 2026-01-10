from flask import Flask
from flask_cors import CORS
from routes import web
from utils import run_cloudflare, run_ngrok
import logging
import sys
import flask.cli
from colorama import Fore, Style, init
import os

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

token = get_token()
init(autoreset=True)

flask.cli.show_server_banner = lambda *args: None
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

PORT = 1111
app = Flask(__name__)
CORS(app)

print(Fore.CYAN + r"""
  ______         _____                
 |  ____|       / ____|               
 | |__ _____  _| |     __ _ _ __ ___  
 |  __/ _ \ \/ / |    / _` | '_ ` _ \ 
 | | |  __/>  <| |___| (_| | | | | | |
 |_|  \___/_/\_\\_____\__,_|_| |_| |_|
""")

print(f"{Fore.YELLOW}[+]{Fore.WHITE} Select Tunnel Method:")
print(f"  {Fore.GREEN}1.{Fore.WHITE} Ngrok")
print(f"  {Fore.GREEN}2.{Fore.WHITE} Cloudflare")

try:
    choice = input(f"\n{Style.BRIGHT}choice > {Style.RESET_ALL}").strip()
    
    web(app)

    if choice == "1":
       if token:
           print(f"{Fore.YELLOW}[+]{Fore.WHITE} Select Ngrok Token:")
           print(f"  {Fore.GREEN}1.{Fore.WHITE} Edit Token")
           print(f"  {Fore.GREEN}2.{Fore.WHITE} Start Ngrok")
           choice1 = input(f"\n{Style.BRIGHT}choice > {Style.RESET_ALL}").strip()
       
           if choice1 == "1":
               token = edit_token()
               run_ngrok(PORT, token)
           elif choice1 == "2":
               run_ngrok(PORT, token)
           else:
               print(f"{Fore.RED}[!] Invalid choice")
       
       else:
           print(f"{Fore.RED}[!] No ngrok token found. Please select 'Edit' to add one first.")
           print(f"{Fore.GREEN}1.{Fore.WHITE} Edit Token")
           choice1 = input(f"\n{Style.BRIGHT}choice > {Style.RESET_ALL}").strip()
           if choice1 == "1":
               token = edit_token()
               run_ngrok(PORT, token)
           else:
               print(f"{Fore.RED}[!] Cannot start Ngrok without token.")





    elif choice == "2":
        run_cloudflare(PORT)
    else:
        print(f"{Fore.RED}[!] Invalid choice. Exiting...")
        sys.exit()

    print(f"{Fore.GREEN}{Style.BRIGHT}[|] Server is live on port {PORT}")
    print(f"{Fore.RED}{Style.BRIGHT}[*] Press Ctrl + C to stop\n")


    if __name__ == '__main__':
        app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

except KeyboardInterrupt:
    print(f"\n{Fore.RED}[!] Shutdown requested...")
    sys.exit()