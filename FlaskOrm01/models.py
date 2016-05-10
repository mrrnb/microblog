import MySQLdb
from application import db

# def get_conn():
#     host = '192.168.66.100'
#     port = 3306
#     db = 'jike'
#     user = 'root'
#     password = '123'
#     conn = MySQLdb.connect(host=host,
#                            user=user,
#                            passwd=password,
#                            db=db,
#                            port=port,
#                            charset='utf8')
#     return conn


# class User(object):
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)

    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    # def save(self):
    #     conn = get_conn()
    #     cur = conn.cursor()
    #     sql = 'insert into user (id, name) VALUES (%s,%s)'
    #     cur.execute(sql,(self.user_id,self.user_name))
    #     conn.commit()
    #     cur.close()
    #     conn.close()
    #
    # @staticmethod
    # def query_all():
    #     conn = get_conn()
    #     cur = conn.cursor()
    #     sql = "select * from user"
    #     cur.execute(sql)
    #     rows = cur.fetchall()
    #     users = []
    #     for r in rows:
    #         user = User(r[0],r[1])
    #         users.append(user)
    #     conn.commit()
    #     cur.close()
    #     conn.close()
    #     return users
    #
    def __str__(self):
        return "id : {}  --  name : {}".format(self.user_id, self.user_name)