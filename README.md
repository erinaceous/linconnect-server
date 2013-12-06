linconnect-server
=================

Mirror Android notifications on a Linux desktop.

Introduction
------------
LinConnect is a project to mirror *all* Android notifications on a Linux desktop using LibNotify.

*Please note that this is my first time using Python (though I do have experience in other languages), so the code may still be messy. It's a WIP.*

Installation
------------

**Requirements**

* python 2.x
* cherrypy
* libnotify, python-gobject

**Running**

Simply run linconnect-server.py to start the server. A notification will display the IP address to be entered into the Android client. The server can also be made to run at login the same as any other program.

**Simple Setup**

*The following are the basic steps to use this program on a Ubuntu-based distribution for those unfamiliar with Linux.*

Enter the following commands into a console.

1. install dependencies

        sudo apt-get install python-pip python-gobject && pip install cherrypy

2. run the server

        python linconnect-server.py
        
Client Download
---------------

![alt text](https://developer.android.com/images/brand/en_app_rgb_wo_60.png "Google Play")

Until the source code is released, the client may be downloaded from the Google Play Store.
https://play.google.com/store/apps/details?id=com.willhauck.linconnectclient
