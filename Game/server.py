import sys 
#from threading import Thread
import webbrowser
import BaseHTTPServer 
import SimpleHTTPServer

serverClass=BaseHTTPServer.HTTPServer
handlerClass=SimpleHTTPServer.SimpleHTTPRequestHandler

Protocol = "HTTP/1.0"
port = 8080
ip = '127.0.0.1'

new = 2 #2 goes to new tab, 0 same and 1 window.
url = "http://"+ip+":{0}".format(port)

handlerClass.protocol = Protocol
httpd = serverClass((ip,port), handlerClass)

sa = httpd.socket.getsockname()
print("\n---\nServing HTTP on {0}, port {1}\n---\n".format(sa[0],sa[1]) )
browserOk = webbrowser.open(url,new=new)

def runWhileTrue():
    while True:
        #print(vars(httpd))
        httpd.handle_request()

runWhileTrue()

#def simpleServer():
#    httpd.serve_forever()

#serverThread = Thread(simpleServer,None)
#serverThread.start()
#print(serverThread)


