import socket


class SocketClient:
    def __init__(self, host, port):
        """"""
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))

    @staticmethod
    def _init(msg: str):
        return msg.encode()

    def send(self, msg):
        self.conn.send(self._init(msg))


host = 'http://4854-1-163-231-92.ngrok.io'
port = 2222
socket_client = SocketClient(host='127.0.0.1', port=port)


if __name__ == '__main__':
    socket_client.send('kevin')
