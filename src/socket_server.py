import socket
from socket_client import Client
import time
from dataclasses import dataclass


###############################
#        Socket Server        #
###############################
import socket
import threading


class SocketServer:

    def __call__(self):
        self._make_server()
        self._set_port()
        self._stack()
        while True:
            print("== START SERVING ==")
            self._start_service()
            while True:
                print("== TRY GET CLIENT ==")
                msg = self._get_client()
                if msg:
                    print("THIS IS msg------->", msg)
                    self.Server.send(b"== You r Gay!! ==")
                time.sleep(1)

    def _make_server(self):
        """
        創建Server
        """
        self.Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _set_port(self):
        """
        綁定port
        """
        server_msg = (socket.gethostname(), 5269, )
        self.Server.bind(server_msg)

    def _stack(self):
        """
        連線佇列
        """
        self.Server.listen(5)

    def _start_service(self):
        self.client, self.addr = self.Server.accept()
        print("Client-->", self.client)
        print("addr---->", self.addr)

    def _get_client(self):
        return self.client.recv(1024)

    def _done(self):
        print("== SERVICE DONE ==")
        self.client.close()  # 關閉連線
        self.Server.close()  # 關閉服務


Server = SocketServer()

if __name__ == "__main__":
    server = threading.Thread(target=Server)
    client = threading.Thread(target=Client)
    server.start()
    time.sleep(0.5)
    client.start()
