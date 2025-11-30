import json
import os

from .constatns import DATA_BASE_TYPES, TABLES_PATH_FILES


def load_metadata(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Файл {e} не найден")
        return {}
    except json.JSONDecodeError as e:
        print(f"Файл {e} не содержит данных")
        return {}
    
def save_metadata(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_table_data(table_name):
    try:
        with open(TABLES_PATH_FILES + table_name, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Таблица {e} не найден")
        return {}
    except json.JSONDecodeError as e:
        print(f"Таблица {e} не содержит данных")
        return {}
    pass

def save_table_data(table_name, data):
    with open(TABLES_PATH_FILES + table_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def get_tables_names():
    table_names = []
    for file_name in os.listdir(TABLES_PATH_FILES):
        if os.path.isfile(os.path.join(TABLES_PATH_FILES, file_name)):
            table_names.append(file_name)
    return table_names

def delete_table(table_name):
    try:
        os.remove(TABLES_PATH_FILES + table_name)
        print(f"Таблица {table_name} успешно удален")
    except FileNotFoundError:
        print(f"Таблица {table_name} не найден")
    except PermissionError:
        print(f"Нет прав на удаление таблицы {table_name}")
    except Exception as e:
        print(f"Ошибка при удалении таблицы: {str(e)}")

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
    
    try:
        if value_type is bool:
            if data == 'false':
                return False
            else:
                return True
        value_type(data)
    except ValueError:
        print('Данные не соответствуют типу')
        return None
    
    return value_type(data)

def get_row(table, num):
    return list(map(lambda x: x['items'][num], table))

def set_new_value_to_row(table_name, colum_name, index, new_value):
    table = load_table_data(table_name)
    column = next(filter(lambda x: x['name'] == colum_name, table), None)
    table[table.index(column)]['items'][index] = new_value
    save_table_data(table_name, table)

def remove_rows(table_name, index):
    table = load_table_data(table_name, )
    for i in range(0, len(table)):
        table[i]['items'].remove(table[i]['items'][index])
    
    save_table_data(table_name, table)



    
