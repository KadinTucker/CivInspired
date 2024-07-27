
def get_neighbors(x, y, lenx, leny):
    neighbors = [wrap_coordinate(x + 1, y, lenx, leny), wrap_coordinate(x - 1, y, lenx, leny),
                 wrap_coordinate(x, y + 1, lenx, leny), wrap_coordinate(x, y - 1, lenx, leny)]
    return neighbors

def wrap_coordinate(x, y, lenx, leny):
    if y < 0:
        x += lenx // 2
        y = -y
    elif y >= leny:
        x += lenx // 2
        y = 2 * leny - y - 1
    x = x % lenx
    return x, y

def get_minimum_distance_coordinate_unvisited(visited, distances):
    coordinate = None
    minimum = -1
    for x in range(len(visited)):
        for y in range(len(visited[x])):
            if not visited[x][y]:
                distance = distances[x][y]
                if distance != -1 and (minimum == -1 or distance < minimum):
                    coordinate = (x, y)
                    minimum = distance
    return coordinate # if None, then it didn't find anything.

def dijkstra_on_matrix(matrix, start_x, start_y):
    """
    Performs Dijkstra's algorithm on a matrix of "weight" values.
    The matrix is considered to have neighbors counted as in the "get neighbors" function above,
    with earth-like wrapping.
    The matrix contains the cost of moving to that point on the grid.
    """
    visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    start_distance = [[-1 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    start_distance[start_x][start_y] = 0
    current_x = start_x
    current_y = start_y
    while True:  # or something?
        neighbors = get_neighbors(current_x, current_y, len(matrix), len(matrix[0]))
        for n in neighbors:
            if not visited[n[0]][n[1]]:
                if matrix[n[0]][n[1]] != -1 and start_distance[current_x][current_y] != -1:
                    new_distance = matrix[n[0]][n[1]] + start_distance[current_x][current_y]
                    if new_distance < start_distance[n[0]][n[1]] or start_distance[n[0]][n[1]] == -1:
                        start_distance[n[0]][n[1]] = new_distance
        visited[current_x][current_y] = True
        next_coordinate = get_minimum_distance_coordinate_unvisited(visited, start_distance)
        if next_coordinate is None:
            break
        current_x = next_coordinate[0]
        current_y = next_coordinate[1]
    return start_distance
