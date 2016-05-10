# coding: utf-8

from flask_script import Manager
from application import app,db
from models import User

manager = Manager(app)


@manager.command
def save():
    # user = User(1,'jikex')
    # user.save()
    user = User(2,'jike2')
    db.session.add(user)
    db.session.commit()

@manager.command
def query_all():
    # users = User.query_all()
    users = User.query.all()
    for u in users:
        print u

if __name__=='__main__':
    manager.run()