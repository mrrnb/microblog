#-*-coding:utf-8-*-
from flask import Flask,Blueprint,request,make_response,redirect,url_for,abort,render_template,session
from flask.ext.script import Manager
# from flask.ext.moment import Moment
from application import app
from flask_login import current_user
from models.post import Post
from models.user import User
from datetime import datetime

indexBp = Blueprint('indexBp',__name__)

# class NameForm(Form):
#     name = StringField('sdfsdf?',validators=[DataRequired()])
#     submit = SubmitField('Submit')

@indexBp.route('/',methods=['GET','POST'])
def index():
    posts = Post.query.all()
    datas = []
    for post in posts:
        if post.status == 0:
            user = User.query.filter(User.id == post.uid).first()
            cn_name = user_get_cnname(user)
            #   判断文章是否结束
            if len(post.content) > 151:
                content = post.content[:150]
                over = 0
            else:
                content = post.content
                over = 1
            data = {
                "id":post.id,
                "title":post.title,
                "content":content,
                "over":over,
                "username":cn_name,
                "status":post.status,
                "updated":post.updated
            }
            datas.append(data)
    # datas = []
    return render_template('index.html',datas=datas)

@indexBp.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    if post:
        user = User.query.filter(User.id == post.uid).first()
        if post.status == 0 or user == current_user:
            cn_name = user_get_cnname(user)
            data = {
                "title":post.title,
                "content":post.content,
                "username":cn_name,
                "status":post.status,
                "updated":post.updated
            }
            return render_template('post.html',data=data)
    return redirect(url_for('indexBp.index'))

def user_get_cnname(user):
    if user:
        return user.cn_name
    else:
        return "匿名"



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500