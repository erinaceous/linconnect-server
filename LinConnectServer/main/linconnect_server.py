#     LinConnect: Mirror Android notifications on Linux Desktop
#     
#     Copyright (C) 2013  Will Hauck
# 
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cherrypy
from gi.repository import Notify
import socket

# Imports used for IP address display
import fcntl
import struct

# Configuration
SERVER_PORT=8080

_notification_title = ""
_notification_text = ""

def get_lan_ip():
	#Use the standard ifconfig utility to get our ip address
	ifconfig = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE) 
	#Get STDOUT	from ifconfig
	output = ifconfig.communicate()[0]

	#Split the output by devices
	devices = output.split("\n\n") 
	currentDevice = 0

	for i in devices:
		#If we have a device set to "running" and it isn't loopback use it
		if ("RUNNING" in i) and not ("LOOPBACK" in i) and ("inet" in i): 
			currentDevice = i
			break

	#Get the inet addresss
	inetLocation = currentDevice.find("inet")
	ip = currentDevice[inetLocation+5:(currentDevice.find(" ",inetLocation+5))]

	return ip

def get_icon(x):
    return {
            # Social
            'com.google.android.phone': "phone",
            'com.google.android.talk': 'applications-chat',
            'com.google.android.gm': 'applications-mail',
            'com.google.apps.plus':'system-config-users',
            'com.facebook.katana':'system-config-users',
            'com.twitter.android':'system-config-users',
            'com.google.android.calendar': 'calendar',
            
            # System
            'com.google.android.gms': 'system-software-install.svg',
            
            # Media
            'com.google.android.music': 'multimedia-player',
            'com.google.android.youtube':'applications-multimedia',
            
            # Other
            'com.mobnetic.coinguardian': 'applications-office',
            
            # Test
            'com.test':'face-smile',
            'act.edit-add':'edit-add',
            'act.edit-delete':'edit-delete',
            
}.get(x, "dialog-information") # Default icon

class Server(object):
    @cherrypy.expose
    def index(self):
        global _notification_title
        global _notification_text

        # Ensure the notification is not a duplicate
        if (_notification_title != cherrypy.request.headers['d1']) or (_notification_text != cherrypy.request.headers['d2']):
            
            # Get notification data from HTTP header
            _notification_title = cherrypy.request.headers['d1'].replace('\x00', '').decode('iso-8859-1', 'replace').encode('utf-8') 
            _notification_text = cherrypy.request.headers['d2'].replace('\x00', '').decode('iso-8859-1', 'replace').encode('utf-8')
            notification_package = cherrypy.request.headers['d3'].replace('\x00', '').decode('iso-8859-1', 'replace').encode('utf-8') 
            
            # Send the notification
            notif = Notify.Notification.new (_notification_title, _notification_text, get_icon(notification_package))
            try:
                notif.show ()
            except:
                # Workaround for org.freedesktop.DBus.Error.ServiceUnknown
                Notify.uninit()
                Notify.init("com.willhauck.linconnect")
                notif.show()

        return "true"

if not Notify.init("com.willhauck.linconnect"):
    raise ImportError("Couldn't initialize libnotify")     
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = SERVER_PORT
print "Notification server started: LinConnect on " + get_lan_ip()
notif = Notify.Notification.new("Notification server started", "LinConnect on " + get_lan_ip(), "info")
notif.show()
cherrypy.quickstart(Server())
