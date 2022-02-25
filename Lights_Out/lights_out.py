import pygame as pg
import sys
import random
import numpy as np

pg.init()
screen_width = 500
screen_height = 600
bg_rect_width = int(screen_width * (5/6))
bg_rect_height = int(screen_width * (5/6))

screen = pg.display.set_mode((screen_width, screen_height))
title_font = pg.font.SysFont("Verdana", 60)
game_font = pg.font.SysFont("Verdana", 15)
pg.display.set_caption("Lights Out")


class Game:
    def __init__(self, n):
        self.size = n
        self.board = []
        for _ in range(n):
            to_add = []
            for _ in range(n):
                to_add.append(False)
            self.board.append(to_add)

    def draw_board(self):
        title = title_font.render("Lights Out", True, (0, 0, 0))
        title_rect = title.get_rect(center=(screen_width // 2, screen_height // 12))
        screen.blit(title, title_rect)

        bg_rect = pg.Rect(0, 0, bg_rect_width, bg_rect_height)
        bg_rect.center = (screen_width // 2, screen_height // 2)
        pg.draw.rect(screen, (0, 0, 0), bg_rect)

        restart_rect = pg.Rect(bg_rect.topleft[0], bg_rect.bottomleft[1] + 20, 100, 50)
        restart_word = game_font.render("Reset Game", True, (0, 0, 0))
        restart_word_rect = restart_word.get_rect(center=restart_rect.center)
        pg.draw.rect(screen, (255, 255, 255), restart_rect)
        screen.blit(restart_word, restart_word_rect)

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
                    pg.draw.circle(screen, (150, 0, 0), square_rect.center, square_rect_width // 2.5)
                    x_offset += square_rect_width
                else:
                    square_rect.x += x_offset
                    square_rect.y += y_offset
                    pg.draw.rect(screen, (0, 0, 150), square_rect, 1)
                    x_offset += square_rect_width

    def change_lights(self, row, col):
        self.board[row][col] = not self.board[row][col]
        if row < self.size - 1:
            self.board[row + 1][col] = not self.board[row + 1][col]
        if row > 0:
            self.board[row - 1][col] = not self.board[row - 1][col]
        if col < self.size - 1:
            self.board[row][col + 1] = not self.board[row][col + 1]
        if col > 0:
            self.board[row][col - 1] = not self.board[row][col - 1]

    def update_board(self, x, y):
        bg_rect = pg.Rect(0, 0, bg_rect_width, bg_rect_height)
        bg_rect.center = (screen_width // 2, screen_height // 2)

        board_x = (x - bg_rect.topleft[0]) // (bg_rect_width // self.size)
        board_y = (y - bg_rect.topleft[1]) // (bg_rect_height // self.size)

        if (board_x >= 0) and (board_x < self.size) and (board_y >= 0) and (board_y < self.size):
            self.change_lights(board_y, board_x)

    def start(self):
        for row in range(self.size):
            for col in range(self.size):
                switch = random.randint(0, 100) < 35
                if switch:
                    self.change_lights(row, col)

    def check_win(self):
        for row in self.board:
            if sum(row) > 0:
                return False
        return True

    def solve(self):
        move_matrix = []
        n = self.size
        for i in range(n * n):
            to_add = []
            for j in range(n * n):
                to_add.append(0)
            move_matrix.append(np.array(to_add))

        for col in range(n * n):
            for row in range(n * n):
                if row == col:
                    move_matrix[row][col] = 1
                    if row + 1 < n * n and col != n - 1:
                        move_matrix[row + 1][col] = 1
                    if row - 1 >= 0 and col % n != 0:
                        move_matrix[row - 1][col] = 1
                    if row + n < n * n:
                        move_matrix[row + n][col] = 1
                    if row - n >= 0:
                        move_matrix[row - n][col] = 1

        move_matrix = np.array(move_matrix)

        # flatten nested list
        curr_board = [num for row in self.board for num in row]

        x = np.linalg.solve(move_matrix, curr_board)
        x = [round(elem) % 2 for elem in x]
        [print(f"Square {i + 1}") for i, square in enumerate(x) if square]
        print(x)
        return x


game = Game(5)
game.start()
win = False
now = 0
while True:
    screen.fill((112, 128, 144))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            game.update_board(mouse_x, mouse_y)

            bg_rect = pg.Rect(0, 0, bg_rect_width, bg_rect_height)
            bg_rect.center = (screen_width // 2, screen_height // 2)

            restart_rect = pg.Rect(bg_rect.topleft[0], bg_rect.bottomleft[1] + 20, 100, 50)

            if restart_rect.collidepoint(mouse_x, mouse_y):
                game.start()

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                ans_list = game.solve()

    if game.check_win() and not win:
        game.draw_board()
        pg.display.update()
        print('noice')
        win = True
        now = pg.time.get_ticks()

    # I'm sure there's a better way to wait a few seconds after winning, but idk
    if win and (pg.time.get_ticks() - now > 3000):
        win = False
        game.start()

    game.draw_board()
    pg.display.update()
