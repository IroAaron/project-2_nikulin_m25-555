import json

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