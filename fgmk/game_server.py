import os
import sys
from threading import Thread
import webbrowser
#import BaseHTTPServer
#import SimpleHTTPServer
try:
    from http.server import HTTPServer as BaseHTTPServer
    from http.server import SimpleHTTPRequestHandler as SimpleHTTPRequestHandler
except ImportError:
    import BaseHTTPServer
    from  SimpleHTTPServer import SimpleHTTPRequestHandler as SimpleHTTPRequestHandler

class NoCacheHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_my_headers()
        SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

def servePage(urlToServe):
    tempOrigiCurDir = os.curdir
    os.chdir(urlToServe)
    serverClass = BaseHTTPServer
    handlerClass = NoCacheHTTPRequestHandler

    Protocol = "HTTP/1.0"
    port = 8080
    ip = '127.0.0.1'
    admIp = ip
    admPort = 8081

    new = 2  # 2 goes to new tab, 0 same and 1 window.
    url = "http://" + ip + ":{0}".format(port)+"?debug=1"

    handlerClass.protocol = Protocol
    try:
        httpdGame = serverClass((ip, port), handlerClass)
    except:
        os.chdir(tempOrigiCurDir)
        return False
    httpdAdm = serverClass((admIp, admPort), handlerClass)

    sa = httpdGame.socket.getsockname()
    sb = httpdAdm.socket.getsockname()
    print("\n---\nServing HTTP on {0}, port {1}\n---\n".format(sa[0], sa[1]))
    print(
        "\n---\nAdm HTTP listening on {0}, port {1}\n---\n".format(sb[0], sb[1]))
    browserOk = webbrowser.open(url, new=new)

    def runGameServer():
        httpdGame.serve_forever()
        print("\nrunGameServer stopped\n")
        httpdAdm.shutdown()
        httpdAdm.socket.close()
        httpdGame.socket.close()
        emit(SIGNAL('browserClosed()'))
        return

    def runAdmServer():
        httpdAdm.handle_request()
        httpdGame.shutdown()
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
