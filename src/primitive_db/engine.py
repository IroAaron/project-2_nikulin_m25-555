from .constatns import METADATA_FILE

import prompt
from . import core
from . import utils

tables = {}
program_state = True

def state_waiting_command():
    command = prompt.string('\n>>>Введите команду: ')
    core.read_command(command)

def run():
    global program_state
    global tables

    tables = utils.load_metadata(METADATA_FILE)
    available_actions["help"]["command"]()
    
    while program_state:
        state_waiting_command()

def finish_program():
    global program_state

    program_state = False

available_actions = {
    "create_table" : {
        "command" : core.action_create_table,
        "description" : "<имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу"
        },
    "list_tables" : {
        "command" : core.action_show_list_tables,
        "description" : "показать список всех таблиц"
        },
    "drop_table" : {
        "command" : core.action_drop_table,
        "description" : "<имя_таблицы> - удалить таблицу"
        },   
    "help" : {
        "command" : core.action_show_commands,
        "description" : "справочная информация"
        },
    "exit" : {
        "command" : core.action_exit,
        "description" : "выйти из программы"
        },
}