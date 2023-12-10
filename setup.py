import os
import json
import ctypes
import requests
import webbrowser
from tkinter import messagebox



APP_VERSION             = "0.0.5"
TITLE_APP               = f"Resizer IMG V {APP_VERSION}"

JSON_FILE_CONF_NAME     = "config.json"

ICON_URL                = "https://raw.githubusercontent.com/Gwigzz/image_resize_py/main/ico.ico"
SOURCE_CODE_LINK        = "https://github.com/Gwigzz/image_resize_py"


class SetupManager:
    
    def __init__(self):

        self.APP_VERSION        = APP_VERSION
        self.JSON_FILE_NAME     = JSON_FILE_CONF_NAME
        self.ICON_URL           = ICON_URL
        self.TITLE_APP          = TITLE_APP

    def setup_config_json_file(self):
        try:
            with open(self.JSON_FILE_NAME, "r") as config_file:
                data_config_json = json.load(config_file)
        except FileNotFoundError:
            messagebox.showwarning(f"Missing {self.JSON_FILE_NAME}", f"The {self.JSON_FILE_NAME} file was not found, we created it !")

            # default config.json
            default_config = {
                "window_width": 850,
                "window_height": 600,
                "bg_color": "#008EC9"
            }

            with open(self.JSON_FILE_NAME, "w") as config_file:
                json.dump(default_config, config_file)
            # load the informations of config after creation
            data_config_json = default_config

        WIN_WIDTH   = data_config_json.get("window_width", 850)
        WIN_HEIGHT  = data_config_json.get("window_height", 600)
        BG_COLOR    = data_config_json.get("bg_color", "#008EC9")

        return WIN_WIDTH, WIN_HEIGHT, BG_COLOR


    def download_and_setup_icon(self):
        if not os.path.isfile("ico.ico"):
            messagebox.showwarning("Icon empty", "The icon is not present. Download in progress...")
            if self.download_icon():
                # print("Téléchargement réussi.")
                messagebox.showinfo("Success Ico", "Successful download icon.")
            else:
                print("Download failed. The application may not function properly without the icone")

    def download_icon(self):
        response = requests.get(self.ICON_URL)
        
        if response.status_code == 200:
            with open(r"ico.ico", "wb") as icon_file:
                icon_file.write(response.content)
            return True
        else:
            return False


    def open_resize_directory(self):
        current_directory = os.getcwd()
        resize_directory = os.path.join(current_directory, f"resize")

        # Check if directory 'resize' exist
        if os.path.exists(resize_directory):
            os.startfile(resize_directory)
            messagebox.showinfo("Open Dir", "The directory has been opened")
        else:
            messagebox.showerror("Error", "The folder 'resize' cannot be found")



class UIManager:

    def __init__(self):

        self.SOURCE_CODE   = SOURCE_CODE_LINK


    def center_window(self, win, WIN_WIDTH, WIN_HEIGHT):
        screen_x = int(win.winfo_screenwidth())
        screen_y = int(win.winfo_screenheight())
        posX     = (screen_x // 2) - (WIN_WIDTH // 2)
        posY     = (screen_y // 2) - (WIN_HEIGHT // 2)
        geo      = "{}x{}+{}+{}".format(WIN_WIDTH, WIN_HEIGHT, posX, posY)
        win.geometry(geo)

    def open_web_page_source_code(self):
        webbrowser.open(f"{self.SOURCE_CODE}")

    
    
    # def set_app_user_model_id(self, app_id):
    #     try:
    #         ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    #     except Exception as e:
    #         print(f"Failed to set AppUserModelID: {e}")