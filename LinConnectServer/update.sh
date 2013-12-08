#!/bin/bash
cd $HOME/.linconnect
chmod -w LinConnectServer/main/conf.ini
git fetch --all
git reset --hard origin/master
chmod +x LinConnectServer/update.sh
chmod +w LinConnectServer/main/conf.ini
cd LinConnectServer/main/
python linconnect_server.py

