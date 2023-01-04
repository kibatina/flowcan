import threading
TIMESTAMP_MAX=4294967295

class Item (object):
    def __init__(self, data):
        self.data = data
        #self.timestamp_value=conv_hexStr_to_integer(data[0])
        #self.timestamp_diff_from_prev = 0
        self.next = None
    
    def setTimestampDiffFromPrev(self,diffVal):
        self.timestamp_diff_from_prev=diffVal
    
    def getTimestampDiffFromPrev(self):
        return self.timestamp_diff_from_prev
    
    def getData(self):
        return self.data
        
class RwQueue(object):
    def __init__(self, maxLength):
        self.whead = None #写访问的头, 固定指向只一个item
        self.rhead = None #读访问的头, reset后指向whead,然后不停的往后移动.
        self.tail = None  #write的时候使用,tail.next用来指向下一个,然后tail移动到下一个.靠whead来记录链表头部.  
        self.length = 0
        self.maxLength = maxLength #容量

        self.clearFlag = False #是否正在被清空
        self.lock = threading.RLock()
    
    def getLength(self):
        return self.length

    def push(self,data):
        if self.clearFlag:
            return
        self.lock.acquire()
        item = None
        try:
            item = Item(data)
        except ValueError:
            print("[error]rwQueue.push:hex转换出错,原始字符串:",data)
            return
        
        if self.whead==None:
            self.whead=item            
        else:
            self.tail.next=item
            #prev_timestamp_value=self.tail.timestamp_value
            #timestampDiff=(item.timestamp_value-prev_timestamp_value)%TIMESTAMP_MAX
            #print("[debug]: timestampDiff", timestampDiff)
            #item.setTimestampDiffFromPrev(timestampDiff)
        self.tail=item   
        self.length+=1
        if self.length > self.maxLength:
            self.whead = self.whead.next
            self.length-=1
        self.lock.release()
                    
    def resetRead(self):
        self.rhead = self.whead
    
    def readHead(self):
        if self.rhead == None or self.clearFlag:
            return None
        resultItem = self.rhead
        self.rhead = self.rhead.next
        return resultItem
    
    def clear(self):
        self.clearFlag = True
        self.lock.acquire()
        head = self.whead
        while head!=None: #此处遍历是为了保证链表里面的对象引用计数为0, gc能够进行,避免内存泄漏
            next = head.next
            head.next = None
            head = next
        self.whead = None #写访问的头
        self.rhead = None #读访问的头
        self.tail = None
        self.length = 0
        
        self.lock.release()
        self.clearFlag = False
        
   
def conv_hexStr_to_integer(hexStr):
    return int((hexStr),16)