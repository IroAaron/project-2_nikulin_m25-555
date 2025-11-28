from .constatns import DATA_BASE_TYPES
from .constatns import METADATA_FILE
from . import engine
from . import utils

def action_show_commands(*args, **kwargs):
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    for command in engine.available_actions.keys():
        print(f"<command> {command} - {engine.available_actions[command]['description']}")

def action_create_table(*args, **kwargs):
    tables = engine.tables

    try:
        table_name = args[0][0]
        table_colums = args[1]
    except IndexError as e:
        print("Таблица не создана. Отсутствуют данные таблицы: имя или колонки")
        return

    if table_name in list(tables.keys()):
        print("Таблица не создана. Таблица с таким именем уже существует")
        return
    elif len(set(table_colums.values()) - set(DATA_BASE_TYPES)) > 1:
        print("Таблица не создана. Недоступный вид табличных данных. " \
        "Доступные типы: " + ', '.join(DATA_BASE_TYPES))
        return

    if not 'ID' in list(table_colums.keys()):
        table_colums['ID'] = 'int'

    colums_list = []
    for i in range(0, len(table_colums.items())):
        colums_list.append({'name' : list(table_colums.keys())[i], 
                            'cell_type' : list(table_colums.values())[i],
                            'items' : []})
    
    
    tables[table_name] = colums_list
    names = []
    for i in range(0, len(colums_list)):
        names.append(f"{colums_list[i]['name']}:{colums_list[i]['cell_type']}")

    print(f"Таблица '{table_name}' успешно создана со столбцами: " + 
          ', '.join(names))
    
    utils.save_metadata(METADATA_FILE, tables)

def action_show_list_tables(*args, **kwargs):
    tables = engine.tables

    if len(tables.items()) == 0:
        print("Ни одной таблицы не создано")
        return

    for table in list(tables.keys()):
        print(f"- {table}")

def action_drop_table(*args, **kwargs):
    tables = engine.tables

    if not args[0][0] in list(tables.keys()):
        print(f'Ошибка: Таблицы "{args[0][0]}" не существует')
        return
    
    tables.pop(args[0][0])
    print(f'Таблица {args[0][0]} успешно удалена')
    utils.save_metadata(METADATA_FILE, tables)
    
def action_exit(*args, **kwargs):
    engine.finish_program()

def read_command(command):
    splited_command = command.split(sep=' ')
    command_and_agrs = {
        "command" : splited_command[0],
        "args" : [],
        "kwargs" : {}
        }
    
    if len(splited_command) > 1:
        for i in range(1, len(splited_command)):
            if ':' in splited_command[i]:
                dict_args = splited_command[i].split(sep=":")
                command_and_agrs["kwargs"][dict_args[0]] = dict_args[1]
            else:
                command_and_agrs["args"].append(splited_command[i])

    try:
        action = engine.available_actions[command_and_agrs["command"]]["command"]
        action(command_and_agrs["args"], command_and_agrs["kwargs"])
    except KeyError as e:
        print(f"Функции <{e}> нет. Попробуйте снова")
