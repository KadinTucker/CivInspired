import random
import sys

import worldgen

CLIMATE_TO_TERRAIN = {
    "-": 2,
    "~": 2,
    "=": 1,
    "g": 3,
    "p": 4,
    "u": 5,
    "I": 11,
    "d": 6,
    "F": 7,
    "S": 8,
    "T": 9,
    "J": 10
}

def split_continents(terrain_map, terrain_blacklist):
    continent_map = [[-1 for _ in range(len(terrain_map[x]))] for x in range(len(terrain_map))]
    continent_sizes = [0]

    def fill_neighbors(x, y, continent):
        for n in worldgen.get_neighbors(x, y, len(terrain_map), len(terrain_map[x])):
            if continent_map[n[0]][n[1]] == -1 and terrain_map[n[0]][n[1]] not in terrain_blacklist:
                continent_map[n[0]][n[1]] = continent
                continent_sizes[continent] += 1
                fill_neighbors(n[0], n[1], continent)

    continent = 0
    all_coords = [(i % len(terrain_map), i // (len(terrain_map)))
                  for i in range(len(terrain_map) * len(terrain_map[0]))]
    random.shuffle(all_coords)
    coord = 0
    while coord < len(all_coords):
        start = all_coords[coord]
        if terrain_map[start[0]][start[1]] not in terrain_blacklist and continent_map[start[0]][start[1]] == -1:
            fill_neighbors(start[0], start[1], continent)
            continent += 1
            continent_sizes.append(1)
        coord += 1
    print(continent)
    return continent_map, continent_sizes

def find_largest_continents(continent_sizes, num_continents):
    indices = [i for i in range(len(continent_sizes))]
    largest = sorted(indices, key=lambda i: continent_sizes[i], reverse=True)
    return largest[:num_continents]

def filter_largest_continents(continent_map, largest, total_continents):
    index_of = [-1 for i in range(total_continents)]
    for l in range(len(largest)):
        index_of[largest[l]] = l
    for x in range(len(continent_map)):
        for y in range(len(continent_map[x])):
            if continent_map[x][y] != -1:
                continent_map[x][y] = index_of[continent_map[x][y]]

def get_biota_continents(terrain_map, terrain_blacklist, number):
    continent_map, sizes = split_continents(terrain_map, terrain_blacklist)
    largest = find_largest_continents(sizes, number)
    filter_largest_continents(continent_map, largest, len(sizes))
    return continent_map

if __name__ == '__main__':
    import pygame
    import io_util
    climate = io_util.load_matrix_from_csv("climate_map.csv")
    for x in range(len(climate)):
        for y in range(len(climate[x])):
            climate[x][y] = CLIMATE_TO_TERRAIN[climate[x][y]]
    temperates_map = get_biota_continents(climate, [1, 2, 7, 8, 9, 10, 11], 4)
    tropics_map = get_biota_continents(climate, [1, 2, 3, 4, 5, 6, 7, 9, 11], 6)

    colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(6)]
    colors += [(50, 50, 50)]
    display = pygame.display.set_mode((800, 600))

    maps = [temperates_map, tropics_map]
    map_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    map_index = (map_index + 1) % len(maps)

        display.fill((0, 0, 0))
        for x in range(len(maps[map_index])):
            for y in range(len(maps[map_index][x])):
                pygame.draw.rect(display, colors[maps[map_index][x][y]], (3 * x, 3 * y, 3, 3))
        pygame.display.update()
