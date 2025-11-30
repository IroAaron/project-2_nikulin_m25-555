import shlex

from prettytable import PrettyTable

from . import engine, utils
from .constatns import AVAILABLE_COMMANDS, DATA_BASE_TYPES, METADATA_FILE


def action_show_commands():
    actions = []
    if not engine.database_state:
        print("\n***Процесс работы с таблицей***")
        actions = engine.available_actions
    else:
        actions = engine.available_table_actions
        print("\n***Процесс работы с данными***")

    print("Функции:")
    for command in actions.keys():
        print(f"<command> {command} - {actions[command]['description']}")

def action_select(table_name, where_clause=None):
    pt = PrettyTable()
    table = utils.load_table_data(table_name)
    pt.field_names = list(map(lambda x: x['name'], table))
    if where_clause is None:
        for i in range(0, len(table[0]['items'])):
            pt.add_row(utils.get_row(table, i))
    else:
        try:
            where_clause.remove('where')
        except ValueError:
            print('Отсутствует обозначатель аргументов добавляемой строки "where"')
            return
        try:
            select_key = where_clause[0]
        except IndexError:
            print('Отсутствует ключ сортировки')
            return
        try:
            where_clause.remove('=')
        except ValueError:
            print('Отсутствует обозначатель фильтра "="')
            return
        try:
            select_filter = where_clause[1]
        except IndexError:
            print('Отсутствует значение сортировки')
            return
        if select_key not in pt.field_names:
            print(f'{select_key} неверный ключ сортировки')
            return
        
        column_by_key = next(filter(lambda x: x['name'] == select_key, table), None)
        if utils.check_data_type(select_filter, column_by_key['cell_type']) is None:
            print("Тип значения сортировки не соответствует типу столбца")
            return
        
        indices = list(filter(
            lambda i: str(column_by_key['items'][i]).lower() == select_filter.lower(), 
            range(len(column_by_key['items']))))
        for indice in indices:
            pt.add_row(utils.get_row(table, indice))

    print(pt)


def action_update(table_name, clauses):
    pt = PrettyTable()
    table = utils.load_table_data(table_name)
    pt.field_names = list(map(lambda x: x['name'], table))
    try:
        clauses.remove('set')
    except ValueError:
        print('Отсутствует обозначатель аргументов обновленный аргументов "set"')
        return
    try:
        set_clause_key = clauses[0]
    except IndexError:
        print('Отсутствует наименование столбца')
        return
    try:
        clauses.remove('=')
    except ValueError:
        print('Отсутствует обозначатель присваивания "="')
        return
    try:
        set_clause_value = clauses[1]
    except IndexError:
        print('Отсутствует новое значение')
        return
    if set_clause_key not in pt.field_names:
        print(f'{set_clause_key} неверное наименование столбца')
        return
    try:
        clauses.remove('where')
    except ValueError:
        print('Отсутствует обозначатель аргументов добавляемой строки "where"')
        return
    try:
        where_clause_key = clauses[2]
    except IndexError:
        print('Отсутствует ключ сортировки')
        return
    try:
        clauses.remove('=')
    except ValueError:
        print('Отсутствует обозначатель фильтра "="')
        return
    try:
        where_clause_filter = clauses[3]
    except IndexError:
        print('Отсутствует значение сортировки')
        return
    if where_clause_key not in pt.field_names:
        print(f'{where_clause_key} неверный ключ сортировки')
        return

    column_by_key = next(filter(lambda x: x['name'] == where_clause_key, table), None)
    if utils.check_data_type(where_clause_filter, column_by_key['cell_type']) is None:
        print("Тип значения сортировки не соответствует типу столбца")
        return
        
    indeces = list(filter(
        lambda i: str(column_by_key['items'][i]).lower() == 
        where_clause_filter.lower(), 
        range(len(column_by_key['items']))))
    
    for i in range(0, len(indeces)):
        utils.set_new_value_to_row(
            table_name, set_clause_key, indeces[i], set_clause_value)
    
    print(f"Запись(и) с ID={indeces} в таблице '{table_name}' успешно обновлены")
    

