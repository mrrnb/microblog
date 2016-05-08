import MySQLdb


def get_conn():
    host = '127.0.0.1'
    port = 3306
    db = 'jikexueyuan'
    user = 'root'
    password = '123456'
    conn = MySQLdb.connect(host=host,
                           user=user,
                           passwd=password,
                           db=db,
                           port=port,
                           charset='utf8')
    return conn


class User(object):
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    def save(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = 'insert into user (user_id, user_name) VALUES (%s, %s)'
        cur.execute(self.user_id,self.user_name)
        conn.commit()
        cur.close()
        conn.close()