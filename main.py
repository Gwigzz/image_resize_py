#coding:utf-8
import tkinter as tk
from image_resizer import ImageResizer
from setup import SetupManager, UIManager


if __name__ == "__main__":

    win         = tk.Tk()
    setup       = SetupManager()
    uiManager   = UIManager()

    WIN_WIDTH, WIN_HEIGHT, BG_COLOR = setup.setup_config_json_file()

    setup.download_and_setup_icon()

    win.title(f"Resize Img v {setup.APP_VERSION}")
    
    image_resizer_instance  = ImageResizer(win, BG_COLOR)

    win.minsize(620, 480)
    win.maxsize(1280, 720)

    # ico
    win.iconbitmap(r"ico.ico", default=r"ico.ico")

    # center window
    uiManager.center_window(win, WIN_WIDTH, WIN_HEIGHT)

    # menu
    mainMenu = tk.Menu(win)

    first_menu = tk.Menu(mainMenu, tearoff=0)
    first_menu.add_command(label="Images folder", command=setup.open_resize_directory)
    first_menu.add_command(label="Exit", command=win.quit)

    second_menu = tk.Menu(mainMenu, tearoff=0)
    second_menu.add_command(label="Source code", state="normal", command=uiManager.open_web_page_source_code)
    # second_menu.add_command(label="Help", state="normal")
    second_menu.add_command(label=f"Version: {setup.APP_VERSION }", state="disabled", underline=1)

    mainMenu.add_cascade(label="Menu", menu=first_menu)
    mainMenu.add_cascade(label="About", menu=second_menu)


    # btn bottom quit app
    btn_quit = tk.Button(win, text="Exit", command=win.quit)
    btn_quit.pack(pady=20, padx=20, side="right", anchor="se")  

    win.config(bg=BG_COLOR, menu=mainMenu)



    win.mainloop()