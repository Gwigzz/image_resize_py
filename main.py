#coding:utf-8
import os
import json
import webbrowser
import requests
import tkinter as tk
# from PIL import Image, ImageTk
from image_resizer import ImageResizer
from tkinter import filedialog, messagebox

APP_VERSION     = "0.0.4"
JSON_FILE_NAME  = "config.json"

# Try to Load the informations of configuration from JSON file
try:
    with open(f"{JSON_FILE_NAME}", "r") as config_file:
        data_config_json = json.load(config_file)
except FileNotFoundError:
    messagebox.showwarning(f"Missing {JSON_FILE_NAME}", f"The {JSON_FILE_NAME} file was not found, we created it !")

    # default config.json
    default_config = {
        "window_width": 850,
        "window_height": 600,
        "bg_color": "#008EC9"
    }

    with open(f"{JSON_FILE_NAME}", "w") as config_file:
        json.dump(default_config, config_file)
    # load the informations of config after creation
    data_config_json = default_config


WIN_WIDTH   = data_config_json.get("window_width", 850)
WIN_HEIGHT  = data_config_json.get("window_height", 600)
BG_COLOR    = data_config_json.get("bg_color", "#008EC9")


def open_resize_directory():
    current_directory = os.getcwd()
    resize_directory = os.path.join(current_directory, f"resize")

    # Check if directory 'resize' exist
    if os.path.exists(resize_directory):
        os.startfile(resize_directory)
        messagebox.showinfo("Open Dir", "The directory has been opened")
    else:
        messagebox.showerror("Error", "The folder 'resize' cannot be found")


def open_web_page_source_code():
    webbrowser.open("https://github.com/Gwigzz/image_resize_py")


if __name__ == "__main__":
    win                     = tk.Tk()
    image_resizer_instance  = ImageResizer(win, APP_VERSION, BG_COLOR)

    win.minsize(620, 480)
    win.maxsize(1280, 720)

    win.iconbitmap(f"ico.ico")

    """
    Center Window
    """
    screen_x = int(win.winfo_screenwidth())
    screen_y = int(win.winfo_screenheight())
    posX = (screen_x // 2) - (WIN_WIDTH // 2)
    posY = (screen_y // 2) - (WIN_HEIGHT // 2)
    geo = "{}x{}+{}+{}".format(WIN_WIDTH, WIN_HEIGHT, posX, posY)
    win.geometry(geo)


    # menu
    mainMenu = tk.Menu(win)

    first_menu = tk.Menu(mainMenu, tearoff=0)
    first_menu.add_command(label="Images folder", command=open_resize_directory)
    first_menu.add_command(label="Exit", command=win.quit)

    second_menu = tk.Menu(mainMenu, tearoff=0)
    second_menu.add_command(label="Source code", state="normal", command=open_web_page_source_code)
    # second_menu.add_command(label="Help", state="normal")
    second_menu.add_command(label=f"Version: {APP_VERSION }", state="disabled", underline=1)

    mainMenu.add_cascade(label="Menu", menu=first_menu)
    mainMenu.add_cascade(label="About", menu=second_menu)


    # btn bottom quit app
    btn_quit = tk.Button(win, text="Exit", command=win.quit)
    btn_quit.pack(pady=20, padx=20, side="right", anchor="se")  

    win.config(bg=BG_COLOR, menu=mainMenu)

    win.mainloop()