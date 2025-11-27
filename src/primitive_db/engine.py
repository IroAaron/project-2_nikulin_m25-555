import prompt

program_state = True

def state_waiting_command():
    command = prompt.string('Введите команду: ')

    try:
        available_actions[command]["command"]()
    except KeyError as e:
        print(f"Неверная команда {e}. Такой команды не существует")

def action_show_commands():
    print('')
    for command in available_actions.keys():
        print(available_actions[command]['description'])
    state_waiting_command()
    
def action_exit():
    global program_state

    program_state = False

def welcome():
    global program_state

    print("\nПервая попытка запустить проект!")
    print("\n***")
    while program_state:
        available_actions["help"]["command"]()
        print('')

available_actions = {
    "help" : {
        "command" : action_show_commands,
        "description" : "<command> help - справочная информация"
        },
    "exit" : {
        "command" : action_exit,
        "description" : "<command> exit - выйти из программы"
        },
}