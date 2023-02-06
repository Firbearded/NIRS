import json
import time
from pymysql import connect
import os

dirpath = 'D:\\Requality\\Projects\\jetos-reqs.posix\\'
db_config = {'host': '127.0.0.1', 'user': 'root', 'password': 'root', 'database': 'nirs'}

json_load_time = 0
json_load_count = 0
json_dir_count = 0

def get_json(dirpath_r):
    global json_load_time
    global json_load_count
    global json_dir_count
    collected_data = []
    jsons = []
    for filename in os.listdir(dirpath_r):
        path = os.path.join(dirpath_r, filename)
        base, ext = os.path.splitext(path)
        if ext == '.json':
            jsons.append(base)
            #start_time = time.time()
            with open(path, "r") as read_file:  # закомментить, чтобы узнать время выполнения остальной части функции
                data = json.load(read_file)
                collected_data.append(data)
            #json_load_time += (time.time() - start_time)
            json_load_count += 1
    for path in jsons:
        if os.path.isdir(path):
            collected_data.append(get_json(path))
            json_dir_count += 1
    return collected_data


def get_sql(config):
    collected_data = {}
    tables = ['node', 'attribute', 'attr_value', 'generator', 'value_provider']
    conn = connect(**config)
    cursor = conn.cursor()

    for table in tables:
        _SQL = f"""select * from {table}"""
        cursor.execute(_SQL)
        data = cursor.fetchall()
        collected_data.update({table: data})

    cursor.close()
    conn.close()
    return collected_data


if __name__ == '__main__':
    n = 100

    sum_json = 0
    for i in range(n):
        start_time = time.time()
        json_data = get_json(dirpath)
        sum_json += (time.time() - start_time)
    print('file count:', json_load_count // n, ' dir count:', json_dir_count // n)
    print('file structure time:', sum_json / n)
    # print('average file in file structure time:', json_load_time / json_load_count)
    # print(json_load_time / n)
    # print(json_other_load / n)
    sum_sql = 0
    for i in range(n):
        start_time = time.time()
        sql_data = get_sql(db_config)
        sum_sql += (time.time() - start_time)
    print('DB time:', sum_sql / n)
    print('DB is ', (sum_json / n) / (sum_sql / n), ' times faster than file structure.')
    # print(json_data[0])
