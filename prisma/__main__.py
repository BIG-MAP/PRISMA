import subprocess
import prisma


def main():
    
    prisma_path = '/'.join(prisma.__path__[0].split('\\')[:-1]) #fin path where prisma is installed
    gui_path = prisma_path +'/gui/'
    subprocess.run(['voila', gui_path + 'GUI.ipynb']) #Open GUI with voila


if __name__ == '__main__':
    main()
