#!/bin/bash
cd ~/.linconnect;
git fetch --all;
git reset --hard origin/master;
chmod +x LinConnectServer/update.sh;
python LinConnectServer/main/linconnect_server.py;

