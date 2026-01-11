import os
import platform
import subprocess
import urllib.request
import re
from pyngrok import ngrok, conf
from colorama import Fore, Style, init

init(autoreset=True)

def get_platform_specs():
    system = platform.system().lower()
    machine = platform.machine().lower()
    #idk
    arch_map = {
        "x86_64": "amd64",
        "amd64": "amd64",
        "aarch64": "arm64",
        "arm64": "arm64",
        "armv7l": "arm"
    }
    arch = arch_map.get(machine, "amd64")
    
    if "windows" in system:
        return ".exe", f"windows-{arch}.exe"
    elif "darwin" in system:
        return "", "darwin-amd64"
    else:
        # Linux or Android "Termux"
        return "", f"linux-{arch}"

def run_cloudflare(port):
    # check Termux
    is_termux = os.path.exists("/data/data/com.termux/files/usr/bin/pkg")
    ext, arch_url = get_platform_specs()
    bin_path = os.path.join(os.getcwd(), f"cloudflared{ext}")

    #  Termux cloudflared
    if is_termux:
        print(f"{Fore.CYAN}[*] Termux detected. Checking for cloudflared...")
        check_pkg = subprocess.run(["which", "cloudflared"], capture_output=True, text=True)
        if check_pkg.returncode == 0:
            bin_path = "cloudflared"
        else:
            print(f"{Fore.RED}[!] Cloudflared not found! Run: pkg install tur-repo && pkg install cloudflared")
            return

    elif not os.path.exists(bin_path):
        url = f"https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-{arch_url}"
        print(f"{Fore.YELLOW}[*] Downloading Cloudflared for {arch_url}...")
        try:
            urllib.request.urlretrieve(url, bin_path)
            if os.name != 'nt': os.chmod(bin_path, 0o755)
        except Exception as e:
            print(f"{Fore.RED}[!] Download failed: {e}")
            return

    print(f"{Fore.YELLOW}[*] Starting Cloudflare Tunnel (Port: {port})...")
    
    process = subprocess.Popen(
        [bin_path, "tunnel", "--url", f"http://localhost:{port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    print(f"{Fore.YELLOW}[*] Searching for public URL...")
    
    for line in iter(process.stdout.readline, ""):
        match = re.search(r"https://[-\w]+\.trycloudflare\.com", line)
        if match:
            url = match.group(0)
            print(f"{Fore.CYAN}{Style.BRIGHT}───────────────────────────────────────")
            print(f"{Fore.GREEN}{Style.BRIGHT}[|] Cloudflare URL: {Fore.CYAN}{url}")
            break

def run_ngrok(port, token):
    if not token or token == "YOUR_TOKEN":
        print(f"{Fore.RED}[!] Ngrok token is missing!")
        return
        
    print(f"{Fore.YELLOW}[*] Starting Ngrok...")
    conf.get_default().auth_token = token
    try:
        public_url = ngrok.connect(port).public_url
        print(f"{Fore.CYAN}{Style.BRIGHT}───────────────────────────────────────")
        print(f"{Fore.GREEN}{Style.BRIGHT}[|] Ngrok URL: {Fore.CYAN}{public_url}")
    except Exception as e:
        print(f"{Fore.RED}[!] Ngrok Error: {e}")

