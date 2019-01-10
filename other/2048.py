import numpy as np
import pandas as pd

def mirror_mat(matrix):
    grid = [row[:] for row in matrix]
    n = len(grid)
    m = len(grid[0])
    m2 = round(m/2)
    for i in range(n):
        for j in range(m2):
            temp = grid[i][j]
            grid[i][j] = grid[i][m-j-1]
            grid[i][m-j-1] = temp
    return grid

def transpose_mat(matrix):
    grid = [row[:] for row in matrix]
    n = len(grid)
    m = len(grid[0])
    for i in range(n):
        for j in range(m):
            if(i<j):
                temp = grid[i][j]
                grid[i][j] = grid[j][i]
                grid[j][i] = temp
    return grid

def print_mat(grid, padding = 2):
    n = len(grid)
    m = len(grid[0])
    pad = ""
    for i in range(padding):
        pad += " "
    for i in range(n):
        row = ""
        for j in range(m):
            row += str(grid[i][j]) + pad
        print(row)
    print("")

def slide_left(matrix):
    grid = [row[:] for row in matrix]
    n = len(grid)
    score = 0
    cleared = 0
    for i in range(n):
        line = grid[i]
        removed = 0
        j=0
        while j<len(line)-1:
            if line[j] == 0:
                line.pop(j)
                removed += 1
            elif line[j] == line[j+1]:
                line.pop(j)
                line[j] *= 2
                removed += 1
                score += line[j]
                cleared += 1
            elif j + 1 < len(line) and line[j+1] == 0:
                line.pop(j+1)
                removed+=1 
            else:
                j += 1
        for _ in range(removed):
            line.append(0)
        grid[i] = line
    return (grid, score, cleared)

def slide_right(matrix):
    grid = [row[:] for row in matrix]
    grid = mirror_mat(grid)
    (grid, score, cleared) = slide_left(grid)
    grid = mirror_mat(grid)
    return (grid, score, cleared)

def slide_up(matrix):
    grid = transpose_mat(matrix)
    (grid, score, cleared) = slide_left(grid)
    grid = transpose_mat(grid)
    return (grid, score, cleared)

def slide_down(matrix):
    grid = transpose_mat(matrix)
    (grid, score, cleared) = slide_right(grid)
    grid = transpose_mat(grid)
    return (grid, score, cleared)


def count_holes(matrix):
    holes = 0
    for i in range(len(matrix)):
        holes += matrix[i].count(0)
    return holes

def eccentricity(matrix, num_sigma=2):
    n = len(matrix)
    m = len(matrix[0])
    grid = np.array(matrix)
    miu = grid.mean()
    sigma = grid.std()
    threshold = round(miu + num_sigma * sigma)
    relevant = np.argwhere(grid >= threshold)
    corners = [[0,0],[0,m-1],[n-1,0],[n-1,m-1]]
    score = 0
    for r in range(len(relevant)):
        dists = []
        for c in range(len(corners)):
            a = relevant[r]
            b = corners[c]
            dists.append(np.linalg.norm(a-b))
            print(dists)
        min_distance = min(dists)
        score += min_distance
    return score

def avg_dist_between_largest(matrix, num_sigma=2):
    grid = np.array(matrix)
    miu = grid.mean()
    sigma = grid.std()
    threshold = round(miu + num_sigma * sigma)
    relevant = np.argwhere(grid >= threshold)
    distances = []
    done = []
    for r0 in range(len(relevant)):
        for r1 in range(len(relevant)):
            if [r0,r1] not in done and [r1,r0] not in done:
                distances.append(np.linalg.norm(relevant[r0]-relevant[r1]))
                done.append([[r0,r1]])
    avg_dist = sum(distances)/len(distances)
    return avg_dist

grid = [[4, 8, 8, 64],
        [0, 0, 0, 0 ],
        [0, 0, 0, 2 ],
        [4, 0, 0, 2 ]]



print(avg_dist_between_largest(grid))