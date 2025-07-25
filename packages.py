import subprocess
import os
import platform
import questionary
import time
import shutil
from pathlib import Path
import re

# ANSI color codes
class Colors:
    RED = "\033[31m"
    CYAN = "\033[36m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    BLACK = "\033[30m"
    PURPLE = "\033[35m"  # Added purple color code
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    END = "\033[0m"

# Global variables
PACKAGES = [
    "slop", "wmctrl", "pulseaudio-utils", "playerctl", "zsh", "rofi", "kitty", "git", "jq",
    "cmake", "npm", "g++", "gettext", "feh", "dash", "bat", "meson", "wget", "curl",
    "xclip", "net-tools", "openvpn", "html2text", "fzf", "rlwrap", "gpick", "trash-cli",
    "brightnessctl", "jsbeautifier", "lxappearance", "ranger", "suckless-tools", "xsel",
    "qt5ct", "libxfixes-dev", "seclists"
]
DPN_DEB_BSPWM = [
    "libxcb-xinerama0-dev", "libxcb-icccm4-dev", "libxcb-randr0-dev", "libxcb-util0-dev",
    "libxcb-ewmh-dev", "libxcb-keysyms1-dev", "libxcb-shape0-dev"
]
DPN_DEB_POLY = [
    "libxcb-xkb-dev", "libxcb-xrm-dev", "libxcb-cursor-dev", "libasound2-dev", "libpulse-dev",
    "i3-wm", "libjsoncpp-dev", "libmpdclient-dev", "libcurl4-openssl-dev", "libnl-genl-3-dev"
]
DPN_DEB_PICOM = [
    "libconfig-dev", "libdbus-1-dev", "libegl-dev", "libev-dev", "libgl-dev", "libepoxy-dev",
    "libpcre2-dev", "libpixman-1-dev", "libx11-xcb-dev", "libxcb1-dev", "libxcb-composite0-dev",
    "libxcb-damage0-dev", "libxcb-glx0-dev", "libxcb-image0-dev", "libxcb-present-dev",
    "libxcb-randr0-dev", "libxcb-render0-dev", "libxcb-render-util0-dev", "libxcb-shape0-dev",
    "libxcb-util-dev", "libxcb-xfixes0-dev", "meson", "ninja-build", "uthash-dev"
]
OS = None
NAME = None
CWD = os.path.join(os.getcwd(), "dotfiles")

# Detect OS
def detect_os():
    global OS, NAME
    try:
        with open("/etc/os-release", "r") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("ID="):
                OS = line.strip().split("=")[1].lower()
            if line.startswith("NAME="):
                NAME = line.strip().split("=")[1].strip('"').split()[0]
    except Exception as e:
        print(f"{Colors.RED}{Colors.BOLD}Error detecting OS: {e}{Colors.END}")
        exit(1)

# Display banner
def banner():
    print(f"""{Colors.RED}{Colors.BOLD}
    ▄█████  ██████ ██▓███  █     █░███▄ ▄███▓▄████▄  ██▓    ██▓▄████▄
    ▓██████▒██    ▒▓██░  ██▓█░ █ ░█▓██▒▀█▀ ██▒██▀ ▀█ ▓██▒   ▓██▒██▀ ▀█
    █    ▄█░ ▓██▄  ▓██░ ██▓▒█░ █ ░█▓██    ▓██▒▓█    ▄▒██░   ▒██▒▓██
    ▒██░█▀   ▒   ██▒██▄█▓▒ ░█░ █ ░█▒██    ▒██▒▓▓▄ ▄██▒██░   ░██▒▓▓▄ ▄██▒
    ░▓█  ▀█▒█████▒▒██▒ ░  ░░██▒██▓▒██▒   ░██▒ ▓███▀ ░██████░██▒ ▓███▀ ░
    ░▒▓███▀▒ ▒▓▒ ▒ ▒▓▒░ ░  ░ ▓░▒ ▒ ░ ▒░   ░  ░ ░▒ ▒  ░ ▒░▓  ░▓ ░ ░▒ ▒░
    ░▒░  ░░ By 47z!Lu7h :)  ░ ░ ░    ▒    ░ ░  ░      ░ ░    ░
    ░     ░        ░        ░        ░
          ░         ░{Colors.END}
    """)

# Fonts installation
def install_fonts():
    fonts = ["ShareTechMono", "IosevkaTermSlab", "DaddyTimeMono", "Iosevka"]
    version = "3.4.0"
    fonts_path = "/usr/share/fonts/nerd_fonts"
    
    print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Getting fonts {Colors.YELLOW}!!!{Colors.END}")
    
    os.makedirs(fonts_path, exist_ok=True, mode=0o755)
    for font in fonts:
        zip_file = f"{font}.zip"
        download_url = f"https://github.com/ryanoasis/nerd-fonts/releases/download/v{version}/{zip_file}"
        print(f"\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Installing {Colors.YELLOW}'{font}'{Colors.END}{Colors.BLUE} in {Colors.PURPLE}{fonts_path}{Colors.END}")
        try:
            subprocess.run(["wget", download_url], check=True)
            subprocess.run(["sudo", "unzip", "-n", zip_file, "-d", fonts_path], check=True)
            os.remove(zip_file)
        except subprocess.CalledProcessError:
            print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing {font}{Colors.END}{Colors.BLUE} ======={Colors.END}")
            exit(1)
    
    subprocess.run(["sudo", "find", fonts_path, "-name", "*Windows Compatible*", "-delete"], check=True)
    subprocess.run(["sudo", "find", fonts_path, "-name", "LICENSE*", "-delete"], check=True)
    subprocess.run(["sudo", "find", fonts_path, "-name", "README*", "-delete"], check=True)
    subprocess.run(["sudo", "find", fonts_path, "-name", "*.txt", "-delete"], check=True)
    subprocess.run(["sudo", "fc-cache", "-fv"], check=True)
    
    print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Getting Candy icons {Colors.CYAN}~~>{Colors.END}")
    try:
        subprocess.run(["wget", "https://github.com/EliverLara/candy-icons/archive/refs/heads/master.zip", "-O", "candy-icons.zip"], check=True)
        subprocess.run(["sudo", "unzip", "-o", "candy-icons.zip", "-d", "/usr/share/icons/"], check=True)
        os.remove("candy-icons.zip")
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing Candy icons{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)

# Compile Bspwm & Sxhkd
def compile_bspwm():
    print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|>{Colors.GREEN} Cloning bspwm & sxhkd{Colors.CYAN} -->{Colors.END}")
    os.makedirs("bspwm", exist_ok=True)
    os.chdir("bspwm")
    try:
        subprocess.run(["git", "clone", "https://github.com/baskerville/bspwm.git"], check=True)
        os.chdir("bspwm")
        subprocess.run(["make"], check=True)
        subprocess.run(["sudo", "make", "install"], check=True)
        os.chdir("..")
        print(f"\n{Colors.BOLD}{Colors.CYAN}<|[+]|>{Colors.GREEN} Cloning Sxhkd{Colors.CYAN} ~~>{Colors.END}")
        subprocess.run(["git", "clone", "https://github.com/baskerville/sxhkd.git"], check=True)
        os.chdir("sxhkd")
        subprocess.run(["make"], check=True)
        subprocess.run(["sudo", "make", "install"], check=True)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error compiling Bspwm/Sxhkd{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)
    finally:
        os.chdir("../..")
        shutil.rmtree("bspwm", ignore_errors=True)

# Compile Polybar
def compile_polybar():
    print(f"\n{Colors.BOLD}{Colors.CYAN}|[+]|> {Colors.GREEN}Cloning & compiling Polybar{Colors.CYAN}~~>{Colors.END}")
    os.makedirs("polybar", exist_ok=True)
    os.chdir("polybar")
    try:
        subprocess.run(["git", "clone", "--recursive", "https://github.com/polybar/polybar"], check=True)
        os.chdir("polybar")
        os.makedirs("build", exist_ok=True)
        os.chdir("build")
        subprocess.run(["cmake", ".."], check=True)
        subprocess.run(["make", "-j" + str(os.cpu_count())], check=True)
        subprocess.run(["sudo", "make", "install"], check=True)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error compiling Polybar{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)
    finally:
        os.chdir("../../..")
        shutil.rmtree("polybar", ignore_errors=True)

# Install Clipmenu
def install_clipmenu():
    if shutil.which("clipmenu"):
        print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}clipmenu {Colors.CYAN}d@n3{Colors.RED}!!{Colors.END}")
        return
    print(f"\n{Colors.BOLD}{Colors.CYAN}|[+]|> {Colors.GREEN}Cloning Clipmenu{Colors.CYAN}~~>{Colors.END}")
    if OS == "debian":
        subprocess.run(["sudo", "apt-get", "install", "-y", "g++", "gcc", "make", "python2.7", "pkg-config", "libx11-dev", "libxkbfile-dev", "libsecret-1-dev"], check=True)
    try:
        subprocess.run(["git", "clone", "https://github.com/cdown/clipmenu.git"], check=True)
        os.chdir("clipmenu")
        subprocess.run(["make"], check=True)
        subprocess.run(["sudo", "make", "install"], check=True)
        os.chdir("..")
        subprocess.run(["git", "clone", "https://github.com/cdown/clipnotify.git"], check=True)
        os.chdir("clipnotify")
        subprocess.run(["make"], check=True)
        subprocess.run(["sudo", "make", "install"], check=True)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error compiling clipmenu{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)
    finally:
        os.chdir("..")
        shutil.rmtree("clipmenu", ignore_errors=True)

