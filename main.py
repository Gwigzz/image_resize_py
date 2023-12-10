import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

APP_VERSION     = "0.2"

BG_COLOR        = "#008EC9"

WIN_WIDTH       = 850
WIN_HEIGHT      = 600


class ImageResizer:
    def __init__(self, win):
        self.win = win
        self.win.title(f"Resize Img V {APP_VERSION}")

        # Variables pour stocker les dimensions
        self.width_var = tk.StringVar(value="150")
        self.height_var = tk.StringVar(value="115")

        self.image_name_var = tk.StringVar(value="resized_image") # deffault value

        # Interface utilisateur
        self.create_widgets()

    def create_widgets(self):
        # Label pour afficher l'image
        self.image_label = tk.Label(self.win, text=f"Resize image V {APP_VERSION}", background=BG_COLOR, font=('Helvetica', 25), fg="#fff")
        self.image_label.pack(pady=10)

        # Bouton pour sélectionner l'image
        select_button = tk.Button(self.win, text="Sélectionner une image", command=self.load_image)
        select_button.pack(pady=10)

        # Entrées pour les dimensions
        width_label = tk.Label(self.win, text="Largeur:", background=BG_COLOR, fg="#fff")
        width_label.pack()
        width_entry = tk.Entry(self.win, textvariable=self.width_var)
        width_entry.pack()

        height_label = tk.Label(self.win, text="Hauteur:", background=BG_COLOR, fg="#fff")
        height_label.pack()
        height_entry = tk.Entry(self.win, textvariable=self.height_var)
        height_entry.pack()


        # new image name (not required)
        image_name_label = tk.Label(self.win, text="Nom image (optionnel):", background=BG_COLOR, fg="#fff")
        image_name_label.pack()
        image_name_entry = tk.Entry(self.win, textvariable=self.image_name_var)
        image_name_entry.pack()

        # Bouton pour redimensionner l'image
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

            # Créer le dossier 'resize' s'il nexiste pas
            output_folder = f"resize"
            os.makedirs(output_folder, exist_ok=True)

            # Obtenir le nom de l'image saisi par l'utilisateur
            user_image_name = self.image_name_var.get().strip()
            if not user_image_name:
                user_image_name = "resized_image"

             # Obtenir l'extension de l'image d'origine
            original_image_path = getattr(self.image_label, 'file_path', '')
            _, original_extension = os.path.splitext(original_image_path)

            # Redimensionne l'image
            resized_image = self.image.resize((width, height), Image.Resampling.BICUBIC)

            # Enregistre l'image redimensionnée dans le dossier courant
            save_path = os.path.join(output_folder, f"{user_image_name}{original_extension}") 
            resized_image.save(save_path)

            messagebox.showinfo("Terminé", "L'image a été redimensionnée avec succès et enregistrée.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des dimensions valides.")



if __name__ == "__main__":
    win = tk.Tk()
    app = ImageResizer(win)

    # win.title(f"Resize Img V {APP_VERSION}")

    win.minsize(620, 480)
    win.maxsize(1280, 720)

    win.config(background=BG_COLOR)
   
    """
    Centre la fenêtre
    """
    screen_x = int(win.winfo_screenwidth())
    screen_y = int(win.winfo_screenheight())
    posX = (screen_x // 2) - (WIN_WIDTH // 2)
    posY = (screen_y // 2) - (WIN_HEIGHT // 2)
    geo = "{}x{}+{}+{}".format(WIN_WIDTH, WIN_HEIGHT, posX, posY)
    win.geometry(geo)

    # btn qui
    btn_quit = tk.Button(win, text="Quitter", command=win.quit)
    btn_quit.pack(pady=20, padx=20, side="right", anchor="se")  



    win.mainloop()