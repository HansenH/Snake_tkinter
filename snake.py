import keyboard # https://github.com/boppreh/keyboard
import threading
import tkinter
import time

TABLE_WIDTH = 20
TABLE_HEIGHT = 20
SNAKE_INITIAL_LENGTH = 4
SPEED = (0.3, 0.25, 0.2, 0.15, 0.1)

class Main():
    def __init__(self):
        self.game = Game()
        self.game.start()

        # self.ui = UI()
        # self.ui.start()

        def up(event):
            self.game.direction = 1

        def down(event):
            self.game.direction = 2

        def left(event):
           self.game.direction = 3

        def right(event):
            self.game.direction = 4

        # keyboard.on_press_key('up', up, suppress=False)
        # keyboard.on_press_key('down', down, suppress=False)
        # keyboard.on_press_key('left', left, suppress=False)
        # keyboard.on_press_key('right', right, suppress=False)
        # keyboard.on_press_key('w', up, suppress=False)
        # keyboard.on_press_key('s', down, suppress=False)
        # keyboard.on_press_key('a', left, suppress=False)
        # keyboard.on_press_key('d', right, suppress=False)

        # keyboard.wait('esc', suppress=True)


class Game(threading.Thread):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.direction = 0
        self.speed_level = 0 
        self.table = [[0 for col in range(TABLE_WIDTH)] for row in range(TABLE_HEIGHT)] # 1 for snake, 2 for apple
        self.head = [int((TABLE_WIDTH) * 0.4), int((TABLE_HEIGHT - 1) / 2)]   # coordinate of snake head
        self.table[int((TABLE_HEIGHT - 1) / 2)][int((TABLE_WIDTH) * 0.7)] = 3   # initialize the apple
        for i in range(SNAKE_INITIAL_LENGTH):
            self.table[self.head[1]][self.head[0] - i] = 1  # initialize the snake

        
        for j in range(len(self.table)):
            print(self.table[j])

    def run(self):
        def one_step():
            if self.direction == 1



        keyboard.wait('esc', suppress=True)

        
        






        
class UI(threading.Thread):
    pass


if __name__ == '__main__':
    main = Main()


# import threading
# import time

# def func1(a):
#     if a > 10:
#         time_end=time.time()
#         print('totally cost',time_end-time_start)
#         return
#     t=threading.Timer(0.1,func1,(a + 1,))
#     t.start()
#     print(a)
#     print('当前线程数为{}'.format(threading.activeCount()))



# func1(1)


