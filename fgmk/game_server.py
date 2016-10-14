import os
import sys
from PyQt5 import QtCore
import webbrowser
import socket
"""
This module aims to serve the game so the html can be opened in Chrome without
the json queries failing for CORS.

The main function here is servePage, which will receive a directory that has the
game, nameded urlToServe and will spawn a server to serve this page, and then
open a browser.

TODO:
In reality it would be more ideal to spawn a server when a project is loaded and
just open a browser pointing to the served ip and port when requested.

Right now I have to have two servers, one for serving the page and the other to
monitor if the page is closed. The js engine has a listener to request a random
json from the port of the control server when the page is closed (or reloaded),
and the control server (httpdAdm) will detect this and kill the main web server
(httpdGame).
"""

# Make DEBUG=True to view log messages from servers.
DEBUG = False

try:
    from http.server import HTTPServer
    from http.server import SimpleHTTPRequestHandler as SimpleHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer
    from  SimpleHTTPServer import SimpleHTTPRequestHandler as SimpleHTTPRequestHandler


class NoCacheHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    This class makes sure that there is no cache when serving the page,
    and that the terminal output is silent unless DEBUG is True.
    """

    def end_headers(self):
        self.send_my_headers()
        SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
    def log_message(self, format, *args):
        if DEBUG:
            try:
                SimpleHTTPRequestHandler.log_message(self, format, *args)
            except IOError:
                pass
        else:
            return

def openBrowser(ip,port):
    """
    Open browser pointing to the served ip and port.
    note the debug variable passed so the js engine creates a listener to notify
    the adm server when the page is closed (or reloaded).
    """
    url = "http://" + ip + ":{0}".format(port)+"?debug=1"
    new = 2  # 2 goes to new tab, 0 same and 1 window.
    browserOk = webbrowser.open(url, new=new)


def getLocalIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# Subclassing QThread
# http://qt-project.org/doc/latest/qthread.html
class AThread(QtCore.QThread):
    statChanged = QtCore.pyqtSignal()
    """
    The Game Server Thread
    """
    def __init__(self, ip, port, directory):
        QtCore.QThread.__init__(self)
        self.ip = ip
        self.port = port
        self.directory = directory
        self.protocol = "HTTP/1.0"

        os.chdir(self.directory)
        self.serverClass = HTTPServer
        self.handlerClass = NoCacheHTTPRequestHandler
        self.handlerClass.protocol = self.protocol
        self.socketerror = False

        try:
            self.httpdGame = self.serverClass((self.ip, self.port), self.handlerClass)
        except OSError:
            self.socketerror = True

        self.running = False

    def run(self):
        if(self.socketerror):
            self.running = False
            return

        self.running = True
        self.statChanged.emit()
        sa = self.httpdGame.socket.getsockname()
        if DEBUG:
            print("\n---\nServing HTTP on {0}, port {1}\n---\n".format(sa[0], sa[1]))

        self.httpdGame.serve_forever()
        self.httpdGame.socket.close()
        if DEBUG:
            print("\nGameServer stopped\n")

        self.running = False
        self.statChanged.emit()

    def stop(self):
        self.httpdGame.shutdown()
        self.statChanged.emit()


class serverController(QtCore.QObject):
    """
    a controller to stop and rerun the server when needed
    """
    serverStatus = QtCore.pyqtSignal('QString')
    def __init__(self, ip='0.0.0.0', port=8080):
        QtCore.QObject.__init__(self)
        self.curdir = os.curdir
        self.localip = getLocalIP()
        self.ip = ip
        self.port = port
        self.directory = ''

    def runServer(self, directory=''):
        if(directory!=''):
            self.directory=directory

        try:
            self.stopServer()
        except:
            pass
        #app = QCoreApplication([])
        self.thread = AThread(self.ip,self.port,self.directory)
        #self.thread.finished.connect(app.exit)
        self.thread.statChanged.connect(self.updateStatus)
        self.thread.start()

    def stopServer(self):
        try:
            self.thread.stop()
        except AttributeError:
            pass

    def updateStatus(self):
        self.serverStatus.emit(self.getStatusMsg())

    def openWebBrowser(self):
        openBrowser(self.ip,self.port)

    def restartAndOpenBrowser(self,directory):
        self.runServer(directory)
        self.openWebBrowser()

    def status(self):
        try:
            stat = self.thread.running
        except AttributeError:
            stat = False

        return stat

    def getStatusMsg(self):
        if(self.ip == '0.0.0.0' or self.ip == '127.0.0.1'):
            ip = self.localip
        else:
            ip = self.ip

        if self.status():
            return 'server running at http://'+ip+':'+str(self.port)+'    '
        else:
            return 'server stopped'+'    '
