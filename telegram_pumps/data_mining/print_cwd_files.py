import os


def print_directory_files():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        print(f)
