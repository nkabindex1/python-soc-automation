import socket
HOST = 'xxxx'
PORT = 22
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)
print("Listening")
s = server_socket.accept()
print("Connected")
