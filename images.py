import tkinter
from color import Color

class Images:
    PATH_BASE = "C:\\Users\\0221PG\\Desktop\\Meine Proiekt\\python\\tetris\\asset\\cute\\"

    def __init__(self):
        self.paths = ["bedrock.png",     # 0
                      "brown.png",       # 1
                      "cyan.png",        # 2
                      "green.png",      # 3
                      "orange.png",     # 4
                      "pink.png",       # 5
                      "purple.png",     # 6
                      "rainbow.png",    # 7
                      "red.png",        # 8
                      "white.png",      # 9
                      "yellow.png"]     # 10
        self.images = []
        for i in range(len(self.paths)):
            self.images.append(tkinter.PhotoImage(file=(Images.PATH_BASE+self.paths[i])))
            self.images[i] = self.images[i].subsample(1, 1)  # divide by 4
            self.images[i] = self.images[i].zoom(1, 1)  # zoom x 2

    def get_image_path(self, color):
        if color == Color.COLOR_MNK_YELLOW:
            return self.images[10]
        elif color == Color.COLOR_MNK_CYAN:
            return self.images[2]
        elif color == Color.COLOR_MNK_VIOLET:
            return self.images[6]
        elif color == Color.COLOR_MNK_GREEN:
            return self.images[3]
        elif color == Color.COLOR_MNK_RED:
            return self.images[8]
        elif color == Color.COLOR_MNK_BLUE:
            return self.images[5]
        elif color == Color.COLOR_MNK_ORANGE:
            return self.images[4]
        elif color == Color.COLOR_MNK_BG2:
            return self.images[7]
        else:
            return self.images[0]