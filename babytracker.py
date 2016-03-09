#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer
import re
from db import BabyDB

PORT = 8000
actions = re.compile(r"^\/db\/(add|getlast)\/([a-zA-Z]{1,32})$")

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    lastgen=0
    def __init__(self,req,client_addr,server):
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self,req,client_addr,server)
    def do_GET(self):
        if "/db/" in self.path:
            return self.dbaction()
        else:
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def dbaction(self):
        m = actions.match(self.path)
        if m is None:
            data = "404 Page not found!"
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(data))
            self.end_headers()
            self.wfile.write(data)


        else:
            db = BabyDB()
            action = m.group(2)
            if m.group(1) == "add":
                ts = db.add(action)
                data = '{"action":"%s","timestamp":%i}' % (action,ts*1000)
            elif m.group(1) == "getlast":
                ts = db.getlast(action)
                data = '{"action":"%s","timestamp":%i}' % (action,ts*1000)
            db.close()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Content-length", len(data))
            self.end_headers()
            self.wfile.write(data)

class MyTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

if __name__ == "__main__":
    from optparse import OptionParser,OptionValueError
    import os,sys
    parser = OptionParser(usage="usage: %prog [options]\n\nRun Babytracker as standalone webserver")
    parser.add_option("-p","--port", dest="port",help="Listening TCP port", metavar="PORT",default=PORT, type="int")
    try:
        (options, args) = parser.parse_args()
        port=options.port
        if not (0<port<2**16):
            raise ValueError("Port number out of range")
    except (OptionValueError, ValueError):
        print "Port must a number in range 1..65535"
        exit(1)

    try:
        np=os.path.dirname(sys.argv[0])
        if np != "":
            os.chdir(os.path.dirname(sys.argv[0]))
        Handler = MyHandler

        httpd = MyTCPServer(("", port), Handler)

        print "serving at port", port
        httpd.serve_forever()
    finally:
        pass
