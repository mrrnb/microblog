#coding:utf-8
from flask import render_template, flash, redirect

from app import app
from .forms import LoginForm
from xszb import xs
from xszb.login1 import Baidu

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Ezreal' } # fake user
    name = '绝色俏王妃'
    username = 'mingruirui'
    password = 'bdszjszrj,2015'
    baidu = Baidu(username, password)
    baidu.login()
    name_gbk = name.decode('utf-8').encode('gbk')
    zhang = 5
    xxx = xs.get_urls(name)
    li = xs.get_content(xxx, zhang)
    # li2 = []
    length = len(li[0])
    # for p in range(len(li[0])):
    #     li2.append(li[0][p]+'</br>'+li[1][p]+'')
    if li != [[],[]]:
        return render_template("index.html",
            title = 'Blog',
            user = user,
            li1 = li[1],
            li0 = li[0],
            length = length,
            name = name)
    else:
        return "Can not get this one!"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = { 'nickname': 'Ezreal' } # fake user
        # name = '医道生香'
        name = form.xsname.data
        name_gbk = name.decode('utf-8').encode('gbk')
        zhang = 1000
        xxx = xs.get_urls(name)
        li = xs.get_content(xxx, zhang)
        length = len(li[0])

        if li != [[],[]]:
            return render_template("index.html",
            title = 'Blog',
            user = user,
            li1 = li[1],
            li0 = li[0],
            length = length,
            name = name)
        else:
            return "Can not get this one!"
    return render_template('login.html',
    title = 'Sign In',
    form = form)
