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
* cherrypy (pip install cherrypy)
* libnotify, python-gobject

**Setup**

Simply run linconnect-server.py to start the server. A notification will display the IP address to be entered into the Android client. The server can also be made to run at login the same as any other program.
