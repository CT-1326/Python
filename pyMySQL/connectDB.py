import pymysql.cursors
import os
from dotenv import load_dotenv
load_dotenv()

connection = pymysql.connect(
    host=os.environ.get('HOST'),
    user=os.environ.get('USER'),
    password=os.environ.get('PASSWORD'),
    db=os.environ.get('DB')
)

with connection:
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM users'
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
