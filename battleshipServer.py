#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import re

PORT_NUMBER = 8080
carrier=['C',0,False]
destroyer=['D',0,False]
cruiser=['R',0,False]
submarine=['S',0,False]
battleship=['B',0,False]



def drawboard(x,y,row,play_board):
        row = ''.join(row)
        play_board[int(y)] = row
        board = open("own_board.txt", "w")
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
        
def htmlboards():
        writeboard = open("own_board.txt")
        board = writeboard.readlines()
        writeboard.close()
        nb = open("own_board.html","w")
        nb.write("<h1> Your Board</h1><br>")
        for line in board:
                nb.write("<p> "+ line+ "</p>")
        nb.close()
        writeboard = open("opp_board.txt")
        board = writeboard.readlines()
        writeboard.close()
        nb = open("opp_board.html","w")
        nb.write("<h1> Your Opponent's Board</h1><br>")
        for line in board:
                nb.write("<p> "+ line+ "</p>")
        nb.close()

        
        
                
                

        
#This class will handles any incoming request from the client
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
                hit =3
                
               
                
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
                        battleshi[2] = True
                
                htmlboards()  
                return

try:
	#Create a web server and define the handler to manage the incoming request
	server = HTTPServer(('0.0.0.0', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()
