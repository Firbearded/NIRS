from pymysql import connect
import time

db_config = {'host': '127.0.0.1', 'user': 'root', 'password': 'root', 'database': 'nirs'}

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
    start_time = time.time()
    sql_data = get_sql(db_config)
    print("--- %s seconds ---" % (time.time() - start_time))
    # print(sql_data)
