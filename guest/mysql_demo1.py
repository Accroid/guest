#需要下载mysql，下载地址https://cdn.mysql.com/archives/mysql-installer/mysql-installer-community-5.5.27.2.msi
import pymysql

db = pymysql.connect(
    # host = 'localhost',
    host='127.0.0.1',
    user = 'root',
    password = 'admin',
    db='guest',
    # port= '3306'
    )

#获取游标
cur = db.cursor()
sql_insert = 'INSERT INTO sign_guest(realname,phone,email,sign,event_id,create_time) VALUES ("tom",18800112233,"tom@mail.com",0,1,NOW());'

try:
    cur.execute(sql_insert)
    db.commit()
except Exception as e:
    db.rollback()
finally:
    db.close()