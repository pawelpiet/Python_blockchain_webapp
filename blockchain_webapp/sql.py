from app import *
from blockchain import *
from sqltransfer import *
from bitcoin import *
import time
import datetime


class Table():
    def __init__(self, table_name, *args):
        self.table=table_name
        self.columns="(%s)" %",".join(args)
        self.colList=args

        if table_check(table_name):
            newdata=""
            for col in self.colList:
                newdata = newdata + "%s varchar(255)," %col

            cursor= mysql.connection.cursor()
            print("create table %s(%s)" %(self.table, newdata[:len(newdata)-1]))
            cursor.execute("create table %s(%s)" %(self.table, newdata[:len(newdata)-1]))
            cursor.close()

    #sciąganie rekordów z DB.

    def select_one(self, where, arg):
        value ={}
        sel="Select * from %s where %s = \"%s\""
        cursor = mysql.connection.cursor()
        ask = cursor.execute(sel %(self.table,where,arg))
        a = ask
        if ask>0:
            value = cursor.fetchone()
        cursor.close()
        return value

    def select_all(self):
        sel="Select * from %s"
        cursor=mysql.connection.cursor()
        ask = cursor.execute(sel %self.table)
        value = cursor.fetchall()
        return value

    #wprowadzanie nowych danych do taabeli

    def insert_one(self, *args):
        values="";
        ins = "insert into %s%s values(%s)"
        for a in args:
            values = values+("\"%s\"," %(a))
        cursor= mysql.connection.cursor();cursor.execute(ins %(self.table,self.columns, values[:len(values)-1]))
        mysql.connection.commit(); cursor.close()
    #usuwanie
    def delete_all(self):
        self.drop_table(); self.__init__(self.table, *self.colList)

    def delete_one(self, where, arg):
        dele = "Delete from %s where %s = \"%s\""
        cursor=mysql.connection.cursor(); cursor.execute(dele %(self.table,where,arg))
        mysql.connection.commit()
        cursor.close()
    def drop_table(self):
        drop = "drop table %s"
        cursor=mysql.connection.cursor(); cursor.execute(drop %self.table); cursor.close()


def select_spec(what,where):
    sel="select %s from %s"
    cursor=mysql.connection.cursor()
    ask = cursor.execute(sel %(what,where))
    value = cursor.fetchall()
    return value

def select(where):
    sel="select * from %s"
    cursor=mysql.connection.cursor()
    ask = cursor.execute(sel %where)
    value = cursor.fetchall()
    return value

def drop_spec(what):
    drop = "drop table %s"
    cursor=mysql.connection.cursor(); cursor.execute(drop %what)
    cursor.close()

######################-Tables Helpers-############################

def tabelBC():
    bc = Table("blockchain","num","hash","beforehash","data","nonce","time")
    return bc

def tabelUS():
    us = Table("users","name","username","useremail","password")
    return us

def tabelAdd():
    us = Table("wallet","address","private","public")
    return us

##################################################################

def showTables():
    cursor= mysql.connection.cursor()

    a = cursor.execute("show tables")
    print(a)
    cursor.close()

def makeBlockchain():
    bc = Blockchain()
    sqlb= tabelBC()
    for i in sqlb.select_all():
        bc.add_block(OneBlock(int(i.get('num')),i.get('beforehash'),i.get('data'),int(i.get('nonce')),i.get('time')))
    return bc

def updateBlockchain(bc):
    sqlb=tabelBC()
    sqlb.delete_all()
    #times = datatime.now()
    for i in bc.chain:
        sqlb.insert_one(str(i.num), i.getHash(), i.hash_before,i.arg,i.nonce,i.timeStamp)
def transfercoins(giver,receiver,coin):
    coin = float(coin)
    if saldo(giver) < coin and giver != 'Credit Card':
        raise Exception("User do not have enought coins")
    elif giver == receiver:
        raise Exception("Wrong receiver username")
    elif check_if_new_user(receiver):
        raise Exception("There is no souch a user")
    bc = makeBlockchain(); n=len(bc.chain)+1
    info="%s--%s--%s" %(giver,receiver,coin)
    bc.mine_block(OneBlock(n,arg = info)); updateBlockchain(bc)


def buyByCard(receiver,coin):
    coin = float(coin)
    giver = 'Credit Card'

    if coin <= 0.00:
        raise Exception("Amount of coin can not be 0.000")

    bc = makeBlockchain();
    n=len(bc.chain)+1
    info="%s--%s--%s" %(giver,receiver,coin)
    bc.mine_block(OneBlock(n,arg = info)); updateBlockchain(bc)



def getAll_trans():
    bc= makeBlockchain().chain

    return bc

def saldo(uname):
    saldo=0.00; bc=makeBlockchain()
    for oneblock in bc.chain:
        info=oneblock.arg.split("--")
        if uname == info[1]:
            saldo = saldo + float(info[2])
        elif uname == info[0]:
            saldo = saldo - float(info[2])
    return saldo

def table_check(tName):
    cursor = mysql.connection.cursor()
    try:
        res = cursor.execute("Select * from %s" %tName)
    except:
        return True
    else:
        return False

def custom_ask(ask):
    cursor = mysql.connection.cursor(); cursor.execute(ask)
    mysql.connection.commit(); cursor.close()

def check_if_new_user(username):
    holders = tabelUS()
    allHolders = holders.select_all()
    unames= [holder.get('username') for holder in allHolders]
    return False if username in unames else True

def getAdress():

    tables = tabelAdd()
    ofile= open('bitcoinWallet.txt','w')

    private = random_key()
    public = privtopub(private)
    address = pubtoaddr(public)

    tables.insert_one(address,private,public)

    print('Address is: '+address)
    print('Private key is: '+private)
    print('Public key is: '+public)

    ofile.write('Address = ' + address)
    ofile.write('Priv_key = ' + private)
    ofile.write('Pub_key = ' + public)

    ofile.close()
