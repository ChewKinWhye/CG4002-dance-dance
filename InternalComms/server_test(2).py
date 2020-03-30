
# coding: utf-8

# In[1]:


from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEException, BTLEDisconnectError
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import os
import sys
import random
import socket
import base64
import numpy as np
from Crypto.Cipher import AES
from Crypto import Random
from random import seed
from random import choice
import pymongo
import datetime
import numpy as np

client = pymongo.MongoClient("mongodb+srv://dbdance_user:dbdance_user@cluster0-axu0z.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client['dashboard-db']

db_sensors = db.sensors
db_predictions = db.predictions

blunoAddress = ['78:DB:2F:BF:37:F5', '50:65:83:6F:6C:B5','78:DB:2F:BF:34:3B']
#, ,
POSITIONS = ['1 2 3', '3 2 1', '2 3 1', '3 1 2', '1 3 2', '2 1 3']
ACTIONS = ['muscle', 'weightlifting', 'shoutout', 'dumbbells', 'tornado', 'facewipe', 'pacman', 'shootingstar']
SYNCDELAY = [ '1.56', '2.23', '3.12', '4.78' ]

# msg = ''
blunoHandshake = [0,0,0]
index = 1
startTime = 0
connectionThreads = []
entryFlag = 1
dataFlag = 0
data_circular_array = np.zeros((3, 12, 3))
insert_pointer = np.array([0, 0, 0])
data_insert_counter = 0

class Encryptor:
    def __init__(self, key):
        self.key = key
        
    def pad(self, s):
        return s + '\0' * (AES.block_size - len(s) % AES.block_size)
        
    def encrypt(self, message, key, key_size = 256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encoded = base64.b64encode(iv + cipher.encrypt(message))
        return encoded
        
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
        elif blunoHandshake[self.index] == 1:
#             print(data)
            self.handleData(data)
        else:
            pass

    def handleData(self,data):
        global entryFlag
        global dataFlag
        global index
        global startTime
        global enc
        global data_circular_array
        global insert_pointer
        global data_insert_counter
        
#         global msg
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
                temp_array = self.orderedStr.split(" ")
                sensor_to_send = {
                    "dancerId": self.index + 1,
                    "sensorAX": float(temp_array[0])/100,
                    "sensorAY": float(temp_array[1])/100,
                    "sensorAZ": float(temp_array[2])/100,
                    "date": datetime.datetime.utcnow()     
                }
                db_sensors.insert_one(sensor_to_send)

                data_to_append = np.array([float(temp_array[0])/100, float(temp_array[1])/100
                                               , float(temp_array[2])/100])
                data_circular_array[self.index][insert_pointer[self.index]] = data_to_append
                data_insert_counter += 1
                insert_pointer[self.index] = (insert_pointer[self.index] + 1) % 12       
                
                if data_insert_counter == 6:
                    data_insert_counter = 0
                    data_feature_extraction = np.zeros((12, 3))
                    for i in range(12):
                        data_feature_extraction[i] = data_circular_array[self.index][insert_pointer[self.index] + i]
                    
                    # Call feature extaction
                    # Pass through model
                    position = choice(POSITIONS)
                    action = choice(ACTIONS)
                    sync_delay = choice(SYNCDELAY)
                    message = '#' + position + '|' + action + '|' + sync_delay + '|'
                    print('Unencrypted message: ' + message)
                    encoded = enc.encrypt(message, enc.key)
                    print('---Sending message---')
                    sock.sendall(encoded)
    #                 while True:
                    try:
                        msg = sock.recv(1024)
                    except socket.timeout as e:
                        err = e.args[0]
                        # this next if/else is a bit redundant, but illustrates how the
                        # timeout exception is setup
                        if err == 'timed out':
    #                             sleep(1)
                            print('recv timed out, retry later')
    #                         continue
                        else:
                            print(e)
    #                             sys.exit(1)
                    except socket.error as e:
                        # Something else happened, handle error, exit, etc.
                        print(e)
    #                         sys.exit(1)
                    else:
                        if len(msg) == 0:
                            print('orderly shutdown on server end')
    #                             sys.exit(0)
                        else:
                            print('New positions received: ' + str(msg))                
                
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
    #dcStart = 0.0
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
#     global msg
    global enc
    ultra96 = centralDev()
    index = 0
    
    seed(1)

    ip_addr = "192.168.43.159"
    port_num = 1234
    
#     msg = ''
    enc = Encryptor('1234567812345678');
    
    # connect to evaluation server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip_addr, port_num)
    sock.connect(server_address)  
    sock.setblocking(False)
    
    time.sleep(10)
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        for bluno in blunoAddress:
            executor.submit(run,bluno,index)
            index += 1       


