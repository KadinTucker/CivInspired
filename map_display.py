import pygame
import sys
import random

import terrain_palettes

TERRAIN_PALETTES = {
    "J": terrain_palettes.JUNGLE_E,
    "d": terrain_palettes.DESERT_E,
    "S": terrain_palettes.SCRUB_E,
    "g": terrain_palettes.GRASSLAND_E,
    "p": terrain_palettes.PLAINS_E,
    "F": terrain_palettes.FOREST_E,
    "T": terrain_palettes.TAIGA_E,
    "u": terrain_palettes.TUNDRA_E,
    "I": terrain_palettes.ICE_E,
    "~": terrain_palettes.OCEAN_E,
    "-": terrain_palettes.COAST_E,
    "=": terrain_palettes.COAST_E,
}

def transpose_matrix(matrix):
    newmatrix = []
    for y in range(len(matrix[0])):
        newmatrix.append([])
        for x in range(len(matrix)):
            newmatrix[y].append(matrix[x][y])
    return newmatrix

def load_matrix_from_csv(filename):
    datafile = open(filename, "r")
    raw_data = datafile.read().split(",\n")
    raw_data.remove("")
    line_data = []
    for line in raw_data:
        line_data.append(line.split(","))
    final_data = transpose_matrix(line_data)
    return final_data

def load_climate_map(filename):
    return load_matrix_from_csv(filename)

def get_draw_coordinate(x, y, map_corner, tile_size, map_dimensions):
    offset = 0
    if tile_size[0] * map_dimensions[0] < PANE_DIMENSIONS[0]:
        offset = (PANE_DIMENSIONS[0] - int(tile_size[0]) * map_dimensions[0]) // 2
    return (offset + (x + map_corner[0]) % map_dimensions[0] * int(tile_size[0]), (y + map_corner[1]) * int(tile_size[0]))

def draw_terrain(display, colormap, map_corner, tile_size):
    for x in range(len(colormap)):
        for y in range(len(colormap[x])):
            c = get_draw_coordinate(x, y, map_corner, tile_size, (len(colormap), len(colormap[x])))
            pygame.draw.rect(display, colormap[x][y],
                             pygame.Rect(c[0], c[1], int(tile_size[0]), int(tile_size[1])))
    pygame.display.update()

def generate_color_map(climatemap):
    colormap = [[(0, 0, 0) for _ in range(len(climatemap[x]))] for x in range(len(climatemap))]
    for x in range(len(climatemap)):
        for y in range(len(climatemap[x])):
            colormap[x][y] = random.choice(TERRAIN_PALETTES[climatemap[x][y]])
    return colormap

PANE_DIMENSIONS = (800, 400)

def main():
    pygame.init()
    font = pygame.font.Font(None, 18)
    display = pygame.display.set_mode(PANE_DIMENSIONS)
    climatemap = load_climate_map("climatemap.csv")
    colormap = generate_color_map(climatemap)
    map_corner = (0, 0)
    tile_size = (8, 8)
    while True:
        display.fill((0, 0, 0))
        draw_terrain(display, colormap, map_corner, tile_size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    map_corner = (map_corner[0] - 5, map_corner[1])
                elif event.key == pygame.K_LEFT:
                    map_corner = (map_corner[0] + 5, map_corner[1])
                if event.key == pygame.K_UP:
                    map_corner = (map_corner[0], map_corner[1] + 5)
                elif event.key == pygame.K_DOWN:
                    map_corner = (map_corner[0], map_corner[1] - 5)
                elif event.key == pygame.K_PLUS:
                    prev_tiles = (PANE_DIMENSIONS[0] / tile_size[0], PANE_DIMENSIONS[1] / tile_size[1])
                    tile_size = (tile_size[0] * 1.5, tile_size[1] * 1.5)
                    new_tiles = (PANE_DIMENSIONS[0] / tile_size[0], PANE_DIMENSIONS[1] / tile_size[1])
                    map_corner = (map_corner[0] - int(prev_tiles[0] - new_tiles[0]) // 2,
                                  map_corner[1] - int(prev_tiles[1] - new_tiles[1]) // 2)
                elif event.key == pygame.K_MINUS:
                    prev_tiles = (PANE_DIMENSIONS[0] / tile_size[0], PANE_DIMENSIONS[1] / tile_size[1])
                    tile_size = (tile_size[0] / 1.5, tile_size[1] / 1.5)
                    new_tiles = (PANE_DIMENSIONS[0] / tile_size[0], PANE_DIMENSIONS[1] / tile_size[1])
                    map_corner = (map_corner[0] - int(prev_tiles[0] - new_tiles[0]) // 2,
                                  map_corner[1] - int(prev_tiles[1] - new_tiles[1]) // 2)

if __name__ == "__main__":
    main()