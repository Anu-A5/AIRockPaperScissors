import socket
import time

class rps_network:

    def __init__(self, HOST, PORT):
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

        self.s.settimeout(30)

        self.DataIn = [0,0,0,0,0,0,0,0]

        self.i = 0

    def writeToProcessing(self, data):        
        self.s.sendall((data + "\n").encode("utf-8"))
        time.sleep(2)

    def readToProcessing(self):  
        data_in = self.s.recv(1024)
        if not data_in: sys.exit(0)
        data_in_a = list(data_in)
        if(len(data_in_a) >= 6):
            self.DataIn = [int(i) - 48 for i in data_in_a]
            print(self.DataIn)

    def start_game(self):
        return self.DataIn[2]

    def determine_user_hand(self):
        hands = ["000", "001", "010"]
        self.writeToProcessing("001" + hands[self.i] + "000")
        if(self.i > 2):
            self.i=0

    def settimeout_1(self):
        self.s.settimeout(1)     

    def settimeout_None(self):
        self.s.settimeout(None)             

    def capture_user_move(self):
        return self.DataIn[1]
    