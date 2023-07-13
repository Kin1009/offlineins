
from base64 import b64decode, b64encode
from shutil import make_archive, move
from sys import argv
from tkinter import Tk
from tkinter.ttk import Label
from zipfile import ZipFile
from os.path import isfile, isdir, basename, splitext
from os import remove
def create_installer(input_path, output_path):
    temp_zip_path = 'temp.zip'
    if isfile(input_path):
        with ZipFile(temp_zip_path, 'w') as zipf:
            zipf.write(input_path, basename(input_path))
    elif isdir(input_path):
        make_archive("temp", 'zip', input_path)
    else:
        print('Invalid input path.')
        return
    with open(temp_zip_path, 'rb') as zip_file:
        base64_data = b64encode(zip_file.read()).decode('utf-8')
    with open(output_path, 'w') as output_file:
        output_file.write(base64_data)
    remove(temp_zip_path)
    win.destroy()
def extract_installer(input_path, output_path):
    with open(input_path, 'r') as input_file:
        base64_data = input_file.read()
    temp_zip_path = 'temp.zip'
    with open(temp_zip_path, 'wb') as zip_file:
        zip_file.write(b64decode(base64_data))
    if output_path.endswith('.zip'):
        move(temp_zip_path, output_path)
    else:
        with ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_path)
    remove(temp_zip_path)
    win.destroy()
def a(): pass
if len(argv) == 2:
    win = Tk()
    win.resizable(0, 0)
    win.protocol("WM_DELETE_WINDOW", a)
    if argv[1].endswith(".ins"):
        win.title("Extracting...")
        Label(win, text="Extracting...").grid(column=0, row=0)
        win.after(1000, lambda: extract_installer(argv[1], argv[1][:-4]))
        win.mainloop()
    else:
        win.title("Packing...")
        Label(win, text="Packing...").grid(column=0, row=0)
        win.after(1000, lambda: create_installer(argv[1], splitext(argv[1])[0] + ".ins"))
        win.mainloop()