# Author: HansenH
# MIT License - Copyright (c) 2021 HansenH
# https://github.com/HansenH/Snake_tkinter

from pynput import keyboard
import threading
import tkinter
from tkinter import messagebox
import random

TABLE_COLS = 20
TABLE_ROWS = 20
SNAKE_INITIAL_LENGTH = 4
MIN_SPEED = 0.12     # the smaller, the faster
MAX_SPEED = 0.04
WINDOW_WIDTH = 500      # UI self.window width
WINDOW_HEIGHT = 500     # UI self.window height
GRID_THICK = 2
GRID_COLOR = '#BBBBBB'
TABLE_COLOR = '#666666'
SNAKE_COLOR = '#FFFF00'
APPLE_COLOR = '#FF0000'
WINDOW_ADAPT = True     # True: self.window can self-adapt, False: lock self.window size


class Game(threading.Thread):
    '''game logic as a thread'''
    def __init__(self):
        super().__init__()
        self.paused = False
        self.game_over = False
        self.snake_length = SNAKE_INITIAL_LENGTH
        self.score = 0
        self.input_queue = []
        self.next_direction = 2  # 1 for up, -1 for down, 2 for right, -2 for left
        self.curr_direction = 2
        self.table = [[0 for col in range(TABLE_COLS)] for row in range(TABLE_ROWS)] # 0 for blank table
        self.head = [int((TABLE_COLS) * 0.4), int((TABLE_ROWS - 1) / 2)]   # coordinate of snake head (x, y)
        self.table[int((TABLE_ROWS - 1) / 2)][int((TABLE_COLS) * 0.7)] = -1   # initialize the apple (-1) on table(y, x)
        for i in range(SNAKE_INITIAL_LENGTH):
            self.table[self.head[1]][self.head[0] - i] = SNAKE_INITIAL_LENGTH - i  # initialize the snake (>0)
                
    def poll_input_queue(self):
        if len(self.input_queue) == 0:
            return
        next = self.input_queue.pop(0)
        if abs(next) == abs(self.curr_direction):
            self.poll_input_queue()
            return
        self.next_direction = next

    def pause(self):
        self.paused = not self.paused

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
                threading.Timer(MIN_SPEED, one_step).start()  # create timer thread for next step
                self.poll_input_queue()
                if self.paused:
                    return
                if self.next_direction == 1:
                    self.head[1] -= 1   # go up
                elif self.next_direction == -1:
                    self.head[1] += 1   # go down
                elif self.next_direction == -2:
                    self.head[0] -= 1   # go left
                elif self.next_direction == 2:
                    self.head[0] += 1   # go right
                else:
                    return  # before start
                self.curr_direction = self.next_direction

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
        

class Main():
    '''Main thread (GUI)'''
    def __init__(self):
        self.window = None
        self.game = Game()
        self.game.start()
        def on_press(key):
            if self.window.focus_displayof() is None:
                return  # no action if no focus
            if key == keyboard.Key.esc or key == keyboard.Key.space:
                self.game.pause()
            elif key == keyboard.Key.up and not self.game.paused:
                self.game.input_queue.append(1)
            elif key == keyboard.Key.down and not self.game.paused:
                self.game.input_queue.append(-1)
            elif key == keyboard.Key.left and not self.game.paused:
                self.game.input_queue.append(-2)
            elif key == keyboard.Key.right and not self.game.paused:
                self.game.input_queue.append(2)
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

    def start(self):
        self.was_paused = False
        self.window = tkinter.Tk()
        self.window.withdraw()
        self.window.title('Snake')
        window_x = int((self.window.winfo_screenwidth() - WINDOW_WIDTH) / 2)
        window_y = int((self.window.winfo_screenheight() - WINDOW_HEIGHT) / 2)
        self.window.geometry('{}x{}+{}+{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT, window_x, window_y))
        self.window.deiconify()

        def on_closing():
            self.game.game_over = True     # to terminate game thread
            self.window.destroy()
        self.window.protocol('WM_DELETE_WINDOW', on_closing)

        def window_adjust(event):
            '''to implement self-adapting of self.window'''
            canvas.configure(
                width=min(self.window.winfo_width(), self.window.winfo_height() * WINDOW_WIDTH / WINDOW_HEIGHT), 
                height=min(self.window.winfo_width() * WINDOW_HEIGHT / WINDOW_WIDTH, self.window.winfo_height()), 
            )
            draw_table(min(self.window.winfo_width(), self.window.winfo_height() * WINDOW_WIDTH / WINDOW_HEIGHT),
                    min(self.window.winfo_width() * WINDOW_HEIGHT / WINDOW_WIDTH, self.window.winfo_height()))
        
        if WINDOW_ADAPT:
            self.window.bind('<Configure>', window_adjust)
        else:
            self.window.resizable(False, False)

        canvas = tkinter.Canvas(
            self.window,
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
                if self.game.paused and not self.was_paused:
                    self.window.title('Snake (PAUSED)')
                    self.was_paused = True
                    return
                if not self.game.paused and self.was_paused:
                    self.window.title('Snake')
                    self.was_paused = False
                    return
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
                    self.game = Game()
                    self.game.start()
                    self.window.focus_force()
                    refresh_screen()
                else:
                    self.window.destroy()

        draw_table(WINDOW_WIDTH, WINDOW_HEIGHT)
        refresh_screen()
        self.window.mainloop()


if __name__ == '__main__':
    main = Main()
    main.start()