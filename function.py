import struct
import sys
import time
import array
import csv
import math

class Function (object):
    def __init__(self):
        self.sdoDataStr = ''
        pass

    #def decStrToHexBytes(self,decstr):
        #tempstr = (str(hex(int(decstr,10))).replace('0x','')).zfill(8)
        #self.sdoDataStr = tempstr[-2:]+tempstr[-4:-2]+tempstr[-6:-4]+tempstr[-8:-6]
        #pass
    #def decStrToHexBytes(self,decstr):
        #canopen是高byte先发送,所以为little.
        #self.sdoDataStr = str((int.to_bytes(int(decstr,10),length=4,byteorder='little',signed=True)).hex())
        #return self.sdoDataStr
        #pass
    def decToHexBytes(self,dec,len):
        #canopen是高byte先发送,所以为little.
        self.sdoDataStr = (str((int.to_bytes(dec,length=len,byteorder='little',signed=True)).hex())).ljust(8,'0')
        return self.sdoDataStr
        pass 
    def decStrToHexBytes(self,decstr,len):
        #canopen是高byte先发送,所以为little.
        try:
            self.sdoDataStr = (str((int.to_bytes(int(decstr,10),length=len,byteorder='little',signed=True)).hex())).ljust(8,'0')
        except:
            self.sdoDataStr = (str((int.to_bytes(int(decstr,10),length=len,byteorder='little',signed=False)).hex())).ljust(8,'0')
        return self.sdoDataStr
        pass
    def hexStrToHexBytes(self,hexstr):
        tempstr = hexstr.zfill(8)
        self.sdoDataStr =tempstr[-2:]+tempstr[-4:-2]+tempstr[-6:-4]+tempstr[-8:-6]
        return self.sdoDataStr
        pass  
    def getSdoDataStr(self):
        return self.sdoDataStr  
        pass
    



    

    