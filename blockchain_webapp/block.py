#Pawel Pietrzak s18793

#!/usr/bin/python
# -*- coding: utf-8 -*-

from hashlib import sha256, sha512
import time
import datetime
from blockchain import *
from sql import *
from sqltransfer import *
def updatehash(*values):
    text = ""; t =sha256()
    for value in values:
        text += str(value)

    t.update(text.encode('utf-8'))
    return t.hexdigest()

class PosBlock(object):
    """docstring for PosBlock."""

    def __init__(self, arg):
        super(PosBlock, self).__init__()
        self.arg = arg



class OneBlock(object):
    """docstring for oneBlock."""
    #hash = None
    #nonce = 0
    #data = None
    #hash_before = 64*"0"
    #timeS = time.time()
    #timeStamp = datetime.datetime.now()


    def __init__(self,num=0, hash_before=64*"0",arg=None, nonce =0,timeStamp=datetime.datetime.now()):
        self.num = num
        self.arg = arg
        self.hash_before = hash_before
        self.nonce = nonce
        self.timeStamp = timeStamp

    def hash(self):
        return updatehash(
            self.hash_before,
            self.num,
            self.arg,
            self.nonce,
            self.timeStamp)

    def getHash(self):
        return self.hash()

    def getbhash(self):
        return self.hash_before

    def printNonce(self):
        return str("Block number %s ,Nonce: %s"%(self.num,self.nonce))

    def __str__(self):
        return str("Block_Number#: %s\nHash: %s\nHash_Before: %s\nData_in_block: %s\nNonce: %s\nTime: %s\n"%(
            self.num,
            self.hash(),
            self.hash_before,
            self.arg,
            self.nonce,
            self.timeStamp
            )
        )
    def gettime(self):
        return self.timeStamp

    def getnonce(self):
        return self.nonce
