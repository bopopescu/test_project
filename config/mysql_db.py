# coding:utf-8

from pymysql import connect, cursors
from pymysql.err import OperationalError
import os
import configparser

# =====读取sqlconfig.ini文件设置=========
cur_path = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(cur_path, "sqlconfig.ini")
cf = configparser.ConfigParser()
cf.read(configPath, encoding='UTF-8')

host = cf.get("sqlconf", "host")
port = cf.get("sqlconf", "port")
user = cf.get("sqlconf", "user")
password = cf.get("sqlconf", "password")
db_name = cf.get("sqlconf", "db")


# ============MYSQL基本操作==============
class DB:
    def __init__(self):
        try:
            # 连接数据库
            self.conn = connect(
                host=host,
                user=user,
                password=password,
                db=db_name,
                charset="utf8mb4",
                cursorclass=cursors.DictCursor
            )
        except OperationalError as e:
            print("Mysql error %d:%s" % (e.args[0], e.args[1]))

    # 清除表数据
    def clear(self, table_name):
        real_sql = "delete from " + table_name + ";"
        with self.conn.cursor() as cursor:
            # 取消外键约束
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute(real_sql)
        self.conn.commit()

    # 插入表数据
    def insert(self, table_name, table_data):
        for key in table_data:
            # table_data[key] = str(table_data[key])
            table_data[key] = "'" + str(table_data[key]) + "'"
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + "(" + key + ") VALUES (" + value + ");"
        print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()

    # 关闭数据库连接
    def close(self):
        self.conn.close()


if __name__ == '_main__':
    db = DB()
    table_name = "user"
    data = {
        "id": 1,
        "username": "小李",
        "password": "123456",
        "telephone": "13298745632",
        "address": "北京东城区",
        "reg_time": "2018-10-30 08:00:00"
    }
    db.clear(table_name)
    db.insert(table_name, data)
    db.close()
