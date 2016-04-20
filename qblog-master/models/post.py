#-*- coding:utf8 -*-
__author__ = 'qiqi'
from sqlalchemy.schema import Column
from application import app,db

class Post(db.Model):
    __tablename__ = 'post'

    id = Column(db.Integer, primary_key=True,autoincrement=True)    #博文ID
    cateid = Column(db.SmallInteger,nullable=False,server_default='0')    #分类ID
    uid = Column(db.Integer,db.ForeignKey('user.id'))    #作者ID
    tag = Column(db.String(255),index=True)    #标签
    status = Column(db.SmallInteger,nullable=False,index=False,server_default='0')  #显示状态 0:正常显示 1:个人可见 2.草稿箱 3.审核
    istop = Column(db.SmallInteger,server_default='0') #是否置顶 0：不置顶 1：置顶第一 2：置顶第二 3：置顶第三 ……
    islock = Column(db.SmallInteger,server_default='0') #是否允许评论 0:允许 1:不允许
    title = Column(db.String(100),index=True)    #标题
    description = Column(db.Text)   #描述
    content = Column(db.Text)   #内容
    commnums =Column(db.Integer,server_default='0')   #回复数量
    viewnums =Column(db.Integer,server_default='0')   #访问数量
    updated = Column(db.DateTime, nullable=False,server_default='0000-00-00 00:00:00')   #更新时间

    def __repr__(self):
        return '<Posts %r>' % (self.title)