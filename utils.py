import os
import sys
import platform
import subprocess
import urllib.request
import re
from pyngrok import ngrok, conf
from colorama import Fore, Style

def get_platform_specs():
    system = platform.system()
    if system == "Windows": return ".exe", "windows-amd64.exe"
    return "", "linux-amd64"

def run_cloudflare(port):
    ext, arch_url = get_platform_specs()
    bin_path = os.path.join(os.getcwd(), f"cloudflared{ext}")

    if not os.path.exists(bin_path):
        url = f"https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-{arch_url}"
        print(f"{Fore.YELLOW}[*] Downloading Cloudflared...")
        urllib.request.urlretrieve(url, bin_path)
        if platform.system() != "Windows": os.chmod(bin_path, 0o755)

    print(f"{Fore.YELLOW}[*] Starting Cloudflare Tunnel...")
    process = subprocess.Popen([bin_path, "tunnel", "--url", f"http://localhost:{port}"], 
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in process.stdout:
        match = re.search(r"https://[-\w]+\.trycloudflare\.com", line)
        if match:
            print(f"{Fore.CYAN}{Style.BRIGHT}───────────────────────────────────────")
            print(f"{Fore.GREEN}{Style.BRIGHT}[|] URL: {Fore.CYAN}{match.group(0)}")
            break

def run_ngrok(port,token):
    print(f"{Fore.YELLOW}[*] Starting Ngrok...")
    conf.get_default().auth_token = token
    try:
        public_url = ngrok.connect(port).public_url
        print(f"{Fore.CYAN}{Style.BRIGHT}───────────────────────────────────────")
        print(f"{Fore.GREEN}{Style.BRIGHT}[|] URL: {Fore.CYAN}{public_url}")
    except Exception as e:
        print(f"{Fore.RED}[!] Ngrok Error: {e}")
        sys.exit(1)