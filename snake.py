# Author: HansenH
# MIT License - Copyright (c) 2021 HansenH
# https://github.com/HansenH/Snake_tkinter

import keyboard # https://github.com/boppreh/keyboard
import threading
import tkinter
from tkinter import messagebox
import random

TABLE_COLS = 20
TABLE_ROWS = 20
SNAKE_INITIAL_LENGTH = 4
SPEED = 0.12     # the smaller, the faster
WINDOW_WIDTH = 500      # UI window width
WINDOW_HEIGHT = 500     # UI window height
GRID_THICK = 2
GRID_COLOR = '#BBBBBB'
TABLE_COLOR = '#666666'
SNAKE_COLOR = '#FFFF00'
APPLE_COLOR = '#FF0000'
WINDOW_ADAPT = True     # True: window can self-adapt, False: lock window size

class Main():
    '''listening key events and create game and ui threads'''
    def __init__(self):
        self.ui = UI()
        self.ui.start()

        def up(event):
            self.ui.game.go_up()

        def down(event):
            self.ui.game.go_down()

        def left(event):
            self.ui.game.go_left()

        def right(event):
            self.ui.game.go_right()

        keyboard.on_press_key('up', up, suppress=False)
        keyboard.on_press_key('down', down, suppress=False)
        keyboard.on_press_key('left', left, suppress=False)
        keyboard.on_press_key('right', right, suppress=False)
        keyboard.on_press_key('w', up, suppress=False)
        keyboard.on_press_key('s', down, suppress=False)
        keyboard.on_press_key('a', left, suppress=False)
        keyboard.on_press_key('d', right, suppress=False)

    def restart(self):
        self.game = Game()
        self.game.start()


class Game(threading.Thread):
    '''game logic as a thread'''
    def __init__(self):
        super().__init__()
        self.game_over = False
        self.snake_length = SNAKE_INITIAL_LENGTH
        self.score = 0
        self.direction = -4  # -4 before start, 1 for up, 2 for down, 3 for left, 4 four right
        self.direction_lock = False
        self.table = [[0 for col in range(TABLE_COLS)] for row in range(TABLE_ROWS)] # 0 for blank table
        self.head = [int((TABLE_COLS) * 0.4), int((TABLE_ROWS - 1) / 2)]   # coordinate of snake head (x, y)
        self.table[int((TABLE_ROWS - 1) / 2)][int((TABLE_COLS) * 0.7)] = -1   # initialize the apple (-1) on table(y, x)
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
        if not self.direction_lock and abs(self.direction) != 4: # start direction is right
            self.direction = 3
            self.direction_lock = True

    def go_right(self):
        if not self.direction_lock and self.direction != 3:
            self.direction = 4
            self.direction_lock = True

    def run(self):
        def new_apple():
            '''create a new apple at a valid position'''
            try:
                apple_index = random.randint(1, TABLE_COLS * TABLE_ROWS - self.snake_length)
                counter = 0
                for i in range(TABLE_ROWS):
                    for j in range(TABLE_COLS):
                        if self.table[i][j] == 0:
                            counter += 1
                            if counter == apple_index:
                                self.table[i][j] = -1
            except ValueError:
                pass

        def one_step():
            '''one step forward'''
            if not self.game_over:
                threading.Timer(SPEED, one_step).start()  # create timer thread for next step

                if self.direction == 1:
                    self.head[1] -= 1   # go up
                elif self.direction == 2:
                    self.head[1] += 1   # go down
                elif self.direction == 3:
                    self.head[0] -= 1   # go left
                elif self.direction == 4:
                    self.head[0] += 1   # go right
                else:
                    return  # before start
                self.direction_lock = False

                if (self.head[1] < 0 or self.head[1] >= TABLE_ROWS
                        or self.head[0] < 0 or self.head[0] >= TABLE_COLS):
                    self.game_over = True   # hit wall
                    return
                if self.table[self.head[1]][self.head[0]] > 0:
                    self.game_over = True   # hit itself
                    return
                if self.table[self.head[1]][self.head[0]] == 0: # if not eating apple
                    for i in range(TABLE_ROWS):
                        for j in range(TABLE_COLS):
                            if self.table[i][j] > 0:
                                self.table[i][j] -= 1   # move body
                else:
                    self.snake_length += 1  # if getting an apple: grow longer
                    self.score += 1
                    new_apple()
                self.table[self.head[1]][self.head[0]] = self.snake_length  # new head

        one_step()
        

