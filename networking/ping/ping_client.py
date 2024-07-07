import socket
import os
from sys import platform
import numpy as np
import socketserver
import time

CWD = os.getcwd()

def get_ip():

    if platform == "linux" or platform == "linux2":
        gw = os.popen("ip -4 route show default").read().split()
        gw = gw[2]
    elif platform == "win32":
        os.system('ipconfig | findstr /i "Gateway" > temp.txt')
        with open("temp.txt", "r") as f:
            gw = f.readlines()[-1].strip().split(" ")[-1]

    

    print("Deafault Gateway: ", gw)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((gw, 0))
    ipaddr = s.getsockname()[0]
    print(f"Host IP is {ipaddr}")
    return ipaddr


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        
        t1 = time.time()
        data, socket = self.request
        socket.sendto(data, self.client_address)
        t2 = time.time()

        print("{} wrote:".format(self.client_address))
        print("sending data -> ", data, "RTT Delay Server:", t2 - t1)


def main():
    HOST = get_ip()   # Standard loopback interface address (localhost)
    PORT = 12345       # Port to listen on (non-privileged ports are > 1023)

    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)

    try:
        server.serve_forever()    
    except KeyboardInterrupt:
        print("closing the server")


if __name__ == '__main__':
    main()