def action_delete(table_name, where_clause):
    pt = PrettyTable()
    table = utils.load_table_data(table_name)
    pt.field_names = list(map(lambda x: x['name'], table))

    try:
        where_clause.remove('where')
    except ValueError:
        print('Отсутствует обозначатель аргументов добавляемой строки "where"')
        return
    try:
        select_key = where_clause[0]
    except IndexError:
        print('Отсутствует ключ сортировки')
        return
    try:
        where_clause.remove('=')
    except ValueError:
        print('Отсутствует обозначатель фильтра "="')
        return
    try:
        select_filter = where_clause[1]
    except IndexError:
        print('Отсутствует значение сортировки')
        return
    if select_key not in pt.field_names:
        print(f'{select_key} неверный ключ сортировки')
        return
        
    column_by_key = next(filter(lambda x: x['name'] == select_key, table), None)
    if utils.check_data_type(select_filter, column_by_key['cell_type']) is None:
        print("Тип значения сортировки не соответствует типу столбца")
        return
    
    indeces = list(filter(
        lambda i: str(column_by_key['items'][i]).lower() == select_filter.lower(), 
        range(len(column_by_key['items']))))
    for index in indeces:
        utils.remove_rows(table_name, index)
    
    print(f"Запись(и) с ID={indeces} в таблице '{table_name}' успешно удалены")

def action_info(table_name):
    pt = PrettyTable()
    table = utils.load_table_data(table_name)
    pt.field_names = list(map(lambda x: x['name'], table))

    for i in range(0, len(table[0]['items'])):
            pt.add_row(utils.get_row(table, i))

    print(pt)

def action_insert(table_name, values):
    if table_name not in utils.get_tables_names():
        print(f"Таблицы с именем {table_name} не существует")
        return
    
    try:
        values = values[values.index('values') + 1:]
    except ValueError:
        print('Отсутствует обозначатель аргументов добавляемой строки "values"')
        return

    if '(' in values[0]:
        values[0] = values[0].replace('(', '')
    else:
        print("Нет фигурной скобки, открывающей начало аргументов")
        return
    
    if ')' in values[len(values) - 1]:
        values[len(values) - 1] = values[len(values) - 1].replace(')', '')
    else:
        print("Нет фигурной скобки, закрывающей конец перечисления аргументов")
        return

    for i in range(0, len(values)):
        if ',' in values[i][-1]:
            values[i] = values[i][:-1]
        elif len(values) > 1 and len(values) - 1 > i:
            print("Нет разделителя ',' между аргументами")
            return

    table = utils.load_table_data(table_name)
    if len(values) != len(table) - 1:
        print("Количество заданных параметров строки " \
        "не соответствует количеству столбцов")
        return

    for i in range(0, len(table) - 1):
        data_type_check = utils.check_data_type(values[i], table[i + 1]['cell_type'])

        if data_type_check is None:
            print(f"Тип {values[i]} не соответствует типу" \
                  f"колонки {table[i + 1]["name"]} таблицы {table_name}")
            return
        values[i] = data_type_check
        
    if len(table[0]['items']) == 0:
        data_id = 1
    else:
        data_id = max(table[0]['items']) + 1
    table[0]['items'].append(data_id)
    for i in range(0, len(table) - 1):
        table[i + 1]['items'].append(values[i])

    utils.save_table_data(table_name, table)
    
    print(f"Запись с ID={data_id} успешно добавлена в таблицу '{table_name}'")

