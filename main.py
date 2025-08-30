from menu_builder import MenuBuilder


def main():
    MenuBuilder('Строительные блоки. %page% // %pages%',
                'building_blocks',
                'shop_building_blocks_%page%').generate()


if __name__ == '__main__':
    main()
