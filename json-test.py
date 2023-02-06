import json
import time
import os

dirpath = 'D:\\Requality\\Projects\\jetos-reqs.posix\\'

def get_json(dirpath_r):
    collected_data = []
    for filename in os.listdir(dirpath_r):
        path = os.path.join(dirpath_r, filename)
        base, ext = os.path.splitext(path)
        if ext == '.json':
            with open(path, "r") as read_file:
                data = json.load(read_file)
                collected_data.append(data)
        elif os.path.isdir(path):
            get_json(path)
    return collected_data


if __name__ == '__main__':
    start_time = time.time()
    json_data = get_json(dirpath)
    print("--- %s seconds ---" % (time.time() - start_time))
    # print(json_data[0])
