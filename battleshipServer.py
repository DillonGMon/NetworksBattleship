#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import re

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_POST(self):
		self.send_response(200)
		#self.send_header('Content-type','text/html')
		#self.end_headers()
		# Send the html message
		#self.wfile.write("Hello World !")
		return
	def do_GET(self):
                xcoord=11
                xmatch= False
                ycoord=11
                ymatch= False
                hit = 1     
                
                content_len = int(self.headers.get('content-length',0))
                post_body = self.rfile.read(content_len)
                coord = re.split('&',str(post_body))
                for item in coord:
                        print(item)
                        if xmatch==False:
                                xcoord =re.sub('[^0-9]','',item)
                                print("x is " + str(xcoord))
                                xmatch=True
                        elif ymatch==False:
                                ycoord=re.sub('[^0-9]','',item)
                                print("y is " + str(ycoord))
                                ymatch=True

                print("the coordinates are "+ str(xcoord)+ " " + str(ycoord))
                if int(xcoord)>=10 or int(ycoord)>=10 :
                        self.send_response(404)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                else:
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()


                if hit:
                        self.wfile.write(b"hit=1")
                        
                return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('0.0.0.0', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()
