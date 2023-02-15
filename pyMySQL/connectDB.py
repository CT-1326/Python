import pymysql.cursors
import os
from dotenv import load_dotenv
load_dotenv()

connection = pymysql.connect(
    host=os.environ.get('HOST'),
    user=os.environ.get('USER'),
    password=os.environ.get('PASSWORD'),
    db=os.environ.get('DB'),
    cursorclass=pymysql.cursors.DictCursor,
)
cursor = connection.cursor()
print('DB init success!')
sql = 'SELECT * FROM users WHERE id = %s'


def get():
    # print(name, type(name))
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()


def getUser(name):
    # print(name, type(name))
    cursor.execute(sql, (name))
    return cursor.fetchone()


def postUser(id, password, email):
    cursor.execute(sql, (id))

    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO users VALUES(default, %s, %s, %s)",
                       (id, password, email))
        connection.commit()
        return 'Done'
    else:
        return 'Already have user!'
