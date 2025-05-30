#!/bin/bash
# Author: Roi Diéguez - aka 47z!Lu7h

	# --> Banner
function banner(){
echo -ne "\t\t\t${red}${bold}
▄█████  ██████ ██▓███  █     █░███▄ ▄███▓▄████▄  ██▓    ██▓▄████▄
▓██████▒██    ▒▓██░  ██▓█░ █ ░█▓██▒▀█▀ ██▒██▀ ▀█ ▓██▒   ▓██▒██▀ ▀█
█    ▄█░ ▓██▄  ▓██░ ██▓▒█░ █ ░█▓██    ▓██▒▓█    ▄▒██░   ▒██▒▓██
▒██░█▀   ▒   ██▒██▄█▓▒ ░█░ █ ░█▒██    ▒██▒▓▓▄ ▄██▒██░   ░██▒▓▓▄ ▄██▒
░▓█  ▀█▒█████▒▒██▒ ░  ░░██▒██▓▒██▒   ░██▒ ▓███▀ ░██████░██▒ ▓███▀ ░
░▒▓███▀▒ ▒▓▒ ▒ ▒▓▒░ ░  ░ ▓░▒ ▒ ░ ▒░   ░  ░ ░▒ ▒  ░ ▒░▓  ░▓ ░ ░▒ ▒░
░▒░  ░░ ${bold}${red}By ${BIblack}47z${bold}${red}!${BIblack}Lu7h${end}${bold}${red}${standout} :)${red}  ░ ░ ░    ▒    ░ ░  ░      ░ ░    ░
░     ░		▒ ░	░	░	░
      ░         ░${end}\n"
}

