import os
import sys
from threading import Thread
import webbrowser

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

def servePage(urlToServe):
    """
    Creates the server
    """
    tempOrigiCurDir = os.curdir
    os.chdir(urlToServe)
    serverClass = HTTPServer
    handlerClass = NoCacheHTTPRequestHandler

    Protocol = "HTTP/1.0"
    port = 8080
    ip = '127.0.0.1'
    admIp = ip
    admPort = 8081

    handlerClass.protocol = Protocol
    try:
        httpdGame = serverClass((ip, port), handlerClass)
    except:
        os.chdir(tempOrigiCurDir)
        return False
    httpdAdm = serverClass((admIp, admPort), handlerClass)

    sa = httpdGame.socket.getsockname()
    sb = httpdAdm.socket.getsockname()
    if DEBUG:
        print("\n---\nServing HTTP on {0}, port {1}\n---\n".format(sa[0], sa[1]))
        print("\n---\nAdm HTTP listening on {0}, port {1}\n---\n".format(sb[0], sb[1]))

    openBrowser(ip,port)

    def runGameServer():
        httpdGame.serve_forever()
        if DEBUG:
            print("\nrunGameServer stopped\n")
        httpdAdm.shutdown()
        httpdAdm.socket.close()
        httpdGame.socket.close()
        emit(SIGNAL('browserClosed()'))
        return

    def runAdmServer():
        httpdAdm.handle_request()
        httpdGame.shutdown()
        if DEBUG:
            print("\nrunAdmServer stopped\n")
        httpdAdm.socket.close()
        httpdGame.socket.close()
        return

    gameServerThread = Thread(target=runGameServer)
    gameServerThread.daemon = True
    admServerThread = Thread(target=runAdmServer)
    admServerThread.daemon = True

    gameServerThread.start()
    admServerThread.start()
    # admServerThread.join()
    os.chdir(tempOrigiCurDir)
    return True
