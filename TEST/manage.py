# coding: utf-8

from flask_script import Manager
from application import app
from models import User

manager = Manager(app)


@manager.command
def save():
    user = User(1,'jiekxueyuan')
    user.save()
@manager.command
def query_all():
    pass

if __name__=='__main__':
    manager.run()