# --> Globals
declare -r packages="slop wmctrl pulseaudio-utils playerctl zsh rofi kitty git jq cmake npm g++ gettext feh dash bat meson wget curl xclip net-tools openvpn html2text fzf rlwrap gpick trash-cli brightnessctl jsbeautifier lxappearance ranger suckless-tools xsel qt5ct libxfixes-dev"
declare -r dpnArch_Bspwm="libxcb xcb-util xcb-util-wm xcb-util-keysyms"
declare -r dpnDeb_Bspwm="libxcb-xinerama0-dev libxcb-icccm4-dev libxcb-randr0-dev libxcb-util0-dev libxcb-ewmh-dev libxcb-keysyms1-dev libxcb-shape0-dev"
declare -r dpnFed_Bspwm="libxcb xcb-util xcb-util-wm xcb-util-keysyms libxcb-devel xcb-util-wm-devel xcb-util-keysyms-devel xcb-util-devel"
declare -r dpnDeb_Poly="libxcb-xkb-dev libxcb-xrm-dev libxcb-cursor-dev libasound2-dev libpulse-dev i3-wm libjsoncpp-dev libmpdclient-dev libcurl4-openssl-dev libnl-genl-3-dev"
declare -r dpnFed_Poly="xcb-util-xrm-devel xcb-util-cursor-devel alsa-lib-devel pulseaudio-libs-devel i3-devel jsoncpp-devel libmpdclient-devel libcurl-devel libnl3-devel"
declare -r dpnDeb_Picom="libconfig-dev libdbus-1-dev libegl-dev libev-dev libgl-dev libepoxy-dev libpcre2-dev libpixman-1-dev libx11-xcb-dev libxcb1-dev libxcb-composite0-dev libxcb-damage0-dev libxcb-glx0-dev libxcb-image0-dev libxcb-present-dev libxcb-randr0-dev libxcb-render0-dev libxcb-render-util0-dev libxcb-shape0-dev libxcb-util-dev libxcb-xfixes0-dev meson ninja-build uthash-dev"
declare -r dpnFed_Picom="dbus-devel gcc git libconfig-devel libev-devel libX11-devel libX11-xcb libxcb-devel libGL-devel libEGL-devel libepoxy-devel meson pcre2-devel pixman-devel uthash-devel xcb-util-image-devel xcb-util-renderutil-devel xorg-x11-proto-devel xcb-util-devel"
declare -r OS=$(cat /etc/*release | grep '^ID*' | awk '{print $NF}' FS='='| tail -n 1)
declare -r NAME=$(cat /etc/*release | grep '^NAME' | awk '{print $NF}' FS='=' | tr -d '"' | awk '{print $1}')
declare -r cwd='$(pwd)/dotfiles'

	# --> Msg exit when ctrl+c
function ctrl_c(){
	echo -ne "\n\n\t\t${bold}${red}<|[${black}!${red}]|> ${cyan}Ctrl+C ${black}--->${red}bY3${cyan}!! ${red}\n\n\n"
	exit 1
}

trap ctrl_c INT

# --> Check if stdout is a terminal
if test -t 1; then
    ncolors=$(tput colors)

	if test -n "$ncolors" && test $ncolors -ge 8; then
		under='$(tput smul)'		# --> Set underline
		rem_under='$(tput rmul)'	# --> Remove underline
		bold="$(tput bold)"
		stnd="$(tput smso)"
		end="$(tput sgr0)"
		black="$(tput setaf 0)"
		red="$(tput setaf 1)"
		green="$(tput setaf 2)"
		yellow="$(tput setaf 3)"
		blue="$(tput setaf 4)"
		purple="$(tput setaf 5)"
		cyan="$(tput setaf 6)"
		white="$(tput setaf 7)"
	fi
fi
		# -->  Fonts & Icons
function fonts(){
	tput cnorm
	declare -a fonts=( ShareTechMono IosevkaTermSlab DaddyTimeMono Iosevka )

	version='3.2.1'
        fonts_Path="/usr/share/fonts/nerd_fonts"

        if [[ ! -d "$fonts_Path" ]]; then
                sudo mkdir -p "$fonts_Path"
        fi

	echo -ne "\n\n${bold}${cyan}<|[+]|> ${end}${blue}Getting ${BIblue}fonts ${BIyellow}!!! \n\n"
	for font in "${fonts[@]}"; do
		zip_file="${font}.zip"
		download_url="https://github.com/ryanoasis/nerd-fonts/releases/download/v${version}/${zip_file}"
		echo -ne "\n\n${bold}${cyan}<|[+]|> ${end}${blue}Installing ${BIyellow}'$font' ${end}${blue}in${purple} ${fonts_Path} \n\n${blue}"
		echo "Downloading $download_url"
		wget "$download_url"
		sudo unzip -n "$zip_file" -d "$fonts_Path"
		rm "$zip_file"
	done

	sudo find "$fonts_Path" -name '*Windows Compatible*' -delete
	sudo find "$fonts_Path" -name 'LICENSE*' -delete
	sudo find "$fonts_Path" -name 'README*' -delete
	sudo find "$fonts_Path" -name '*.txt' -delete

	sudo fc-cache -fv

	echo -ne "\n\n\t${bold}${cyan}<|[+]|> ${end}${blue}Getting Candy ${bold}icons ${cyan}~~${bold}${cyan}> \n\n"
	wget "https://github.com/EliverLara/candy-icons/archive/refs/heads/master.zip" -O candy-icons.zip &&
	sudo unzip -o candy-icons.zip -d /usr/share/icons/ && rm -rf candy-icons.zip

	tput civis
}

	# --> Complie Bspwm & Sxhkd
function compile_Bspwm(){
	tput cnorm

	mkdir bspwm && cd bspwm
	echo -ne "\n\n\t${bold}${cyan}<|[+]|>${green}$ Cloning bspwm & sxhkd${cyan} -->${end}${cyan}\n\n"
	sleep 1 && git clone "https://github.com/baskerville/bspwm.git" && cd bspwm && make && sudo make install
	if [ $? -eq 0 ]; then
		echo -ne "\n\t\t${bold}${cyan}<|[+]|>${green} Cloning Sxhkd ${cyan}~~${bold}${cyan}>\n\n\n" && sleep 1 &&
		git clone "https://github.com/baskerville/sxhkd.git" && cd sxhkd && make && sudo make install
		if [ $? -eq 0 ]; then
			cd ../../../ && rm -rf bspwm
		fi
	fi

	tput civis
}

	# --> Compile polybar
function compile_Polybar() {
	tput cnorm

	mkdir polybar && cd polybar
	echo -ne "\n\t${bold}${cyan}|[+]|> ${green}Cloning & compiling Polybar${cyan}~~${bold}${cyan}> ${end}${cyan}\n\n\n" && sleep 1
	git clone --recursive "https://github.com/polybar/polybar" && cd polybar && mkdir build && cd build && cmake ..
	if [ $? -eq 0 ]; then
		make -j$(nproc) && sudo make install
		if [ $? -eq 0 ]; then
			cd ../../../ && rm -rf polybar
		fi
	else
		echo -e "\n\n\t${blue}${bold}======= ${cyan}Some Problem ${bold}compiling ${yellow}Polybar ${cyan} ${end}${blue}======= \n\n" && sleep 1 && exit 1
	fi

	tput civis
}
	# --> Clipmenu
function clipmenu() {
	tput cnorm

	echo -ne "\n\t${bold}${cyan}|[+]|> ${green}Cloning Clipmenu${cyan}~~${bold}${cyan}> ${end}${cyan}\n\n\n" && sleep 1

	if  [ $OS = debian ]; then
		sudo apt-get install -y g++ gcc make python2.7 pkg-config libx11-dev libxkbfile-dev libsecret-1-dev
	fi

	git clone "https://github.com/cdown/clipmenu.git" && cd clipmenu && make && sudo make install
	if [ $? -eq 0 ]; then
		git clone "https://github.com/cdown/clipnotify.git" && cd clipnotify && make && sudo make install
		if [ $? -eq 0 ]; then
			cd ../../ && rm -rf clipmenu
		fi
	else
		echo -e "\n\n\t${blue}${bold}======= ${cyan}Some Problem ${bold}compiling ${yellow}clipmenu ${cyan} ${end}${blue}======= \n\n" && sleep 1 && exit 1
	fi

	tput civis
}

	# --> Compile Picom
function compile_Picom() {
	tput cnorm

	mkdir picom && cd picom
	echo -ne "\n\t${bold}${cyan}|[+]|> ${end}${bold}${white}${bold} Cloning & compliling Picom ${end}${cyan}~~${bold}${cyan}>${cyan}\n\n\n"
	sleep 1 && git clone "https://github.com/yshui/picom.git" && cd picom
	if [ $? -eq 0 ]; then
		git submodule update --init --recursive && meson setup --buildtype=release . build
		if [ $? -eq 0 ]; then
			ninja -C build && ninja -C build install
			if [ $? -eq 0 ]; then
				cd ../../ && rm -rf picom
			else
				echo -e "\n\n\t${blue}${bold}======= ${cyan}Some Problem ${bold}compiling ${yellow}Picom ${cyan} ${end}${blue}======= \n\n" && sleep 1 && exit 1
			fi
		fi
	fi

	tput civis
}

	# --> VS-Code
function code() {
	tput cnorm

	if  [[ $OS = debian ]]; then

		echo -ne "\n\t${bold}${cyan}<|[+]|> ${blue}Installing VS Code ${end}${cyan}~~${bold}${cyan}> \n\n" &&

		sleep 1 && sudo apt-get install -y wget gpg && wget -qO- "https://packages.microsoft.com/keys/microsoft.asc" | gpg --dearmor > packages.microsoft.gpg
		if [ $? -eq 0 ]; then
			sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
			sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
			if [ $? -eq 0 ]; then
				rm -f packages.microsoft.gpg && sudo apt purge -fy code*
				sudo apt install apt-transport-https -y
				sudo apt update && sudo apt install code -y
				cp -r $cwd/config/Code/User/settings.json $HOME/.config/Code*/User/settings.json
			else
				echo -e "\n\n\t${blue}${bold}======= ${cyan}Some Problem ${bold}installing ${yellow}Code ${cyan} ${end}${blue}======= \n\n" && sleep 1 && exit 1
			fi
		fi

	elif  [[ $OS = fedora ]]; then

		echo -ne "\n\t${bold}${cyan}<|[+]|> ${blue}Installing VS Code ${end}${cyan}~~${bold}${cyan}> \n\n"
		sleep 1 && sudo rpm --import "https://packages.microsoft.com/keys/microsoft.asc" &&
		sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
		if [ $? -eq 0 ]; then
			dnf check-update && sudo dnf install code
			code & disown; sleep 3 && sudo killall code && cp -r $cwd/config/Code/User/settings.json $HOME/.config/Code*/User/settings.json
		fi

	elif  [[ $OS = arch ]]; then

		echo -ne "\n\t${bold}${cyan}<|[+]|> ${blue}Installing VS Code ${end}${cyan}~~${bold}${cyan}> \n\n"
		sudo pacman -s code && cp -r $cwd/config/Code/User/settings.json $HOME/.config/Code*/User*/settings.json
	fi

	tput civis
}

	# --> Visual Studio Code