# Compile Picom
def install_picom():
    print(f"\n{Colors.BOLD}{Colors.CYAN}|[+]|> {Colors.END}{Colors.WHITE}Cloning & compiling Picom{Colors.CYAN}~~>{Colors.END}")
    os.makedirs("picom", exist_ok=True)
    os.chdir("picom")
    try:
        subprocess.run(["git", "clone", "https://github.com/yshui/picom.git"], check=True)
        os.chdir("picom")
        subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=True)
        subprocess.run(["meson", "setup", "--buildtype=release", ".", "build"], check=True)
        subprocess.run(["ninja", "-C", "build"], check=True)
        subprocess.run(["ninja", "-C", "build", "install"], check=True)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error compiling Picom{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)
    finally:
        os.chdir("../..")
        shutil.rmtree("picom", ignore_errors=True)

# Install VS Code
def install_vscode():
    print(f"\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.BLUE}Installing VS Code{Colors.CYAN}~~>{Colors.END}")
    if OS == "debian":
        try:
            subprocess.run(["sudo", "apt-get", "install", "-y", "wget", "gpg"], check=True)
            subprocess.run(["wget", "-qO-", "https://packages.microsoft.com/keys/microsoft.asc", "|", "gpg", "--dearmor"], stdout=open("packages.microsoft.gpg", "wb"), check=True)
            subprocess.run(["sudo", "install", "-D", "-o", "root", "-g", "root", "-m", "644", "packages.microsoft.gpg", "/etc/apt/keyrings/packages.microsoft.gpg"], check=True)
            with open("/etc/apt/sources.list.d/vscode.list", "w") as f:
                f.write("deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main")
            os.remove("packages.microsoft.gpg")
            subprocess.run(["sudo", "apt", "purge", "-fy", "code*"], check=True)
            subprocess.run(["sudo", "apt", "install", "apt-transport-https", "-y"], check=True)
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "code", "-y"], check=True)
            shutil.copytree(f"{CWD}/config/Code/User", f"{os.path.expanduser('~')}/.config/Code/User", dirs_exist_ok=True)
        except subprocess.CalledProcessError:
            print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing VS Code{Colors.END}{Colors.BLUE} ======={Colors.END}")
            exit(1)
    elif OS == "fedora":
        try:
            subprocess.run(["sudo", "rpm", "--import", "https://packages.microsoft.com/keys/microsoft.asc"], check=True)
            with open("/etc/yum.repos.d/vscode.repo", "w") as f:
                f.write("[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc")
            subprocess.run(["dnf", "check-update"], check=True)
            subprocess.run(["sudo", "dnf", "install", "code"], check=True)
            subprocess.run(["code"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            time.sleep(3)
            subprocess.run(["sudo", "killall", "code"], check=True)
            shutil.copytree(f"{CWD}/config/Code/User", f"{os.path.expanduser('~')}/.config/Code/User", dirs_exist_ok=True)
        except subprocess.CalledProcessError:
            print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing VS Code{Colors.END}{Colors.BLUE} ======={Colors.END}")
            exit(1)
    elif OS == "arch":
        try:
            subprocess.run(["sudo", "pacman", "-S", "code"], check=True)
            shutil.copytree(f"{CWD}/config/Code/User", f"{os.path.expanduser('~')}/.config/Code/User", dirs_exist_ok=True)
        except subprocess.CalledProcessError:
            print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing VS Code{Colors.END}{Colors.BLUE} ======={Colors.END}")
            exit(1)

# Install LSD
def install_lsd():
    if shutil.which("lsd"):
        print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.RED}l5d {Colors.CYAN}d0n3{Colors.RED}!!{Colors.END}")
        return
    print(f"\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.BLUE}Downloading lsd{Colors.CYAN}~~>{Colors.END}")
    try:
        if OS == "debian":
            subprocess.run(["sudo", "apt", "install", "lsd", "-y"], check=True)
        elif OS == "arch":
            subprocess.run(["sudo", "pacman", "-S", "lsd"], check=True)
        elif OS == "fedora":
            subprocess.run(["sudo", "dnf", "install", "lsd", "-y"], check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["wget", "https://github.com/lsd-rs/lsd/releases/download/v1.1.2/lsd_1.1.2_amd64.deb", "-O", "lsd.deb"], check=True)
            subprocess.run(["sudo", "dpkg", "-i", "lsd.deb"], check=True)
            os.remove("lsd.deb")
        except subprocess.CalledProcessError:
            print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing lsd{Colors.END}{Colors.BLUE} ======={Colors.END}")
            exit(1)

# Install RustScan
def install_rustscan():
    if shutil.which("rustscan"):
        print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}RustScan {Colors.CYAN}d@n3!!{Colors.END}")
        return
    try:
        subprocess.run(["wget", "https://github.com/bee-san/RustScan/releases/download/2.4.1/rustscan.deb.zip"], check=True)
        subprocess.run(["unzip", "rustscan.deb.zip"], check=True)
        subprocess.run(["sudo", "dpkg", "-i", "rustscan_2.4.1_amd64.deb"], check=True)
        for f in Path.cwd().glob("rustscan*"):
            f.unlink()
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing RustScan{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)

