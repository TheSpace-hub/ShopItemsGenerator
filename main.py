from typing import Any
from math import ceil

import json

import yaml


def get_building_blocks() -> dict[str, dict[str, Any]]:
    with open('blocks.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def get_menu_template(menu_index: int, pages: int) -> dict:
    return {
        'size': 45,
        'menu_title': f'Магазин СБ // Страница {menu_index}',
        'items': {
            'arrow_back': {
                'display_name': '&bВернуться в магазин',
                'left_click_commands': ['[openguimenu] shop'],
                'material': 'basehead-eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvYjZlMTRmMmI3ZDFmNWNiNmY1NmFiM2U2ODgxZmM4NDkwZWRhNmZmMmQxZDQ4YTMyNDFkMTQ3MjIzY2IzIn19fQ==',
                'slot': 0
            },
            'arrow_next': {
                'display_name': '&bВернуться в магазин',
                'left_click_commands': [
                    f'[openguimenu] shop_building_blocks_{menu_index + 1 if menu_index + 1 <= pages else 1}'],
                'material': 'basehead-eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvNDJiMGMwN2ZhMGU4OTIzN2Q2NzllMTMxMTZiNWFhNzVhZWJiMzRlOWM5NjhjNmJhZGIyNTFlMTI3YmRkNWIxIn19fQ==',
                'slot': 26
            },
            'arrow_prev': {
                'display_name': '&bВернуться в магазин',
                'left_click_commands': [
                    f'[openguimenu] shop_building_blocks_{menu_index - 1 if menu_index - 1 >= 1 else pages}'],
                'material': 'basehead-eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvZDU5YmUxNTU3MjAxYzdmZjFhMGIzNjk2ZDE5ZWFiNDEwNDg4MGQ2YTljZGI0ZDVmYTIxYjZkYWE5ZGIyZDEifX19',
                'slot': 18
            },

        }
    }


def main():
    slot = 10
    menu_index = 1

    blocks = get_building_blocks()

    print(ceil(len(blocks) / 21))

    menu: dict = get_menu_template(menu_index, ceil(len(blocks) / 21))

    for material, value in blocks.items():
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
            menu: dict = get_menu_template(menu_index, ceil(len(blocks) / 21))
    with open(f'shop_building_blocks_{menu_index}.yml', 'w', encoding='utf-8') as file:
        file.write(yaml.dump(menu, allow_unicode=True))


if __name__ == '__main__':
    main()
