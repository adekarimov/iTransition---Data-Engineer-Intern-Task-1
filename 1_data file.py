import re
import json

def fix_quotes(text):
    # кавычка
    return re.sub(r'(?<=\w)"(?=\w)', r'\\"', text)


def load_data(file_path):
    data = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # объекты
    items = re.split(r'},\s*{', content)

    for i, item in enumerate(items):
        item = item.strip()

        # фигурные скобки
        if not item.startswith('{'):
            item = '{' + item
        if not item.endswith('}'):
            item = item + '}'

        # ruby → json
        item = re.sub(r':(\w+)=>', r'"\1":', item)

        # проблемные кавычки
        item = fix_quotes(item)

        # одинарные кавычки
        item = item.replace("'", '"')

        try:
            obj = json.loads(item)
            data.append(obj)
        except Exception as e:
            print(f"Skipped record {i}: {item[:100]}")

    print(f"Loaded records: {len(data)}")
    return data


if __name__ == "__main__":
    data = load_data("task1_d.json")

    # проверка
    print(type(data))
    print(data[:2])