#coding:utf-8
import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

APP_VERSION     = "0.2"

WIN_WIDTH       = 850
WIN_HEIGHT      = 600

BG_COLOR        = "#008EC9"


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
        self.image_label = tk.Label(self.win, text=f"Resize image V {APP_VERSION}", background=BG_COLOR, font=('Helvetica', 25), fg="#fff")
        self.image_label.pack(pady=10)

        # Btn for select image
        select_button = tk.Button(self.win, text="Sélectionner une image", command=self.load_image)
        select_button.pack(pady=10)

        # Dimension Frame label/entry for W & H
        dimension_frame = tk.Frame(self.win, background="orange")
        dimension_frame.pack(side="top", padx=5, pady=10)

        width_label = tk.Label(dimension_frame, text="Largeur:", background=BG_COLOR, fg="#fff")
        width_label.pack(side="left")
        width_entry = tk.Entry(dimension_frame, textvariable=self.width_var, width=6)
        width_entry.pack(side="left")

        height_label = tk.Label(dimension_frame, text="Hauteur:", background=BG_COLOR, fg="#fff")
        height_label.pack(side="left")
        height_entry = tk.Entry(dimension_frame, textvariable=self.height_var, width=6)
        height_entry.pack(side="left")

        # new image name (not required)
        image_name_label = tk.Label(self.win, text="Nom image (optionnel):", background=BG_COLOR, fg="#fff")
        image_name_label.pack()
        image_name_entry = tk.Entry(self.win, textvariable=self.image_name_var)
        image_name_entry.pack()

        # Btn resizing img
        resize_button = tk.Button(self.win, text="Redimensionner", command=self.resize_image)
        resize_button.pack(pady=10)

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
                messagebox.showerror("Erreur", "Veuillez séléctionner une image")
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

            messagebox.showinfo("Terminé", "L'image a été redimensionnée avec succès et enregistrée.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des dimensions valides.")



if __name__ == "__main__":
    win = tk.Tk()
    app = ImageResizer(win)

    win.minsize(620, 480)
    win.maxsize(1280, 720)

   
    """
    Centre la fenêtre
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
    first_menu.add_command(label="Quitter", command=win.quit)

    second_menu = tk.Menu(mainMenu, tearoff=0)
    second_menu.add_command(label="Help", state="disabled")

    mainMenu.add_cascade(label="Menu", menu=first_menu)
    mainMenu.add_cascade(label="About", menu=second_menu)


    # btn qui
    btn_quit = tk.Button(win, text="Quitter", command=win.quit)
    btn_quit.pack(pady=20, padx=20, side="right", anchor="se")  




    win.config(background=BG_COLOR, menu=mainMenu)

    win.mainloop()