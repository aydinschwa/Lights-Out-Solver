import numpy as np


def gauss_elim(A):
    rows_left = list(range(len(A)))
    new_rowlist = []
    for col_idx in range(len(A)):
        # among rows left, list of row-labels whose rows have a nonzero in position col_idx
        rows_with_nonzero = [row_idx for row_idx in rows_left if A[row_idx][col_idx] != 0]
        if rows_with_nonzero:
            pivot_idx = rows_with_nonzero[0]
            rows_left.remove(pivot_idx)
            new_rowlist.append(A[pivot_idx])
            for row_idx in rows_with_nonzero[1:]:
                multiplier = A[row_idx][col_idx] // A[pivot_idx][col_idx]
                A[row_idx] -= multiplier * A[pivot_idx]
                A[row_idx] = A[row_idx] % 2

    return np.array(new_rowlist)



def triangular_solve_n(rowlist, b):
    x = [0] * len(rowlist)
    for i in reversed(range(len(rowlist))):
        dot_prod = sum([rowlist[i][col] * x[col] for col in range(len(rowlist))])
        x[i] = ((b[i] - dot_prod) % 2) / rowlist[i][i]
    return x


A = []
n = 3
for i in range(n*n):
    to_add = []
    for j in range(n*n):
        to_add.append(0)
    A.append(to_add)

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

# A = [[0, 2, 3, 4, 5],
#      [0, 0, 0, 3, 2],
#      [1, 2, 3, 4, 5],
#      [0, 0, 0, 6, 7],
#      [0, 0, 0, 9, 9]]

A = np.array(A)

A_echelon = gauss_elim(A)
print(A_echelon)
# print(triangular_solve_n(A_echelon, [1, 1, 1, 0, 1, 0, 1, 0, 1]))
# [print(elem) for elem in A_echelon]


























