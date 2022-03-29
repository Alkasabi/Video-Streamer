
from tkinter import Frame
import cv2 ,random,socket,base64,imutils,time


class UDP_Streamer():
    def __init__(self) -> None:
        self.BUFF_SIZE = 65535
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,self.BUFF_SIZE)
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name) #192.168.1.102#  
        self.client_add=[]
        self.client_add.append( ("127.0.0.1",5051) )
        print("print Host IP",self.host_ip)
        self.port = 9999
        self.img_size= (400,600)
        self.socket_address = (self.host_ip,self.port)

    def set_frame_size(self,size):
        self.img_size=size

    def set_client_add(self,client_add):
        self.client_add.append( client_add )

    def send_frame(self,frame):
        try:
            self.encode_frame(frame)
            self.create_packet()
            self.send_buffer()
        except Exception as e:
            print("send frame",e)
        
    def encode_frame(self,frame):
        self.alpha = 1.2 # Contrast control (1.0-3.0)
        self.beta = 0 # Brightness control (0-100)
        self.full_frame=frame
        self.small_frame=cv2.resize(self.full_frame,self.img_size)
        self.frame = cv2.convertScaleAbs(self.small_frame, alpha=self.alpha, beta=self.beta)
        #self.frame = imutils.resize(self.frame,width=self.width)
        encoded,self.buffer = cv2.imencode('.jpg',self.frame,[cv2.IMWRITE_JPEG_QUALITY,80])
        self.buffer = base64.b64encode(self.buffer)
        
    def create_packet(self):
        header=format(0x010203)
        tail=format(0x0405060)
        header=header.encode('utf-8')
        tail=tail.encode('utf-8')
        self.packet= header+self.buffer+tail
        
    def send_buffer(self):
        print("packet len ",len(self.packet)) 
        total=0
        for y in range(0,len(self.packet),60000):
            chunk=self.packet[y:y+60000]
            #print(udp_buffer)
            total=total+len(chunk)
            for cl in self.client_add:
                try:
                    self.server_socket.sendto(chunk,cl)
                except Exception as e:
                    print("Error in send frame to ",cl,e)

            time.sleep(0.01)

if __name__=="__main__":

    img=cv2.imread("test.jpg")
    
    streamer=UDP_Streamer()
    streamer.set_frame_size((600,400))
    #streamer.encode_frame(img)
    #streamer.create_packet()
    
    vid_file="traffic.mp4"
    vid=cv2.VideoCapture(vid_file)

    while True:
        ret,frame=vid.read()
        if ret:
            streamer.send_frame(frame)
            cv2.imshow("streamer",frame)
            cv2.waitKey(1)
            
        #streamer.send_buffer()
        #streamer.send_frame(img)
        #time.sleep(1)
        
