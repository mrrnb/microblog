#-*- coding:utf8 -*-
__author__ = 'qiqi'

from application import app,db,lm
from flask import Blueprint,request,redirect,render_template,g,url_for,session,flash,jsonify
from flask_login import login_user,logout_user,current_user,login_required
from sqlalchemy import and_
from models import User
import json
userBp = Blueprint('userBp',__name__)

@lm.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()

@userBp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(request.args.get("next") or url_for("indexBp.index"))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        remember_me = request.form['remember_me']
        user = User.query.filter(and_(User.name == username,User.status==0)).first()
        res = {}
        if user:
            if user.verify_password(password):
                if login_user(user):
                    res['code'] = 0 #登陆成功
                    user.ip = request.remote_addr
                    db.session.commit()
                    next = request.args.get('next')
                    if next_is_valid(next):
                        res['next_page'] = next
                else:
                    res['code'] = 1 #账户被禁用
            else:
                res['code'] = 2 #密码错误
        else:
            res['code'] = 3 #未找到该账户
        return jsonify(res)
    return render_template("login.html")

def next_is_valid(next):
    return True

@userBp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("indexBp.index"))