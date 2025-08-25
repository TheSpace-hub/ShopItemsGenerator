from typing import Any
from math import floor

import json

import yaml


def get_building_blocks() -> dict[str, dict[str, Any]]:
    with open('building_blocks.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def main():
    slot = 10
    menu_index = 1

    menu: dict = {
        'open_command': f'shop_building_block_{menu_index}',
        'size': 45,
        'menu_title': f'Магазин строительных блоков // Страница {menu_index}',
        'items': {}
    }

    for material, value in get_building_blocks().items():
        name: str = value['name']
        price: int = value['price']
        menu['items'][material] = {
            'material': material,
            'display_name': f'&b{name}',
            'slot': slot,
            'lore': [
                f'&7Купить ЛКМ за {price}₽',
                f'&7Продать ПКМ за {floor(price / 2)}₽'
            ]
        }

        slot += 1
        if slot == 17:
            slot = 19
        elif slot == 26:
            slot = 28
        elif slot == 35:
            with open(f'shop_building_blocks_{menu_index}.yml', 'w', encoding='utf-8') as file:
                file.write(yaml.dump(menu))
            menu_index += 1
            slot = 10
            menu: dict = {
                'open_command': f'shop_building_block_{menu_index}',
                'size': 45,
                'menu_title': f'Магазин строительных блоков // Страница {menu_index}',
                'items': {}
            }
    with open(f'shop_building_blocks_{menu_index}.yml', 'w', encoding='utf-8') as file:
        file.write(yaml.dump(menu))



if __name__ == '__main__':
    main()
