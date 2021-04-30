#需要下载mysql，下载地址https://cdn.mysql.com/archives/mysql-installer/mysql-installer-community-5.5.27.2.msi
#需要mysqldb
from pymysql import cursors,connect

conn = connect(
    host='127.0.0.1',
    user = 'root',
    password = 'admin',
    db='guest',
    charset='utf8mb4',
    cursorclass=cursors.DictCursor)

conn.cursor()
sql = 'INSERT INTO sign_guest(realname,phone,email,sign,event_id,create_time) VALUES ("tom",18800112233,"tom@mail.com",0,1,NOW());'
cursors.execute(sql)
conn.commit()
#
# try:
#     with conn.cursor() as cursors:
#         #创建嘉宾数据
#         sql = 'INSERT INTO sign_guest(realname,phone,email,sign,event_id,create_time) VALUES ("tom",18800112233,"tom@mail.com",0,1,NOW());'
#         #提交事务
#         cursors.execute(sql)
#         #提交数据库执行
#         conn.commit()
#
#     with conn.cursor() as cursor:
#         #查询新增的嘉宾
#         sql = "SELECT realname,phone,email,sign FROM sign_guest WHERE phone=%s"
#         cursors.execute(sql,('18800112233'))
#         result = cursor.fetchone()
#         print(result)
# finally:
#     conn.close()