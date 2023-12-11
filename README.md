## Image resize V 0.0.5

* A simple application for resizing images

### Python libs used in project
``` python
import os
import time
import json
import ctypes
import requests
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from PIL import Image, ImageTk
from setup import SetupManager, UIManager
from tkinter import messagebox, filedialog, ttk
```

### config.json
`
The config.json file is automatically generated if it doesn't exist.
`
``` json
{
    "window_width": 850,
    "window_height": 600,
    "bg_color": "#008EC9",
    "resized_image_folder_name": "resize"
}
```

#### Compilation with pyinstaller
> pyinstaller --onefile --windowed --noconsole --icon="ico.ico" main.py