import random
import sys

import macro_resource
import macro_resourcegen
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

def spawn_resource(terrain_map, resource_id, abundance, valid_continents=(), continent_map=None):
    """
    Abundance is on a scale from 0.0 to 1.0, the chance of the resource appearing on an individual tile with a weight of 1.
    Assuming a total resource favorability of 1.0, if we want 1 in X tiles (approximately) to have the resource,
    then abundance should be 1 / X.
    If a fraction X of the map should be filled with the resource (again, favorability of 1.0),
    then abundance should be X.
    If a fraction Y of the map should be filled with ANY resource (again, favorability of 1.0),
    then abundance should be Y / n, where n is the number of different resources.
    A back-of-napkin calculation suggests 0.002 might be a good value for abundance.
    Abundance may also depend on the resource, though ideally this is accounted for in the weights.
    """
    spawn_map = [[False for _ in range(len(terrain_map[x]))] for x in range(len(terrain_map))]
    for x in range(len(terrain_map)):
        for y in range(len(terrain_map[x])):
            if continent_map is None or continent_map[x][y] in valid_continents:
                if random.random() < abundance * macro_resourcegen.RESOURCE_TERRAIN_FAVOR[resource_id][terrain_map[x][y]]:
                    spawn_map[x][y] = True
    return spawn_map

def compile_spawn_maps(spawn_maps):
    """
    Compiles a list of "spawn maps" that each tell whether a certain resource spawns in each location in the world.
    Resolves all conflicts (resources appearing on the same tile) with uniform randomness.
    Assumes that the list spawn_maps is indexed by resource id,
    and that all spawn maps have the same dimensions (obviously).
    """
    resource_map = [[0 for _ in range(len(spawn_maps[0][x]))] for x in range(len(spawn_maps[0]))]
    for x in range(len(spawn_maps[0])):
        for y in range(len(spawn_maps[0][x])):
            appearing = []
            for k in range(len(spawn_maps)):
                if spawn_maps[k][x][y]:
                    appearing.append(k)
            if len(appearing) > 0:
                resource_map[x][y] = random.choice(appearing)
    return resource_map

def get_resource_continents(terrain_map):
    continents = []
    for i in range(len(macro_resourcegen.CONTINENT_GROUP_TERRAIN_BLACKLIST)):
        continents.append(get_biota_continents(terrain_map, macro_resourcegen.CONTINENT_GROUP_TERRAIN_BLACKLIST[i],
                                               macro_resourcegen.CONTINENT_GROUP_DIVISIONS[i]))
    return continents

def assign_continents_to_resources():
    assignments = [[] for _ in range(len(macro_resource.RESOURCE_NAMES))]
    for i in range(len(macro_resourcegen.CONTINENT_GROUP_MEMBERS)):
        continents = [i for i in range(macro_resourcegen.CONTINENT_GROUP_DIVISIONS[i])]
        resources = macro_resourcegen.CONTINENT_GROUP_MEMBERS[i][:]
        random.shuffle(continents)
        random.shuffle(resources)
        index = 0
        print("AGAIN", i)
        while index < len(continents) or index < len(macro_resourcegen.CONTINENT_GROUP_MEMBERS[i]):
            print(index, resources[index % len(resources)])
            # noinspection PyTypeChecker
            assignments[resources[index % len(resources)]].append(continents[index % len(continents)])
            index += 1
    return assignments

def generate_spawn_maps(terrain_map):
    spawn_maps = [None for i in range(len(macro_resource.RESOURCE_NAMES))]
    continent_assignments = assign_continents_to_resources()
    print(continent_assignments)
    continents = get_resource_continents(terrain_map)
    print(len(macro_resourcegen.RESOURCE_CONTINENTAL_GROUP))
    for i in range(len(spawn_maps)):
        continent_group = macro_resourcegen.RESOURCE_CONTINENTAL_GROUP[i]
        continent = None
        if continent_group != 0:
            continent = continents[continent_group - 1]
        spawn_maps[i] = spawn_resource(terrain_map, i, 0.004, continent_assignments[i], continent)
    return spawn_maps


if __name__ == '__main__':
    import pygame
    import io_util
    climate = io_util.load_matrix_from_csv("climate_map.csv")
    for x in range(len(climate)):
        for y in range(len(climate[x])):
            climate[x][y] = CLIMATE_TO_TERRAIN[climate[x][y]]
    temperates_map = get_biota_continents(climate, [1, 2, 7, 8, 9, 10, 11], 4)
    tropics_map = get_biota_continents(climate, [1, 2, 3, 4, 5, 6, 7, 9, 11], 6)

    spawn_maps = generate_spawn_maps(climate)

    # spawn_maps = [spawn_resource(climate, i, 0.002) for i in range(len(macro_resource.RESOURCE_NAMES))]
    resource_map = compile_spawn_maps(spawn_maps)

    colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(50)]
    colors += [(50, 50, 50)]
    #res_class_colors = [(50, 50, 50), (50, 205, 50), (35, 70, 35), (100, 100, 20), (200, 50, 220)]
    #res_colors = [res_class_colors[macro_resourcegen.RESOURCE_CONTINENTAL_GROUP[i]]
    #              for i in range(len(macro_resource.RESOURCE_NAMES))]
    active_res = 0
    res_colors = [(50, 50, 50) for _ in range(len(macro_resource.RESOURCE_NAMES))]
    res_colors[active_res] = (255, 255, 0)

    display = pygame.display.set_mode((800, 600))

    maps = [temperates_map, tropics_map, resource_map]
    colormaps = [colors, colors, res_colors]
    map_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    map_index = (map_index + 1) % len(maps)
                elif event.key == pygame.K_SPACE:
                    res_colors[active_res] = (50, 50, 50)
                    active_res = (active_res + 1) % len(res_colors)
                    res_colors[active_res] = (255, 255, 0)
                    print(macro_resource.RESOURCE_NAMES[active_res])

        display.fill((0, 0, 0))
        for x in range(len(maps[map_index])):
            for y in range(len(maps[map_index][x])):
                pygame.draw.rect(display, colormaps[map_index][maps[map_index][x][y]], (3 * x, 3 * y, 3, 3))
        pygame.display.update()
