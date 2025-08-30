from typing import Any
from math import ceil

import json

import yaml


def get_building_blocks() -> dict[str, dict[str, Any]]:
    with open('blocks.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def get_menu_template(menu_index: int) -> dict:
    return {
        'size': 45,
        'menu_title': f'Магазин строительных блоков // Страница {menu_index}',
        'items': {}
    }


def main():
    slot = 10
    menu_index = 1

    menu: dict = get_menu_template(menu_index)

    for material, value in get_building_blocks().items():
        name: str = value['name']
        price: int = value['price'] * 16
        menu['items'][material] = {
            'material': material,
            'amount': 16,
            'display_name': f'&b{name}',
            'slot': slot,
            'lore': [
                f'&7Купить ЛКМ за {price}₽',
                f'&7Продать ПКМ за {ceil(price / 2)}₽'
            ],
            'left_click_commands': [
                f'[console] give %player_name% {material} 16',
                f'[takemoney] {price}'
            ],
            'left_click_requirement': {
                'requirements': {
                    'has_money': {
                        'type': 'has money',
                        'amount': price
                    }
                },
                'deny_commands': ['[message]&b| &cТебе нужны деньги для этого!']
            },
            'right_click_commands': [
                f'[console] clear %player_name% {material} 16',
                f'[givemoney] {ceil(price / 2)}'
            ],
            'right_click_requirement': {
                'requirements': {
                    'has_money': {
                        'type': 'has item',
                        'material': material
                    }
                },
                'deny_commands': ['[message]&b| &cУ тебя нету этого в инвентаре!']
            }
        }

        slot += 1
        if slot == 17:
            slot = 19
        elif slot == 26:
            slot = 28
        elif slot == 35:
            with open(f'shop_building_blocks_{menu_index}.yml', 'w', encoding='utf-8') as file:
                file.write(yaml.dump(menu, allow_unicode=True))
            menu_index += 1
            slot = 10
            menu: dict = get_menu_template(menu_index)
    with open(f'shop_building_blocks_{menu_index}.yml', 'w', encoding='utf-8') as file:
        file.write(yaml.dump(menu, allow_unicode=True))


if __name__ == '__main__':
    main()
