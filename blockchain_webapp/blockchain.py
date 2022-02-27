#Pawel Pietrzak s18793

#!/usr/bin/python
# -*- coding: utf-8 -*-
from block import *
from hashlib import sha256, sha512
import time
import datetime
from sql import *
from sqltransfer import *





class Blockchain():
    dif = 2
    nNon = dif * "0"
    timeStamp = datetime.datetime.now()
    def __init__(self):
        self.chain=[]

    def add_block(self,oneblock):
        self.chain.append(oneblock)

    def mine_block(self,oneblock):
        try: oneblock.hash_before=self.chain[-1].hash()
        except IndexError: pass
        while True:
            if oneblock.hash()[:2] == "0" * self.dif:
                self.add_block(oneblock); break
            else:
                oneblock.nonce += 1
                print(oneblock.nonce)

    def remove_block(self,oneblock):
        self.chain.remove(oneblock)

    def isValidBlockchain(self):
        for b in range(1,len(self.chain)):
            #if(b>1)
            previous = self.chain[b-1].hash()
            now = self.chain[b].hash_before
            if previous[:self.dif] != 2*"0" or now != previous:
                return False
        return True


    def last_block(self):
        return self.chain[-1]

def main():
    pass
if __name__ == '__main__':
    main()
