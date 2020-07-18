import game
import block
import stage

# ゲームのタイトル
title = "テトリス"
# 画面
width = stage.Stage.WIDTH
height = stage.Stage.HEIGHT

tetris = game.Game(title, width * block.Block.SCALE, height * block.Block.SCALE)
tetris.start()
