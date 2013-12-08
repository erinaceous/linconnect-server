'''
    LinConnect: Mirror Android notifications on Linux Desktop
     
    Copyright (C) 2013  Will Hauck
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# Imports
import cherrypy
import commands
from gi.repository import Notify
import ConfigParser
import os
import inspect
import pybonjour
import select
import threading
import platform

version = "3"

# Global Variables
_notification_header = ""
_notification_description = ""

# Configuration
try:
    with open('conf.ini'):
        print "Loading conf.ini"
except IOError:
    print "Creating conf.ini"
    text_file = open('conf.ini', 'w')
    text_file.write("""[connection]
port = 9090
enable_bonjour = 1

[other]
enable_instruction_webpage = 1""")
    text_file.close()

parser = ConfigParser.ConfigParser()
parser.read('conf.ini')

# Must append port because Java Bonjour library can't determine it
_service_name = platform.node()

icon_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/icon_cache.png"

class Notification(object):
    if parser.getboolean('other', 'enable_instruction_webpage') == 1:
        def index(self):
            return """
            <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
    
            <html>
            <head>
                <link href='http://fonts.googleapis.com/css?family=Roboto:400,300' rel=
                'stylesheet' type='text/css'>
                <style type="text/css">
                    body {
                        background-image:url('http://i.imgur.com/l32gHMA.png');
                background-repeat:repeat;
                    }
                    
                    .box {
                        width: 400px;
                        height: 375px;
            
                        position: absolute;
                        top:0;
                        bottom: 0;
                        left: 0;
                        right: 0;
            
                        margin: auto;
                        text-align:center;
                    }
                        
                    a:link {color:#505050;}    /* unvisited link */
                    a:visited {color:#505050;} /* visited link */
                    a:hover {color:#202020;}   /* mouse over link */
                    a:active {color:#A0A0A0;}  /* selected link */
                        
                </style>
                <title>LinConnect</title>
            </head>
            
            <body>
                <div class="box">
                    <h1 style="font-family: 'Roboto', sans-serif; font-weight:300;">
                    LinConnect r""" + version + """ Server Up</h1><span style=
                    "font-family: 'Roboto', sans-serif; font-weight:400;"><b>Local IP
                    Addresses</b><br><i>For Use in Client Configuration</i><br><pre>""" + get_local_ip("<br>") + """</pre></span>
                    <a href=
                    "https://play.google.com/store/apps/details?id=com.willhauck.linconnectclient">
                    <img alt="Android app on Google Play" src=
                    "https://developer.android.com/images/brand/en_app_rgb_wo_60.png"></a><br>
            
                    <br>
                    <span style=
                    "font-family: 'Roboto', sans-serif; font-weight:300;"><a href=
                    "https://plus.google.com/+WillHauckYYC">Google Plus</a> | <a href=
                    "https://github.com/hauckwill">GitHub</a> | Donate via <a href=
                    "https://play.google.com/store/apps/details?id=com.willhauck.donation">Google
                    Play</a> / <a href=
                    "bitcoin:1125MguyS1feaop99bCDPQG6ukUcMuvVBo?label=Will%20Hauck&amp;message=Donation%20for%20LinConnect">
                    Bitcoin</a></span>
                </div>
            </body>
            </html>"""
        index.exposed = True
    
    def notif(self, notif_icon):
        global _notification_header
        global _notification_description
        
        # Get icon
        try:
            os.remove("icon_cache.png") 
        except:
            print "Creating icon cache..."
        file_object = open("icon_cache.png", "a")
        while True:
            data = notif_icon.file.read(8192)
            if not data:
                break
            file_object.write(data)
        file_object.close()
            
        # Ensure the notification is not a duplicate
        if (_notification_header != cherrypy.request.headers['NOTIF-HEADER']) or (_notification_description != cherrypy.request.headers['NOTIF-DESCRIPTION']):
            
            # Get notification data from HTTP header
            _notification_header = cherrypy.request.headers['NOTIF-HEADER'].replace('\x00', '').decode('iso-8859-1', 'replace').encode('utf-8') 
            _notification_description = cherrypy.request.headers['NOTIF-DESCRIPTION'].replace('\x00', '').decode('iso-8859-1', 'replace').encode('utf-8')
            
            # Send the notification
            notif = Notify.Notification.new (_notification_header, _notification_description, icon_path)
            try:
                notif.show ()
            except:
                # Workaround for org.freedesktop.DBus.Error.ServiceUnknown
                Notify.uninit()
                Notify.init("com.willhauck.linconnect")
                notif.show()

        return "true"
    notif.exposed = True
    
def register_callback(sdRef, flags, errorCode, name, regtype, domain):
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        print "Registered Bonjour service " + name
        
def initialize_bonjour(): 
    sdRef = pybonjour.DNSServiceRegister(name = _service_name,
                                     regtype = "_linconnect._tcp",
                                     port = int(parser.get('connection', 'port')),
                                     callBack = register_callback)
    try:
        try:
            while True:
                ready = select.select([sdRef], [], [])
                if sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(sdRef)
        except KeyboardInterrupt:
            pass
    finally:
        sdRef.close()

def get_local_ip(delim):
    ips = ""
    for ip in commands.getoutput("/sbin/ip address | grep -i 'inet ' | awk {'print $2'} | sed -e 's/\/[^\/]*$//'").split("\n"):
        if "127" not in ip:
            ips += ip + ":" + parser.get('connection', 'port') + delim
    return ips
       
# Initialization
if not Notify.init("com.willhauck.linconnect"):
    raise ImportError("Error initializing libnotify")     

# Start Bonjour if desired
if parser.getboolean('connection', 'enable_bonjour') == 1:
    thr = threading.Thread(target=initialize_bonjour)
    thr.start() 

print "Configuration instructions at http://localhost:" + parser.get('connection', 'port')
notif = Notify.Notification.new("Notification server started", "Configuration instructions at\nhttp://localhost:" + parser.get('connection', 'port'), "info")
notif.show()

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = int(parser.get('connection', 'port'))

cherrypy.quickstart(Notification())