def action_create_table(table_name, colums):
    tables = engine.tables
    if ':' in table_name:
        print("Таблица не создана. Отсутствуют данные таблицы: имя")
        return

    colums_names = []
    colums_types = []

    for i in range(0, len(colums)):
        try:
            colum_data = colums[i].split(':')
            colums_names.append(colum_data[0])
            colums_types.append(colum_data[1])
        except ValueError:
            print("Таблица не создана. Нет разделителя " \
            "между типом данных и именем столбца")
            return
        if '' == colums_types[i]:
            print(f"Таблица не создана. Для колонки '{colums_names[i]}'" \
                   "не указан тип данных")
            return
        if '' == colums_names[i]:
            print(f"Таблица не создана. Для колонки {i} не указано имя")
            return
        
    if len(colums_names) == 0:
        print(f"Таблица {table_name} не создана. Не указаны столбцы")
        return
    if table_name in list(tables.keys()):
        print("Таблица не создана. Таблица с таким именем уже существует")
        return
    for colums_type in colums_types:
        if colums_type not in DATA_BASE_TYPES:
            print(f"Таблица не создана. {colums_type} недостимый тип." \
            " Доступные типы: " + ', '.join(DATA_BASE_TYPES))
            return

    first_row_list = []

    if 'ID' not in list(colums):
        first_row_list.append({'name' : 'ID', 
                            'cell_type' : 'int',
                            'items' : []})
        
    for i in range(0, len(colums)):
        first_row_list.append({'name' : colums_names[i], 
                            'cell_type' : colums_types[i],
                            'items' : []})
    
    
    tables[table_name] = first_row_list
    names = []
    for i in range(0, len(first_row_list)):
        names.append(f"{first_row_list[i]['name']}:{first_row_list[i]['cell_type']}")

    print(f"Таблица '{table_name}' успешно создана со столбцами: " + 
          ', '.join(names))
    if not engine.database_state:
        utils.save_metadata(METADATA_FILE, tables)
    else:
        utils.save_table_data(table_name, first_row_list)


def action_show_list_tables():
    tables = utils.get_tables_names() if engine.database_state else engine.tables

    if len(tables) == 0:
        print("Ни одной таблицы не создано")
        return

    for table in list(tables.keys()):
        print(f"- {table}")

def action_drop_table(table_name):
    tables = utils.get_tables_names() if engine.database_state else engine.tables

    if engine.database_state:
        utils.delete_table(table_name)
        return
    
    if table_name not in list(tables.keys()):
        print(f'Ошибка: Таблицы "{table_name}" не существует')
        return
    
    tables.pop(table_name)
    print(f'Таблица "{table_name}" успешно удалена')
    utils.save_metadata(METADATA_FILE, tables)
    
def action_exit():
    engine.finish_program()

def read_command(command):
    command_multiplayer = ''

    for com in command:
        command_multiplayer += com
        command_name = next(
            (cmd for cmd in AVAILABLE_COMMANDS if cmd == command_multiplayer), None)
        if command_name is not None:
            break
    try:
        values = shlex.split(command.replace(command_name, ''))
    except TypeError as e:
        print(f"Команда {e} не найдена")

    for i in range(0, len(values)):
        if '"' in values:
            values[i] = values[i].replace('"', '')
        if "'" in values:
            values[i] = values[i].replace("'", '')

    match command_name:
        case 'create_table':
            try:
                action_create_table(values[0], values[1:])
            except IndexError:
                print("Отсутствуют необходимые аргументы")
        case 'list_tables':
            action_show_list_tables()
        case 'drop_table':
            try:
                action_drop_table(values[0])
            except IndexError:
                print("Отсутствуют необходимые аргументы")
        case 'insert into':
            try:
                action_insert(values[0], values[1:])
            except IndexError:
                print("Отсутствуют необходимые аргументы")
        case 'select from':
            try:
                if len(values[1:]) > 0:
                    action_select(values[0], values[1:])
                else:
                    action_select(values[0])
            except IndexError:
                print("Отсутствуют необходимые аргументы")
        case 'update':
            try:
                action_update(values[0], values[1:])
            except IndexError:
                print("Отсутствуют необходимые аргументы")
        case 'delete from':
            try:
                action_delete(values[0], values[1:])
            except IndexError:
                print("Отсутствуют необходимые аргументы")
        case 'info':
            try:
                action_info(values[0])
            except IndexError:
                print("Отсутствуют необходимые аргументы")
        case 'help':
            action_show_commands()
        case 'exit':
            action_exit()
        case _:
            print(f'Команды "{command_name}" нет. Попробуйте еще раз')