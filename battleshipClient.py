import http.client
import sys

HOST_NAME = '0.0.0.0'
PORT_NUMBER = '8080'
xcoord = sys.argv[1]
ycoord = sys.argv[2]

connection = http.client.HTTPConnection("localhost:"+PORT_NUMBER)
connection.request("POST","/","x=" + xcoord + "&y=" + ycoord)
response = connection.getresponse()
print("The response is " + (str)(response.status))
print("finished")