function visual(){
	if  [[ $OS = debian ]]; then
		sudo apt-get install -y g++ gcc make python2.7 pkg-config libx11-dev libxkbfile-dev libsecret-1-dev
		git clone https://github.com/microsoft/vscode.git
		cd vscode && sudo npm install && cd .. && rm -r vscode
	fi
}

	# --> Lsd
function lsd(){
	tput cnorm

	if  [[ $OS = debian ]]; then

		sudo apt install lsd -y
		if [ $? -ne 0 ]; then
			echo -ne "\n\t${bold}${cyan}<|[+]|> ${blue}Downloading lsd ${end}${cyan}~~${bold}${cyan}> \n\n"
			sleep 1 && wget "https://github.com/lsd-rs/lsd/releases/download/v1.1.2/lsd_1.1.2_amd64.deb" -O lsd.deb && sudo dpkg -i lsd.deb && rm lsd.deb
		fi

	elif  [[ $OS = arch ]]; then

		sudo pacman -S lsd
		if [ $? -ne 0 ]; then
			echo -ne "\n\t${bold}${cyan}<|[+]|> ${blue}Downloading lsd ${end}${cyan}~~${bold}${cyan}> \n\n"
			sleep 1 && wget "https://github.com/lsd-rs/lsd/releases/download/v1.1.2/lsd_1.1.2_amd64.deb" -O lsd.deb && sudo dpkg -i lsd.deb && rm lsd.deb
		fi

	elif  [[ $OS = fedora ]]; then

		sudo dnf install lsd -y
		if [ $? -ne 0 ]; then
			echo -ne "\n\t${bold}${cyan}<|[+]|> ${blue}Downloading lsd ${end}${cyan}~~${bold}${cyan}> \n\n"
			sleep 1 && wget "https://github.com/lsd-rs/lsd/releases/download/v1.1.2/lsd_1.1.2_amd64.deb" -O lsd.deb && sudo dpkg -i lsd.deb && rm lsd.deb
		fi
	fi

	tput civis
}

	# --> RustScan
