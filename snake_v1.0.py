from tkinter import *
from random import randint


class GameBoard:
    def __init__(self, size_x=300, size_y=300):
        self.board = Tk()
        self.size_x = size_x
        self.size_y = size_y
        self.board.geometry('{}x{}'.format(self.size_x, self.size_y))
        self.board.mainloop()


class Snake:
    def __init__(self, tk_environment):
        # launching Tkinter environment
        self.master = tk_environment
        # setting width and height of the main window
        self.master.geometry('400x400')
        # setting title
        self.master.title('Snake game with Tkinter')
        # defying game board
        self.board = Canvas(self.master, width=300, height=300, background='grey')
        # creating first snake's block
        self.snake = self.board.create_rectangle(50, 50, 60, 60, fill='green')
        self.snake2 = self.board.create_rectangle(40, 50, 50, 60, fill='blue')
        self.snake3 = self.board.create_rectangle(30, 50, 40, 60, fill='blue')
        # defying snake's body
        self.snake_body = [self.snake, self.snake2, self.snake3]
        # placing game board in main window
        self.board.place(x=50, y=50)
        # defying variables to move snake blocks on the screen
        self.x, self.y = 0, 0
        # snake speed(1square/value in ms)
        self.speed = 1001
        # defying a food abject
        self.food = None
        # setting auto snake switch to turn off
        self.auto_snake = 0
        self.text_speed = StringVar()
        self.points = StringVar()
        self.player_name = ""

        self.game_menu()
        self.movement()

    def movement(self):
        # defying snake head moves on board
        self.board.move(self.snake, self.x, self.y)
        # defying snake body moves on board
        if not (self.x == 0 and self.y == 0):
            for block in self.snake_body[1:][::-1]:
                if self.snake_body.index(block) == 1:
                    c = self.board.coords(self.snake)
                    self.board.coords(self.snake_body[1], (c[0] - self.x, c[1] - self.y, c[2] - self.x, c[3] - self.y))
                else:
                    previous_block_coords = self.board.coords(self.snake_body[self.snake_body.index(block) - 1])
                    self.board.coords(block, previous_block_coords)

        # The snake grows up after eat a food
        if self.food and self.board.coords(self.snake) == self.board.coords(self.food):
            # last block coordinates
            lbc = self.board.coords(self.snake_body[-1])
            new_block = self.board.create_rectangle(lbc[0], lbc[1], lbc[2], lbc[3], fill='blue')
            self.snake_body.append(new_block)
            self.points.set(len(self.snake_body) - 3)

        # defying stop conditions
        stop_condition = False
        snake_position = self.board.coords(self.snake)
        # adding snake's body blocks to prohibited fields
        for block in self.snake_body[1:]:
            if self.board.coords(self.snake) == self.board.coords(block):
                self.board.create_rectangle(snake_position[0] - self.x, snake_position[1] - self.y,
                                            snake_position[2] - self.x, snake_position[3] - self.y,
                                            fill='red')
                stop_condition = True

        if 0 > snake_position[0] or snake_position[0] >= 300 or 0 < snake_position[1] >= 300 or snake_position[1] < 0:
            # creating a red block on the place where the snake hit a wall
            self.board.create_rectangle(snake_position[0] - self.x, snake_position[1] - self.y,
                                        snake_position[2] - self.x, snake_position[3] - self.y,
                                        fill='red')
            stop_condition = True

        # checking if the move is allowed
        if not stop_condition:
            # repeating snake move after self.speed in ms
            self.board.after(self.speed, self.movement)
            # eating the food by the snake
            if self.food:

                if snake_position == self.board.coords(self.food):
                    self.board.delete(self.food)
                    self.food = None
            # creating new food
            if not self.food:
                self.food = self.food_creator()

        else:
            # saving score to file
            self.player_name = 'test'
            self.score_handler()

        # turning on/off auto snake
        if self.auto_snake % 2 != 0:
            food_coords = self.board.coords(self.food)
            snake_coords = self.board.coords(self.snake)
            if snake_coords[0] > food_coords[0]:
                self.x = -10
            if snake_coords[1] > food_coords[1]:
                self.y = -10
            if snake_coords[0] < food_coords[0]:
                self.x = 10
            if snake_coords[1] < food_coords[1]:
                self.y = 10

    def game_menu(self):
        speed_text = self.text_speed
        speed_text.set(self.speed)
        snake_speed_label = Label(self.master, textvariable=speed_text)
        snake_speed_label.pack()
        points_text = self.points
        points_text.set(len(self.snake_body) - 3)
        points_text_label = Label(self.master, textvariable=points_text)
        points_text_label.pack()

    def score_handler(self):
        player_name = self.player_name
        f = open("high-score.txt", "a+")
        f.write('Player {} - score: {} \r\n'.format(player_name, self.points.get()))

    def food_creator(self):
        f1 = randint(0, 29) * 10
        f2 = randint(0, 29) * 10
        food = self.board.create_oval(f1, f2, f1 + 10, f2 + 10, fill='yellow')
        return food

    def left(self, event):
        if (self.board.coords(self.snake)[0] - 10 != self.board.coords(self.snake2)[0]) and (
                self.board.coords(self.snake)[1] + 0 != self.board.coords(self.snake2)[1]):
            self.x = -10
            self.y = 0

    def right(self, event):
        if (self.board.coords(self.snake)[0] + 10 != self.board.coords(self.snake2)[0]) and (
                self.board.coords(self.snake)[1] != self.board.coords(self.snake2)[1]):
            self.x = 10
            self.y = 0

    def up(self, event):
        if (self.board.coords(self.snake)[0] != self.board.coords(self.snake2)[0]) and (
                self.board.coords(self.snake)[1] - 10 != self.board.coords(self.snake2)[1]):
            self.y = -10
            self.x = 0

    def down(self, event):
        if (self.board.coords(self.snake)[0] != self.board.coords(self.snake2)[0]) and (
                self.board.coords(self.snake)[1] + 10 != self.board.coords(self.snake2)[1]):
            self.y = 10
            self.x = 0

    def speed_up(self, event):
        self.speed -= 10
        self.text_speed.set(self.speed)

    def speed_down(self, event):
        self.speed += 10
        self.text_speed.set(self.speed)

    def auto_snake_switch(self, event):
        self.auto_snake += 1


if __name__ == "__main__":
    master = Tk()
    snake = Snake(master)
    master.bind("<KeyPress-Left>", lambda e: snake.left(e))
    master.bind("<KeyPress-Right>", lambda e: snake.right(e))
    master.bind("<KeyPress-Up>", lambda e: snake.up(e))
    master.bind("<KeyPress-Down>", lambda e: snake.down(e))
    master.bind("<KeyPress-q>", lambda e: snake.speed_up(e))
    master.bind("<KeyPress-a>", lambda e: snake.speed_down(e))
    master.bind("<KeyPress-z>", lambda e: snake.auto_snake_switch(e))

    master.mainloop()
