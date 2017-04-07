import pymysql


def connect(sql):
    conn = pymysql.connect(user='user', passwd='1234', db='todolist', charset="utf8")
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result


def create_list(list_name, user_id):
    sql = "insert into list (list_name, user_id) values ('{name}', '{id}')".format(name=list_name, id=user_id)
    connect(sql)


def get_lists():
    sql = 'select * from list'
    return connect(sql)


def get_list_detail(list_id):
    sql = "select * from list where id={id}".format(id=list_id)
    return connect(sql)


def edit_list_name(list_id, new_name):
    sql = "update list set list_name='{name}' where id={id}".format(name=new_name, id=list_id)
    connect(sql)


def destroy_list(list_id):
    sql = "delete from list where id={id}".format(id=list_id)
    connect(sql)
