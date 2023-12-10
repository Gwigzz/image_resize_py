#coding:utf-8
import os
import tkinter as tk
from PIL import Image, ImageTk
from setup import SetupManager, UIManager
from tkinter import messagebox, filedialog


class ImageResizer:
    """
    The main class Image Resize
    """
    def __init__(self, win, BG_COLOR):
        self.win = win

        self.BG_COLOR = BG_COLOR

        # var for save the dimensions
        self.width_var = tk.StringVar(value="150")
        self.height_var = tk.StringVar(value="115")

        self.image_name_var = tk.StringVar(value="resized_image") # deffault value

        # User Interface
        self.create_widgets()

    def create_widgets(self):
        # Label for display image
        self.image_label = tk.Label(self.win, text=f"Resize image", background=self.BG_COLOR, font=('Helvetica', 25), fg="#fff")
        self.image_label.pack(pady=10)

        # Btn for select image
        select_button = tk.Button(self.win, text="Select an image", command=self.load_image)
        select_button.pack(pady=10)



        # Dimension Frame label/entry for W & H
        dimension_frame = tk.Frame(self.win, background=self.BG_COLOR)
        dimension_frame.pack(side="top", padx=5, pady=10)

        width_label = tk.Label(dimension_frame, text="Width:", background=self.BG_COLOR, fg="#fff")
        width_label.pack(side="left", padx=3)
        width_entry = tk.Entry(dimension_frame, textvariable=self.width_var, width=6)
        width_entry.pack(side="left", padx=3)

        height_label = tk.Label(dimension_frame, text="Height:", background=self.BG_COLOR, fg="#fff")
        height_label.pack(side="left", padx=3)
        height_entry = tk.Entry(dimension_frame, textvariable=self.height_var, width=6)
        height_entry.pack(side="left", padx=3)


        # new image name (not required)
        image_name_label = tk.Label(self.win, text="Image name (optional):", background=self.BG_COLOR, fg="#fff")
        image_name_label.pack()
        image_name_entry = tk.Entry(self.win, textvariable=self.image_name_var)
        image_name_entry.pack()


        # Btn resizing img
        resize_button = tk.Button(self.win, text="Resize image", command=self.resize_image)
        resize_button.pack(pady=30, padx=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(file_path)

            print(self)

    def display_image(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((150, 150))  # Redimensionne l'image pour l'affichage
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        self.image_label.file_path = file_path

    def resize_image(self):
        try:

            if not hasattr(self, 'image'):
                messagebox.showwarning("Warning", "Please select an image")
                return

            width = int(self.width_var.get())
            height = int(self.height_var.get())

            # Creat folder "resize" if not exist
            output_folder = f"resize"
            os.makedirs(output_folder, exist_ok=True)

            # get the image name from user
            user_image_name = self.image_name_var.get().strip()
            if not user_image_name:
                user_image_name = "resized_image"

             # get the original extension
            original_image_path = getattr(self.image_label, 'file_path', '')
            _, original_extension = os.path.splitext(original_image_path)

            # resizing image
            resized_image = self.image.resize((width, height), Image.Resampling.BICUBIC)

            # save the image resizing in "resize" folder
            save_path = os.path.join(output_folder, f"{user_image_name}{original_extension}") 
            resized_image.save(save_path)

            messagebox.showinfo("Completed", "The image has been successfully resized and saved.")
        except ValueError:
            messagebox.showwarning("Warning", "Please enter valid dimensions.")





if __name__ == "__main__":

    win         = tk.Tk()
    setup       = SetupManager()
    uiManager   = UIManager()

    WIN_WIDTH, WIN_HEIGHT, BG_COLOR = setup.setup_config_json_file()

    # if not icon download it
    setup.download_and_setup_icon()

    win.title(setup.TITLE_APP)
    
    image_resizer_instance  = ImageResizer(win, BG_COLOR)

    win.minsize(620, 480)
    win.maxsize(1280, 720)

    # ico
    win.iconbitmap(r"ico.ico", default=r"ico.ico")

    # center window
    uiManager.center_window(win, WIN_WIDTH, WIN_HEIGHT)

    # set the app ID
    # uiManager.set_app_user_model_id(f"ResizeImgV{setup.APP_VERSION}")

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