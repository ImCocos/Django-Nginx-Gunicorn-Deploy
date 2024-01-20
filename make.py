import os


path = input('Enter an absolute path to your bashrc/zshrc file(to make aliases): ')
if not os.path.exists(path):
    raise ValueError(f'Path "{path}" does  not exists!')


with open(path, 'a') as file:
    file.write(f'\nalias sitemanager="python3.11 {os.path.join(os.path.dirname(__file__), "main.py")}"')
