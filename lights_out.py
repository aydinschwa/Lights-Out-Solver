import pygame as pg
import sys
import random


pg.init()
screen_width = 500
screen_height = 500
bg_rect_width = screen_width - 150
bg_rect_height = screen_height - 150

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Lights Out")


class Game:
    def __init__(self, n):
        self.size = n
        self.board = []
        for _ in range(n):
            to_add = []
            for _ in range(n):
                to_add.append(0)
            self.board.append(to_add)

    def draw_board(self):
        bg_rect = pg.Rect(0, 0, bg_rect_width, bg_rect_height)
        bg_rect.center = (screen_width // 2, screen_height // 2)
        pg.draw.rect(screen, (0, 0, 0), bg_rect)

        for i, row in enumerate(self.board):
            y_offset = (bg_rect_height // self.size) * i
            x_offset = 0
            square_rect_width = bg_rect_width // self.size
            square_rect_height = bg_rect_height // self.size
            for square in row:
                square_rect = pg.Rect(0, 0, square_rect_width, square_rect_height)
                square_rect.topleft = bg_rect.topleft
                if square:
                    square_rect.x += x_offset
                    square_rect.y += y_offset
                    pg.draw.rect(screen, (0, 0, 150), square_rect, 1)
                    pg.draw.circle(screen, (150, 0, 0), square_rect.center, 20)
                    x_offset += square_rect_width
                else:
                    square_rect.x += x_offset
                    square_rect.y += y_offset
                    pg.draw.rect(screen, (0, 0, 150), square_rect, 1)
                    pg.draw.circle(screen, (0, 150, 0), square_rect.center, 20)
                    x_offset += square_rect_width

    def change_lights(self, row, col):
        self.board[row][col] = not self.board[row][col]
        if row < 4:
            self.board[row + 1][col] = not self.board[row + 1][col]
        if row > 0:
            self.board[row - 1][col] = not self.board[row - 1][col]
        if col < 4:
            self.board[row][col + 1] = not self.board[row][col + 1]
        if col > 0:
            self.board[row][col - 1] = not self.board[row][col - 1]

    def update_board(self, x, y):
        # TODO: figure out how to actually make clicks work with arbitrary board size
        x_offset = (screen_width - bg_rect_width) // 2
        y_offset = (screen_height - bg_rect_height) // 2
        board_x = (x // x_offset) - 1
        board_y = (y // y_offset) - 1
        if board_x <= 4 and board_y <= 4:
            self.change_lights(board_y, board_x)

    def start(self):
        for row in range(self.size):
            for col in range(self.size):
                switch = random.randint(0, 100) > 15
                if switch:
                    self.change_lights(row, col)


game = Game(5)
game.start()
while True:
    screen.fill((112, 128, 144))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            game.update_board(mouse_x, mouse_y)

    game.draw_board()
    pg.display.update()
