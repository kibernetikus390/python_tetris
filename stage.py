import random
import block
from color import Color, color_background, change_color

class Stage:
    """
    テトリスの盤面を管理するクラス
    """
    game = 0    # Gameクラスの参照
    WIDTH = 10
    HEIGHT = 20
    CELL_NONE = 0   # 空
    CELL_BLOCK = 1  # ブロック
    CELL_FIXED = 2  # 固定ブロック
    CELL_GHOST = 3  # ゴーストブロック
    SPEEDUP = 0.005

    DROP_TIMER = 0.3    # ブロックが自然落下する時間
    GRACE_TIMER = 0.2   # ブロックが固定されるまでの猶予
    INCOMING_SET = []   # 次のブロック
    INCOMING_MAX = 5    # 次のブロック　表示最大数

    hold_block = None
    hold_used = False


    def __init__(self, game):
        """
        盤面を生成する
        """
        self.score = 0
        self.game_over = False
        self.data = [[Stage.CELL_NONE for x in range(Stage.WIDTH)] for y in range(Stage.HEIGHT)]
        self.block = block.Block()
        self.type = block.Block.TYPE_O
        self.rot = block.Block.ROT_0
        self.can_drop = True
        self.timer = 0.0
        self.grace_timer = 0.0
        self.__set_next_block()
        self.color_scheme = "MONOKAI"
        self.game = game

    def reset(self):
        self.score = 0
        self.hold_used = False
        self.DROP_TIMER = 0.3
        self.INCOMING_SET.clear()
        self.game_over = False
        self.data = [[Stage.CELL_NONE for x in range(Stage.WIDTH)] for y in range(Stage.HEIGHT)]
        self.block = block.Block()
        self.type = block.Block.TYPE_O
        self.rot = block.Block.ROT_0
        self.can_drop = True
        self.timer = 0.0
        self.grace_timer = 0.0
        self.__set_next_block()

    def update(self):
        """
        ステージの更新
        """
        self.timer += self.game.get_delta()         # タイマーを計算
        self.grace_timer += self.game.get_delta()   # タイマーを計算
        if self.game_over:
            pass
        else:
            self.__drop_block()                         # ブロックを落とす
            self.__write_current_block_to_stage()       # ブロックを書き込む

    def get_score(self):
        return self.score

    def delete_complete_line(self):
        """
        完成したラインを削除し、上のラインを詰める
        """
        for stage_y in range(Stage.HEIGHT):
            # 埋まったラインを探す
            is_filled = True
            for stage_x in range(Stage.WIDTH):
                if self.data[stage_y][stage_x] == Stage.CELL_NONE:
                    is_filled = False
                    break
            # 埋まったラインが見つかった場合
            if is_filled:
                self.score += 1
                # ラインを消す
                for stage_x in range(Stage.WIDTH):
                    self.data[stage_y][stage_x] = Stage.CELL_NONE
                # 消したラインより上のラインを下に詰める
                for shift_stage_y in reversed(range(stage_y+1)):
                    for shift_stage_x in reversed(range(Stage.WIDTH)):
                        from_x = shift_stage_x
                        from_y = shift_stage_y - 1
                        if not self.__is_position_out_of_stage(from_x, from_y):
                            self.data[shift_stage_y][shift_stage_x] = self.data[from_y][from_x]

    def hold(self):
        if self.hold_used:
            return
        self.hold_used = True
        if self.hold_block is None:
            self.hold_block = self.type
            self.__set_next_block()
        else:
            previous_type = self.__set_next_block(self.hold_block)
            self.hold_block = previous_type

    def input(self, key):
        """
        キー入力
        """
        if key == "space":
            # ポーズ
            self.can_drop = not self.can_drop
        elif key == "Escape":
            self.reset()
            self.game.reset()
        elif key == "c":
            change_color()
        elif key == "w":
            print("Input: HOLD")
            self.hold()
        elif key == "e":
            print("Input: ROTATE:e")
            # 回転
            self.__rotate(clockwise=True)
        elif key == "q":
            print("Input: ROTATE:q")
            # 回転
            self.__rotate(clockwise=False)
        elif key == "a" and not self.__is_collision_left():
            # 移動 左
            self.block.pos_x -= 1
        elif key == "s":
            # ハードドロップ
            self.__hard_drop()
        elif key == "d" and not self.__is_collision_right():
            # 移動 右
            self.block.pos_x += 1

    def __game_over(self):
        self.game_over = True
        for y in range(len(self.data)):
                print(self.data[y])

    def __rotate(self, clockwise=True):
        """
        ブロックを回転する
        clockwise : 時計回りか
        """
        # 新しい角度を求める
        new_rot = self.rot
        if clockwise:
            new_rot -= 1
        else:
            new_rot += 1
        if new_rot < block.Block.ROT_0:
            new_rot = block.Block.ROT_270
        elif block.Block.ROT_270 < new_rot:
            new_rot = block.Block.ROT_0

        # 新しい角度で、周りに干渉しないかチェック。スポーンできない場合は回転しない
        if not self.__is_block_collide_where(0, 0, new_rot):
            # 干渉しない
            self.rot = new_rot
        else:
            for offset_y in [0, 1, -1, 2, -2]:
                for offset_x in [1, -1, 2, -2]:
                    if not self.__is_block_collide_where(offset_x, offset_y, new_rot):
                        self.block.pos_x += offset_x
                        self.block.pos_y += offset_y
                        self.rot = new_rot
                        break
                else:
                    continue
                break

    def __drop_block(self):
        """
        ブロックを1つ下に(自然)落下させる
        """
        if self.timer < self.DROP_TIMER:
            return
        self.timer = 0.0

        if self.__is_collision_bottom():
            if self.grace_timer >= self.GRACE_TIMER:
                self.__fix_block()
        else:
            if self.can_drop:
                self.block.pos_y += 1
                self.grace_timer = 0.0

    def __hard_drop(self):
        """
        ハードドロップ
        """
        counter = 0
        while not self.__is_block_collide_where(0, 1, check_boundary=False):
            counter += 1
            self.block.pos_y += 1
        if counter == 0:
            self.grace_timer = self.GRACE_TIMER
        else:
            self.grace_timer = self.GRACE_TIMER/3

    def __fix_block(self):
        """
        ブロックを固定する
        """
        self.hold_used = False
        for object_y in range(block.Block.SIZE):
            for object_x in range(block.Block.SIZE):
                world_x = self.block.pos_x + object_x
                world_y = self.block.pos_y + object_y
                if not self.__is_position_out_of_stage(world_x, world_y) and\
                        self.block.get_cell_data(self.type, self.rot, object_x, object_y) == Stage.CELL_BLOCK:
                    self.data[world_y][world_x] = Stage.CELL_FIXED
        # 完了したラインを消す
        self.delete_complete_line()
        # 次に落とすブロックを設定する
        self.__set_next_block()
        # タイマーをへらす
        self.DROP_TIMER -= Stage.SPEEDUP

    def __set_next_block(self, type=None):
        """
        次に落下するブロックを設定する
        スポーンできない場合、ゲームオーバー
        :param: type 設定したいタイプ
        :return: タイプを設定していた場合、以前落下途中だったタイプを返す
        """
        self.block = block.Block()
        if type is None:
            # ブロックセットが空なら、次のを生成する
            if len(self.INCOMING_SET) <= Stage.INCOMING_MAX:
                block_types_list = [i for i in range(self.block.TYPE_MAX)]
                #self.INCOMING_SET = []
                for i in range(self.block.TYPE_MAX):
                    index_to_pop = random.randint(0, len(block_types_list)-1)
                    self.INCOMING_SET.append(block_types_list.pop(index_to_pop))
            # タイプと回転を初期化
            self.type = self.INCOMING_SET.pop(0)
        else:
            previous_type = self.type
            self.type = type
            return previous_type
        self.rot = block.Block.ROT_0

        if self.__is_block_collide_where(0, 0, rotation=0, check_boundary=False):
            self.__game_over()

    def __write_current_block_to_stage(self):
        """
        ステージにブロックを合成する
        :return:
        """
        # FIXED以外をNONEに書き換える
        for stage_y in range(Stage.HEIGHT):
            for stage_x in range(Stage.WIDTH):
                if self.data[stage_y][stage_x] == Stage.CELL_FIXED:
                    continue
                self.data[stage_y][stage_x] = Stage.CELL_NONE

        # 落下予測を書き込む
        predict_offset = self.__get_predict_position()
        self.__write_block_to_stage(self.block.pos_x, self.block.pos_y+predict_offset-1, Stage.CELL_GHOST)

        # ブロックの位置を書き込む
        self.__write_block_to_stage(self.block.pos_x, self.block.pos_y, Stage.CELL_BLOCK)

    def __get_predict_position(self):
        """
        落下予測位置の座標を取得する
        :return: 落下予測位置の座標
        """
        offset = 1
        while not self.__is_block_collide_where(0, offset):
            offset += 1
        return offset

    def __write_block_to_stage(self, pos_x, pos_y, data):
        """
        ブロックのソリッド部分をステージに書き込む
        :param pos_x: ブロックのx座標
        :param pos_y: ブロックのy座標
        :param data: 書き込むデータ
        """
        for object_y in range(block.Block.SIZE):
            for object_x in range(block.Block.SIZE):
                world_x = pos_x + object_x
                world_y = pos_y + object_y
                if self.__is_position_out_of_stage(world_x, world_y):
                    continue
                if self.data[world_y][world_x] in (Stage.CELL_FIXED,):
                    continue
                if self.get_cell_data(object_x, object_y, self.rot) == Stage.CELL_BLOCK:
                    self.data[world_y][world_x] = data

    def get_cell_data(self, local_x, local_y, rot=0, index=-1):
        if index == -1:
            return self.block.get_cell_data(self.type, rot, local_x, local_y)
        return self.block.get_cell_data(self.INCOMING_SET[index], rot, local_x, local_y)

    def __is_position_out_of_stage(self, world_x, world_y):
        """
        指定した座標が範囲外か調べる
        """
        return world_x < 0 or Stage.WIDTH <= world_x or world_y < 0 or Stage.HEIGHT <= world_y

    def __is_position_colliding_with_fixed(self, world_x, world_y):
        if 0 <= world_y < len(self.data) and 0 <= world_x < len(self.data[0]):
            return self.data[world_y][world_x] == Stage.CELL_FIXED
        else:
            return False

    def __is_collision_bottom(self, rot=-1):
        """
        下の衝突判定を行う
        """
        if rot == -1:
            rot = self.rot
        return self.__is_block_collide_where(0, 1, rot, False)

    def __is_collision_right(self, rot=-1, offset=0):
        """
        右の衝突判定を行う
        """
        if rot == -1:
            rot = self.rot
        return self.__is_block_collide_where(1+offset, 0, rot)

    def __is_collision_left(self, rot=-1, offset=0):
        """
        左の衝突判定を行う
        """
        if rot == -1:
            rot = self.rot
        return self.__is_block_collide_where(-1-offset, 0, rot)

    def __is_block_collide_where(self, offset_x=0, offset_y=0, rotation=-1, check_boundary=True):
        """
        下の衝突判定を行う
        ブロックのX,Y座標
        """
        if rotation == -1:
            rotation = self.rot

        pos_x = self.block.pos_x
        pos_y = self.block.pos_y

        for object_y in range(block.Block.SIZE):
            for object_x in range(block.Block.SIZE):
                world_x = pos_x + object_x + offset_x
                world_y = pos_y + object_y + offset_y
                if self.block.get_cell_data(self.type, rotation, object_x, object_y) == Stage.CELL_BLOCK:
                    if self.__is_position_colliding_with_fixed(world_x, world_y):
                        # 固定ブロックとのコリジョンチェック
                        return True
                    elif check_boundary and self.__is_position_out_of_stage(world_x, world_y):
                        # 境界線チェック
                        return True
                    elif self.HEIGHT <= world_y:
                        # 下線とのチェック
                        return True
                    else:
                        continue
        return False

    def get_color(self):
        if self.type == block.Block.TYPE_O:
            return Color.COLOR_MNK_YELLOW
        elif self.type == block.Block.TYPE_I:
            return Color.COLOR_MNK_CYAN
        elif self.type == block.Block.TYPE_T:
            return Color.COLOR_MNK_VIOLET
        elif self.type == block.Block.TYPE_S:
            return Color.COLOR_MNK_GREEN
        elif self.type == block.Block.TYPE_Z:
            return Color.COLOR_MNK_RED
        elif self.type == block.Block.TYPE_J:
            return Color.COLOR_MNK_BLUE
        else:
            return Color.COLOR_MNK_ORANGE