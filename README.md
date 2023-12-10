## Image resize V 0.0.5

* A simple application for resizing images

### Python libs used in project
``` python
import os
import json
import ctypes
import requests
import webbrowser
import tkinter as tk
from setup import SetupManager
from PIL import Image, ImageTk
from image_resizer import ImageResizer
from tkinter import filedialog, messagebox
```

### config.json
`
The config.json file is automatically generated if it doesn't exist.
`
``` json
{
    "window_width": 850,
    "window_height": 600,
    "bg_color": "#008EC9"
}
```

### Compilation
> pyinstaller --onefile --windowed --noconsole --icon="ico.ico" main.py