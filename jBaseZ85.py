#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : shpik (shpik.korea at gmail.com)


class jBaseZ85:
    _ALPHA = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"
    _RALPHA = [
        68,0,84,83,82,72,0,75,76,70,65,0,63,62,
        69,0,1,2,3,4,5,6,7,8,9,64,0,73,66,74,71,
        81,36,37,38,39,40,41,42,43,44,45,46,47,
        48,49,50,51,52,53,54,55,56,57,58,59,60,61,
        77,0,78,67,0,0,10,11,12,13,14,15,16,17,18,
        19,20,21,22,23,24,25,26,27,28,29,30,31,32,
        33,34,35,79,0,80 
    ];
    _RALSHIFT = 33

    def __init__(self, inp):
        self.data = inp

    def encQuater(self,data):
        value = 0
        for i in range(4):
            value |= (data[i]&0xFF) << (i*8)
        out = []
        magic = [0x31C84B1,0x95EED,0x1C39, 0x55, 1]
        for i in range(len(magic)):
            out.append( self._ALPHA[(value/magic[i])%85] )
        return out

    def encode(self):
        data = self.data
        length = len(self.data)
        index = 0
        buf = [0 for _ in range(4)]
        enc_data = []

        while length >= 4:
            buf[3] = ord(data[index])
            index +=1
            buf[2] = ord(data[index])
            index +=1
            buf[1] = ord(data[index])
            index +=1
            buf[0] = ord(data[index])
            index +=1
            tmpBuf = self.encQuater(buf)
            for i in tmpBuf:
                enc_data.append(i)
            length -= 4

        # if length is not zero, then it is padded by encPad funcion.
        if length > 0:
            buf = [0 for _ in range(length)]
            for i in range(length,0,-1):
                buf[i-1] = ord(data[index])
                index += 1
            tmpBuf = self.encPad(buf)
            for i in tmpBuf:
                enc_data.append(i)
        return ''.join(enc_data)

    def encPad(self, data):
        value = 0
        out = [0 for i in range(len(data)+1)]
        magic = [0x31C84B1,0x95EED,0x1C39, 0x55, 1]

        if len(data) == 3:
            value |= (data[2]&0xFF) << 16
            value |= (data[1]&0xFF) << 8
        elif len(data) == 2:
            value |= (data[1]&0xFF) << 8
        
        value |= (data[0]&0xFF)
        if len(data) == 3:
            out[3] = self._ALPHA[(value/magic[1])%85]
            out[2] = self._ALPHA[(value/magic[2])%85]
        elif len(data) == 2:
            out[2] = self._ALPHA[(value/magic[2])%85]
        
        out[1] = self._ALPHA[(value/magic[3])%85]
        out[0] = self._ALPHA[(value/magic[4])%85]

        return out

    def decode(self):
        data = self.data
        length = len(self.data)
        index = 0
        buf = [0 for _ in range(5)]
        dec_data = []

        while length >= 5:
            for i in range(5):
                buf[i] = ord(data[index+i])
            index += 5
            length -= 5
            tmpBuf = self.decQuater(buf)
            for i in tmpBuf:
                dec_data.append(i)
        
        if length > 0:
            buf = [0 for _ in range(length)]
            for i in range(length):
                buf[i] = ord(data[index])
                index += 1
            tmpBuf = self.decPad(buf)
            for i in tmpBuf:
                dec_data.append(i)
            
        return ''.join(dec_data)

    def decQuater(self,data):
        magic = [0x31C84B1,0x95EED,0x1C39, 0x55, 1]
        out = []
        value = 0
        for i in range(len(magic)):
            value += self._RALPHA[data[i] - self._RALSHIFT] * magic[i]

        for i in range(4):
            out.append(chr((value>>((3-i)*8))&0xFF))
        
        return out
    
    def decPad(self,data):
        magic = [0x31C84B1,0x95EED,0x1C39, 0x55, 1]
        out = [0 for _ in range(len(data)-1)]
        value = 0
        if len(data) == 4:
            value += self._RALPHA[data[3]-self._RALSHIFT] * magic[1]
            value += self._RALPHA[data[2]-self._RALSHIFT] * magic[2]
            value += self._RALPHA[data[1]-self._RALSHIFT] * magic[3]
        elif len(data) == 3:
            value += self._RALPHA[data[2]-self._RALSHIFT] * magic[2]
            value += self._RALPHA[data[1]-self._RALSHIFT] * magic[3]
        elif len(data) == 2:
            value += self._RALPHA[data[1]-self._RALSHIFT] * magic[3]
        value += self._RALPHA[data[0]-self._RALSHIFT] * magic[4]
        for i in range(len(data)-1):
            out[i] = chr((value >> (8*(len(data)-i-2)))&0xFF)
        return out

if __name__=="__main__":
    s = 'hello, shpik'
    enc = jBaseZ85(s).encode()
    print 'original : ',s
    print 'encode : ',enc
    print 'decode : ',jBaseZ85(enc).decode()
