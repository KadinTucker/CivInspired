

def write_matrix_to_csv(matrix, filename):
    """
    Given any matrix, write the matrix to a csv file
    The rows of the csv are the inner lists of the matrix
    """
    rows = []
    for x in range(len(matrix)):
        row = []
        for y in range(len(matrix[x])):
            row.append(str(matrix[x][y]))
        rows.append(",".join(row))
    csv = "\n".join(rows)
    newfile = open(filename, "w")
    newfile.writelines(csv)
    newfile.close()

def load_matrix_from_csv(filename):
    """
    Load a csv file with given filename into a matrix
    Is the inverse operation of the function `write_matrix_to_csv`
    Loads the entries as raw strings; use `set_matrix_to_integers` or `set_matrix_to_floats`
        to convert to the relevant type
    """
    datafile = open(filename, "r")
    raw_data = datafile.read().split("\n")
    line_data = []
    for line in raw_data:
        line_data.append(line.split(","))
    return line_data

def transpose_matrix(matrix):
    """
    Transpose the given matrix, making its rows its columns and its columns its rows
    """
    new_matrix = []
    for y in range(len(matrix[0])):
        new_matrix.append([])
        for x in range(len(matrix)):
            new_matrix[y].append(matrix[x][y])
    return new_matrix

def set_matrix_to_integers(matrix):
    """
    Set all entries of a matrix to integers, from e.g. strings
    """
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            matrix[x][y] = int(matrix[x][y])

def set_matrix_to_floats(matrix):
    """
    Set all entries of a matrix to floats, from e.g. strings
    """
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            matrix[x][y] = float(matrix[x][y])
