import json
import os
from pymysql import connect
import time


dirpath = 'D:\\Requality\\Projects\\jetos-reqs.posix\\'
db_config = {'host': '127.0.0.1', 'user': 'root', 'password': 'root', 'database': 'nirs'}
project_name = 'jetos-reqs.posix'
root = '9f92c37e-4780-4672-90c9-78c952fd8639'
id_attr = 1
id_attr_val = 1


def insert_db(data, conn, parent):
    global id_attr, id_attr_val
    cursor = conn.cursor()
    node_insert = f"insert into node values('{data['uuid']}', '{parent}', '{project_name}')"
    try:
        conn.begin()
        cursor.execute(node_insert)
        for attr_name in data['attributes']:
            attr = data['attributes'][attr_name]
            raw_attr_value = attr['value']['value']
            if 'type' in attr['value'].keys():
                provider_type = attr['value']['type']
            else:
                provider_type = '0'
            if 'atype' in attr['value'].keys():
                raw_attr_type = attr['value']['atype']
            else:
                raw_attr_type = '0'

            symb = '\''
            if f"""{raw_attr_value}""".find('\'') >= 0:  # Из-за проблем с загрузкой,
                # если в тектсе есть и ', и ", то все " заменим на '
                if f"""{raw_attr_value}""".find('\"') >= 0:
                    raw_attr_value = f"""{raw_attr_value}"""
                    raw_attr_value = raw_attr_value.replace('\'', '\"')
                    # print(raw_attr_value)
                    symb = '\''
                else:
                    symb = '\"'
            value_provider_insert = f"""insert into value_provider values({id_attr_val},{symb}{raw_attr_value}{symb},
                                             '{raw_attr_type}','{provider_type}','0')"""
            # print(type(str(raw_attr_value)))
            # print(value_provider_insert)
            cursor.execute(value_provider_insert)

            attr_scope = 0
            if 'availability' in attr.keys():
                if attr['availability'] == 'DIRECT_CHILDREN':
                    attr_scope = 1
                elif attr['availability'] == 'SUBTREE':
                    attr_scope = 2
            if 'key' in attr.keys():
                attr_name = attr['key']
            if 'flag' in attr.keys():
                attr_flag = attr['flag']
            else:
                attr_flag = 0
            if 'origin' in attr.keys():  # Должно быть отдельно, потому что можем встретить раньше начального
                # либо надо каждый раз проверять, есть ли уже атрибут с таким именем и определяющим узлом, но я не хочу
                uuid_using = attr['origin']
                cursor1 = conn.cursor()
                _SQL = f"""select id_attribute from attribute where UUID_defining = '{uuid_using}'"""
                cursor1.execute(_SQL)
                right_id_attr = cursor1.fetchall()[0][0]
                cursor1.close()
            else:
                right_id_attr = id_attr
                uuid_using = data['uuid']
                attribute_insert = f"""insert into attribute values({id_attr},'{data['uuid']}','{attr_name}',NULL,
                    {attr_flag},{attr_scope})"""
                id_attr += 1
                cursor.execute(attribute_insert)
                # print(attribute_insert)
            attr_value_insert = f"""insert into attr_value values({id_attr_val},{symb}{raw_attr_value}{symb},'{raw_attr_type}',
                    {right_id_attr},'{uuid_using}')"""
            # print(attr_value_insert)
            cursor.execute(attr_value_insert)
            id_attr_val += 1
        conn.commit()
    except Exception as e:
        print('Ошибка')
        print(node_insert)
        print(data)

        conn.rollback()

    cursor.close()


def fill_db(dirpath_r, conn, parent):
    parents = {}
    jsons = []
    for filename in os.listdir(dirpath_r):
        path = os.path.join(dirpath_r, filename)
        base, ext = os.path.splitext(path)
        if ext == '.json':
            jsons.append(base)
            with open(path, "r") as read_file:
                data = json.load(read_file)
                insert_db(data, conn, parent)

                filepath, folder = os.path.split(base)
                parents.update({folder: data['uuid']})

    for path in jsons:
        folderpath, folder = os.path.split(path)
        if os.path.isdir(path):
            if folder in parents.keys():
                fill_db(path, conn, parents[folder])
    #print(parents)


def config_and_fill(dirpath_r, config, root_r):
    conn = connect(**config)
    fill_db(dirpath_r, conn, root_r)
    conn.close()

if __name__ == '__main__':
    start_time = time.time()
    config_and_fill(dirpath, db_config, root)
    print("--- %s seconds ---" % (time.time() - start_time))