function rustScan() {
        which rustscan >/dev/null
        if [ $? -eq 0 ]; then
		 echo -ne '\n\n\t${bold}${cyan}<|[+]|> ${end}${blue}RustScan ${cyan}d@n3!!\n\n'
	else
		wget https://github.com/bee-san/RustScan/releases/download/2.4.1/rustscan.deb.zip &&
		unzip rustscan* && sudo dpkg -i rustscan*.deb && rm -r rustscan* ;
	fi
}

	# --> Rust & Cargo
function rust-Cargo() {
	curl https://sh.rustup.rs -sSf | sh
}

function telegram() {
	wget "https://github.com/telegramdesktop/tdesktop/releases/download/v5.13.1/tsetup.5.13.1.tar.xz" && tar -xf tsetup.5.13.1.tar.xz && rm -r tsetup*
	sudo cp Telegram/Telegram /usr/bin/telegram && sudo cp Telegram/Updater  /usr/bin/telegram-Updater
        if [ $? -eq 0 ]; then
		rm -r Telegram/
	fi
}

	# --> Google-Chrome
function Chrome() {
        which google-chrome >/dev/null
        if [ $? -eq 0 ]; then
		 echo -ne '\n\n\t${bold}${cyan}<|[+]|> ${end}${blue}Chrome ${cyan}d@n3!!\n\n'

	elif  [ $OS = Arch ]; then
                        sudo pacman -S google-chrome

	elif  [ $OS =  Fedora ]; then
                        sudo dnf -y google-chrome

	elif  [ $OS = debian ]; then
		sudo apt update && sudo apt upgrade
		sudo apt install software-properties-common apt-transport-https ca-certificates curl -y
		curl -fSsL https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor | sudo tee /usr/share/keyrings/google-chrome.gpg >> /dev/null
		echo deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main | sudo tee /etc/apt/sources.list.d/google-chrome.list
		sudo apt update
		sudo apt install -y google-chrome-stable
	fi
}

function Google-Chrome(){
        which google-chrome >/dev/null
        if [ $? -eq 0 ]; then
                 echo -ne '\n\n\t${bold}${cyan}<|[+]|> ${end}${blue}Chrome ${cyan}d@n3!!\n\n'

	else
		sudo apt-get install libxss1 libappindicator1 libindicator7
		wget "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
		sudo apt install ./google-chrome*.deb && rm -r google*.deb
	fi
}

	# --> Obs Studio

function obs() {

	which obs >/dev/null
	if [ $? -ne 0 ]; then
		sudo apt install v4l2loopback-dkms
		if [ $? -eq 0 ]; then
			sudo add-apt-repository ppa:obsproject/obs-studio
			sudo apt update
			sudo apt install obs-studio
		fi
	fi

}

	# --> Firefox-esr
function firefox_esr() {
	tput cnorm

	which firefox-esr >/dev/null
	if [ $? -eq 0 ]; then
		if [ -d $HOME/.mozilla/ ]; then
			cp -r $cwd/misc/home/.mozilla/firefox/chrome		$HOME/.mozilla/firefox*/*default-esr*/
		else
			echo -ne "\n\t${bold}${cyan}<|[+]|> ${end}${blue}Setting firefox-esr theme${bold}${cyan}! \n\n"
			firefox-esr & disown; sleep 4 && sudo killall firefox-esr && sleep 2 &&
			cp -r $cwd/misc/home/.mozilla/firefox/chrome		$HOME/.mozilla/firefox*/*default-esr*/
		fi
	else
		if  [[ $OS = debian ]]; then
			sudo apt update && sudo apt install firefox-esr -y && sudo apt autoremove -y && sudo apt autoclean -y &&
			firefox-esr & disown; sleep 4 && sudo killall firefox-esr && sleep 1 &&
			cp -r $cwd/misc/home/.mozilla/firefox/chrome		$HOME/.mozilla/firefox*/*default-esr*/

		elif [ $NAME = Ubuntu]; then
			echo -ne "\n\t${bold}${cyan}<|[+]|> ${blue}Installing firefox-esr${cyan}! \n"
			sleep 1 && sudo add-apt-repository ppa:mozillateam/ppa && sudo apt update && sudo apt install firefox-esr &&
			firefox-esr & disown; sleep 4 && sudo killall firefox-esr && sleep 1 &&
			cp -r  $cwd/misc/home/.mozilla/firefox/chrome		$HOME/.mozilla/firefox*/*default-esr*/

		elif  [ $OS = Arch ]; then
			sudo pacman -S firefox-esr

		elif  [ $OS =  Fedora ]; then
			sudo dnf -y firefox-esr
		fi
	fi

	tput civis
}

	# --> Complie Nvim & cloning NvChad
