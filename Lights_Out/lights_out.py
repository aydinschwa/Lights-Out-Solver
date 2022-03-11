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

        self.solution_vector = [0] * (n * n)

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
            for j, square in enumerate(row):
                grid_pos = (self.size * i) + j
                square_rect = pg.Rect(0, 0, square_rect_width, square_rect_height)
                square_rect.topleft = bg_rect.topleft
                if square:
                    square_rect.x += x_offset
                    square_rect.y += y_offset
                    pg.draw.rect(screen, (0, 0, 150), square_rect, 1)
                    pg.draw.circle(screen, (150, 0, 0), square_rect.center, square_rect_width // 2.5)
                    if self.solution_vector[grid_pos]:
                        hint_rect = square_rect.topright
                        hint_rect = (hint_rect[0] - square_rect_width // 10, hint_rect[1] + square_rect_width // 10)
                        pg.draw.circle(screen, (255, 223, 0), hint_rect, square_rect_width // 10)

                else:
                    square_rect.x += x_offset
                    square_rect.y += y_offset
                    pg.draw.rect(screen, (0, 0, 150), square_rect, 1)
                    if self.solution_vector[grid_pos]:
                        hint_rect = square_rect.topright
                        hint_rect = (hint_rect[0] - square_rect_width // 10, hint_rect[1] + square_rect_width // 10)
                        pg.draw.circle(screen, (255, 223, 0), hint_rect, square_rect_width // 10)

                x_offset += square_rect_width

    def change_lights(self, row, col):
        self.board[row][col] = not self.board[row][col]
        grid_pos = (self.size * row) + col
        if row < self.size - 1:
            self.board[row + 1][col] = not self.board[row + 1][col]
        if row > 0:
            self.board[row - 1][col] = not self.board[row - 1][col]
        if col < self.size - 1:
            self.board[row][col + 1] = not self.board[row][col + 1]
        if col > 0:
            self.board[row][col - 1] = not self.board[row][col - 1]
        self.solution_vector[grid_pos] = 0

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

    def _get_move_matrix(self):
        move_matrix = []
        n = self.size
        for _ in range(n * n):
            to_add = [0] * n * n
            move_matrix.append(to_add)

        for col in range(n * n):
            for row in range(n * n):
                if row == col:
                    move_matrix[row][col] = 1
                    if row + 1 < n * n and col % n != n - 1:
                        move_matrix[row + 1][col] = 1
                    if row - 1 >= 0 and col % n != 0:
                        move_matrix[row - 1][col] = 1
                    if row + n < n * n:
                        move_matrix[row + n][col] = 1
                    if row - n >= 0:
                        move_matrix[row - n][col] = 1

        return np.array(move_matrix)

    def solve(self):

        def gauss_elim(A):
            rows_left = list(range(len(A)))
            new_rowlist = []
            for col_idx in range(len(A)):
                # among rows left, list of row-labels whose rows have a nonzero in position col_idx
                rows_with_nonzero = [row_idx for row_idx in rows_left if A[row_idx][col_idx]]
                if rows_with_nonzero:
                    pivot_idx = rows_with_nonzero[0]
                    rows_left.remove(pivot_idx)
                    new_rowlist.append(A[pivot_idx])
                    for row_idx in rows_with_nonzero[1:]:
                        A[row_idx] -= (A[row_idx][col_idx] // A[pivot_idx][col_idx]) * A[pivot_idx]
                        A[row_idx] = A[row_idx] % 2

            if rows_left:
                [new_rowlist.append(A[row]) for row in rows_left]

            return np.array(new_rowlist)

        def triangular_solve_n(row_list, b):
            x = np.zeros(len(row_list))
            for i in reversed(range(len(row_list))):
                dot_prod = np.dot(row_list[i], x)
                x[i] = (b[i] - dot_prod) % 2
            return x

        curr_board = [[num] for row in self.board for num in row]
        move_matrix = self._get_move_matrix()
        move_matrix = np.append(move_matrix, curr_board, axis=1)
        echelon_matrix = gauss_elim(move_matrix)

        ans_col = echelon_matrix[:, -1]
        echelon_matrix = np.delete(echelon_matrix, -1, 1)

        moves = triangular_solve_n(echelon_matrix, ans_col)

        return moves

    def use_solution_vector(self):
        for i in range(self.size):
            for j in range(self.size):
                grid_pos = (self.size * i) + j
                if self.solution_vector[grid_pos]:
                    self.change_lights(i, j)


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
                game.solution_vector = game.solve()
            if event.key == pg.K_s:
                game.use_solution_vector()

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
