import numpy as np

A = []
n = 5
for i in range(n*n):
    to_add = []
    for j in range(n*n):
        to_add.append(0)
    A.append(np.array(to_add))

for col in range(n*n):
    for row in range(n*n):
        if row == col:
            A[row][col] = 1
            if row + 1 < n*n and col != n - 1:
                A[row + 1][col] = 1
            if row - 1 >= 0 and col % n != 0:
                A[row - 1][col] = 1
            if row + n < n*n:
                A[row + n][col] = 1
            if row - n >= 0:
                A[row - n][col] = 1

test_board = [False, False, False, False, True,
              False, True, False, True, True,
              True, True, True, False, True,
              False, True, False, False, False,
              False, False, False, False, False]

A = np.array(A)




