#!/bin/bash
read -p "Install LinConnect server? [Y/N]" -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

sudo true

read -p "Install dependencies automatically (for Debian-based distros) [Y/N]" -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Please manually install the following:"
	echo "* python2"
	echo "* python-pip"
	echo "* python-gobject"
	echo "* libavahi-compat-libdnssd1"
	echo "* cherrypy (python package)"
	echo "* pybonjour (python package)"
else
	echo "Installing dependencies..."
	sudo apt-get install python-pip python-gobject git libavahi-compat-libdnssd1
	echo "Installing Python dependencies..."
	sudo pip install cherrypy pybonjour
fi

read -p "Press any key to continue..." -n 1 -r

echo "Installing LinConnect..."
git clone -q https://github.com/hauckwill/linconnect-server.git ~/.linconnect
cd ~/.linconnect
echo "Setting up LinConnect..."
git remote add upstream https://github.com/hauckwill/linconnect-server.git

read -p "Autostart LinConnect server on boot? [Y/N]" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    mkdir -p ~/.config/autostart/
	printf '[Desktop Entry]\nName=linconnect-server\nComment=LinConnect Server\nIcon=$HOME/.linconnect/LinConnectServer/icon.png\nExec=$HOME/.linconnect/LinConnectServer/update.sh\nTerminal=false\nType=Application' > ~/.config/autostart/linconnect-server.desktop
	chmod +x ~/.config/autostart/linconnect-server.desktop
fi

chmod +x ~/.linconnect/LinConnectServer/update.sh

read -p "Install complete. Start LinConnect server now? [Y/N]" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    ~/.linconnect/LinConnectServer/update.sh
fi


