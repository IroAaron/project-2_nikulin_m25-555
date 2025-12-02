import prompt

from . import core, utils
from .constatns import METADATA_FILE

tables = {}
program_state = True
database_state = False

def state_waiting_command():
    command = prompt.string('\n>>>Введите команду: ')
    core.read_command(command)

def run():
    global program_state
    global tables

    tables = utils.load_metadata(METADATA_FILE)
    core.action_show_commands()
    
    while program_state:
        state_waiting_command()

def run_database():
    global program_state
    global database_state
    
    database_state = True

    core.action_show_commands()    
    
    while program_state:
        state_waiting_command()

def finish_program():
    global program_state

    program_state = False


available_actions = {
    "create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. " : {
        "description" : "создать таблицу"
        },
    "list_tables" : {
        "description" : "показать список всех таблиц"
        },
    "drop_table" : {
        "description" : "<имя_таблицы> - удалить таблицу"
        },   
    "help" : {
        "description" : "справочная информация"
        },
    "exit" : {
        "description" : "выйти из программы"
        },
}

available_table_actions = {
    "create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. -" : {
        "description" : "создать таблицу"
        },
    "insert into <имя_таблицы> values (<значение1>, <значение2>, ...)" : {
        "description" : "создать запись"
        },
    "select from <имя_таблицы> where <столбец> = <значение>" : {
        "description" : "прочитать записи по условию"
        },
    "select from <имя_таблицы>" : {
        "description" : "прочитать все записи"
        },
    "update <имя_таблицы> set <столбец1> = <новое_значение1> where" \
        " <столбец_условия> = <значение_условия>" : {
        "description" : "обновить запись"
        },
    "delete from <имя_таблицы> where <столбец> = <значение>" : {
        "description" : "удалить запись"
        },
    "info <имя_таблицы>" : {
        "description" : "вывести информацию о таблице"
        },
    "help" : {
        "description" : "справочная информация"
        },
    "exit" : {
        "description" : "выйти из программы"
        },
}