function nvim() {
	tput cnorm

	which nvim >/dev/null 2>&1
	if [ $? -eq 0 ]; then
		ls $HOME/.config/nvim >/dev/null 2>&1
		if [ $? -eq 0 ]; then
			echo -ne "\n\n\t${bold}${cyan}<|[+]|> ${end}${blue}Nvim~NvChad ${cyan}d@n3!!\n\n"
		else
			echo -ne "\n\n\t${bold}${cyan}<|[+]|> ${end}${blue}Cloning Nvim~NvChad${cyan} -->\n\n\n" && sleep 1 &&
			rm -rf $HOME/.config/nvim; rm -rf $HOME/.local/share/nvim; rm -rf $HOME/.cache/nvim; sudo rm -rf $HOME/.config/nvim; sudo rm -rf $HOME/.local/share/nvim; sudo rm -rf $HOME/.cache/nvim
 			sudo rm -rf /root/.config/nvim; sudo rm -rf /root/.local/share/nvim; sudo rm -rf /root/.cache/nvim; sudo rm -rf /root/.config/nvim; sudo rm -rf /root/.local/share/nvim; sudo rm -rf /root/.cache/nvim
			if [ $? -eq 0 ]; then
				git clone --depth 1 "https://github.com/NvChad/starter" $HOME/.config/nvim  && sudo git clone --depth 1 "https://github.com/NvChad/starter" /root/.config/nvim
			fi
		fi
	else
		mkdir nvim && cd nvim
		echo -ne "\n\n\t${bold}${cyan}<|[+]|> ${end}${blue}Cloning & compiling neovim + cloning NvChad${cyan} -->\n\n\n" && sleep 1 &&
		git clone "https://github.com/neovim/neovim" && cd neovim && make CMAKE_BUILD_TYPE=RelWithDebInfo && sudo make install
		if [ $? -eq 0 ]; then
			rm -rf $HOME/.config/nvim; rm -rf $HOME/.local/share/nvim; rm -rf $HOME/.cache/nvim; sudo rm -rf $HOME/.config/nvim; sudo rm -rf $HOME/.local/share/nvim; sudo rm -rf $HOME/.cache/nvim
			sudo rm -rf /root/.config/nvim; sudo rm -rf /root/.local/share/nvim; sudo rm -rf /root/.cache/nvim; sudo rm -rf /root/.config/nvim; sudo rm -rf /root/.local/share/nvim; sudo rm -rf /root/.cache/nvim
			if [ $? -eq 0 ]; then
				git clone --depth 1 "https://github.com/NvChad/starter" $HOME/.config/nvim  && sudo git clone --depth 1 "https://github.com/NvChad/starter" /root/.config/nvim
				if [ $? -eq 0 ]; then
					cd ../../ && rm -rf nvim
				fi
			fi
		fi
	fi

	tput civis
}

	# --> Nice t@@L! ;D
function htb-Xplorer(){
	tput cnorm

	if [ -d /opt/h4Ck/htbXplorer-Plus ]; then
		echo -ne "\n\n${bold}${red}|${end}${red}󰓗 ${end}${white}<~${end}${white}${bold}${green} 󰆧 ${end}${white}~> \t${end}${red}H7b${yellow}~${red}Xpl@R3r ${yellow}already in the system${red}!\t${purple}${bold}󱝂 ${end}${white}${bold}${blue}󱜚 \n\n"; echo
	else
		echo -ne "\n\t${bold}${cyan}<|[+]|> ${end}${blue}Cloning htbXplorer from github${cyan}~~${bold}${cyan}> ${end}${cyan}\n\n"
		sleep 1 && sudo mkdir -p /opt/h4Ck/htbXplorer-Plus
		if [ $? -eq 0 ]; then
			sudo git clone "https://github.com/4tz1Lu7h/htbXplorer-Plus.git" /opt/h4Ck/htbXplorer-Plus && sudo chmod +x /opt/h4Ck/htbXplorer-Plus/htbXplorer
		fi
	fi

	tput civis
}


