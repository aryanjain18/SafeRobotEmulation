import socket
import time
import numpy as np

HOST = '192.168.0.101'  # The server's hostname or IP address
PORT = 12345        # The port used by the server
TIMEOUT = 5


rtt_log = open("rtt_log.txt", "w")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
def sendData():
    data = 'ack'
    bytedata = data.tobytes()
    sock.sendto(bytedata, (HOST, PORT))
    sock.settimeout(TIMEOUT)

    data, address  = sock.recvfrom(1024)
    return data,  address


def getAverage(file):
    with open(file, "r") as f:
            data = f.readlines()
            data = np.array([float(x.strip().split(": ")[-1]) for x in data[1:]])

    with open(file, "a") as f:
        f.write(f"average: {data.mean()}")
    return


def socketHandler():

    t = None
    i = 0

    while(True):
        t = time.time()

        try: 
            recived, address = sendData()
            rtt_log.write(f"{i}: {time.time() - t}\n")

            print(f"reciving data: {recived}, echoing from: {address}")
        except Exception as e:
            print("timeout occured:", e)



def main():
    try:
        socketHandler()
    
    except KeyboardInterrupt:
        print("closig the client")

    finally:
        sock.close()
        getAverage("rtt_log.txt")

if __name__ == '__main__':
    main()

