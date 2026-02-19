import numpy as np
import time
import os

matrix = np.random.choice([0, 1], size=(30, 30), p=[0.8, 0.2])

print("Game of Life (30x30)")
time.sleep(2)

while True:
    try:
        os.system('clear')
        for row in matrix:
            print(''.join('# ' if cell else '  ' for cell in row))
        
        new_matrix = np.zeros_like(matrix)
        for i in range(30):
            for j in range(30):
                neighbors = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni = i + di
                        nj = j + dj
                        if 0 <= ni < 30 and 0 <= nj < 30:
                            neighbors += matrix[ni, nj]
                
                if matrix[i, j] == 1:
                    new_matrix[i, j] = 1 if neighbors in [2, 3] else 0
                else:
                    new_matrix[i, j] = 1 if neighbors == 3 else 0
        
        matrix = new_matrix
        time.sleep(0.1)
        
    except KeyboardInterrupt:
        print("\nStopped")
        break