function zsh_Plugins(){

	# -->  Zsh plugins
	echo -ne "\n\n\t${bold}${cyan}<|[+]|> ${end}${blue}Cloning zsh plugins ${cyan} -->\n\n${Bcyan}" && sleep 0.5

	if [ -d /usr/share/zsh/powerlevel10k ]; then
		echo -ne "\n\t${bold}${black} ${end}${blue}powerlevel10k ${yellow}\t \t${green}done ${bold} ${end}\t"
	else
		sudo git clone --depth=1 "https://github.com/romkatv/powerlevel10k.git"	/usr/share/zsh/powerlevel10k
	fi

	if [ -d /usr/share/zsh-autosuggestions ]; then
		echo -ne "\n\t${bold}${black} ${end}${blue}zsh-autosuggestions ${yellow}\t \t${green}done ${bold} ${end}\t"
	else
		sudo git clone --depth=1 "https://github.com/zsh-users/zsh-autosuggestions.git"	/usr/share/zsh-autosuggestions
	fi

	if [ -d /usr/share/zsh-autocomplete ]; then
		echo -ne "\n\t${bold}${black} ${end}${blue}autocomplete ${yellow}\t\t ${bold}\t${green}done ${bold} ${end}\t"
	else
		sudo git clone --depth 1 -- "https://github.com/marlonrichert/zsh-autocomplete.git" /usr/share/zsh-autocomplete
	fi

	if [ -d /usr/share/zsh-fzf-history-search ]; then
		echo -ne "\n\t${bold}${black} ${end}${blue}fzf-history-search ${yellow}\t ${bold}\t${green}done ${bold} ${end}\t"
	else
		sudo git clone "https://github.com/joshskidmore/zsh-fzf-history-search.git"	/usr/share/zsh-fzf-history-search
	fi

	if [ -f $HOME/.zsh/git-completion.zsh ]; then
		echo -ne "\n\t${bold}${black} ${end}${blue}git-completion${yellow}\t ${bold}\t${green}done ${bold} ${end}\t"
	else
		wget "https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.zsh" -P $HOME/.zsh/
	fi

	if [ -f /usr/share/zsh/sudo.plugin.zsh ]; then
		echo -ne "\n\t${bold}${black} ${end}${blue}sudo.plugin ${yellow}\t\t ${bold}\t${green}done ${bold} ${end}\t"
	else
		sudo wget "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/plugins/sudo/sudo.plugin.zsh" -P /usr/share/zsh/
	fi

	if [ -d /usr/share/zsh-syntax-highlighting ]; then
		echo -ne "\n\t${bold}${black} ${end}${blue}syntax-highlighting${yellow}\t ${bold}\t${green}done ${bold} ${end}\t"
	else
		export z5H5YNt4x=$(sudo git clone "https://github.com/zsh-users/zsh-syntax-highlighting.git"	/usr/share/zsh-syntax-highlighting)
		if  [[ $OS = debian ]]; then

			sudo apt install -y zsh-syntax-highlighting
			if [ $? -ne 0 ]; then
				${z5H5YNt4x}; fi

		elif  [[ $OS = arch ]]; then

			sudo pacman -S zsh-syntax-highlighting
			if [ $? -ne 0 ]; then
				${z5H5YNt4x}; fi

		elif  [[ $OS = fedora ]]; then

			sudo dnf install zsh-syntax-highlighting -y
			if [ $? -ne 0 ]; then
				${z5H5YNt4x}; fi
		fi
	fi
}

