#coding:utf-8
import os
import json
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox


APP_VERSION     = "0.0.4"

# Try to Load the informations of configuration from JSON file
try:
    with open("config.json", "r") as config_file:
        data_config_json = json.load(config_file)
except FileNotFoundError:
    messagebox.showwarning("Info Config","The config.json file was not found, we created it !")
    # default config.json
    default_config = {
        "window_width": 850,
        "window_height": 600,
        "bg_color": "#008EC9"
    }
    with open("config.json", "w") as config_file:
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


class ImageResizer:
    """
    The main class Image Resize
    """
    def __init__(self, win):
        self.win = win
        self.win.title(f"Resize Img V {APP_VERSION}")

        # var for save the dimensions
        self.width_var = tk.StringVar(value="150")
        self.height_var = tk.StringVar(value="115")

        self.image_name_var = tk.StringVar(value="resized_image") # deffault value

        # User Interface
        self.create_widgets()

    def create_widgets(self):
        # Label for display image
        self.image_label = tk.Label(self.win, text=f"Resize image", background=BG_COLOR, font=('Helvetica', 25), fg="#fff")
        self.image_label.pack(pady=10)

        # Btn for select image
        select_button = tk.Button(self.win, text="Select an image", command=self.load_image)
        select_button.pack(pady=10)



        # Dimension Frame label/entry for W & H
        dimension_frame = tk.Frame(self.win, background=BG_COLOR)
        dimension_frame.pack(side="top", padx=5, pady=10)

        width_label = tk.Label(dimension_frame, text="Width:", background=BG_COLOR, fg="#fff")
        width_label.pack(side="left", padx=3)
        width_entry = tk.Entry(dimension_frame, textvariable=self.width_var, width=6)
        width_entry.pack(side="left", padx=3)

        height_label = tk.Label(dimension_frame, text="Height:", background=BG_COLOR, fg="#fff")
        height_label.pack(side="left", padx=3)
        height_entry = tk.Entry(dimension_frame, textvariable=self.height_var, width=6)
        height_entry.pack(side="left", padx=3)



        # new image name (not required)
        image_name_label = tk.Label(self.win, text="Image name (optional):", background=BG_COLOR, fg="#fff")
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
                messagebox.showerror("Error", "Please select an image")
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
            messagebox.showerror("Error", "Please enter valid dimensions.")



if __name__ == "__main__":
    win = tk.Tk()
    app = ImageResizer(win)

    win.minsize(620, 480)
    win.maxsize(1280, 720)

   
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
    first_menu.add_command(label="View Images", command=open_resize_directory)
    first_menu.add_command(label="Exit", command=win.quit)

    second_menu = tk.Menu(mainMenu, tearoff=0)
    second_menu.add_command(label="Help", state="normal")
    second_menu.add_command(label=f"Version: {APP_VERSION }", state="disabled", underline=1)

    mainMenu.add_cascade(label="Menu", menu=first_menu)
    mainMenu.add_cascade(label="About", menu=second_menu)


    # btn bottom quit app
    btn_quit = tk.Button(win, text="Exit", command=win.quit)
    btn_quit.pack(pady=20, padx=20, side="right", anchor="se")  

    win.config(bg=BG_COLOR, menu=mainMenu)

    win.mainloop()