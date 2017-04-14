import pymysql


user = "CREATE TABLE IF NOT EXISTS user ( " \
    "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
    "name VARCHAR(100) NOT NULL, " \
    "email VARCHAR(100) NOT NULL) " \
    "ENGINE = InnoDB "

list = "CREATE TABLE IF NOT EXISTS list ( " \
    "id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
    "list_name VARCHAR(100) NOT NULL, " \
    "user_id SMALLINT UNSIGNED NOT NULL, " \
    "FOREIGN KEY (user_id) " \
    "REFERENCES user (id) " \
    "ON DELETE CASCADE) ENGINE = InnoDB;"

item = "CREATE TABLE IF NOT EXISTS item ( " \
    "id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
    "item_name VARCHAR(100) NOT NULL, " \
    "done TINYINT(1) DEFAULT 0, " \
    "list_id MEDIUMINT UNSIGNED NOT NULL, " \
    "FOREIGN KEY (list_id) " \
    "REFERENCES list (id) " \
    "ON DELETE CASCADE) ENGINE = InnoDB;"

subtask = "CREATE TABLE IF NOT EXISTS subtask ( " \
    "id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
    "subtask_name VARCHAR(100) NOT NULL, " \
    "item_id MEDIUMINT UNSIGNED NOT NULL, " \
    "FOREIGN KEY (item_id) " \
    "REFERENCES item (id) " \
    "ON DELETE CASCADE) ENGINE = InnoDB;"

queries = [user, list, item, subtask]


def execute(sql):
    conn = pymysql.connect(user='user', passwd='1234',
                           db='todolist', charset="utf8", autocommit=True)
    try:
        with conn.cursor() as cursor:
            for line in sql:
                cursor.execute(line)
    finally:
        conn.close()

execute(queries)