# Install Rust & Cargo
def install_rust_cargo():
    try:
        subprocess.run(["curl", "https://sh.rustup.rs", "-sSf", "|", "sh"], shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing Rust & Cargo{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)

# Install Telegram
def install_telegram():
    if shutil.which("telegram"):
        print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Telegram {Colors.CYAN}d@n3!!{Colors.END}")
        return
    try:
        subprocess.run(["wget", "https://github.com/telegramdesktop/tdesktop/releases/download/v5.13.1/tsetup.5.13.1.tar.xz"], check=True)
        subprocess.run(["tar", "-xf", "tsetup.5.13.1.tar.xz"], check=True)
        subprocess.run(["sudo", "cp", "Telegram/Telegram", "/usr/bin/telegram"], check=True)
        subprocess.run(["sudo", "cp", "Telegram/Updater", "/usr/bin/telegram-Updater"], check=True)
        shutil.rmtree("Telegram", ignore_errors=True)
        for f in Path.cwd().glob("tsetup*"):
            f.unlink()
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing Telegram{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)

# Install Google Chrome
def install_chrome():
    if shutil.which("google-chrome"):
        print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Chrome {Colors.CYAN}d@n3!!{Colors.END}")
        return
    try:
        if OS == "debian":
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "software-properties-common", "apt-transport-https", "ca-certificates", "curl", "-y"], check=True)
            subprocess.run(["curl", "-fSsL", "https://dl.google.com/linux/linux_signing_key.pub", "|", "sudo", "gpg", "--dearmor", "-o", "/usr/share/keyrings/google-chrome.gpg"], check=True)
            with open("/etc/apt/sources.list.d/google-chrome.list", "w") as f:
                f.write("deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main")
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "google-chrome-stable"], check=True)
        elif OS == "arch":
            subprocess.run(["sudo", "pacman", "-S", "google-chrome"], check=True)
        elif OS == "fedora":
            subprocess.run(["sudo", "dnf", "-y", "google-chrome"], check=True)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing Google Chrome{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)

