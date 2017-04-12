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
    list_sql = "select * from list where id=%s"
    list_data = connect(list_sql, list_id)
    items_sql = "select * from item where list_id=%s"
    items_data = connect(items_sql, list_id)
    return list_data, items_data


def edit_list_name(list_id, new_name):
    sql = "update list set list_name=%s where id=%s"
    connect(sql, new_name, list_id)


def destroy_list(list_id):
    sql = "delete from list where id=%s"
    connect(sql, list_id)


def create_item(item_name, list_id):
    sql = "insert into item (item_name, list_id) values (%s, %s)"
    connect(sql, item_name, list_id)


def get_item_detail(item_id):
    sql = "select * from item where id=%s"
    return connect(sql, item_id)


def edit_item_name(item_id, new_name):
    sql = "update item set item_name=%s where id=%s"
    connect(sql, new_name, item_id)


def destroy_item(item_id):
    sql = "delete from item where id=%s"
    connect(sql, item_id)


def item_check_box(item_id, value):
    sql = "update item set done=%s where id=%s"
    connect(sql, value, item_id)
