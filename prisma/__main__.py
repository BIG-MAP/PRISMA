# © Copyright 2021, PRISMA’s Authors

import subprocess
import prisma


def main():
    # Find path where prisma is installed
    prisma_path = '/'.join(prisma.__path__[0].split('\\')[:-1])
    gui_path = prisma_path + '/gui/'
    # Open GUI with voila
    subprocess.run(['voila', gui_path + 'GUI.ipynb'])


if __name__ == '__main__':
    main()
