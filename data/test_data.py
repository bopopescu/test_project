from config.mysql_db import DB

# 创建测试数据
datas = {
    'user': [
        {'id': 1, 'username': '小李', 'password': '123456', 'telephone': '13298745632', 'address': '北京东城区',
         'reg_time': '2018-10-30 08:00:00'},
        {'id': 2, 'username': '小王', 'password': '234567', 'telephone': '13298745632', 'address': '香港',
         'reg_time': '2018-10-29 08:00:00'},
        {'id': 3, 'username': '小白', 'password': '111111', 'telephone': '13298745632', 'address': '澳门',
         'reg_time': '2018-10-28 08:00:00'},
        {'id': 4, 'username': '小丽', 'password': '369852', 'telephone': '13298745632', 'address': '上海浦东新区',
         'reg_time': '2018-10-27 08:00:00'},
        {'id': 5, 'username': '小佳', 'password': '789456', 'telephone': '13298745632', 'address': '广州天河新区',
         'reg_time': '2018-10-26 08:00:00'},
    ]
}


# 将测试数据插入表中
def init_data():
    db = DB()
    for table, data in datas.items():
        db.clear(table)
        for d in data:
            db.insert(table, d)
    db.close()


if __name__ == '__main__':
    init_data()