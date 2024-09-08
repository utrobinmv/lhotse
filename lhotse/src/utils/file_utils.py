import os
import json
import pandas as pd

def dict_to_json(dict_str):
    return json.dumps(dict_str, ensure_ascii=False)

def make_dirs(path, debug=False):
    try:
        os.makedirs(path)
    except OSError:
        if debug:
            print("Создать директорию %s не удалось" % path)
    else:
        if debug:
            print("Успешно создана директория %s " % path)

def get_file_extension(filename):
    if "." in filename:
        return filename.split(".")[-1]
    return ''

def read_manifest(f):
    text_data = f.decode('utf-8')
                      
    lines = text_data.splitlines()  # Decode byte string and split into lines
    
    data_list = []
    for line in lines:
        # Parse each line into a dictionary
        # data_dict = {}
        data_dict = json.loads(line)
        # parts = line.split(': ')
        # for part in parts:
        #     key, value = part.split(':')
        #     data_dict[key.strip()] = value.strip()
        
        data_list.append(data_dict)
    
    # Convert list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(data_list)                      
    return df
