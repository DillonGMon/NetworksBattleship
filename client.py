import http.client
import sys
import re

HOST_NAME = sys.argv[1]
PORT_NUMBER = sys.argv[2]
xcoord = sys.argv[3]
ycoord = sys.argv[4]

def resolve(hit):
    board = open("opp_board.txt")
    play_board = board.readlines()
    board.close()
    row = list(play_board[int(ycoord)])
    if hit == 0:
        row[int(xcoord)] = 'O'
    else:
        row[int(xcoord)] = 'X'
    row = ''.join(row)
    play_board[int(ycoord)] = row
    board = open("opp_board.txt", "w")
    for item in play_board:
        board.write(str(item))
    board.close()
    
connection = http.client.HTTPConnection(HOST_NAME+":"+PORT_NUMBER)
connection.request("GET","/","x=" + xcoord + "&y=" + ycoord)
response = connection.getresponse()
if response.status == 200:
    result = response.read()
    result = re.sub("'",'', str(result))
    result = re.split('&', str(result))
    hit = int(re.sub('[^0-9]','', result[0]))
    if hit == 0:
        print("Miss!")
    else:
        print("Hit!")
    if len(result) > 1:
        sunk = re.sub('/sunk=','', result[1])
        if sunk == 'D':
            print("Sank a Destroyer!")
        elif sunk == 'R':
            print("Sank a Cruiser!")
        elif sunk == 'C':
            print("Sank a Carrier!")
        elif sunk == 'S':
            print("Sank a Submarine!")
        elif sunk == 'B':
            print("Sank a Battleship!")
        else:
            print("Who knows what you sank?")
            print(sunk)
    resolve(hit)
elif response.status == 404:
    print("Those coordinates are out of bounds!")
elif response.status == 410:
    print("You've already fired on those coordinates!")
elif response.status == 400:
    print("Your coordinates were improperly formatted, please try again")
