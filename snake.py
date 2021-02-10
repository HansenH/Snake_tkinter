import keyboard # https://github.com/boppreh/keyboard
import threading
import tkinter
import random
# import time
# import os

TABLE_WIDTH = 20
TABLE_HEIGHT = 20
SNAKE_INITIAL_LENGTH = 4
SPEED = 0.14     # the smaller, the faster

class Main():
    '''listening key events and create game and ui threads'''
    def __init__(self):
        self.game = Game()
        self.game.start()
        # self.ui = UI()
        # self.ui.start()

        def up(event):
            self.game.go_up()

        def down(event):
            self.game.go_down()

        def left(event):
            self.game.go_left()

        def right(event):
            self.game.go_right()

        keyboard.on_press_key('up', up, suppress=False)
        keyboard.on_press_key('down', down, suppress=False)
        keyboard.on_press_key('left', left, suppress=False)
        keyboard.on_press_key('right', right, suppress=False)
        keyboard.on_press_key('w', up, suppress=False)
        keyboard.on_press_key('s', down, suppress=False)
        keyboard.on_press_key('a', left, suppress=False)
        keyboard.on_press_key('d', right, suppress=False)


class Game(threading.Thread):
    '''game logic as a thread'''
    def __init__(self):
        super().__init__()
        self.game_over = False
        self.score = 0
        self.snake_length = SNAKE_INITIAL_LENGTH
        self.direction = 4      # 1 for up, 2 for down, 3 for left, 4 four right
        self.direction_lock = False
        self.table = [[0 for col in range(TABLE_WIDTH)] for row in range(TABLE_HEIGHT)] # 0 for blank table
        self.head = [int((TABLE_WIDTH) * 0.4), int((TABLE_HEIGHT - 1) / 2)]   # coordinate of snake head (x, y)
        self.table[int((TABLE_HEIGHT - 1) / 2)][int((TABLE_WIDTH) * 0.7)] = -1   # initialize the apple (-1) on table(y, x)
        for i in range(SNAKE_INITIAL_LENGTH):
            self.table[self.head[1]][self.head[0] - i] = SNAKE_INITIAL_LENGTH - i  # initialize the snake (>0)

    def go_up(self):
        if not self.direction_lock and self.direction != 2:
            self.direction = 1
            self.direction_lock = True

    def go_down(self):
        if not self.direction_lock and self.direction != 1:
            self.direction = 2
            self.direction_lock = True

    def go_left(self):
        if not self.direction_lock and self.direction != 4:
            self.direction = 3
            self.direction_lock = True

    def go_right(self):
        if not self.direction_lock and self.direction != 3:
            self.direction = 4
            self.direction_lock = True

    def run(self):
        def new_apple():
            '''create a new apple at a valid position'''
            apple_index = random.randint(1, TABLE_WIDTH * TABLE_HEIGHT - self.snake_length)
            counter = 0
            for i in range(TABLE_HEIGHT):
                for j in range(TABLE_WIDTH):
                    if self.table[i][j] == 0:
                        counter += 1
                        if counter == apple_index:
                            self.table[i][j] = -1

        def one_step():
            '''one step forward'''
            if not self.game_over:
                threading.Timer(SPEED, one_step).start()    #create timer thread for next step

                if self.direction == 1:
                    self.head[1] -= 1
                elif self.direction == 2:
                    self.head[1] += 1
                elif self.direction == 3:
                    self.head[0] -= 1
                elif self.direction == 4:
                    self.head[0] += 1
                self.direction_lock = False

                if (self.head[1] < 0 or self.head[1] >= TABLE_HEIGHT
                        or self.head[0] < 0 or self.head[0] >= TABLE_WIDTH):
                    self.game_over = True   #hit wall
                    return
                if self.table[self.head[1]][self.head[0]] > 0:
                    self.game_over = True   # hit itself
                    return
                if self.table[self.head[1]][self.head[0]] == 0: # if not eating apple
                    for i in range(TABLE_HEIGHT):
                        for j in range(TABLE_WIDTH):
                            if self.table[i][j] > 0:
                                self.table[i][j] -= 1   # move body
                else:
                    self.snake_length += 1  # if getting an apple: grow longer
                    new_apple()
                self.table[self.head[1]][self.head[0]] = self.snake_length  #move head

                # os.system("cls")
                # for i in self.table:
                #     print(i)

        one_step()
        

class UI(threading.Thread):
    pass


if __name__ == '__main__':
    main = Main()