import json
import os

from src import decorators

from .constatns import DATA_BASE_TYPES, TABLES_PATH_FILES


@decorators.handle_db_errors
def load_metadata(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

@decorators.handle_db_errors
def save_metadata(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

@decorators.handle_db_errors
def load_table_data(table_name):
    with open(TABLES_PATH_FILES + table_name + '.json', 'r', encoding='utf-8') as file:
        return json.load(file)

@decorators.handle_db_errors
def save_table_data(table_name, data):
    with open(TABLES_PATH_FILES + table_name + '.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

@decorators.handle_db_errors
def get_tables_names():
    table_names = []
    for file_name in os.listdir(TABLES_PATH_FILES):
        if os.path.isfile(os.path.join(TABLES_PATH_FILES, file_name)):
            table_names.append(file_name)
    return table_names

@decorators.handle_db_errors
def delete_table(table_name):
    os.remove(TABLES_PATH_FILES + table_name)
    print(f"Таблица {table_name} успешно удалена")

@decorators.handle_db_errors
def check_data_type(data, data_type):
    value_type = None
    match data_type:
        case 'str':
            value_type = str
        case 'int':
            value_type = int
        case 'bool':
            value_type = bool
        case _:
            print(f"{data} является недостимым типом данных."  \
        "Доступные типы: ") + ', '.join(DATA_BASE_TYPES)
            return None
    
    if value_type is bool:
        if data == 'false':
            return False
        else:
            return True
    value_type(data)
    
    return value_type(data)

@decorators.handle_db_errors
def get_row(table, num):
    return list(map(lambda x: x['items'][num], table))

@decorators.handle_db_errors
def set_new_value_to_row(table_name, colum_name, index, new_value):
    table = load_table_data(table_name)
    column = next(filter(lambda x: x['name'] == colum_name, table), None)
    table[table.index(column)]['items'][index] = new_value
    save_table_data(table_name, table)
    return table[0]['items'][index]

@decorators.handle_db_errors
def remove_rows(table_name, indeces):
    table = load_table_data(table_name)
    removed_ids = []
    for index in indeces:
        removed_ids.append(table[0]['items'][index])

    for removed_id in removed_ids:
        index = table[0]['items'].index(removed_id)
        for i in range(0, len(table)):
                table[i]['items'].pop(index)
    
    save_table_data(table_name, table)
    return removed_ids
    
