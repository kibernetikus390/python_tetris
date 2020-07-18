import time

from stage import Stage
import tkinter
from block import Block, get_color
from color import Color
import tkinter.font as font
from images import Images
from color import Color, color_background, color_foreground, get_color_scheme


class Game:
    """
    ゲーム全体を管理するクラスです
    このクラスを生成し、start()メソッドを呼び出すことでゲームを開始します
    """
    delta = 0.0
    LOOP_TIMER = 10
    UI_WIDTH = 100

    def __init__(self, title, width, height):
        """
        ゲームの各パラメータの状態を初期化し、ゲームを開始させる準備をします
        title: ゲームタイトル
        width: 画面幅
        height: 画面高さ
        """
        self.title = title
        self.width = width + Game.UI_WIDTH
        self.height = height
        self.root = tkinter.Tk()
        self.root.bind("<KeyPress>", self.__input)
        self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height)
        self.stage = Stage(self)
        self.stage.game = self
        self.prev_timer = time.time()
        self.gameover_rendered = False
        self.font_gameover = font.Font(root=self.root, size=50)
        self.images = Images()
        self.reset()

    def reset(self):
        self.prev_timer = time.time()
        self.gameover_rendered = False


    def start(self):
        """
        ゲームを開始させるメソッドです
        """
        self.__init()

    def __init(self):
        """
        ゲームの初期化を行うメソッドです
        """
        self.__make_window()
        self.__game_loop()
        self.root.mainloop()

    def __make_window(self):
        """
        ゲーム画面を作成する
        """
        self.root.title(self.title)
        self.canvas.pack()

    def __game_loop(self):
        """
        ゲームのメインロジックを定義する
        """
        self.__delta()
        self.__update()
        self.__render()
        self.root.after(self.LOOP_TIMER, self.__game_loop)

    def __delta(self):
        self.new_timer = time.time()
        self.delta = self.new_timer - self.prev_timer
        self.prev_timer = self.new_timer

    def get_delta(self):
        return self.delta

    def __input(self, e):
        """
        ユーザーからの入力処理を定義します
        """
        self.stage.input(e.keysym)

    def __update(self):
        """
        ゲーム全体の更新処理を定義します
        """
        self.stage.update()
        pass

    def __render(self):
        """
        ゲームの描画処理を定義します
        """
        if self.gameover_rendered:
            return
        self.canvas.delete("block")

        # 背景
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=color_background(), tag="block")

        for y in range(Stage.HEIGHT):
            for x in range(Stage.WIDTH):
                # マスのデータを取得
                cel_data = self.stage.data[y][x]
                color = None
                if cel_data == Stage.CELL_BLOCK:
                    # 移動中のブロック
                    color = Stage.get_color(self.stage)
                elif cel_data == Stage.CELL_FIXED:
                    # 固定されたブロック
                    color = Color.COLOR_MNK_BG1
                elif cel_data == Stage.CELL_GHOST:
                    # 固定されたブロック
                    color = Color.COLOR_MNK_BG2
                else:
                    # その他(空)
                    continue
                # ゲームオーバーなら赤くする
                if self.stage.game_over:
                    self.canvas.create_text( Stage.WIDTH * Block.SCALE / 2, Stage.HEIGHT * Block.SCALE / 2,
                                             text="草", font=self.font_gameover, fill=color_foreground(), tag="block")
                    color = Color.COLOR_MNK_RED
                    self.gameover_rendered = True
                self.__render_block_main(x, y, color)

        self.__render_ui()

    def __render_ui(self):
        # 区切り線
        self.canvas.create_line(self.width-Game.UI_WIDTH, 0, self.width-Game.UI_WIDTH, self.height, fill=color_foreground(), tag="block")
        # Score
        base_x = Stage.WIDTH * Block.SCALE + Game.UI_WIDTH/2 - (Block.SCALE_INCOMING * Block.SIZE/2)
        base_y = 50
        self.canvas.create_text( Stage.WIDTH * Block.SCALE + Game.UI_WIDTH/2, 32, text="SCORE", fill=color_foreground(), tag="block")
        self.canvas.create_text( Stage.WIDTH * Block.SCALE + Game.UI_WIDTH/2, 50, text=str(self.stage.get_score()*100), fill=color_foreground(), tag="block")

        # HOLD
        base_y += 50
        holding = self.stage.hold_block
        if holding is not None:
            for local_y in range(Block.SIZE):
                for local_x in range(Block.SIZE):
                    if self.stage.block.get_cell_data(holding, 0, local_x, local_y) == 1:
                        self.__render_block_ui(
                            base_x + Block.SCALE_INCOMING*local_x,
                            base_y + Block.SCALE_INCOMING*local_y,
                            get_color(holding))

        self.canvas.create_text( Stage.WIDTH * Block.SCALE + Game.UI_WIDTH/2, 150, text="HOLD", fill=color_foreground(), tag="block")
        # NEXT
        self.canvas.create_text( Stage.WIDTH * Block.SCALE + Game.UI_WIDTH/2, 200, text="NEXT", fill=color_foreground(), tag="block")
        base_y = 225
        for i in range(Stage.INCOMING_MAX):
            for local_y in range(Block.SIZE):
                for local_x in range(Block.SIZE):
                    if self.stage.get_cell_data(local_x, local_y, 0, i) == Stage.CELL_BLOCK:
                        offset_x = 0
                        self.__render_block_ui(
                            base_x + Block.SCALE_INCOMING*local_x + offset_x,
                            base_y + Block.SCALE_INCOMING*local_y + i * 50,
                            get_color(self.stage.INCOMING_SET[i]))

    def __render_block_ui(self, screen_x, screen_y, color):
        """
        ブロック描画関数を呼び出すもの （UI用）
        """
        self.__render_block(
            screen_x, screen_y,
            screen_x + Block.SCALE_INCOMING, screen_y + Block.SCALE_INCOMING, color)

    def __render_block_main(self, pos_x, pos_y, color):
        """
        ブロック描画関数を呼び出すもの
        """
        if get_color_scheme() == "MONOKAI":
            self.__render_block(
                pos_x*Block.SCALE, pos_y*Block.SCALE,
                pos_x*Block.SCALE+Block.SCALE, pos_y*Block.SCALE+Block.SCALE, color)
        else:
            self.canvas.create_image(pos_x * Block.SCALE, pos_y * Block.SCALE, anchor=tkinter.NW,
                                     image=self.images.get_image_path(color), tag="block")

    def __render_block(self, start_x, start_y, end_x, end_y, color):
        """
        ブロック描画
        """
        self.canvas.create_rectangle(
            start_x, start_y, end_x, end_y,
            fill=color, outline=Color.COLOR_MNK_BG0, tag="block")