import json
import os.path
from math import ceil

import yaml


class MenuBuilder:
    def __init__(self, name: str, data: str, prefix: str, folder: str):
        """
        Создание экземпляра меню
        :param name: Отображаемое название с заменой %page% на номер страницы, а %pages% на кол-во страниц.
        :param data: Имя файла с параметрами.
        :param prefix: Префикс для файла с заменой %page% на номер страницы.
        :param folder: Папка, в которую будут сохранены меню.
        """
        self.name: str = name
        self.items: dict[str, dict[str, str | int]] = self.get_items(os.path.join('input', data + '.json'))
        self.prefix: str = prefix
        self.folder: str = folder

    def generate(self):
        """
        Сгенерировать файлы меню.
        :return:
        """
        index: int = 0

        if not os.path.exists(os.path.join('output', self.folder)):
            os.mkdir(os.path.join('output', self.folder))

        for page in self.build_all_pages():
            index += 1
            with open(os.path.join('output', self.folder,
                                   f'{self.prefix}.yml'.replace('%page%', str(index))
                                   ), 'w', encoding='utf-8') as file:
                file.write(yaml.dump(page, allow_unicode=True))

    def build_all_pages(self) -> list[dict]:
        """
        Собрать все страницы.
        :return: Список из страниц.
        """
        pages: list[dict[str, int]] = []
        items: dict = {}
        for material, price in self.items.items():
            items[material] = price
            if len(items) == 21:
                pages.append(self.build_page(len(pages) + 1, items))
                items = {}

        if len(items) > 0:
            pages.append(self.build_page(len(pages) + 1, items))

        return pages

    def build_page(self, page: int, items: dict[str, int]) -> dict:
        """
        Собрать страницу.
        :param page: Номер страницы.
        :param items: Список предметов.
        :return: Страница.
        """
        page: dict = self.get_menu_template(page)

        index: int = 0
        for material, price in items.items():
            slot: int = self.get_slot_by_index(index)
            page['items'][material] = self.get_item(slot, material, price)
            index += 1

        return page

    @classmethod
    def get_items(cls, data: str) -> dict[str, dict[str, str | int]]:
        """
        Получение предметов и цен.
        :param data: Путь до файла с параметрами.
        """
        with open(data, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    def get_menu_template(self, page: int):
        """
        Получение шаблона страницы.
        :param page: Номер страницы.
        :return: Шаблон меню.
        """
        pages: int = ceil(len(self.items) / 21)
        return {
            'size': 45,
            'menu_title': self.name.replace('%page%', str(page)).replace('%pages%', str(pages)),
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
                        f'[openguimenu] shop_building_blocks_{page + 1 if page + 1 <= pages else 1}'],
                    'material': 'basehead-eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvNDJiMGMwN2ZhMGU4OTIzN2Q2NzllMTMxMTZiNWFhNzVhZWJiMzRlOWM5NjhjNmJhZGIyNTFlMTI3YmRkNWIxIn19fQ==',
                    'slot': 26
                },
                'arrow_prev': {
                    'display_name': '&bВернуться в магазин',
                    'left_click_commands': [
                        f'[openguimenu] shop_building_blocks_{page - 1 if page - 1 >= 1 else pages}'],
                    'material': 'basehead-eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvZDU5YmUxNTU3MjAxYzdmZjFhMGIzNjk2ZDE5ZWFiNDEwNDg4MGQ2YTljZGI0ZDVmYTIxYjZkYWE5ZGIyZDEifX19',
                    'slot': 18
                }
            }
        }

    @classmethod
    def get_item(cls, slot: int, material: str, price: int):
        """
        Получить ячейку с предметом.
        :param slot: Слот предмета.
        :param material: Материал.
        :param price: Цена за предмет.
        :return: Ячейка с предметом.
        """
        return {
            'material': material,
            'amount': 16,
            'slot': slot,
            'lore': [
                '',
                f'&a ▸ Купить ЛКМ за &f{price}₽',
                f'&a ▸ Продать ПКМ за &f{ceil(price / 2)}₽'
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

    @staticmethod
    def get_slot_by_index(index: int) -> int:
        """
        Получить слот в зависимости от индекса.
        :return: Номер слота.
        """
        if 0 <= index <= 6:
            return index + 10
        elif 7 <= index <= 13:
            return index + 12
        elif 14 <= index <= 20:
            return index + 14
        return -1
