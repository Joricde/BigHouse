import json


def find_keyword(keyword, path):
    with open(path, encoding='utf-8') as f:
        file_end = False
        keyword = str(keyword)
        list = []
        # 'bid': 42728.9,
        while not file_end:
            file_data = f.readline()
            if file_data == '':
                file_end = True
                break
            get_file_str = json.dumps(file_data)
            pos = get_file_str.find(keyword)
            keyword_value = get_file_str[get_file_str.find(':', pos) + 2: get_file_str.find(',', pos)]
            list.append(float(keyword_value))
    return list



