from menu_builder import MenuBuilder


def main():
    MenuBuilder('Строительные блоки. %page% // %pages%',
                'building_blocks',
                'shop_building_blocks%page%',
                'shop_building_blocks').generate()


if __name__ == '__main__':
    main()
