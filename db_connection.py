import pymysql


def connect(sql, *args):
    conn = pymysql.connect(user='user', passwd='1234',
                           db='todolist', charset="utf8", autocommit=True)
    result = None
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, args)
            result = cursor.fetchall()
    finally:
        conn.close()
    return result


def create_list(list_name, user_id):
    sql = "insert into list (list_name, user_id) values (%s, %s)"
    connect(sql, list_name, user_id)


def get_lists():
    sql = 'select * from list'
    return connect(sql)


def get_list_detail(list_id):
    sql = "select * from list where id=%s"
    return connect(sql, list_id)


def edit_list_name(list_id, new_name):
    sql = "update list set list_name=%s where id=%s"
    connect(sql, new_name, list_id)


def destroy_list(list_id):
    sql = "delete from list where id=%s"
    connect(sql, list_id)
