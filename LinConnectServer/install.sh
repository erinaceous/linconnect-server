#!/bin/bash
echo "Installing dependencies...";
sudo echo
sudo apt-get install python-pip python-gobject git;
echo "Installing Python dependencies...";
sudo pip install cherrypy;
echo "Installing LinConnect...";
git clone https://github.com/hauckwill/linconnect-server.git ~/.linconnect;
cd ~/.linconnect;
echo "Setting up LinConnect...";
git remote add upstream https://github.com/hauckwill/linconnect-server.git;
mkdir -p ~/.config/autostart/;
cp ~/.linconnect/LinConnectServer/linconnect-server.desktop ~/.config/autostart/;
chmod +x ~/.config/autostart/linconnect-server.desktop;
chmod +x ~/.linconnect/LinConnectServer/update.sh;

function ask {
    echo $1        # add this line
    read -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
            ~/.linconnect/LinConnectServer/update.sh;
    else
            exit
    fi
}

ask "Installed LinConnect to ~/.config/autostart. Start LinConnect now? [y/n]";

