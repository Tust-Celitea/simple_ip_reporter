#!/usr/bin/python

import socket

# config server port
server_port=12000

# start server use defined port

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(('',server_port))
server_socket.listen(1)

print("Server is ready to listen at port {}".format(server_port))

while True:
    connection,addr=server_socket.accept()
    response=connection.recv(1024)
    print("Ping from {}".format(response))
