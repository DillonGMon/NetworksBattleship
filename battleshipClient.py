import http.client

HOST_NAME = '10.152.191.254'
PORT_NUMBER = '8080'

connection = http.client.HTTPConnection("localhost:"+PORT_NUMBER)
connection.request("GET","/")
response = connection.getresponse()
print("status is " +response.status)
print("finished")
