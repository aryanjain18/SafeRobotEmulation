import socket
import numpy as np
from cprof import *
from mapping import *
import time
from utils import SERIAL, HOST, PORT, TIMEOUT


detection_log = open("detection_log.txt", "w")
rtt_log = open("rtt_log.txt", "w")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
def sendData(data):
    bytedata = data.tobytes()
    sock.sendto(bytedata, (HOST, PORT))
    sock.settimeout(TIMEOUT)

    data, address  = sock.recvfrom(1024)
    data = np.frombuffer(data, dtype='<u2', count=-1)  
    return data,  address


def getAverage(file):
    with open(file, "r") as f:
            data = f.readlines()
            data = np.array([float(x.strip().split(": ")[-1]) for x in data[1:]])

    with open(file, "a") as f:
        f.write(f"average: {data.mean()}")

    return


def socketHandler(fireFly):

    detector = create_detector()
    t = None
    i = 0

    while(True):
        t = time.time()
        rows = steady_state(fireFly, detector) 
        if len(rows) < 1: continue

        detection_log.write(f"{i}: {time.time() - t}\n")
        print("sending", rows)

        try: 
            recived, address = sendData(rows)
            rtt_log.write(f"{i}: {time.time() - t}\n")

            print(f"reciving data: {recived}, echoing from: {address}")
        except Exception as e:
            print("timeout occured:", e)

        i += 1

        # if(i > 100):
        #     detection_log.close()
        #     rtt_log.close()
        #     break


def main():
    try:
        system = PySpin.System.GetInstance()
        fireFly_list = system.GetCameras()
        fireFly = fireFly_list.GetBySerial(SERIAL)
        
        fireFly.Init()
        fireFly.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
        fireFly.BeginAcquisition()  

        socketHandler(fireFly)
    
    except KeyboardInterrupt:
        print("closig the client")

    finally:
        fireFly.EndAcquisition()
        sock.close()

        getAverage("detection_log.txt")
        getAverage("rtt_log.txt")

if __name__ == '__main__':
    main()

