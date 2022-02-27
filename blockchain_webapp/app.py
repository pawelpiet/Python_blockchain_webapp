#!/usr/bin/python
# -*- coding: utf-8 -*-
from wtforms import StringField, Form, DecimalField, IntegerField, TextAreaField, PasswordField,validators
from flask import Flask, flash, url_for, request, logging, session, redirect, render_template
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL

from sql import *
from sqltransfer import *
from blockchain import *
from cryptos import *
from wallet import *

#from userforms import *

from functools import wraps
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'crypto'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'



mysql=MySQL(app)






@app.route("/register", methods =['GET','POST'])
def register():
    form=FormToReg(request.form)
    users = Table("users", "name", "username","useremail","password")
    print('1')
    if request.method == 'POST' and form.validate():
        print('2')
        fullname=form.name.data
        uname=form.username.data
        uemail=form.useremail.data
        print('3')
        if check_if_new_user(uname):
            upass=sha256_crypt.encrypt(form.password.data)
            users.insert_one(fullname,uname,uemail,upass)
            user_logged(uname)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('register'))

    return render_template('reg.html', form = form)


def check_login(p):
    @wraps(p)
    def wrap(*a,**b):
        if 'logged_in' in session:
            print('---logged in-----')
            return p(*a,**b)
        else:
            print('---access denied---')
            return redirect(url_for('login'))
    return wrap


@app.route("/home",methods =['GET','POST'])
@check_login
def home():
    c = giveCryptos()
    s = session.get('username')
    sal= saldo(s)
    bc = getAll_trans()
    select = select_spec("username","users")
    print(select)

    return render_template('home.html',session=session,s=s, sal=sal,btc=c[1],bc=bc)

def user_logged(username):
    users = Table("users", "name", "username","useremail","password")
    oneuser=users.select_one("username",username)
    session['logged_in']=True
    session['username']=username
    session['name']=oneuser.get('name')
    session['useremail']= oneuser.get('useremail')

@app.route("/login",methods=['POST','GET'])
def login():
    if 'POST'==request.method:

        uname=request.form['username']
        userinput=request.form['password']
        users = Table("users", "name", "username","useremail","password")
        u=users.select_one("username",uname)

        #tests= users.select_all();
        #print(tests)
        #print(u.get('username'))
        correctpass=u.get('password')
        print(correctpass)
        print(userinput)
        print(uname)
        if correctpass is None:
            print('No user like this')
            return redirect(url_for('login'))
        else:
            if sha256_crypt.verify(userinput,correctpass):
                user_logged(uname)
                print('you are logged')
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
    return render_template('log.html')
@app.route("/logout")
def user_logout():
    session.clear()
    print('logout')
    return redirect(url_for('login'))


@app.route("/transfer", methods=['POST','GET'])
@check_login
def transfer():
    f=FormToTransfer(request.form)
    s = saldo(session.get('username'))
    print(s)
    if request.method == 'POST':
        transfercoins(session.get('username'), f.username.data,f.value.data)
        print(f.username.data)

    return render_template('transfer.html',s=s, form=f)


@app.route("/about")
@check_login
def about():
    return render_template('about.html')



@app.route("/buy", methods=['POST','GET'])
@check_login
def byCard():
    f = FormToCard(request.form)
    s = saldo(session.get('username'))
    print(s)
    if request.method == 'POST':
        buyByCard(session.get('username'), f.value.data)


    return render_template('cardpurchase.html',s = s, form=f)

@app.route("/nft", methods=['POST','GET'])
@check_login
def nft():
    return render_template('nft.html')


@app.route("/")
def index():

    #transfercoins("bank","kowal",200)
    #users = Table("users","name","username","useremail","password")
    #users.insert_one("Kajo kat","kk","kk@gmail.com","kajo") fadgadsesssdqwsdassds

    return render_template('index.html')



@app.route('/my-link/')
def my_link():
  getAdress()
  return redirect(url_for('home'))


@app.route("/welcome")
def welcome():
    showTables()
    c = giveCryptos()

    return render_template('welcome.html',c=c)


class FormToCard(Form):
    """docstring for FormToCard."""
    fullname=StringField('Enter your full name',[validators.Length(min=2,max=80)])
    cardnum=StringField('Enter amount of coins',[validators.Length(min=16,max=16)])
    cardsec=StringField('Enter CVV number',[validators.Length(min=3,max=4)])
    carddat=StringField('Enter date of exprience',[validators.Length(min=5,max=6)])
    value=StringField('Enter amount of coins',[validators.Length(min=1,max=30)])
class FormToReg(Form):
    """docstring for FormToReg."""
    name=StringField('Enter your name & surname',[validators.Length(min=1,max=70)])
    username=StringField('Enter username you want to use',[validators.Length(min=1,max=50)])
    useremail=StringField('Enter your emial address',[validators.Length(min=1,max=50)])
    password=PasswordField('Enter your password',[validators.DataRequired(),validators.Length(min=6,max=64), validators.EqualTo('conf', message='Wrong password with another')])
    conf=PasswordField('Check password is correct')
class FormToTransfer(Form):
    """docstring for FormToLog."""
    username=StringField('Enter username',[validators.Length(min=1,max=30)])
    value=StringField('Enter amount of coins',[validators.Length(min=1,max=30)])


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run( debug = True)
