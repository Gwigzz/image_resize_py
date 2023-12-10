## Image resize V 0.0.4

* A simple application for resizing images

### Require python libs
``` python
import os
import json
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
```

### config.json
`
the file is automatically generated if it doesn't exist
`
``` json
{
    "window_width": 850,
    "window_height": 600,
    "bg_color": "#008EC9"
}
```