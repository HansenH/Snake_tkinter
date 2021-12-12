# Author: HansenH
# MIT License - Copyright (c) 2021 HansenH
# https://github.com/HansenH/Snake_tkinter

import snake
import threading

class AutoPlayer():
    def __init__(self, game: snake.Game):
        self.game = game
        self.game.go_right()
        self.play()

    def play(self):
        if not self.game.game_over:
            threading.Timer(0.01, self.play).start()
            if self.game.head[0] == snake.TABLE_COLS - 2 and self.game.direction == 4 and self.game.head[1] < snake.TABLE_ROWS - 1:
                self.game.go_down()
            elif self.game.head[0] == snake.TABLE_COLS - 2 and self.game.direction == 2:
                self.game.go_left()
            elif self.game.head[0] == 0 and self.game.direction == 3:
                self.game.go_down()
            elif self.game.head[0] == 0 and self.game.direction == 2:
                self.game.go_right()
            elif self.game.head[0] == snake.TABLE_COLS - 1 and self.game.direction == 4 and self.game.head[1] == snake.TABLE_ROWS - 1:
                self.game.go_up()
            elif self.game.head[0] == snake.TABLE_COLS - 1 and self.game.direction == 1 and self.game.head[1] == 0:
                self.game.go_left()

if __name__ == '__main__':
    snake.SPEED = 0.02
    player = AutoPlayer(snake.Main().ui.game)