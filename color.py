COLOR_SCHEME = "MONOKAI"

class Color:
    COLOR_MNK_RED = "#f92672"
    COLOR_MNK_MAGENTA = "#fd5ff0"
    COLOR_MNK_VIOLET = "#ae81ff"
    COLOR_MNK_BLUE = "#66d9ef"
    COLOR_MNK_GREEN = "#a6e22e"
    COLOR_MNK_YELLOW = "#e6db74"
    COLOR_MNK_ORANGE = "#fd971f"
    COLOR_MNK_CYAN = "#a1efe4"
    COLOR_MNK_BG0 = "#272822"
    COLOR_MNK_BG1 = "#3e3d32"
    COLOR_MNK_BG2 = "#75715e"
    COLOR_MNK_FG0 = "#f8f8f2"
    COLOR_MNK_FG1 = "#cfcfc2"

def change_color():
    global COLOR_SCHEME
    if COLOR_SCHEME == "MONOKAI":
        COLOR_SCHEME = "CUTE"
    else:
        COLOR_SCHEME = "MONOKAI"

def get_color_scheme():
    global COLOR_SCHEME
    return COLOR_SCHEME

def color_foreground():
    global COLOR_SCHEME
    if COLOR_SCHEME == "MONOKAI":
        return Color.COLOR_MNK_FG0
    else:
        return Color.COLOR_MNK_BG0

def color_background():
    global COLOR_SCHEME
    if COLOR_SCHEME == "MONOKAI":
        return Color.COLOR_MNK_BG0
    else:
        return Color.COLOR_MNK_FG0