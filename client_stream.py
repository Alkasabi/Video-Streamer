# This is client code to receive video frames over UDP
from tkinter import Frame
import cv2, imutils, socket
import numpy as np
import time
import base64


BUFF_SIZE = 65536
UDP_IP = "127.0.0.1"

UDP_PORT = 5051
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.bind((UDP_IP, UDP_PORT))
header=format(0x010203)
tail=format(0x0405060)

packet=None

while True:
    try:
        if packet:
            buffer,_ =client_socket.recvfrom(BUFF_SIZE)
            packet=packet+str(buffer)
        else:
            buffer,_ =client_socket.recvfrom(BUFF_SIZE)
            packet=str(buffer)

        #print(" packet size",len(packet))
        head_flag=packet.find(header)
        tail_flag=packet.find(tail)
        if head_flag > -1 and tail_flag > -1  :
            #print("got packet header",len(packet))
            bin_frame=packet[len(header)+2:-len(tail)-1]
            print("frame size",len(bin_frame))
            #bin_packet=bytearray(packet)
            data = base64.b64decode(bin_frame,' /')
            npdata = np.frombuffer(data,dtype=np.uint8)
            frame = cv2.imdecode(npdata,1)
            #frame = cv2.putText(frame,"Recived Frame")
            cv2.imshow("RECEIVING Violation image",frame)
            cv2.waitKey(1)
            packet=None
    except Exception as e:
        packet=None
        print(e)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
        break

