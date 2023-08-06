import threading
import time
import socket
import struct
import time
import sys
import datetime
class ModbusData:
    def __init__(self,IP,port):
        self.IP = IP
        self.port = port
        self.X = []
        self.Y = []
        self.Z = []
        self.F = []
        self.UT = []
        self.SPS = 0
        self.scale = 0
        self.connect_success=False
        self.wait=False
        self.S303_3Axis=True

        self.lock = threading.Lock()
        self.background_thread = threading.Thread(target=self.connect, args=(IP,port), daemon=True)
        self.background_thread.start()

    def connect(self,IP,port):
        arr = [0x01, 0x02, 0x00, 0x00, 0x00, 0x06, 0x01, 0x06, 0x00, 0xc0, 0x00, 0x10]
        link=struct.pack("%dB"%(len(arr)),*arr)

        try: 
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e: 
            print ("Error creating socket: %s" % e) 
            sys.exit(1) 
        
        # Second try-except block -- connect to given host/port 
        try: 
            client.connect((IP,port))
            print("connect success")
            #print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' + str(datetime.datetime.now()))
            self.connect_success = True
        except : 
            print ("FAIL") 
            sys.exit(1) 
        

        client.send(link)

        while True:
            link1 = client.recv(24080)
            
            string = link1.hex()
            #print(string)

            #第一個    
            if('53594e43' in string):
                tmp=''
                #print(string)
                tmp = tmp + string
                #print("-----T="+str(len(tmp)))  
                #XYZstorage(string[70:])
                CRC16 = tmp[-4:]
                #print(len(tmp))
                
                tmp_header = int(tmp[12:14], 16)
                tmp_header = (tmp_header + 11) * 2
                #header
                header =tmp[:tmp_header]
                UTime = header[30:32] + header[28:30] + header[26:28] + header[24:26] + header[22:24]  
                UTime = int(UTime, base=16)
                #print(UTime)
                SPS = header[48:50] + header [46:48]
                SPS = int(SPS, base=16)
                
                scale = header [44:46] + header[42:44] + header [40:42] + header[38:40] 
                
                
                binary_number = bytes.fromhex(scale)
                
                scale = struct.unpack('!f', binary_number)[0]
                scale = format(scale,'.2f')
                #print("scale" + str(scale))

                #print(CRC16)
                XYZdata = tmp[tmp_header:-4]
                #print(header[52:54])
                if(header[52:54] == '03'):
                    self.S303_3Axis = True
                elif(header[52:54] == '04'):
                    self.S303_3Axis = False
                
                self.UT.append(UTime)
                self.SPS = SPS
                self.scale = scale

                if(self.S303_3Axis):
                    xconnect, yconnect, zconnect = data_cut(XYZdata,self.S303_3Axis)
                    self.X.extend(xconnect)
                    self.Y.extend(yconnect)
                    self.Z.extend(zconnect)
                else:
                    xconnect, yconnect, zconnect, fconnect = data_cut(XYZdata,self.S303_3Axis)
                    self.X.extend(xconnect)
                    self.Y.extend(yconnect)
                    self.Z.extend(zconnect)
                    self.F.extend(fconnect)

                if(len(self.X)>60000):
                    del self.X[:1000]
                    del self.Y[:1000]
                    del self.Z[:1000]
                    del self.F[:1000]
                    del self.UT[:1]

    def get_IP(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.IP
        except :
            print("Connect Fail, so Nothing in list")

    def get_Port(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.port
        except :
            print("Connect Fail, so Nothing in list")

    def get_Now_Channel1(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.X[-1000:]
        except :
            print("Connect Fail, so Nothing in list")
    def get_Now_Channel2(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Y[-1000:]                  
        except :
            print("Connect Fail, so Nothing in list")
    def get_Now_Channel3(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Z[-1000:]          
        except :
            print("Connect Fail, so Nothing in list")
    def get_Now_Channel4(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.F[-1000:]                
        except :
            print("Connect Fail, so Nothing in list")    
    def get_Now_UnixTime(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.UT[-1]
        except :
            print("Connect Fail, so Nothing in list")
    def get_SPS(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.SPS
        except :
            print("Connect Fail, so Nothing in list")
    def get_Scale(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.scale
        except :
            print("Connect Fail, so Nothing in list")

    def get_NsecondChannel1Data(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.UT)<N):
            print("Only have "+ str(len(self.UT)) + " Second Data")
            N = len(self.UT)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*1000
        Xreturn = []
        UTreturn = []
        try:
            Xreturn.extend(self.X[-N1000:])
            UTreturn.extend(self.UT[-N:])
            return Xreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")
    def get_NsecondChannel2Data(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.UT)<N):
            print("Only have "+ str(len(self.UT)) + " Second Data")
            N = len(self.UT)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*1000
        Yreturn = []
        UTreturn = []
        try:
            Yreturn.extend(self.Y[-N1000:])
            UTreturn.extend(self.UT[-N:])
            return Yreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")
        
    def get_NsecondChannel3Data(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.UT)<N):
            print("Only have "+ str(len(self.UT)) + " Second Data")
            N = len(self.UT)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*1000
        Zreturn = []
        UTreturn = []
        try:
            Zreturn.extend(self.Z[-N1000:])
            UTreturn.extend(self.UT[-N:])
            return Zreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")
    
    def get_NsecondChannel4Data(self,N):
        #print("len(Data)" + str(len(Data)))
        if(self.S303_3Axis==True):
            print("You don't have Channel 4")
            return 
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.UT)<N):
            print("Only have "+ str(len(self.UT)) + " Second Data")
            N = len(self.UT)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*1000
        Freturn = []
        UTreturn = []
        try:
            Freturn.extend(self.F[-N1000:])
            UTreturn.extend(self.UT[-N:])
            return Freturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")


def data_cut(XYZstr,S303_3Axis):
    #print(S303_3Axis)
    xdata_cut = []
    ydata_cut = []
    zdata_cut = []
    fdata_cut = []
    flag = 0
    #Little Endian 轉回正常
    XYZhex = ''
    #print(len(XYZstr))
    
    #每4個byte為一組處理
    for i in range(0, len(XYZstr), 8):
        XYZdecimal=0
        a = XYZstr[i:i+2]
        b = XYZstr[i+2:i+4]
        c = XYZstr[i+4:i+6]
        d = XYZstr[i+6:i+8]
        XYZhex = d+c+b+a
        #hex to decimal 
        if(len(XYZhex)==8):
            XYZdecimal=struct.unpack('>f',bytes.fromhex(XYZhex))[0]
        #print(type(XYZdecimal))
        #print(XYZhex)
        #print(XYZdecimal)
        
        #儲存進XYZ的陣列
        if(S303_3Axis):
            if(flag == 0):
                xdata_cut.append(XYZdecimal)
                flag = flag +1
            elif(flag == 1):
                ydata_cut.append(XYZdecimal)
                flag = flag +1
            elif(flag == 2):
                zdata_cut.append(XYZdecimal)
                flag = 0
        else:
            if(flag == 0):
                xdata_cut.append(XYZdecimal)
                flag = flag +1
            elif(flag == 1):
                ydata_cut.append(XYZdecimal)
                flag = flag +1
            elif(flag == 2):
                zdata_cut.append(XYZdecimal)
                flag = flag +1
            elif(flag == 3):
                fdata_cut.append(XYZdecimal)
                flag = 0
    
    
    #print("XYZstr: " + str(len(XYZstr)))
    if(S303_3Axis):
        return xdata_cut, ydata_cut, zdata_cut
    else:
        return xdata_cut, ydata_cut, zdata_cut, fdata_cut



if __name__ == '__main__':
    XXXX = ModbusData('10.0.0.50',502)
    aaaa = ModbusData('10.0.0.68',502)
    """aaaa = ModbusData('10.0.0.180',502)    
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' + str(datetime.datetime.now()))

    time.sleep(2)
    x, n= XXXX.get_NsecondChannel3Data(10)
    print(len(x))
    print(len(n))
    """
    
    while True:
        #bbbb = aaaa.get_Now_Channel1()
        #data = XXXX.get_Now_Channel1()
        print(len(aaaa.get_Now_Channel4()))
        print(len(XXXX.get_Now_Channel4()))
        #print("Current data:", len(my_obj.get_Now_UnixTime()))
        time.sleep(1)
    
    
