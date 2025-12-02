import json
import time
from functools import wraps

import prompt


def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. " \
            "Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except IndexError as e:
            print(f"Ошибка: Неверный индекс {e} коллекции")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
        except json.JSONDecodeError as e:
            print(f"Ошибка вывода данных {e}")
    return wrapper

def confirm_action(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            match action_name:
                case 'удаление таблицы':
                    command = prompt.string('\n>>>Вы уверены, ' \
                    'что хотите выполнить "удаление таблицы"? [y/n]: ')
                    match command:
                        case 'y':
                            return func(*args, **kwargs)
                        case 'n':
                            print("Отмена удаления")
                            return None
                        case _:
                            print("Команда неккоректна, " \
                            "операция удаления отменена")
                            return None
                case 'удаление строк':
                    command = prompt.string('\n>>>Вы уверены, ' \
                    'что хотите выполнить "удаление строк"? [y/n]: ')
                    match command:
                        case 'y':
                            return func(*args, **kwargs)
                        case 'n':
                            print("Отмена удаления")
                            return None
                        case _:
                            print("Команда неккоректна, " \
                            "операция удаления отменена")
                            return None
                case _:
                    print('Неверное наименование операции')
                    return None
        return wrapper
    return decorator

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        duration = end_time - start_time

        print(f"Функция {func.__name__} выполнилась за " + 
            f"{duration:.3f} секунд")
        return result
    
    return wrapper

def create_cacher():
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            print(f"[CACHE] Результат для '{key}' взят из кэша")
            return cache[key]
        
        result = value_func
        cache[key] = result
        print(f"[CACHE] Результат для '{key}' записан в кэш")
        return result

    return cache_result
    
