import socket
import time
import datetime


class SocketServer:
    """socket server"""
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

    def run(self):
        while True:
            connect, address = self.server.accept()
            now = datetime.datetime.now().replace(microsecond=False)
            client_message = str(connect.recv(1024), encoding='utf-8')
            print(f'{client_message}--{address[0]}:{str(address[1])}--{now}')


host = 'http://4854-1-163-231-92.ngrok.io'
port = 2222
socket_server = SocketServer(host='127.0.0.1', port=port)


if __name__ == '__main__':
    """socket server"""
    socket_server.run()

