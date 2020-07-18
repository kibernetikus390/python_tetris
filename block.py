import stage
from color import Color


class Block:
    """
    テトリミノを定義するクラスです。
    """
    SIZE = 4    # ブロックのサイズ
    SCALE = 32  # 描画サイズ
    SCALE_INCOMING = 6 # 描画サイズ(メニュー)
    TYPE_O = 0
    TYPE_I = 1
    TYPE_T = 2
    TYPE_S = 3
    TYPE_Z = 4
    TYPE_J = 5
    TYPE_L = 6
    TYPE_MOSAIC = 7
    TYPE_TREE = 8
    TYPE_MAX = TYPE_L
    ROT_0 = 0
    ROT_90 = 1
    ROT_180 = 2
    ROT_270 = 3

    def __init__(self):
        """
        テトリミノブロックのポジションを初期化し
        ブロックを生成する
        """
        self.pos_x = int(stage.Stage.WIDTH / 2 - Block.SIZE / 2)
        self.pos_y = -2
        self.blocks = [
            # O-Block
            [
                # O-0deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 1, 1, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0]
                ],
                # O-90deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 1, 1, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0]
                ],
                # O-180deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 1, 1, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0]
                ],
                # O-270deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 1, 1, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0]
                ]
            ],
            # I-Block
            [
                # O-0deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0]
                ],
                # O-90deg-Block
                [
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 0, 0]
                ],
                # O-180deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0]
                ],
                # O-270deg-Block
                [
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 0, 0]
                ]
            ],
            # T-Block
            [
                # T-0deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 1, 0, 0],
                    [1, 1, 1, 0],
                    [0, 0, 0, 0]
                ],
                # O-270deg-Block
                [
                    [0, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0]
                ],
                # O-180deg-Block
                [
                    [0, 0, 0, 0],
                    [1, 1, 1, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0]
                ],
                # O-90deg-Block
                [
                    [0, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0]
                ]
            ],
            # S-Block
            [
                # S-0deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 1, 1, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0]
                ],
                # S-90deg-Block
                [
                    [1, 0, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0]
                ],
                # S-180deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 1, 1, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0]
                ],
                # S-270deg-Block
                [
                    [1, 0, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0]
                ]
            ],
            # Z-Block
            [
                # Z-0deg-Block
                [
                    [0, 0, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0]
                ],
                # Z-90deg-Block
                [
                    [0, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 0, 0, 0],
                    [0, 0, 0, 0]
                ],
                # Z-180deg-Block
                [
                    [0, 0, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0]
                ],
                # Z-270deg-Block
                [
                    [0, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 0, 0, 0],
                    [0, 0, 0, 0]
                ]
            ],
            # J-Block
            [
                # J-0deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 1, 1],
                    [0, 0, 0, 0]
                ],
                # J-90deg-Block
                [
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0]
                ],
                # J-180deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 1, 1, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 0]
                ],
                # J-270deg-Block
                [
                    [0, 1, 1, 0],
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0]
                ]
            ],
            # L-Block
            [
                # L-0deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 0, 0, 1],
                    [0, 1, 1, 1],
                    [0, 0, 0, 0]
                ],
                # L-90deg-Block
                [
                    [0, 1, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 0]
                ],
                # L-180deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 1, 1, 1],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0]
                ],
                # L-270deg-Block
                [
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0]
                ]
            ],
            # *-Block
            [
                # *-0deg-Block
                [
                    [1, 0, 1, 0],
                    [0, 1, 0, 1],
                    [1, 0, 1, 0],
                    [0, 1, 0, 1]
                ],
                # *-90deg-Block
                [
                    [0, 1, 0, 1],
                    [1, 0, 1, 0],
                    [0, 1, 0, 1],
                    [1, 0, 1, 0]
                ],
                # *-180deg-Block
                [
                    [1, 0, 1, 0],
                    [0, 1, 0, 1],
                    [1, 0, 1, 0],
                    [0, 1, 0, 1]
                ],
                # *-270deg-Block
                [
                    [0, 1, 0, 1],
                    [1, 0, 1, 0],
                    [0, 1, 0, 1],
                    [1, 0, 1, 0]
                ]
            ],
            # TREE-Block
            [
                # *-0deg-Block
                [
                    [0, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 1, 0, 0]
                ],
                # *-90deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 0, 1, 0],
                    [1, 1, 1, 1],
                    [0, 1, 0, 0]
                ],
                # *-180deg-Block
                [
                    [0, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 1, 0, 0]
                ],
                # *-270deg-Block
                [
                    [0, 0, 0, 0],
                    [0, 0, 1, 0],
                    [1, 1, 1, 1],
                    [0, 1, 0, 0]
                ]
            ]
        ]

    def get_cell_data(self, block_type, rot, x, y):
        """
        指定されたブロックの1マスのデータを主直
        """
        return self.blocks[block_type][rot][y][x]

def get_color(type):
    if type == Block.TYPE_O:
        return Color.COLOR_MNK_YELLOW
    elif type == Block.TYPE_I:
        return Color.COLOR_MNK_CYAN
    elif type == Block.TYPE_T:
        return Color.COLOR_MNK_VIOLET
    elif type == Block.TYPE_S:
        return Color.COLOR_MNK_GREEN
    elif type == Block.TYPE_Z:
        return Color.COLOR_MNK_RED
    elif type == Block.TYPE_J:
        return Color.COLOR_MNK_BLUE
    else:
        return Color.COLOR_MNK_ORANGE

def get_color_image(type):
    if type == Block.TYPE_O:
        return Color.COLOR_MNK_YELLOW
    elif type == Block.TYPE_I:
        return Color.COLOR_MNK_CYAN
    elif type == Block.TYPE_T:
        return Color.COLOR_MNK_VIOLET
    elif type == Block.TYPE_S:
        return Color.COLOR_MNK_GREEN
    elif type == Block.TYPE_Z:
        return Color.COLOR_MNK_RED
    elif type == Block.TYPE_J:
        return Color.COLOR_MNK_BLUE
    else:
        return Color.COLOR_MNK_ORANGE