# Install OBS Studio
def install_obs():
    if shutil.which("obs"):
        print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}obs {Colors.CYAN}d@n3{Colors.RED}!!{Colors.END}")
        return
    try:
        subprocess.run(["sudo", "apt", "install", "-y", "v4l2loopback-dkms"], check=True)
        subprocess.run(["sudo", "add-apt-repository", "ppa:obsproject/obs-studio", "-y"], check=True)
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "obs-studio"], check=True)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing OBS Studio{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)

# Install Firefox ESR
def install_firefox_esr():
    if shutil.which("firefox-esr"):
        if os.path.exists(os.path.expanduser("~/.mozilla")):
            shutil.copytree(f"{CWD}/misc/home/.mozilla/firefox/chrome", f"{os.path.expanduser('~')}/.mozilla/firefox/*default-esr*/", dirs_exist_ok=True)
        else:
            print(f"\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Setting firefox-esr theme{Colors.CYAN}!{Colors.END}")
            subprocess.run(["firefox-esr"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            time.sleep(4)
            subprocess.run(["sudo", "killall", "firefox-esr"], check=True)
            time.sleep(1)
            shutil.copytree(f"{CWD}/misc/home/.mozilla/firefox/chrome", f"{os.path.expanduser('~')}/.mozilla/firefox/*default-esr*/", dirs_exist_ok=True)
        return
    try:
        if OS == "debian":
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "firefox-esr", "-y"], check=True)
            subprocess.run(["sudo", "apt", "autoremove", "-y"], check=True)
            subprocess.run(["sudo", "apt", "autoclean", "-y"], check=True)
            subprocess.run(["firefox-esr"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            time.sleep(4)
            subprocess.run(["sudo", "killall", "firefox-esr"], check=True)
            time.sleep(1)
            shutil.copytree(f"{CWD}/misc/home/.mozilla/firefox/chrome", f"{os.path.expanduser('~')}/.mozilla/firefox/*default-esr*/", dirs_exist_ok=True)
        elif NAME == "Ubuntu":
            print(f"\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.BLUE}Installing firefox-esr{Colors.CYAN}!{Colors.END}")
            subprocess.run(["sudo", "add-apt-repository", "ppa:mozillateam/ppa"], check=True)
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "firefox-esr"], check=True)
            subprocess.run(["firefox-esr"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            time.sleep(4)
            subprocess.run(["sudo", "killall", "firefox-esr"], check=True)
            time.sleep(1)
            shutil.copytree(f"{CWD}/misc/home/.mozilla/firefox/chrome", f"{os.path.expanduser('~')}/.mozilla/firefox/*default-esr*/", dirs_exist_ok=True)
        elif OS == "arch":
            subprocess.run(["sudo", "pacman", "-S", "firefox-esr"], check=True)
        elif OS == "fedora":
            subprocess.run(["sudo", "dnf", "-y", "firefox-esr"], check=True)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing Firefox ESR{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)

# Install Neovim & NvChad
def install_nvim():
    if shutil.which("nvim"):
        if os.path.exists(os.path.expanduser("~/.config/nvim")):
            print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Nvim~NvChad {Colors.CYAN}d@n3!!{Colors.END}")
        else:
            print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Cloning Nvim~NvChad{Colors.CYAN} -->{Colors.END}")
            for path in [os.path.expanduser("~/.config/nvim"), os.path.expanduser("~/.local/share/nvim"), os.path.expanduser("~/.cache/nvim"),
                         "/root/.config/nvim", "/root/.local/share/nvim", "/root/.cache/nvim"]:
                shutil.rmtree(path, ignore_errors=True)
            subprocess.run(["git", "clone", "--depth", "1", "https://github.com/NvChad/starter", os.path.expanduser("~/.config/nvim")], check=True)
            subprocess.run(["sudo", "git", "clone", "--depth", "1", "https://github.com/NvChad/starter", "/root/.config/nvim"], check=True)
        return
    print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Cloning & compiling neovim + cloning NvChad{Colors.CYAN} -->{Colors.END}")
    os.makedirs("nvim", exist_ok=True)
    os.chdir("nvim")
    try:
        subprocess.run(["git", "clone", "https://github.com/neovim/neovim"], check=True)
        os.chdir("neovim")
        subprocess.run(["make", "CMAKE_BUILD_TYPE=RelWithDebInfo"], check=True)
        subprocess.run(["sudo", "make", "install"], check=True)
        os.chdir("..")
        for path in [os.path.expanduser("~/.config/nvim"), os.path.expanduser("~/.local/share/nvim"), os.path.expanduser("~/.cache/nvim"),
                     "/root/.config/nvim", "/root/.local/share/nvim", "/root/.cache/nvim"]:
            shutil.rmtree(path, ignore_errors=True)
        subprocess.run(["git", "clone", "--depth", "1", "https://github.com/NvChad/starter", os.path.expanduser("~/.config/nvim")], check=True)
        subprocess.run(["sudo", "git", "clone", "--depth", "1", "https://github.com/NvChad/starter", "/root/.config/nvim"], check=True)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing Neovim/NvChad{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)
    finally:
        os.chdir("../..")
        shutil.rmtree("nvim", ignore_errors=True)

# Install htbXplorer
def install_htb_xplorer():
    if os.path.exists("/opt/h4Ck/htbXplorer-Plus"):
        print(f"\n\n{Colors.BOLD}{Colors.RED}|{Colors.END}{Colors.RED}󰓗 {Colors.END}{Colors.WHITE}<~{Colors.END}{Colors.WHITE}{Colors.BOLD}{Colors.GREEN} 󰆧 {Colors.END}{Colors.WHITE}~> \t{Colors.END}{Colors.RED}H7b{Colors.YELLOW}~{Colors.RED}Xpl@R3r {Colors.YELLOW}already in the system{Colors.RED}!\t{Colors.PURPLE}{Colors.BOLD}󱝂 {Colors.END}{Colors.WHITE}{Colors.BOLD}{Colors.BLUE}󱜚{Colors.END}")
        return
    print(f"\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Cloning htbXplorer from github{Colors.CYAN}~~>{Colors.END}")
    try:
        subprocess.run(["sudo", "mkdir", "-p", "/opt/h4Ck/htbXplorer-Plus"], check=True)
        subprocess.run(["sudo", "git", "clone", "https://github.com/4tz1Lu7h/htbXplorer-Plus.git", "/opt/h4Ck/htbXplorer-Plus"], check=True)
        subprocess.run(["sudo", "chmod", "+x", "/opt/h4Ck/htbXplorer-Plus/htbXplorer"], check=True)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing htbXplorer{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)

# Install Zsh plugins
def install_zsh_plugins():
    print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Cloning zsh plugins {Colors.CYAN} -->{Colors.END}")
    plugins = [
        ("powerlevel10k", "https://github.com/romkatv/powerlevel10k.git", "/usr/share/zsh/powerlevel10k"),
        ("zsh-autosuggestions", "https://github.com/zsh-users/zsh-autosuggestions.git", "/usr/share/zsh-autosuggestions"),
        ("zsh-autocomplete", "https://github.com/marlonrichert/zsh-autocomplete.git", "/usr/share/zsh-autocomplete"),
        ("zsh-fzf-history-search", "https://github.com/joshskidmore/zsh-fzf-history-search.git", "/usr/share/zsh-fzf-history-search"),
        ("git-completion.zsh", "https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.zsh", os.path.expanduser("~/.zsh/git-completion.zsh")),
        ("sudo.plugin.zsh", "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/plugins/sudo/sudo.plugin.zsh", "/usr/share/zsh/sudo.plugin.zsh"),
        ("zsh-syntax-highlighting", "https://github.com/zsh-users/zsh-syntax-highlighting.git", "/usr/share/zsh-syntax-highlighting")
    ]
    for name, url, path in plugins:
        if os.path.exists(path):
            print(f"\n{Colors.BOLD}{Colors.BLACK} {Colors.END}{Colors.BLUE}{name}{Colors.YELLOW}\t \t{Colors.GREEN}done {Colors.BOLD}{Colors.END}")
        else:
            try:
                if "zsh-syntax-highlighting" in name:
                    if OS == "debian":
                        subprocess.run(["sudo", "apt", "install", "-y", "zsh-syntax-highlighting"], check=True)
                    elif OS == "arch":
                        subprocess.run(["sudo", "pacman", "-S", "zsh-syntax-highlighting"], check=True)
                    elif OS == "fedora":
                        subprocess.run(["sudo", "dnf", "install", "zsh-syntax-highlighting", "-y"], check=True)
                    else:
                        subprocess.run(["sudo", "git", "clone", url, path], check=True)
                else:
                    if os.path.isdir(path):
                        subprocess.run(["sudo", "git", "clone", "--depth", "1", url, path], check=True)
                    else:
                        subprocess.run(["wget", url, "-P", os.path.dirname(path)], check=True)
            except subprocess.CalledProcessError:
                print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing {name}{Colors.END}{Colors.BLUE} ======={Colors.END}")
                exit(1)
            print(f"\n{Colors.BOLD}{Colors.BLACK} {Colors.END}{Colors.BLUE}{name}{Colors.YELLOW}\t \t{Colors.GREEN}done {Colors.BOLD}{Colors.END}")

# Install dotfiles
def install_dotfiles():
    print(f"\n\n{Colors.BOLD}{Colors.CYAN}<[+]> {Colors.END}{Colors.BLUE}Copying {Colors.BOLD}dotfiles{Colors.CYAN}{Colors.END}")
    configs = ["bspwm", "polybar", "picom", "sxhkd", "kitty", "rofi"]
    for config in configs:
        config_path = os.path.expanduser(f"~/.config/{config}")
        if os.path.exists(config_path):
            shutil.move(config_path, f"{config_path}.OLD")
    shutil.copytree(f"{CWD}/config", os.path.expanduser("~/.config"), dirs_exist_ok=True)
    if NAME == "Kali":
        subprocess.run(["sudo", "apt", "install", "-y", "neowofetch"], check=True)
    else:
        subprocess.run(["sudo", "apt", "install", "-y", "neofetch"], check=True)
    subprocess.run(["sudo", "cp", "-r", f"{CWD}/misc/usr/share", "/usr/share"], check=True)
    if os.path.exists(os.path.expanduser("~/.zshrc")):
        shutil.move(os.path.expanduser("~/.zshrc"), os.path.expanduser("~/.zshrc.OLD"))
    for item in Path(f"{CWD}/misc/home").glob(".*"):
        shutil.copy(item, os.path.expanduser("~"))
    try:
        with open("/etc/passwd", "r") as f:
            passwd = f.read()
        passwd = re.sub(r"bash", "zsh", passwd)
        with open("/etc/passwd", "w") as f:
            f.write(passwd)
        subprocess.run(["sudo", "ln", "-s", "-f", os.path.expanduser("~/.zsh"), "/root"], check=True)
        subprocess.run(["sudo", "ln", "-s", "-f", os.path.expanduser("~/.zshrc"), "/root"], check=True)
        subprocess.run(["sudo", "ln", "-s", "-f", os.path.expanduser("~/.p10k.zsh"), "/root"], check=True)
        print(f"\n{Colors.BOLD}{Colors.BLACK}󰧟{Colors.END}{Colors.CYAN}Dotfiles {Colors.YELLOW}\t {Colors.BOLD}\t{Colors.GREEN}Done{Colors.WHITE}! {Colors.BOLD}{Colors.GREEN}{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing dotfiles: {e}{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)

# Main function
def main(selected_functions):
    # Install packages if needed (e.g., for Pentest Base)
    if "pentest_base" in selected_functions or "all_in_one" in selected_functions:
        print(f"\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Installing Packages {Colors.BOLD}{Colors.CYAN}~~>{Colors.END}")
        if OS == "debian":
            try:
                subprocess.run(["sudo", "apt", "install", "-y"] + PACKAGES, check=True)
            except subprocess.CalledProcessError:
                print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error installing packages{Colors.END}{Colors.BLUE} ======={Colors.END}")
                exit(1)
        elif OS == "arch" or OS == "fedora":
            print(f"\n\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Still in development for {Colors.BOLD}{Colors.YELLOW}{OS.capitalize()} {Colors.CYAN}Distro {Colors.END}{Colors.BLUE} ======={Colors.END}")
            exit(1)

    # Check and install or compile components
    if "install_picom" not in selected_functions and shutil.which("picom"):
        print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.RED}p1C0m {Colors.CYAN}d0n3{Colors.RED}!!{Colors.END}")
    elif "install_picom" in selected_functions:
        if OS == "debian":
            try:
                subprocess.run(["sudo", "apt", "install", "picom", "-y"], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(["sudo", "apt", "install", "-y"] + DPN_DEB_PICOM, check=True)
                install_picom()
        elif OS == "arch":
            try:
                subprocess.run(["sudo", "pacman", "-S", "picom"], check=True)
            except subprocess.CalledProcessError:
                install_picom()
        elif OS == "fedora":
            try:
                subprocess.run(["sudo", "dnf", "install", "picom"], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(["sudo", "dnf", "install"] + DPN_DEB_PICOM, check=True)
                install_picom()

    if "compile_bspwm" not in selected_functions and shutil.which("bspwm"):
        print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.RED}b5pWm {Colors.CYAN}d0n3{Colors.RED}!!{Colors.END}")
    elif "compile_bspwm" in selected_functions:
        if OS == "debian":
            try:
                subprocess.run(["sudo", "apt", "install", "bspwm", "sxhkd", "-y"], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(["sudo", "apt", "install", "-y"] + DPN_DEB_BSPWM, check=True)
                compile_bspwm()
        elif OS == "arch":
            try:
                subprocess.run(["sudo", "pacman", "-S", "bspwm", "sxhkd"], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(["sudo", "pacman", "-S"] + ["libxcb", "xcb-util", "xcb-util-wm", "xcb-util-keysyms"], check=True)
                compile_bspwm()
        elif OS == "fedora":
            try:
                subprocess.run(["sudo", "dnf", "install", "bspwm", "sxhkd", "-y"], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(["sudo", "dnf", "install"] + ["libxcb", "xcb-util", "xcb-util-wm", "xcb-util-keysyms", "libxcb-devel", "xcb-util-wm-devel", "xcb-util-keysyms-devel", "xcb-util-devel"], check=True)
                compile_bspwm()

    if "compile_polybar" not in selected_functions and shutil.which("polybar"):
        print(f"\n\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.RED}p0ly {Colors.CYAN}d0n3{Colors.RED}!!{Colors.END}")
    elif "compile_polybar" in selected_functions:
        if OS == "debian":
            try:
                subprocess.run(["sudo", "apt", "install", "polybar", "-y"], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(["sudo", "apt", "install", "-y"] + DPN_DEB_POLY, check=True)
                compile_polybar()
        elif OS == "arch":
            try:
                subprocess.run(["sudo", "pacman", "-S", "polybar"], check=True)
            except subprocess.CalledProcessError:
                compile_polybar()
        elif OS == "fedora":
            try:
                subprocess.run(["sudo", "dnf", "install", "polybar"], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(["sudo", "dnf", "install"] + ["xcb-util-xrm-devel", "xcb-util-cursor-devel", "alsa-lib-devel", "pulseaudio-libs-devel", "i3-devel", "jsoncpp-devel", "libmpdclient-devel", "libcurl-devel", "libnl3-devel"], check=True)
                compile_polybar()

    function_map = {
        "install_fonts": install_fonts,
        "compile_bspwm": compile_bspwm,
        "compile_polybar": compile_polybar,
        "install_clipmenu": install_clipmenu,
        "install_picom": install_picom,
        "install_vscode": install_vscode,
        "install_lsd": install_lsd,
        "install_rustscan": install_rustscan,
        "install_rust_cargo": install_rust_cargo,
        "install_telegram": install_telegram,
        "install_chrome": install_chrome,
        "install_obs": install_obs,
        "install_firefox_esr": install_firefox_esr,
        "install_nvim": install_nvim,
        "install_htb_xplorer": install_htb_xplorer,
        "install_zsh_plugins": install_zsh_plugins,
        "install_dotfiles": install_dotfiles
    }

    for func_name in selected_functions:
        if func_name in function_map:
            function_map[func_name]()

# Main execution
if __name__ == "__main__":
    detect_os()
    if os.geteuid() == 0:
        print(f"\n\n{Colors.BOLD}{Colors.RED}<|{Colors.BLACK}[{Colors.RED}!{Colors.BLACK}]{Colors.RED}|{Colors.BLACK}[{Colors.RED}!{Colors.BLACK}]{Colors.RED}|> \t{Colors.CYAN}You do not have to be {Colors.RED}root {Colors.CYAN}to execute this script \t{Colors.RED};-){Colors.END}")
        exit(1)
    
    banner()
    print(f"\n{Colors.CYAN}<|{Colors.BOLD}[{Colors.RED}+{Colors.CYAN}]{Colors.END}{Colors.CYAN}|{Colors.CYAN}>{Colors.BOLD}{Colors.BLACK} ~~~ {Colors.END}{Colors.BLUE}This Script Will Add {Colors.BOLD}{Colors.CYAN}Bspwm {Colors.END}{Colors.BLUE}Desktop Environment To Your Linux.")
    print(f"\n{Colors.CYAN}<|{Colors.BOLD}[{Colors.RED}+{Colors.CYAN}]{Colors.END}{Colors.CYAN}|{Colors.CYAN}>{Colors.BOLD}{Colors.BLACK} ~~~ {Colors.END}{Colors.BLUE}Alongside with some other packages like:\n\t\t{Colors.CYAN}Polybar{Colors.BLUE},{Colors.CYAN} Picom{Colors.BLUE},{Colors.CYAN} ZHS{Colors.BLUE},{Colors.CYAN} Sxhkd{Colors.BLUE},{Colors.CYAN} Nvim{Colors.BLUE},{Colors.CYAN} VS-Code{Colors.BLUE},{Colors.CYAN} firefox_esr{Colors.BLUE},{Colors.CYAN} Lsd{Colors.BLUE}...")

    choices = [
        {"name": "All in One (Install all components)", "value": "all_in_one"},
        {"name": "Pentest Base (Bspwm, Picom, Polybar, Nvim, Lsd, htb-Xplorer, Zsh Plugins, Clipmenu, VS Code, Chrome, Dotfiles, Firefox ESR)", "value": "pentest_base"},
        {"name": "Install Fonts", "value": "install_fonts"},
        {"name": "Compile Bspwm & Sxhkd", "value": "compile_bspwm"},
        {"name": "Compile Polybar", "value": "compile_polybar"},
        {"name": "Install Clipmenu", "value": "install_clipmenu"},
        {"name": "Compile Picom", "value": "install_picom"},
        {"name": "Install VS Code", "value": "install_vscode"},
        {"name": "Install LSD", "value": "install_lsd"},
        {"name": "Install RustScan", "value": "install_rustscan"},
        {"name": "Install Rust & Cargo", "value": "install_rust_cargo"},
        {"name": "Install Telegram", "value": "install_telegram"},
        {"name": "Install Google Chrome", "value": "install_chrome"},
        {"name": "Install OBS Studio", "value": "install_obs"},
        {"name": "Install Firefox ESR", "value": "install_firefox_esr"},
        {"name": "Install Neovim & NvChad", "value": "install_nvim"},
        {"name": "Install htbXplorer", "value": "install_htb_xplorer"},
        {"name": "Install Zsh Plugins", "value": "install_zsh_plugins"},
        {"name": "Install Dotfiles", "value": "install_dotfiles"}
    ]

    selected = questionary.checkbox(
        "Select the components to install:",
        choices=choices
    ).ask()

    if not selected:
        print(f"\n{Colors.CYAN}<{Colors.BOLD}{Colors.BLACK}|{Colors.CYAN}[{Colors.BLACK}!{Colors.CYAN}]{Colors.BOLD}{Colors.BLACK}|{Colors.END}{Colors.CYAN}>\t{Colors.BOLD}{Colors.BLACK}\t~~~>>\t\t{Colors.RED}By3{Colors.CYAN}!!{Colors.BOLD}{Colors.BLACK}\t\t<<~~~~{Colors.END}")
        exit(0)

    # Handle All in One and Pentest Base
    if "all_in_one" in selected:
        selected = [choice["value"] for choice in choices if choice["value"] != "all_in_one" and choice["value"] != "pentest_base"]
    elif "pentest_base" in selected:
        selected = [
            "compile_bspwm", "install_picom", "compile_polybar", "install_nvim",
            "install_lsd", "install_htb_xplorer", "install_zsh_plugins", "install_clipmenu",
            "install_vscode", "install_chrome", "install_dotfiles", "install_firefox_esr"
        ]

    print(f"\n{Colors.BLUE}{Colors.BOLD}======================================================================== ")
    print(f"{Colors.BLUE}{Colors.BOLD}   -|-|-|-|- {Colors.CYAN}Installing package for {Colors.END}{Colors.RED}{NAME} {Colors.END}{Colors.BLUE}-|-|-|-|-")
    print(f"{Colors.BLUE}{Colors.BOLD}======================================================================== ")

    print(f"\n{Colors.BOLD}{Colors.CYAN}<|[+]|> {Colors.END}{Colors.BLUE}Upgrading System {Colors.BOLD}{Colors.CYAN}~~>{Colors.END}")
    try:
        if OS == "debian":
            if NAME == "Parrot":
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "parrot-upgrade"], check=True)
                subprocess.run(["sudo", "apt", "autoremove", "-y"], check=True)
                subprocess.run(["sudo", "dpkg", "--configure", "-a"], check=True)
            elif NAME == "Kali":
                subprocess.run(["sudo", "apt", "update", "-y"], check=True)
                subprocess.run(["sudo", "apt", "-y", "upgrade"], check=True)
                subprocess.run(["sudo", "apt", "autoremove", "-y"], check=True)
                subprocess.run(["sudo", "dpkg", "--configure", "-a"], check=True)
        elif OS == "arch" or OS == "fedora":
            print(f"\n\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Still in development for {Colors.BOLD}{Colors.YELLOW}{OS.capitalize()} {Colors.CYAN}Distro {Colors.END}{Colors.BLUE} ======={Colors.END}")
            exit(1)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.BLUE}{Colors.BOLD}======= {Colors.CYAN}Error upgrading system{Colors.END}{Colors.BLUE} ======={Colors.END}")
        exit(1)

    main(selected)

    print(f"\n{Colors.BOLD}{Colors.RED}<{Colors.END}{Colors.BLACK}|{Colors.END}{Colors.BLUE}[{Colors.BOLD}{Colors.RED}!{Colors.END}{Colors.BLUE}]{Colors.BLACK}|{Colors.BOLD}{Colors.RED}>{Colors.END}{Colors.BLUE} To-Dos{Colors.RED} ~~>{Colors.END}")
    print(f"\n\t{Colors.END}{Colors.RED}~{Colors.END}{Colors.BLUE} Open a terminal & type {Colors.END}{Colors.CYAN}nvim {Colors.END}{Colors.BLUE}to finish its configuration.")
    print(f"\n\t{Colors.END}{Colors.RED}~{Colors.END}{Colors.BLUE} For dark theme Firefox-esr, open it & type => {Colors.END}{Colors.CYAN}about{Colors.RED}:{Colors.END}{Colors.CYAN}config{Colors.END}{Colors.BLUE}, then search for -->")
    print(f"\n\t{Colors.END}{Colors.RED}<{Colors.END}{Colors.CYAN}toolkit.legacyUserProfileCustomizations.stylesheets{Colors.END}{Colors.RED}>{Colors.BLUE}, and set it to {Colors.BOLD}{Colors.CYAN}True{Colors.END}{Colors.BLUE}.")
    print(f"\n\n{Colors.BOLD}{Colors.RED}------/-/-/-/~~~~>> >>> {Colors.END}{Colors.YELLOW}Try reboot and select {Colors.BOLD}{Colors.RED}Bspwm {Colors.END}{Colors.YELLOW}as desktop Environment. Enjoy!! {Colors.RED};-){Colors.END}{Colors.RED} <<< <<~~~~~\\-\\-\\------{Colors.END}")
