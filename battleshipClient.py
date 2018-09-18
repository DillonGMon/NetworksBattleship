import http.client
import sys

HOST_NAME = '10.152.191.254'
PORT_NUMBER = '8080'
xcoord = sys.argv[1]
ycoord = sys.argv[2]

connection = http.client.HTTPConnection("localhost:"+PORT_NUMBER)
connection.request("GET","/","x=" +xcoord + "&y="+ ycoord)
response = connection.getresponse()
result = response.read()

print("status is " +(str(response.status)))
print("the result is " + str(result))
print("finished")
