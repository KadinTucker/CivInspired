import math
import random

#min. 3 for both
# We like 360, 180, for lat long kind of thing
# Civ 3 does 100 x 100 for standard maps
# 158 x 63 makes for an aspect ratio of 360 x 140, and approximately keeps the 10000 total tiles of 100 x 100
# 140 x 70 makes for an aspect ratio of 2 : 1, and approximately keeps the 10000 total of 100 x 100

LENX = 40
LENY = 20

def get_neighbors(x, y):
    neighbors = []
    if x == LENX - 1:
        neighbors.append([0, y])
        neighbors.append([LENX - 2, y])
    elif x == 0:
        neighbors.append([1, y])
        neighbors.append([LENX - 1, y])
    else:
        neighbors.append([x - 1, y])
        neighbors.append([x + 1, y])
    if y == LENY - 1:
        neighbors.append([x, y - 1])
        neighbors.append([(x + LENX // 2) % LENX, y])
    elif y == 0:
        neighbors.append([x, 1])
        neighbors.append([(x + LENX // 2) % LENX, y])
    else:
        neighbors.append([x, y + 1])
        neighbors.append([x, y - 1])
    # FOR NO WRAPPING AROUND: 
    # if y < LENY - 1:
    #     neighbors.append([x, y + 1])
    # if y > 0:
    #     neighbors.append([x, y - 1])
    return neighbors

def wrap_coordinate(x, y):
    if y < 0:
        x += LENX // 2
        y = -y
    elif y >= LENY:
        x += LENX // 2
        y = 2 * LENY - y - 1
    x = x % LENX
    return x, y

def write_matrix_to_csv(matrix, filename):
    csv = ""
    for y in range(len(matrix[0])):
        row = ""
        for x in range(len(matrix)):
            row += str(matrix[x][y]) + ","
        csv += row + "\n"
    # print(csv)
    # print()
    # print()
    newfile = open(filename, "w")
    newfile.writelines(csv)
    newfile.close()

"""
The world consists of a set of plates. 
Each plate starts with one starting location, then spreads out to its neighbors in the following manner:
 - Tiles in the world are sequenced in a random order
 - If a tile without a plate is adjacent to another tile of an existing plate, it takes that plate's value
 - The world is cylindrical, with rows wrapping around
The plates are then sorted by their sizes, and the most optimal combination of plate sizes is chosen to match the land cover ratio:
 - Plates that are larger than the land cover ratio are disregarded and automatically ocean
 - With the remaining plates, all possible sums of their sizes are computed (this takes 2^n time, so avoid too many plates!)
 - The sum that is closest to the land cover ratio is picked out, and those plates added to make this optimal sum are land and the rest ocean.
Each plate is randomly assigned a cardinal direction of movement
The tiles that are borders between plates are then found, if they border a tile from a different plate they are a boundary. 
For each such border, the resulting elevation of the tile is affected based on the directions of movements of the plates
 - If the tile is moving toward the other plate it borders, the border is convergent.
 - If the tile is moving away from the other plate it borders, the border is divergent.
 - If the tile is moving parallel to the other, nothing happens
The the type of border and the types of plates involved determine what happens:
                           Continent  Ocean
Convergent: Continent       mountains   volcanos
            Oceanic         -           volcanic islands
Divergent:  Continent       ocean       ocean
            Oceanic         -           ocean
If more than two plates collide, the number of continental plates is preserved. 2C + 1O -> 2C, and 1C + 2O -> 1C 1O
"""



NPLATES = 5
LAND_COVER = 0.40

def create_plates():

    world_plates = [[-1 for i in range(LENY)] for j in range(LENX)]
    plate_sizes = [0 for i in range(NPLATES)]

    total_assigned = NPLATES

    # initialize plates

    for i in range(NPLATES):
        x = random.randint(0, LENX - 1)
        y = random.randint(0, LENY - 1)
        world_plates[x][y] = i

    # generate coordinate lists

    xvals = [i for i in range(LENX)]
    yvals = [i for i in range(LENY)]

    # grow plates

    while total_assigned < LENX * LENY:
        random.shuffle(xvals)
        random.shuffle(yvals)
        for x in xvals:
            for y in yvals:
                if world_plates[x][y] == -1:
                    neighbors = get_neighbors(x, y)
                    random.shuffle(neighbors)
                    for n in neighbors:
                        if world_plates[n[0]][n[1]] != -1:
                            world_plates[x][y] = world_plates[n[0]][n[1]]
                            plate_sizes[world_plates[n[0]][n[1]]] += 1
                            total_assigned += 1
                            break
    return world_plates, plate_sizes

# Some functions with different ways of assigning plates as continental versus oceanic

def archipelago_gen():
    plate_types = [0 for i in range(NPLATES)]
    plate_indices = [i for i in range(NPLATES)]
    random.shuffle(plate_indices)

    for i in range(int(NPLATES * LAND_COVER)):
        plate_types[plate_indices[i]] = 1
    return plate_types

def continents_gen(world_plates, plate_sizes):
    plate_types = [0 for i in range(NPLATES)]
    # Hemispheres: -1 means not yet assigned, 0 means both, 1 means east, 2 means west
    plate_hemispheres = [-1 for i in range(NPLATES)]
    for y in range(LENY):
        for x in range(LENX):
            if x < LENX / 2:
                hemisphere = 2
            else:
                hemisphere = 1
            if plate_hemispheres[world_plates[x][y]] == -1:
                plate_hemispheres[world_plates[x][y]] = hemisphere
            elif plate_hemispheres[world_plates[x][y]] != hemisphere:
                plate_hemispheres[world_plates[x][y]] = 0
    hemispheric = []
    for p in range(NPLATES):
        if plate_hemispheres[p] >= 1:
            hemispheric.append(p)
    total_land = 0
    index = 0
    random.shuffle(hemispheric)
    while total_land < LAND_COVER * LENX * LENY and index < len(hemispheric):
        plate_types[hemispheric[index]] = 1
        total_land += plate_sizes[hemispheric[index]]
        index += 1
    return plate_types

def continents_gen_new(world_plates, plate_sizes):
    plate_types = [0 for i in range(NPLATES)]
    xvals = [i for i in range(LENX)]
    yvals = [i for i in range(LENY)]
    done_plates = []
    total_area = 0
    random.shuffle(xvals)
    for x in xvals:
        random.shuffle(yvals)
        for y in yvals:
            plate = world_plates[x][y]
            antiplate = world_plates[(x + int(LENX / 2)) % LENX][LENY - y - 1]
            if not plate in done_plates:
                if antiplate in done_plates:
                    plate_types[plate] = 1 - plate_types[antiplate]
                else:
                    plate_types[plate] = 1
                    plate_types[antiplate] = 0
                if plate_types[plate] == 1:
                    total_area += plate_sizes[plate]
                if total_area >= LAND_COVER * LENX * LENY:
                    return plate_types
                done_plates.append(plate)
    return plate_types


# =========== NEW TECTONICS ALGORITHM ===========

def get_plate_velocity(scale):
    magnitude = random.random() * scale
    angle = 2 * math.pi * random.random()
    return (int(math.cos(angle) * magnitude), int(math.sin(angle) * magnitude))

# We decide that continental plates are faster than oceanic plates because that makes more interesting world gens (in reality, oceanic plates are "less impactful")
def assign_plate_velocities(plate_types, base_velocity = 4, continent_velocity = 5, ocean_velocity = 1):
    return [get_plate_velocity(base_velocity + continent_velocity * plate_types[i] + ocean_velocity * (1 - plate_types[i])) for i in range(NPLATES)]

def move_plates(world_plates, plate_types):
    # Now, move plates and imprint their elevation onto the world
    # Going too far north/south makes it wrap around to halfway around the x-axis
    num_plates = [[[0, 0] for i in range(LENY)] for j in range(LENX)] # The number of plates that have landed on each tile; oceanic, continental, respectively
    plate_velocities = assign_plate_velocities(plate_types)
    for x in range(LENX):
        for y in range(LENY):
            destination_x, destination_y = wrap_coordinate(x + plate_velocities[world_plates[x][y]][0], y + plate_velocities[world_plates[x][y]][1])
            # if destination_y < 0:
            #     destination_y = -destination_y
            #     destination_x += LENX // 2
            # elif destination_y >= LENY:
            #     destination_y = 2 * LENY - destination_y
            #     destination_x += LENX // 2
            # destination_x = destination_x % LENX
            num_plates[destination_x][destination_y][plate_types[world_plates[x][y]]] += 1
    return num_plates

# TODO: make plate movements happen twice?

"""
V = continental volcanos
I = volcanic islands
M = mountains
l = flat land
. = oceanic plate
- = nothing left behind (ocean or rift valley)

NUM PLATES of EACH TYPE:
Oceanic:        0   1   2   3
Continental:    
0               -   .   I   I
1               l   V   V   V
2               M   M   M   M
3               M   M   M   M

rules:
at least 2 continental -> M
at least 1 continental and at least 1 ocean -> V
at least 1 continental and no ocean -> l
no continental from here on out; all cases accounted for.
at least 2 oceanic -> I
exactly 1 oceanic -> .
no plates at all -> -
"""
def assign_tectonic_class(num_plates):
    tile_class = [[" " for i in range(LENY)] for j in range(LENX)]
    for y in range(LENY):
        for x in range(LENX):
            if num_plates[x][y][1] >= 2:
                tile_class[x][y] = "M"
            elif num_plates[x][y][1] >= 1 and num_plates[x][y][0] >= 1:
                tile_class[x][y] = "V"
            elif num_plates[x][y][1] >= 1 and num_plates[x][y][0] == 0:
                tile_class[x][y] = "l"
            elif num_plates[x][y][0] >= 2:
                tile_class[x][y] = "I"
            elif num_plates[x][y][0] == 1:
                tile_class[x][y] = "."
            else:
                tile_class[x][y] = "-"
    return tile_class

# TODO: repeat plate movements, have plates influence each other's movements

def generate_continents_tile_class():
    world_plates, plate_sizes = create_plates()
    plate_types = continents_gen(world_plates, plate_sizes)
    num_plates = move_plates(world_plates, plate_types)
    return assign_tectonic_class(num_plates)

"""
Elevation:
 - Elevation on the land is determined by proximity to the nearest water, plus other geological formations, plus a bit of noise
 - Mountains, whether continental or volcanic in nature, also tend to increase the elevation of surrounding formations
 - Mountains are taller than volcanos
Climate:
 - Temperature depends on latitude and altitude
 - Water access depends on three things:
   - Direction of prevailing winds; i.e., where water comes from (footprint)
   - Rain shadow
   - Evaporation amount (due to temperature)
 - These things are determined in latitude bands, with different coastal directions:
   - East coast:
     - 0-10: Jungle
     - 10-25: Plains/Forest mix
     - 25-40: Grassland
     - 40-50: Forest
     - 50+: Tundra
   - West coast:
     - 0-15: Jungle
     - 15-30: Desert
     - 30-40: Grassland
     - 45-60: Forest
     - 60+: Taiga
   - Continental:
     - 0-15: Jungle
     - 15-40: Desert
     - 40-50: Plains
     - 50-60: Forest (on plains)
     - 60+ Taiga/Tundra mix
 - A place is considered coastal if it does not have above a certain amount of elevation gain. Whichever elevation gain is smaller to source the water.
 - The world, in y coordinate, is considered to be between -70 and +70 latitude. 
"""

OCEANS = ["."]
SEAS = [".", "I"]
WATERS = [".", "I", "-"]
LANDS = ["l", "M", "V"]

WORLDSIZE = math.sqrt(LENX * LENY)
CONTINENT_LEVEL = 0.7
SEA_LEVEL = 1.0
ELEV_GAIN = 0.0025 # how much elevation is gained per tile away from nearest body of water per size of world. In a 100 tile world, 0.01 is 1 elevation per tile. 
MOUNTAIN_ELEV = 4 # in real world analogy, about 1500 m. 
MOUNTAIN_ELEV_SHARING = 0.25 # how much of mountain elevation is shared with its neighboring tiles
VOLCANO_ELEV = 2 # in real world analogy, about 750 m. 
VOLCANO_ELEV_SHARING = 0.25 # how much of volcano elevation is shared with its neighboring tiles
DIVERGENCE_ELEV = 0.1 # the elevation bonus given to divergence zones (the class - )
DIVERGENCE_LOWERING = 0.5 # the fraction of elevation gain of divergence zones due to distance from actual oceans
ISLAND_BASE_ELEV = 0.5 # the base elevation of oceanic island areas
DEEP_ISLAND_ELEV_GAIN = 0.005 # the amount of elevation gained per tile away from the nearest non-island body of water per world size
ISLAND_BONUS_ELEV = 0.6 # the amount of extra elevation an island area gets if it gets so lucky
ISLAND_CHANCE = 0.3 # the chance of a volcanic area in the ocean forming land
ISLAND_SHARING = 0.3 # the amount of elevation an island gives to its neighbors if it indeed forms
LATITUDE_GAIN_PER_ELEVATION = 4 # based on rough b.o.n. calculation, reduced a bit for playability
LATITUDE_RANGE = 180.0 # the total range of latitude covered in the y direction of the world
MAX_WATER_SOURCE_ELEVATION = (MOUNTAIN_ELEV + 4 * LENX * ELEV_GAIN) / 6.0
RELATIVE_SLOPE_HILL_THRESHHOLD = 1.5 # how many times more the slope is than the typical inland slope for terrain to be considered "hills"
RELATIVE_SLOPE_MOUNTAIN_THRESHHOLD = 6 # how many times more the slope is than the typical inland slope for terrain to be considered "mountains"

def find_nearest_distance_to_water(tile_classes, location, waters):
    """
    inefficiently finds the closest distance to water for a given location
    """
    min_distance = LENX + LENY
    for x in range(len(tile_classes)):
        for y in range(len(tile_classes[x])):
            if tile_classes[x][y] in WATERS:
                distance = abs(location[0] - x) + abs(location[1] - y)
                if distance < min_distance:
                    min_distance = distance
    return min_distance

def build_elevation_map(tile_class):
    """
    Constructs a map of elevations based on the tile classes defined previously
    """
    elev_map = [[0.0 for i in range(LENY)] for j in range(LENX)]
    for x in range(LENX):
        for y in range(LENY):
            if tile_class[x][y] in LANDS:
                elev_map[x][y] += CONTINENT_LEVEL + find_nearest_distance_to_water(tile_class, (x, y), WATERS) * WORLDSIZE * ELEV_GAIN
                if tile_class[x][y] == "M":
                    elev_map[x][y] += MOUNTAIN_ELEV
                    for n in get_neighbors(x, y):
                        elev_map[n[0]][n[1]] += MOUNTAIN_ELEV * MOUNTAIN_ELEV_SHARING
                elif tile_class[x][y] == "V":
                    elev_map[x][y] += VOLCANO_ELEV
                    for n in get_neighbors(x, y):
                        elev_map[n[0]][n[1]] += VOLCANO_ELEV * VOLCANO_ELEV_SHARING
            if tile_class[x][y] == "I":
                elev_map[x][y] += ISLAND_BASE_ELEV + find_nearest_distance_to_water(tile_class, (x, y), OCEANS) * WORLDSIZE * DEEP_ISLAND_ELEV_GAIN
                if random.random() < ISLAND_CHANCE:
                    elev_map[x][y] += ISLAND_BONUS_ELEV
                    for n in get_neighbors(x, y):
                        elev_map[n[0]][n[1]] += ISLAND_SHARING
            if tile_class[x][y] == "-":
                elev_map[x][y] += DIVERGENCE_ELEV + find_nearest_distance_to_water(tile_class, (x, y), SEAS) * WORLDSIZE * DIVERGENCE_LOWERING
    return elev_map

"""
l - above 1 elevation
- - below 1 elevation, but not connected to an actual ocean, defined as tile class `.`
. - below 1 elevation, and connected to an actual ocean, defined as tile class `.`
"""
def build_ocean_connection_map(elev_map):
    connection_map = [["" for i in range(LENY)] for j in range(LENX)]
    for x in range(LENX):
        for y in range(LENY):
            if elev_map[x][y] == 0.0:
                connection_map[x][y] = "."
            elif elev_map[x][y] >= SEA_LEVEL:
                connection_map[x][y] = "l"
            else:
                connection_map[x][y] = "-"
    def connect_neighbors_to_ocean(connection_map, x, y):
        neighbors = get_neighbors(x, y)
        for n in neighbors:
            if connection_map[n[0]][n[1]] == "-":
                connection_map[n[0]][n[1]] = "."
                connect_neighbors_to_ocean(connection_map, n[0], n[1])
    for x in range(LENX):
        for y in range(LENY):
            if connection_map[x][y] == ".":
                connect_neighbors_to_ocean(connection_map, x, y)
    return connection_map


def find_water_longitudinally(connection_map, elev_map, location, direction):
    """
    Finds the distance to the nearest major water body to a location in an east or west direction only
    direction: East: +1; West: -1
    Also counts the total elevation loss down to the water
    """
    distance = 0
    elev_loss = 0
    found = connection_map[location[0]][location[1]] == "."
    search_location = location
    while not found and distance < LENX:
        initial_elev = elev_map[search_location[0]][search_location[1]]
        distance += 1
        search_location = ((search_location[0] + direction) % LENX, search_location[1])
        found = elev_map[search_location[0]][search_location[1]] < 1
        if not found:
            elev_loss += max(initial_elev - elev_map[search_location[0]][search_location[1]], 0)
    return distance, elev_loss

"""
Water classes:
- - open water (ocean or lake)
w - west coast
e - east coast
i - both sides coast
c - inland continent
"""
def build_waterclass_map(elev_map):
    waterclass_map = [["" for i in range(LENY)] for j in range(LENX)]
    connection_map = build_ocean_connection_map(elev_map)
    for x in range(LENX):
        for y in range(LENY):
            if connection_map[x][y] == ".":
                waterclass_map[x][y] = "-"
            else:
                east_dist, east_elev = find_water_longitudinally(connection_map, elev_map, (x, y), 1)
                west_dist, west_elev = find_water_longitudinally(connection_map, elev_map, (x, y), -1)
                east_coast = east_elev < MAX_WATER_SOURCE_ELEVATION
                west_coast = west_elev < MAX_WATER_SOURCE_ELEVATION
                if west_coast and east_coast:
                    waterclass_map[x][y] = "i"
                elif west_coast:
                    waterclass_map[x][y] = "w"
                elif east_coast:
                    waterclass_map[x][y] = "e"
                else:
                    waterclass_map[x][y] = "c"
    return waterclass_map

# csv = ""
# for y in range(LENY):
#     row = ""
#     for x in range(LENX):
#         row += waterclass_map[x][y] + ","
#     csv += row + "\n"
# # print(csv)
# # print()
# # print()
# newfile = open("watermap.csv", "w")
# newfile.writelines(csv)

def convert_to_latitude(y):
    return LATITUDE_RANGE / LENY * (y - LENY / 2)

"""
Climate Key:
J - Jungle
S - "Scrubland" (Plains/Fprest mix)
g - Grassland
F - Forest (temperate forest)
u - Tundra
d - Desert
T - Taiga
p - Plains
I - Ice Cap
- - Ice sheet ocean
~ - Ocean
 - These things are determined in latitude bands, with different coastal directions:
   - East coast:
     - 0-10: Jungle
     - 10-25: Plains/Forest mix
     - 25-40: Grassland
     - 40-50: Forest
     - 50-60: Plains
     - 60+: Tundra
   - West coast:
     - 0-15: Jungle
     - 15-30: Desert
     - 30-40: Grassland
     - 40-50: Forest
     - 60+: Taiga
   - Both East and West - takes the wetter of the east/west variety
     - 0-15: Jungle
     - 15-25: Plains forest
     - 25-40: Grassland
     - 40-60: Forest
     - 60+: Taiga
   - Continental:
     - 0-15: Jungle
     - 15-40: Desert
     - 40-50: Plains
     - 50-60: Forest (on plains)
     - 60+ Taiga/Tundra mix
 - Arctic: (regardless of other class):
     - 70+ latitude - ice cap
"""

def build_climateclass_map(waterclass_map, elev_map):
    climateclass_map = [["" for i in range(LENY)] for j in range(LENX)]
    for x in range(LENX):
        for y in range(LENY):
            latitude = abs(convert_to_latitude(y)) + LATITUDE_GAIN_PER_ELEVATION * (elev_map[x][y] - 1)
            if waterclass_map[x][y] == "-":
                if latitude >= 70:
                    climateclass_map[x][y] = "-"
                else:
                    climateclass_map[x][y] = "~"
            else:
                if latitude >= 70:
                    climateclass_map[x][y] = "I"
                elif waterclass_map[x][y] == "e":
                    if latitude < 10:
                        climateclass_map[x][y] = "J"
                    elif latitude < 25:
                        climateclass_map[x][y] = "S"
                    elif latitude < 40:
                        climateclass_map[x][y] = "g"
                    elif latitude < 50:
                        climateclass_map[x][y] = "F"
                    elif latitude < 60:
                        climateclass_map[x][y] = "p"
                    else:
                        climateclass_map[x][y] = "u"
                elif waterclass_map[x][y] == "w":
                    if latitude < 10:
                        climateclass_map[x][y] = "J"
                    elif latitude < 15:
                        climateclass_map[x][y] = "S"
                    elif latitude < 30:
                        climateclass_map[x][y] = "d"
                    elif latitude < 40:
                        climateclass_map[x][y] = "g"
                    elif latitude < 60:
                        climateclass_map[x][y] = "F"
                    else:
                        climateclass_map[x][y] = "T"
                elif waterclass_map[x][y] == "i":
                    if latitude < 15:
                        climateclass_map[x][y] = "J"
                    elif latitude < 25:
                        climateclass_map[x][y] = "S"
                    elif latitude < 40:
                        climateclass_map[x][y] = "g"
                    elif latitude < 60:
                        climateclass_map[x][y] = "F"
                    else:
                        climateclass_map[x][y] = "T"
                elif waterclass_map[x][y] == "c":
                    if latitude < 10:
                        climateclass_map[x][y] = "J"
                    elif latitude < 15:
                        climateclass_map[x][y] = "S"
                    elif latitude < 40:
                        climateclass_map[x][y] = "d"
                    elif latitude < 50:
                        climateclass_map[x][y] = "p"
                    elif latitude < 60:
                        climateclass_map[x][y] = "p"
                    else:
                        climateclass_map[x][y] = "T"
    return climateclass_map

def get_maximum_slope(elev_map, x, y, lower_bound=SEA_LEVEL):
    max_slope = 0
    for n in get_neighbors(x, y):
        if elev_map[n[0]][n[1]] > lower_bound:
            slope = elev_map[n[0]][n[1]] - elev_map[x][y]
            if slope > max_slope:
                max_slope = slope
    return max_slope

"""
Key:
. - deep ocean; topography is irrelevant
+ - shallow ocean
v - sink; all neighbors are taller or at level with the location
f - flat; no slope is high enough for the location to be considered a hill
H - hill; at least one slope is high enough for the location to be considered a hill
M - mountain; at least one slope is high enough for the location to be considered a mountain
"""
def build_topography_map(elev_map):
    topography_map = [["" for i in range(LENY)] for j in range(LENX)]
    connection_map = build_ocean_connection_map(elev_map)
    for x in range(LENX):
        for y in range(LENY):
            if connection_map[x][y] == ".":
                if elev_map[x][y] < CONTINENT_LEVEL:
                    topography_map[x][y] = "."
                else:
                    topography_map[x][y] = "+"
            else:
                slope = get_maximum_slope(elev_map, x, y)
                if slope <= 0:
                    topography_map[x][y] = "v"
                else:
                    slope_factor = slope / (WORLDSIZE * ELEV_GAIN)
                    if slope_factor >= RELATIVE_SLOPE_MOUNTAIN_THRESHHOLD:
                        topography_map[x][y] = "M"
                    elif slope_factor >= RELATIVE_SLOPE_HILL_THRESHHOLD:
                        topography_map[x][y] = "H"
                    else:
                        topography_map[x][y] = "f"
    return topography_map

"""
Direction of flow, from high to low slopes. If the centre is the lowest, the direction is 0. 
    1 2 3
    4 0 5
    6 7 8
"""
diagonals = [1, 3, 6, 8]

def get_d8_coordinate_list_from(x, y):
    return [(x, y), wrap_coordinate(x - 1, y - 1), wrap_coordinate(x, y - 1), wrap_coordinate(x + 1, y - 1), wrap_coordinate(x - 1, y), wrap_coordinate(x + 1, y), wrap_coordinate(x - 1, y + 1), wrap_coordinate(x, y + 1), wrap_coordinate(x + 1, y + 1)]

def build_d8_map(elev_map):
    flow_map = [["" for i in range(LENY)] for j in range(LENX)]
    for x in range(LENX):
        for y in range(LENY):
            min_slope = 0
            min_slope_index = 0
            n = get_d8_coordinate_list_from(x, y)
            for i in range(len(n)):
                slope = elev_map[n[i][0]][n[i][1]] - elev_map[x][y]
                if i in diagonals:
                    slope *= 0.71 
                if slope < min_slope:
                    min_slope = slope
                    min_slope_index = i
            flow_map[x][y] = min_slope_index
    return flow_map

CLIMATE_WATER_CONTRIBUTION = {
    "J" : 4,
    "S" : 2,
    "g" : 2,
    "F" : 3,
    "u" : 1,
    "d" : 0,
    "T" : 2,
    "p" : 1,
    "I" : 1,
    "-" : 0,
    "~" : 0
}
CLIMATE_WATER_LOSS = {
    "J" : 1,
    "S" : 2,
    "g" : 1,
    "F" : 1,
    "u" : 0,
    "d" : 1,
    "T" : 0,
    "p" : 0,
    "I" : 0,
    "-" : 0,
    "~" : 0
}
RUNOFF_LOSS_COEFF = 0.25 # How much of relative runoff is lost when flowing through lossy terrains
RIVER_THRESHHOLD = WORLDSIZE / 16

def build_water_accumulation_map(climate_map, elev_map):
    accumulation_map = [[0.0 for i in range(LENY)] for j in range(LENX)]
    d8 = build_d8_map(elev_map)
    for x in range(LENX):
        for y in range(LENY):
            contribution = CLIMATE_WATER_CONTRIBUTION[climate_map[x][y]]
            destx = x
            desty = y
            while contribution > 0 and climate_map[x][y] not in ["-", "~"] and d8[destx][desty] != 0:
                flow_direction = get_d8_coordinate_list_from(destx, desty)[d8[destx][desty]]
                destx = flow_direction[0]
                desty = flow_direction[1]
                accumulation_map[destx][desty] += contribution
                contribution -= CLIMATE_WATER_LOSS[climate_map[destx][desty]] * RUNOFF_LOSS_COEFF
    return accumulation_map

def build_watershed_map(climate_map, elev_map):
    watershed_map = [["" for i in range(LENY)] for j in range(LENX)]
    accumulation_map = build_water_accumulation_map(climate_map, elev_map)
    for x in range(LENX):
        for y in range(LENY):
            if climate_map[x][y] in ["-", "~"]:
                watershed_map[x][y] = "."
            elif accumulation_map[x][y] >= RIVER_THRESHHOLD:
                watershed_map[x][y] = "|"
            else:
                watershed_map[x][y] = "-"
    return watershed_map

def get_climate_from_tectonics(tile_class):
    elev_map = build_elevation_map(tile_class)
    waterclass_map = build_waterclass_map(elev_map)
    return build_climateclass_map(waterclass_map, elev_map)

def generate_write_all_maps():
    world_plates, plate_sizes = create_plates()
    plate_types = continents_gen(world_plates, plate_sizes)
    write_matrix_to_csv(world_plates, "platesmap.csv")
    plates_density = move_plates(world_plates, plate_types)
    write_matrix_to_csv(plates_density, "tectonicsmap.csv")
    tile_class = assign_tectonic_class(plates_density)
    write_matrix_to_csv(tile_class, "geologymap.csv")
    elev_map = build_elevation_map(tile_class)
    write_matrix_to_csv(elev_map, "elevationmap.csv")
    waterclass_map = build_waterclass_map(elev_map)
    write_matrix_to_csv(waterclass_map, "waterclassmap.csv")
    climate_map = build_climateclass_map(waterclass_map, elev_map)
    write_matrix_to_csv(climate_map, "climatemap.csv")
    topography_map = build_topography_map(elev_map)
    write_matrix_to_csv(topography_map, "topographymap.csv")
    watershed_map = build_watershed_map(climate_map, elev_map)
    write_matrix_to_csv(watershed_map, "watershedmap.csv")

def build_climate_from_scratch():
    return get_climate_from_tectonics(generate_continents_tile_class())

def build_elev_from_scratch():
    world_plates, plate_sizes = create_plates()
    plate_types = continents_gen(world_plates, plate_sizes)
    plates_density = move_plates(world_plates, plate_types)
    tile_class = assign_tectonic_class(plates_density)
    return build_elevation_map(tile_class)

if __name__ == "__main__":
    generate_write_all_maps()