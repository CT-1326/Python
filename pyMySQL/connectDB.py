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


def getUsers():
    # print(id, type(id))
    cursor.execute('SELECT * FROM users')
    connection.commit()
    return cursor.fetchall()


def getUser(id):
    # print(id, type(id))
    cursor.execute(sql, (id))
    connection.commit()
    return cursor.fetchone()


def postUser(id, password, email):
    cursor.execute(sql, (id))

    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO users VALUES(default, %s, %s, %s)",
                       (id, password, email))
        connection.commit()
        return 'Add Done'
    else:
        return 'Already have user!'


def putUser(id, new_id, password, email):
    cursor.execute(sql, (id))

    if cursor.rowcount != 0:
        cursor.execute("UPDATE users SET id = %s, password = %s, email = %s WHERE id = %s",
                       (new_id, password, email, id))
        connection.commit()
        return 'Update Done'
    else:
        return 'No have user!'


def delUser(id):
    cursor.execute(sql, (id))

    if cursor.rowcount != 0:
        cursor.execute("DELETE FROM users WHERE id = %s", id)
        connection.commit()
        return 'Delete Done'
    else:
        return 'No have user!'