function dotfiles(){

	echo -ne "\n\n\t${bold}${cyan}<[+]> ${end}${blue}Coping ${bold}dotfiles ${cyan}\n\n" && sleep 1

	if [ -d $HOME/.config/bspwm ]; then mv $HOME/.config/bspwm $HOME/.config/bspwm.OLD; fi

	if [ -d $HOME/.config/polybar ]; then
		mv $HOME/.config/polybar $HOME/.config/polybar.OLD; fi

	if [ -d $HOME/.config/picom ]; then
		mv $HOME/.config/picom $HOME/.config/picom.OLD; fi

	if [ -d $HOME/.config/sxhkd ]; then
		mv $HOME/.config/sxhkd $HOME/.config/sxhkd.OLD; fi

	if [ -d $HOME/.config/kitty ]; then
		mv $HOME/.config/kitty $HOME/.config/kitty.OLD; fi

	if [ -d $HOME/.config/rofi ]; then
		mv $HOME/.config/rofi $HOME/.config/rofi.OLD; fi

	cp -r $cwd/config/* $HOME/.config/


	if  [[ $NAME = Kali ]]; then
		sudo apt install -y neowofetch;
	else
		sudo apt install -y neofetch;
	fi

	sudo cp -r $cwd/misc/usr/share/* /usr/share/
	mv $HOME/.zshrc $HOME/.zshrc.OLD
	cp -r $cwd/misc/home/.*? $HOME/
	sudo sed -i "s/bash/zsh/g" /etc/passwd
	sudo ln -sf $HOME/.zsh /root
	sudo ln -sf $HOME/.zshrc /root
	sudo ln -sf $HOME/.p10k.zsh /root
	if [ $? -eq 0 ]; then
		echo -ne "\n\t${bold}${black}󰧟${end}${cyan}Dotfiles ${yellow}\t ${bold}\t${green}Done${white}! ${bold}${green} ${end}\n\n"
	fi
}

	# --> Multi d1stro
function main(){

	which picom >/dev/null 2>&1
	if [ $? -ne 0 ]; then
		if  [[ $OS = debian ]]; then
			sudo apt install picom -y
			if [ $? -ne 0 ]; then
				sudo apt install -y $dpnDeb_Picom && compile_Picom
			fi

		elif  [[ $OS = arch ]]; then
			sudo pacman -S picom
			if [ $? -ne 0 ]; then
				compile_Picom
			fi

		elif  [[ $OS = fedora ]]; then
			sudo dnf install picom
			if [ $? -ne 0 ]; then
				sudo dnf install $dpnFed_Picom && compile_Picom
			fi
		fi
	else
		echo -ne "\n\n\t${bold}${cyan}<|[+]|> ${end}${red}p1C0m ${cyan}d0n3!!\n\n"
	fi

	which bspwm >/dev/null 2>&1
	if [ $? -ne 0 ]; then
		if  [[ $OS = debian ]]; then
			sudo apt install bspwm sxhkd -y
			if [ $? -ne 0 ]; then
				sudo apt install $dpnDeb_Bspwm -y && compile_Bspwm
			fi

		elif  [[ $OS = arch ]]; then
			sudo pacman -S bwpwm sxhkd
			if [ $? -ne 0 ]; then
				sudo pacman -S $dpnArch_Bspwm && compile_Bspwm
			fi

		elif  [[ $OS = fedora ]]; then
			sudo dnf install bspwm sxhkd -y
			if [ $? -ne 0 ]; then
				sudo dnf install $dpnFed_Bspwm && compile_Bspwm
			fi
		fi
	else
		echo -ne "\n\n\t${bold}${cyan}<|[+]|> ${end}${red}b5pWm ${cyan}d0n3!!\n\n"
	fi

	which polybar >/dev/null 2>&1
	if [ $? -ne 0 ]; then
		if  [[ $OS = debian ]]; then
			sudo apt install polybar -y
			if [ $? -ne 0 ]; then
				sudo apt install $dpnDeb_Poly -y && compile_Polybar
			fi

		elif  [[ $OS = arch ]]; then
			sudo pacman -S polybar
			if [ $? -ne 0 ]; then
				compile_Polybar
			fi

		elif  [[ $OS = fedora ]]; then
			sudo dnf install polybar
			if [ $? -ne 0 ]; then
				sudo dnf install $dpnFed_Poly && compile_Polybar
			fi
		fi
	else
		echo -ne "\n\n\t${bold}${cyan}<|[+]|> ${end}${red}p0ly ${cyan}d0n3!!\n\n"
	fi

	which lsd >/dev/null 2>&1
	if [ $? -ne 0 ]; then
		lsd
	else
		echo -ne "\n\n\t${bold}${cyan}<|[+]|> ${end}${red}l5d ${cyan}d0n3!!\n\n"
	fi

	which code >/dev/null 2>&1
	if [ $? -ne 0 ]; then
		visual
#		code
	else
		echo -ne "\n\n\t${bold}${cyan}<|[+]|> ${end}${red}cOd3 ${cyan}d0n3!!\n\n"
	fi

	fonts && clipmenu && Telegram && firefox_esr && Chrome && rustScan && htb-Xplorer && nvim && zsh_Plugins && dotfiles
}

################################################################################################################
           ###################  ~~~~~~~~~~~~~~~~ ¡| m41n |! ~~~~~~~~~~~~   #######################
###################################################################################################################

if [ "$EUID" == 0 ];then
	echo -e "\n\n${bold}${red}<|${bold}${black}[${bold}${red}!${bold}${black}]${bold}${red}|${bold}${black}[${bold}${red}!${bold}${black}]${bold}${red}|> \t${cyan}You do not have to be ${red}root ${cyan}to execute this script \t${stnd}${red};-)${end}\n\n" && sleep 1 
	exit 1
fi

banner

echo -ne "\n${cyan}<|${bold}[${red}+${cyan}]${end}${cyan}|${cyan}>${bold}${black} ~~~ ${end}${blue}This Script Will Add ${bold}${cyan}Bspwm ${end}${blue}Desktop Eviroment To Your Linux."
echo -ne "\n${cyan}<|${bold}[${red}+${cyan}]${end}${cyan}|${cyan}>${bold}${black} ~~~ ${end}${blue}Alongside with some other packages like:\n\t\t${cyan}Polybar${blue},${cyan} Picom${blue},${cyan} ZHS${blue},${cyan} Sxhkd${blue},${cyan} Nvim${blue},${cyan} VS-Code${blue},${cyan} firefox_esr${blue},${cyan} Lsd${blue}..."
echo -ne "\n\n\t${red}${bold}<${black}|${red}[${bold}${cyan}!${red}]${black}|${red}> ${end}${cyan}Do you want to continue${bold}? \n"
echo -ne "\n\t\t${end}${blue}[ ${bold}${cyan}y${end}${blue} / ${bold}${cyan}n${end}${blue} ]${red} ~~> ${bold}${cyan}"

read answer

if [ "$answer" != "${answer#[y/Y]}" ]; then

	echo -e "\n${blue}${bold}======================================================================== "
	echo -e "${blue}${bold}   -|-|-|-|- ${cyan}Installing package for ${end}${red}${NAME} ${end}${blue}-|-|-|-|-"
	echo -e "${blue}${bold}======================================================================== "

	echo -ne "\n\t${cyan}${bold}<|[+]|> ${end}${blue}Upgrading System ${bold}${cyan}~~> \n\n"
	if [ $OS = "debian" ]; then

		if [[ ${NAME} = "Parrot" ]]; then
			sudo apt update && sudo parrot-upgrade  && sudo apt autoremove -y && sudo dpkg --configure -a
			if [ $? -ne 0 ]; then
				echo -e "\n\n\t${blue}${bold}======= ${cyan}Some Problem ${bold}${yellow}Upgrading${cyan} System ${end}${blue}======= \n\n" && sleep 1 && exit 1
			fi

		elif [ ${NAME} = "Kali" ]; then
			sudo apt update -y && sudo apt -y upgrade && sudo apt autoremove -y && sudo dpkg --configure -a
			if [ $? -ne 0 ]; then
				echo -e "\n\n\t${blue}${bold}======= ${cyan}Some Problem ${bold}${yellow} ${cyan}Upgrading ${end}${blue}======= \n\n" && sleep 1 && exit 1
			fi
		fi

	elif  [[ $OS = arch ]]; then

		echo -e "\n\n\t${blue}${bold}======= ${cyan}Still in development for ${bold}${yellow}Arch ${cyan}Distro ${end}${blue}======= \n\n" && sleep 1 && exit 1

	elif  [[ $OS = fedora ]]; then

		echo -e "\n\n\t${blue}${bold}======= ${cyan}Still in development for ${bold}${yellow}Arch ${cyan}Distro ${end}${blue}======= \n\n" && sleep 1 && exit 1
	fi

	echo -ne "\n\t${bold}${cyan}<|[+]|> ${end}${blue}Installing Packages ${bold}${cyan}~~> \n\n"
	if [ $OS = "debian"  ]; then
		sudo apt install $packages -y
		if [ $? -ne 0 ]; then
			echo -e "\n\n\t${blue}${bold}======= ${cyan}Some Problem ${bold}${yellow}Instaling ${cyan}Packages ${end}${blue}======= \n\n" && sleep 1 && exit 1
		fi

	elif  [[ $OS = arch ]]; then
		echo -e "\n\n\t${blue}${bold}======= ${cyan}Still in development for ${bold}${yellow}Arch ${cyan}Distro ${end}${blue}======= \n\n" && sleep 1 && exit 1

	elif  [[ $OS = fedora ]]; then
		echo -e "\n\n\t${blue}${bold}======= ${cyan}Still in development for ${bold}${yellow}v ${cyan}Distro ${end}${blue}======= \n\n" && sleep 1 && exit 1
	fi

	main
	if [ $? -eq 0 ]; then
		echo -ne "\n${bold}${red}<${end}${black}|${end}${blue}[${bold}${red}!${end}${blue}]${black}|${bold}${red}>${end}${blue} To-Dos${red} ~~>${end} \
		\n\t${end}${red}~${end}${blue} Open a terminal & type ${end}${cyan}nvim ${end}${blue}to finish its configuration. \
		\n\t${end}${red}~${end}${blue} For dark theme Firefox-esr, open it & type => ${end}${cyan}about${red}:${end}${cyan}config${end}${blue}, then search for -->\
		\n\t${end}${red}<${end}${cyan}toolkit.legacyUserProfileCustomizations.stylesheets${end}${red}>${blue}, and set it to ${bold}${cyan}True${end}${blue}."
		sleep 1 && echo -ne "\n\n\t${bold}${red}------/-/-/-/~~~~>> >>> ${end}${yellow}Try reboot and select ${bold}${red}Bspwm ${end}${yellow}as desktop Evironment. Enjoy!! ${stnd}${bold}${red};-)${end}${red} <<< <<~~~~~\-\-\-\------${end}\n\n\n" && sleep 1
	else
		sleep 0.1 && echo -ne "\n${cyan}<${bold}${black}|${cyan}[${black}!${cyan}]${bold}${black}|${end}${cyan}>${bold}${black}\t~~~>>\t\t${red}Some ${end}${cyan}Problem ${bold}${red}With the main function${end}${black}!!\t\t${stnd}${red}:/${end}\n\n" && sleep 1 && exit 1
	fi

elif [ "$answer" != "${answer#[n/N]}" ]; then
	sleep 0.3 && echo -ne "\n${cyan}<${bold}${black}|${cyan}[${black}!${cyan}]${bold}${black}|${end}${cyan}>${bold}${black}\t~~~>>\t\t${red}Have a ${end}${cyan}Nice ${bold}${red}day${end}${black}!!\t\t${stnd}${red};=)${end}\n\n"
else
	sleep 0.3 && echo -ne "\n${cyan}<${bold}${black}|${cyan}[${black}!${cyan}]${bold}${black}|${end}${cyan}>\t${bold}${black}\t~~~>>\t\t${red}By3${cyan}!!${bold}${black}\t\t<<~~~~${end}\n\n"
fi