class UI(threading.Thread):
    '''a self-adapting GUI window'''
    def __init__(self):
        super().__init__()
        self.new_game()

    def new_game(self):
        self.game = Game()
        self.game.start()

    def run(self):
        window = tkinter.Tk()
        window.withdraw()
        window.title('Snake')
        window_x = int((window.winfo_screenwidth() - WINDOW_WIDTH) / 2)
        window_y = int((window.winfo_screenheight() - WINDOW_HEIGHT) / 2)
        window.geometry('{}x{}+{}+{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT, window_x, window_y))
        window.deiconify()

        def on_closing():
            self.game.game_over = True     # to terminate game thread
            window.destroy()
        window.protocol('WM_DELETE_WINDOW', on_closing)

        def window_adjust(event):
            '''to implement self-adapting of window'''
            canvas.configure(
                width=min(window.winfo_width(), window.winfo_height() * WINDOW_WIDTH / WINDOW_HEIGHT), 
                height=min(window.winfo_width() * WINDOW_HEIGHT / WINDOW_WIDTH, window.winfo_height()), 
            )
            draw_table(min(window.winfo_width(), window.winfo_height() * WINDOW_WIDTH / WINDOW_HEIGHT),
                    min(window.winfo_width() * WINDOW_HEIGHT / WINDOW_WIDTH, window.winfo_height()))
        
        if WINDOW_ADAPT:
            window.bind('<Configure>', window_adjust)
        else:
            window.resizable(False, False)

        canvas = tkinter.Canvas(
            window,
            highlightthickness=0,
            bd=0,
            width=WINDOW_WIDTH, 
            height=WINDOW_HEIGHT, 
            bg=GRID_COLOR
        )
        canvas.pack(expand='yes')

        cells = [[0 for col in range(TABLE_COLS)] for row in range(TABLE_ROWS)]

        def draw_table(cell_width, cell_height):
            canvas.delete('all')
            for i in range(TABLE_ROWS):
                for j in range(TABLE_COLS):
                    cells[i][j] = canvas.create_rectangle(
                        j * cell_width / TABLE_COLS,
                        i * cell_height / TABLE_ROWS,
                        (j + 1) * cell_width / TABLE_COLS,
                        (i + 1) * cell_height / TABLE_ROWS,
                        fill=TABLE_COLOR, 
                        outline=GRID_COLOR, 
                        width=GRID_THICK /2
                    )
        
        def refresh_screen():
            if not self.game.game_over:
                canvas.after(10, refresh_screen)
                for i in range(TABLE_ROWS):
                    for j in range(TABLE_COLS):
                        if self.game.table[i][j] < 0:
                            canvas.itemconfigure(cells[i][j], fill=APPLE_COLOR)
                        elif self.game.table[i][j] > 0:
                            canvas.itemconfigure(cells[i][j], fill=SNAKE_COLOR)
                        else:
                            canvas.itemconfigure(cells[i][j], fill=TABLE_COLOR)
            else:
                if self.game.score == TABLE_ROWS * TABLE_COLS - SNAKE_INITIAL_LENGTH:
                    messagebox.showinfo(message='    YOU WIN!    \n\n    Your score: {}'.format(self.game.score))
                else:
                    messagebox.showinfo(message='    GAME OVER!    \n\n    Your score: {}'.format(self.game.score))
                ans = messagebox.askyesno(message='Do you want to play again?')
                if ans:
                    self.new_game()
                    refresh_screen()
                else:
                    window.destroy()

        draw_table(WINDOW_WIDTH, WINDOW_HEIGHT)
        refresh_screen()
        window.mainloop()


if __name__ == '__main__':
    main = Main()