
# coding: utf-8

# In[ ]:


from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEException, BTLEDisconnectError
import threading
from concurrent.futures import ThreadPoolExecutor
import time

blunoAddress = ['78:DB:2F:BF:34:3B', '78:DB:2F:BF:37:F5','1C:BA:8C:1D:31:CB']
#,,


blunoHandshake = [0,0,0]
index = 1
startTime = 0
connectionThreads = []
entryFlag = 1
dataFlag = 0
class NotificationDelegate(DefaultDelegate):

    def __init__(self,index):
        DefaultDelegate.__init__(self)
        self.orderedStr = ""
        self.sensorValues = list()
        self.index = index
    
    def handleNotification(self, cHandle, rawData):
        global blunoHandshake
        data = rawData.decode("utf-8")
        if data == "ACK":
            if blunoHandshake[self.index] == 0:
                blunoHandshake[self.index] = 1
                print("Bluno " + str(self.index) + " has acknowledged the Hello!")
        if blunoHandshake[self.index] == 1:
            self.handleData(data)
        else:
            pass

    def handleData(self,data):
        global entryFlag
        global dataFlag
        global index
        global startTime
        if(entryFlag):
            print("Data from Bluno " + str(self.index))
            entryFlag = 0
        dataLen = len(data)
        self.orderedStr += data
        if(data[dataLen-1] == "z"):
            entryFlag = 1
            #dataFlag = 1
            dataFlag = 0
            msgLen = len(self.orderedStr)
            if(self.checksumCheck(self.orderedStr,msgLen)):
                self.orderedStr = self.orderedStr[:msgLen-2] + "\0"
                print(self.orderedStr)
#                 print(index)
#                 print(time.time() - startTime)
#                index += 1
#                if index == 1000:
#                    startTime = time.time()
#                if index == 2000:
#                    print(time.time()-startTime)
                #output = self.orderedStr
                #%%capture output
                #x = output.stdout
                #%store x > output.txt0
                for f in self.orderedStr.split():
                    pass
                    #self.sensorValues.append(float(f))
                self.orderedStr = ""
            else:
                self.orderedStr = ""
        return self.orderedStr

   # def handleDatav2(self,data):
   #     global entryFlag
   #     global dataFlag
   #     if(entryFlag):
   #         print("Data from Bluno " + str(self.index))
   #         entryFlag = 0
   #     dataLen = len(data)
   #     self.orderedStr += data
   #     if(data[dataLen-1] == "z"):
   #         entryFlag = 1
   #         dataFlag = 1
   #         msgLen = len(self.orderedStr)
   #         self.orderedStr = self.orderedStr[:msgLen-2] + "\0"
   #         self.sensorValues.append(float(f) for f in self.orderedStr.split())
   #         self.orderedStr = ""
   #         
   #         self.orderedStr = ""
   #     return self.orderedStr

   # def checksumCheckv2(self,sensorValues):
   #     checksum = 0.0
   #     for i in range(0,7):
   #         checksum += sensorValues[i]
   #     if checksum == sensorValues[6]:
   #         return True
   #     else:
   #         return False
        
    def checksumCheck(self,msgString,msgLen):
        index = 0
        checksum = 0 
        while index < msgLen-2:
            checksum ^= ord(msgString[index])
            index += 1
        
        checksum = (checksum%95) + 33
        if(checksum == ord(msgString[msgLen-2])):
            return True
        else:
            print("Err msg detected.")
            return False

def run(blunoAddr,index):
    global blunoHandshake
    global dataFlag
    global startTime
    while True:
        print("Trying to connect bluno " + str(index))
        try:
            p = Peripheral(blunoAddr)
            p.withDelegate(NotificationDelegate(index))
            blunoService = p.getServiceByUUID("0000dfb0-0000-1000-8000-00805f9b34fb")
            serviceChara = blunoService.getCharacteristics()[0]
            break
        except:
            continue
    print("Connected to bluno " + str(index))
    while blunoHandshake[index] == 0:
        initHandshake(serviceChara)
        if(p.waitForNotifications(1)):
            break
        else: 
            continue

    while(sum(blunoHandshake) != len(blunoHandshake)):
        time.sleep(3)
    startTime = time.time()
    dcStart = 0.0
    while True:
        try:
            if(p.waitForNotifications(1)):
                dcStart = 0.0
           # else:
         #     if dataFlag == 1:
         #         ackData(serviceChara)
         #         print("ack")
         #           dataFlag = 0
            else:
                dcCurr = time.time()
                if dcCurr - dcStart >= 3:
                    p.disconnect()
                    reconnect(blunoAddr,index)
                else:
                    pass
            continue
        except:
            print("Bluno " + str(index) + " has disconnected. Attempting to reconnect...")
            p.disconnect()
            break
    reconnect(blunoAddr,index)

def reconnect(blunoAddr,index):
    #global dataFlag
    #dataFlag = 1
    while True:
        try:
            run(blunoAddr,index)
            break
        except:
            print("Failed to reconnect Bluno " + str(index) + ", retrying...")
            continue
        
def initHandshake(serviceChara):
    serviceChara.write(bytes("H","utf-8"))
    
def ackData(serviceChara):
    serviceChara.write(bytes("R","utf-8"))

class centralDev(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    ultra96 = centralDev()
    index = 0
    with ThreadPoolExecutor(max_workers=3) as executor:
        for bluno in blunoAddress:
            executor.submit(run,bluno,index)
            index += 1
        
            


# In[1]:




