A = [[1, 1, 0, 1, 0, 0, 0, 0, 0],
     [1, 1, 1, 0, 1, 0, 0, 0, 0],
     [0, 1, 1, 0, 0, 1, 0, 0, 0],
     [1, 0, 0, 1, 1, 0, 1, 0, 0],
     [0, 1, 0, 1, 1, 1, 0, 1, 0],
     [0, 0, 1, 0, 1, 1, 0, 0, 1],
     [0, 0, 0, 1, 0, 0, 1, 1, 0],
     [0, 0, 0, 0, 1, 0, 1, 1, 1],
     [0, 0, 0, 0, 0, 1, 0, 1, 1]]

b = [1, 1, 0, 1, 0, 0, 0, 1, 0]

A = [[float(elem) for elem in row] for row in A]
b = [float(elem) for elem in b]
print(b)

n = len(A)
# forward elimination
for k in range(0, n - 1):
    # switch pivot row if pivot is 0
    if A[k][k] == 0:
        for i, row in enumerate(A[k + 1:]):
            if row[k]:
                A[k], A[i + k + 1] = A[i + k + 1], A[k]
                break
    for i in range(k + 1, n):
        if A[i][k] == 0:
            continue
        ratio = A[i][k] / A[k][k]
        for j in range(k, n - 1):
            A[i][j] -= ratio * A[k][j]
            A[i][j] = A[i][j] % 2

[print(row) for row in A]
[print(val) for val in b]


x = [0] * n
for i in reversed(range(len(A))):
    dot_prod = sum([A[i][col] * x[col] for col in range(len(A))])
    x[i] = ((b[i] - dot_prod) % 2) / A[i][i]

print(x)

