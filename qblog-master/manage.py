#-*- coding:utf8 -*-
__author__ = 'qiqi'

from application import app
from flask.ext.script import Manager
from flask.ext.script import Server


import blueprint

manager = Manager(app)
manager.add_command('runserver',Server(host=app.config.get('HOST'), port=app.config.get('SERVER_PORT'), use_debugger=app.config.get('DEBUG')))

@manager.command
def create_data():
    with app.app_context():
        from application import db
        import models
        db.create_all()

@manager.command
def encrypt():
    from werkzeug.security import generate_password_hash
    hash_password = generate_password_hash('sdfsdf')
    print hash_password

if __name__ == '__main__':
    manager.run()