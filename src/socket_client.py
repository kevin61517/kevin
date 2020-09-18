###############################
#        Socket Client        #
###############################
import socket
import time
import datetime


class SocketClient:
    def __call__(self):
        self._start_client()
        self._try_connect()
        self._send_msg()
        while True:
            resp = self._get_resp()
            if resp:
                print("resp:", resp)
                break
            else:
                time.sleep(1)
        self._connect_done()

    def _start_client(self):
        print("== CLIENT START ==")
        self.Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _try_connect(self):
        print("== TRY CONNECT SERVER ==")
        client_msg = (socket.gethostname(), 5269)
        self.Client.connect(client_msg)

    def _send_msg(self):
        print("== TRY TO SEND ==")
        self.Client.send('== This is for test =='.encode())
        print("== SEND SUCCESS ==")

    def _get_resp(self):
        print("TRY GET RESP")
        return self.Client.recv(1024)
        # return

    @classmethod
    def _connect_done(cls):
        Client.close()
        print("== CONNECT DONE ==")


Client = SocketClient()


###############################
#        Socket Client        #
###############################
