import tkinter
from color import Color
from pathlib import Path

class Images:
    def __init__(self):
        self.paths = ["\\asset\\cute\\bedrock.png",     # 0
                      "\\asset\\cute\\brown.png",       # 1
                      "\\asset\\cute\\cyan.png",        # 2
                      "\\asset\\cute\\green.png",      # 3
                      "\\asset\\cute\\orange.png",     # 4
                      "\\asset\\cute\\pink.png",       # 5
                      "\\asset\\cute\\purple.png",     # 6
                      "\\asset\\cute\\rainbow.png",    # 7
                      "\\asset\\cute\\red.png",        # 8
                      "\\asset\\cute\\white.png",      # 9
                      "\\asset\\cute\\yellow.png"]     # 10
        self.images = []
        for i in range(len(self.paths)):
            self.images.append(tkinter.PhotoImage(file=(Images.make_absolute_path(self.paths[i]))))
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

    @classmethod
    def make_absolute_path(self, relative_path):
        """
        相対パスを絶対パスへ変換
        """
        return (str(Path(__file__).parent) + relative_path).replace("\\", "/")