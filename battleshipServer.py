#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import re
import sys

PORT_NUMBER = sys.argv[1]
BOARD = sys.argv[2]
carrier=['C',0,False]
destroyer=['D',0,False]
cruiser=['R',0,False]
submarine=['S',0,False]
battleship=['B',0,False]



def drawboard(x,y,row,play_board):
        row = ''.join(row)
        play_board[int(y)] = row
        board = open(BOARD, "w")
        for item in play_board:
                board.write(str(item))
        board.close()


def checkHit(x,y):
        board = open("own_board.txt")
        play_board = board.readlines()
        board.close()
        row = list(play_board[int(y)])
        target = row[int(x)]
        print("the target is "+ target)
        if  row[int(x)]=='C':
                carrier[1]+=1
                row[int(x)]='X'
                drawboard(x,y,row,play_board)
                return 1
        elif row[int(x)]=='D':
                destroyer[1] +=1
                row[int(x)]='X'
                drawboard(x,y,row,play_board)
                return 1
        elif row[int(x)]=='B':
                battleship[1] +=1
                row[int(x)]='X'
                drawboard(x,y,row,play_board)
                return 1
        elif row[int(x)]=='R':
                cruiser[1] +=1
                row[int(x)]='X'
                drawboard(x,y,row,play_board)
                return 1
        elif row[int(x)]=='S':
                submarine[1] +=1
                row[int(x)]='X'
                drawboard(x,y,row,play_board)
                return 1
        elif row[int(x)]=='_':
                row[int(x)]='O'
                drawboard(x,y,row,play_board)
                return 0
        else:
                
                
                return 3
        
def htmlboards(self, current_board):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print("ownboard")
        writeboard = open(current_board)
        board = writeboard.readlines()
        writeboard.close()
        if(current_board == "own_board.txt"):
                self.wfile.write(b"<h1> Your Board</h1><br>")
        else:
                self.wfile.write(b"<h1> Their Board</h1><br>")
        for line in board:
                self.wfile.write(b"<p> "+ bytes(line,'utf-8')+ b"</p>")
        
        
                
                

        
#This class will handles any incoming request from the client
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
                print (str(self.path))
                xmatch= False
                ymatch= False

                content_len = int(self.headers.get('content-length',0))
                post_body = self.rfile.read(content_len)
                if (str(post_body) != "b''"):
                        coord = re.split('&',str(post_body))
                        print(str(post_body))
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
                        if xcoord.isdigit() and ycoord.isdigit():
                                
                                
                                if int(xcoord)>=10 or int(ycoord)>=10 or int(xcoord)<0 or int(ycoord)<0:
                                        self.send_response(404)
                                        self.send_header("Content-type", "text/html")
                                        self.end_headers()
                                else:
                                        hit = checkHit(xcoord,ycoord)
                                if hit ==3:
                                        self.send_response(410)
                                        self.send_header("Content-type", "text/html")
                                        self.end_headers() 
                                        
                                else:
                                        
                                        self.send_response(200)
                                        self.send_header("Content-type", "text/html")
                                        self.end_headers()
                        else:
                                self.send_response(400)
                                self.send_header("Content-type", "text/html")
                                self.end_headers()     

                                                                        #sends a hit or miss message
                        if hit==0:
                                self.wfile.write(b"hit=0")
                        elif hit==1:
                                self.wfile.write(b"hit=1")


                                                                        #sends message for if a ship was sunk
                        if carrier[1]>=5 and carrier[2]==False:
                                self.wfile.write(b"&/sunk=C")
                                carrier[2] = True
                        elif destroyer[1]>=2 and destroyer[2]==False:
                                self.wfile.write(b"&/sunk=D")
                                destroyer[2] = True
                        elif cruiser[1]>=3 and cruiser[2]==False:
                                self.wfile.write(b"&/sunk=R")
                                cruiser[2] = True
                        elif submarine[1]>=3 and submarine[2]==False:
                                self.wfile.write(b"&/sunk=S")
                                submarine[2]=True
                        elif battleship[1]>=4 and Sbattleship[2]==False:
                                self.wfile.write(b"&/sunk=B")
                                battleship[2] = True
                
                        htmlboards()
                elif self.path=="/own_board.html":
                        htmlboards(self,"own_board.txt")
                elif self.path=="/opp_board.html":
                        htmlboards(self, "opp_board.txt")
                        
                else:
                      #  print(str(self.get()))
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        
                return

try:
	#Create a web server and define the handler to manage the incoming request
	server = HTTPServer(('0.0.0.0', int(PORT_NUMBER)), myHandler)
	print ('Started httpserver on port ' , PORT_NUMBER)
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print ('Shutting down the web server')
	server.socket.close()
