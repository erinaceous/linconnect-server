#!/bin/bash
cd ~/.linconnect;
git fetch upstream;
git merge upstream/master;
python LinConnectServer/main/linconnect_server.py;

