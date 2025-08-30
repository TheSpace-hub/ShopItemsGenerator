import shutil
import os

from menu_builder import MenuBuilder


def recreate_output():
    """
    Очищает папку 'output'.
    :return:
    """
    if os.path.exists('output'):
        shutil.rmtree('output')
    os.mkdir('output')


def main():
    recreate_output()

    MenuBuilder('Строительные блоки. %page% // %pages%',
                'building_blocks',
                'shop_building_blocks_%page%',
                'shop_building_blocks').generate()


if __name__ == '__main__':
    main()
