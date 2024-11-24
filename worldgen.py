import math
import random

import io_util
import dijkstra
import macro_worldgen

def get_neighbors(x, y, lenx, leny):
    """
    Gets all of the coordinates that neighbor the given x, y coordinate
    Uses the `wrap_coordinate` function to handle wrapping over the edges
    """
    neighbors = [wrap_coordinate(x + 1, y, lenx, leny), wrap_coordinate(x - 1, y, lenx, leny),
                 wrap_coordinate(x, y + 1, lenx, leny), wrap_coordinate(x, y - 1, lenx, leny)]
    return neighbors

def wrap_coordinate(x, y, lenx, leny):
    """
    Wraps a coordinate so that it does not go over the edges of the world
    If the x coordinate is outside the range of possible indices, the coordinate
        wraps around directly to the opposite edge
    If the y coordinate is outside the range of possible indices, the coordinate
        wraps around to the same distance from the edge, but halfway around in the x coordinate
    This wrapping aims to mimic the wrapping of latitude and longitude in spherical coordinates
    """
    if y < 0:
        x += lenx // 2
        y = -y
    elif y >= leny:
        x += lenx // 2
        y = 2 * leny - y - 1
    x = x % lenx
    return x, y

def create_plates():
    """
    Creates tectonic plates to be moved around, making topography and shaping the world
    """
    world_plates = [[-1 for _ in range(macro_worldgen.LENY)] for _ in range(macro_worldgen.LENX)]
    plate_sizes = [0 for _ in range(macro_worldgen.N_PLATES)]

    # Record the total number of tiles assigned to a plate
    total_assigned = macro_worldgen.N_PLATES

    # Initialize plates by randomly planting single plates
    for i in range(macro_worldgen.N_PLATES):
        x = random.randint(0, macro_worldgen.LENX - 1)
        y = random.randint(0, macro_worldgen.LENY - 1)
        world_plates[x][y] = i

    # Generate coordinate lists
    xvals = [i for i in range(macro_worldgen.LENX)]
    yvals = [i for i in range(macro_worldgen.LENY)]

    # Grow plates, shuffling coordinate lists, until all tiles have been assigned a plate
    while total_assigned < macro_worldgen.LENX * macro_worldgen.LENY:
        random.shuffle(xvals)
        random.shuffle(yvals)
        for x in xvals:
            for y in yvals:
                if world_plates[x][y] == -1:
                    neighbors = get_neighbors(x, y, macro_worldgen.LENX, macro_worldgen.LENY)
                    random.shuffle(neighbors)
                    for n in neighbors:
                        if world_plates[n[0]][n[1]] != -1:
                            world_plates[x][y] = world_plates[n[0]][n[1]]
                            plate_sizes[world_plates[n[0]][n[1]]] += 1
                            total_assigned += 1
                            break
    return world_plates, plate_sizes

def continents_gen(world_plates, plate_sizes):
    """
    Assigns each plate as either continental or oceanic, according to a 'continents' generation
    This means that only plates that are entirely located in one hemisphere are assigned as continents
    """
    plate_types = [0 for _ in range(macro_worldgen.N_PLATES)]
    # Hemispheres: -1 means not yet assigned, 0 means both, 1 means east, 2 means west
    plate_hemispheres = [-1 for _ in range(macro_worldgen.N_PLATES)]
    for y in range(len(world_plates[0])):
        for x in range(len(world_plates)):
            if x < len(world_plates) / 2:
                hemisphere = 2
            else:
                hemisphere = 1
            if plate_hemispheres[world_plates[x][y]] == -1:
                plate_hemispheres[world_plates[x][y]] = hemisphere
            elif plate_hemispheres[world_plates[x][y]] != hemisphere:
                plate_hemispheres[world_plates[x][y]] = 0
    hemispheric = []
    for p in range(macro_worldgen.N_PLATES):
        if plate_hemispheres[p] >= 1:
            hemispheric.append(p)
    total_land = 0
    index = 0
    random.shuffle(hemispheric)
    while (total_land < macro_worldgen.LAND_COVER * len(world_plates) * len(world_plates[0])
           and index < len(hemispheric)):
        plate_types[hemispheric[index]] = 1
        total_land += plate_sizes[hemispheric[index]]
        index += 1
    return plate_types

def get_plate_velocity(scale):
    """
    For the purposes of moving plates, get a randomized plate velocity in two dimensions
    Returns a tuple of x and y components of velocity
    """
    magnitude = random.random() * scale
    angle = 2 * math.pi * random.random()
    return int(math.cos(angle) * magnitude), int(math.sin(angle) * magnitude)

def assign_plate_velocities(plate_types):
    """
    Assigns randomized plate velocities to each plate, depending on their types
    """
    return [get_plate_velocity(macro_worldgen.PLATE_VELOCITY + macro_worldgen.CONTINENT_VELOCITY * plate_types[i]
                               + macro_worldgen.OCEAN_VELOCITY * (1 - plate_types[i])) for i in range(len(plate_types))]

def move_plates(world_plates, plate_types, plate_velocities):
    """
    Plates move and intersect each other, according to the provided velocities
    Returns a map describing how many oceanic and how many continental plates end up on each location at the end
    """
    num_plates = [[[0, 0] for _ in range(len(world_plates[x]))] for x in range(len(world_plates))]
    for x in range(len(world_plates)):
        for y in range(len(world_plates[x])):
            destination_x, destination_y = wrap_coordinate(x + plate_velocities[world_plates[x][y]][0],
                                                           y + plate_velocities[world_plates[x][y]][1],
                                                           len(world_plates), len(world_plates[x]))
            num_plates[destination_x][destination_y][plate_types[world_plates[x][y]]] += 1
    return num_plates

def assign_tectonic_class(num_plates):
    """
    Given the number of oceanic/continental plates landing on each tile after movement, assign a 'tile class'
    according to the following rules:
     - If there are at least two continental plates, assign M 'Mountain'
     - If there is exactly one continental plate and at least one oceanic plate, assign V 'Volcano'
     - If there is exactly one continental plate and no oceanic plates, assign l 'land'
     - If there are no continental plates and at least two oceanic plates, assign I 'island'
     - If there are no continental plates and exactly one oceanic plate, assign . 'ocean'
     - If there are no plates at all, assign - 'rift'
    """
    tile_class = [[" " for _ in range(len(num_plates[x]))] for x in range(len(num_plates))]
    for y in range(len(num_plates[0])):
        for x in range(len(num_plates)):
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

def get_water_distance_map(tile_classes, waters):
    """
    Using Dijkstra's algorithm, create a map of distance to the nearest water
    The difficulty of water is defined as 0, and the difficulty of land is 1.
    Defines water as being one of the classes in the list `waters`
    """
    start = None
    dijkstra_matrix = []
    for x in range(len(tile_classes)):
        dijkstra_matrix.append([])
        for y in range(len(tile_classes[x])):
            if tile_classes[x][y] in waters:
                dijkstra_matrix[x].append(0)
                if start is None:
                    start = (x, y)
            else:
                dijkstra_matrix[x].append(1)
    return dijkstra.dijkstra_on_matrix(dijkstra_matrix, start[0], start[1])

def build_elevation_map(tile_class):
    """
    Constructs a map of elevations based on the tile classes defined previously
    Oceans have a default level of 0, while continents and rifts  have a higher level
    Mountains, volcanoes, and islands all have a chance to form, and if they do, they gain a bonus elevation
        and increase the elevation of their neighboring tiles
    """
    elev_map = [[0.0 for _ in range(len(tile_class[x]))] for x in range(len(tile_class))]
    waterdist_map = get_water_distance_map(tile_class, [".", "-"])
    for x in range(len(tile_class)):
        for y in range(len(tile_class[x])):
            if tile_class[x][y] in ["l", "M", "V", "I"]:
                elev_map[x][y] += macro_worldgen.CONTINENT_LEVEL + waterdist_map[x][y] * macro_worldgen.ELEV_GAIN
                if tile_class[x][y] == "M":
                    if random.random() < macro_worldgen.MOUNTAIN_CHANCE:
                        elev_map[x][y] += macro_worldgen.MOUNTAIN_ELEV
                        for n in get_neighbors(x, y, len(tile_class), len(tile_class[x])):
                            elev_map[n[0]][n[1]] += macro_worldgen.MOUNTAIN_SHARING
                elif tile_class[x][y] == "V":
                    if random.random() < macro_worldgen.VOLCANO_CHANCE:
                        elev_map[x][y] += macro_worldgen.VOLCANO_ELEV
                        for n in get_neighbors(x, y, len(tile_class), len(tile_class[x])):
                            elev_map[n[0]][n[1]] += macro_worldgen.VOLCANO_SHARING
            if tile_class[x][y] == "I":
                if random.random() < macro_worldgen.ISLAND_CHANCE:
                    elev_map[x][y] += macro_worldgen.ISLAND_ELEV
                    for n in get_neighbors(x, y, len(tile_class), len(tile_class[x])):
                        elev_map[n[0]][n[1]] += macro_worldgen.ISLAND_SHARING
            if tile_class[x][y] == "-":
                elev_map[x][y] += macro_worldgen.RIFT_LEVEL
    return elev_map

def build_ocean_connection_map(elev_map):
    """
    Assigns a class to each tile determining whether it is connected to an ocean
    Ocean here is defined as an elevation of 0
    Any tiles with an elevation higher than `sea_level` are always above land and not connected to an ocean
    Other tiles (with elevation between 0 and `sea_level`) are considered connected to an ocean
        if they neighbor a tile that is also connected to an ocean
    This is determined recursively, with ocean tiles trivially connected to an ocean,
        and non-ocean tiles that are connected to an ocean attempt to connect their neighbors
    The connection map has the tile classes:
     - '.', deep ocean with elevation 0
     - 'l', land above sea level
     - '-', land: below sea level but not connected to an ocean
     - '+', ocean: above elevation 0 and below sea level, and connected to an ocean
    """
    connection_map = [["" for _ in range(len(elev_map[x]))] for x in range(len(elev_map))]
    # Start by initializing the connection map, setting . for oceans, l for above sea level, and - for candidates
    for x in range(len(connection_map)):
        for y in range(len(connection_map[x])):
            if elev_map[x][y] == 0.0:
                connection_map[x][y] = "."
            elif elev_map[x][y] >= macro_worldgen.SEA_LEVEL:
                connection_map[x][y] = "l"
            else:
                connection_map[x][y] = "-"

    def connect_neighbors_to_ocean(connection_map, x, y):
        """
        Recursion function
        If a neighbor of the active tile, at (x, y), are in the class '-',
            then it is converted to '+', (connected to ocean but not ocean),
            and that then the function runs again with that neighbor as the active tile
        """
        neighbors = get_neighbors(x, y, len(connection_map), len(connection_map[x]))
        for n in neighbors:
            if connection_map[n[0]][n[1]] == "-":
                connection_map[n[0]][n[1]] = "+"
                connect_neighbors_to_ocean(connection_map, n[0], n[1])

    # Now, initialize the recursion by running the recursion on all ocean tiles found
    for x in range(len(connection_map)):
        for y in range(len(connection_map[x])):
            if connection_map[x][y] == ".":
                connect_neighbors_to_ocean(connection_map, x, y)
    return connection_map

def find_water_longitudinally(connection_map, elev_map, location, direction):
    """
    Finds the distance to the nearest major water body to a location, in an east or west direction only
    direction: East: +1; West: -1
    Also counts the total elevation loss down to sea level from the elevation map provided
    Returns the longitudinal distance to the nearest major water body and the total elevation loss to get there
    """
    distance = 0
    elev_loss = 0
    found = connection_map[location[0]][location[1]] in [".", "+"]
    search_location = location
    while not found and distance < len(connection_map):
        initial_elev = elev_map[search_location[0]][search_location[1]]
        distance += 1
        search_location = ((search_location[0] + direction) % len(connection_map), search_location[1])
        found = connection_map[search_location[0]][search_location[1]] in [".", "+"]
        elev_loss += max(initial_elev
                         - max(elev_map[search_location[0]][search_location[1]], macro_worldgen.SEA_LEVEL), 0)
    return distance, elev_loss

def build_waterclass_map(elev_map):
    """
    Given an elevation map, get a 'waterclass' map that gives the direction(s), if any, from which atmospheric
        water is sourced for each tile
    For each land tile, the nearest distance to water and the elevation loss are calculated in both east and west
        directions
    Under a composition of elevation gain and distance,
    Five water classes are then distinguished:
     - i: the tile can get water from both east and west
     - w: the tile can get water from the west
     - e: the tile can get water from the east
     - c: the tile is 'continental' and does not have a major source of atmospheric water
     - -: the tile is oceanic and not considered
    TODO: Add an "intensity", which says how many rainshadows away it is, to allow for more gradient-like rainshadows
    """
    waterclass_map = [["" for _ in range(len(elev_map[x]))] for x in range(len(elev_map))]
    connection_map = build_ocean_connection_map(elev_map)
    for x in range(len(elev_map)):
        for y in range(len(elev_map[x])):
            if connection_map[x][y] == "." or connection_map[x][y] == "+":
                waterclass_map[x][y] = "-"
            else:
                east_dist, east_elev = find_water_longitudinally(connection_map, elev_map,(x, y), 1)
                west_dist, west_elev = find_water_longitudinally(connection_map, elev_map,(x, y), -1)
                east_coast = (east_elev * macro_worldgen.DISTANCE_PER_ELEV
                              + east_dist < macro_worldgen.RAINSHADOW_DISTANCE)
                west_coast = (west_elev * macro_worldgen.DISTANCE_PER_ELEV
                              + west_dist < macro_worldgen.RAINSHADOW_DISTANCE)
                if west_coast and east_coast:
                    waterclass_map[x][y] = "i"
                elif west_coast:
                    waterclass_map[x][y] = "w"
                elif east_coast:
                    waterclass_map[x][y] = "e"
                else:
                    waterclass_map[x][y] = "c"
    return waterclass_map

def convert_to_latitude(y, leny):
    """
    Converts a world y coordinate to a latitude
    Assuming that the y coordinates span 90 to -90 degrees
    """
    return 180 / leny * (y - leny / 2)

def build_climateclass_map(waterclass_map, elev_map):
    """
    Builds a climate class map, which is the final step in generation
    Climate class is determined by the water class, elevation, and latitude
    Primarily, water class (which direction(s) water could come from, or which "coast" the tile is found on, if any)
        and latitude determine what climate is found
    """
    climateclass_map = [["" for _ in range(len(waterclass_map[x]))] for x in range(len(waterclass_map))]
    for x in range(len(waterclass_map)):
        for y in range(len(waterclass_map[x])):
            latitude = abs(convert_to_latitude(y, len(waterclass_map[x])))
            temperature_latitude = (latitude + macro_worldgen.LATITUDE_PER_ELEV
                                    * max(elev_map[x][y] - macro_worldgen.SEA_LEVEL, 0))
            if waterclass_map[x][y] == "-":
                # If the tile is underwater, but above "continent level", it becomes a coast
                if elev_map[x][y] >= macro_worldgen.CONTINENT_LEVEL:
                    climateclass_map[x][y] = "="
                # If the tile is underwater and so cold as to be the coldest temperature class, make sea ice
                elif temperature_latitude >= macro_worldgen.CLIMATE_TEMPERATURE_LATITUDE[-1]:
                    climateclass_map[x][y] = "-"
                # Otherwise, the tile is ocean
                else:
                    climateclass_map[x][y] = "~"
            # Otherwise, the tile is land, and wetness is determined according to waterclass
            else:
                west_wetness = macro_worldgen.CLIMATE_WEST_COAST_WETNESS[-1]
                for i in range(len(macro_worldgen.CLIMATE_WEST_COAST_LATITUDE)):
                    if latitude < macro_worldgen.CLIMATE_WEST_COAST_LATITUDE[i]:
                        west_wetness = macro_worldgen.CLIMATE_WEST_COAST_WETNESS[i]
                        break
                east_wetness = macro_worldgen.CLIMATE_EAST_COAST_WETNESS[-1]
                for i in range(len(macro_worldgen.CLIMATE_EAST_COAST_LATITUDE)):
                    if latitude < macro_worldgen.CLIMATE_EAST_COAST_LATITUDE[i]:
                        east_wetness = macro_worldgen.CLIMATE_EAST_COAST_WETNESS[i]
                        break
                if waterclass_map[x][y] == "i":
                    wetness = max(west_wetness, east_wetness)
                elif waterclass_map[x][y] == "w":
                    wetness = west_wetness
                elif waterclass_map[x][y] == "e":
                    wetness = east_wetness
                else:
                    wetness = 0
                temperature_class = macro_worldgen.CLIMATE_TEMPERATURE_CLASS[-1]
                for i in range(len(macro_worldgen.CLIMATE_TEMPERATURE_LATITUDE)):
                    if temperature_latitude < macro_worldgen.CLIMATE_TEMPERATURE_LATITUDE[i]:
                        temperature_class = macro_worldgen.CLIMATE_TEMPERATURE_CLASS[i]
                        break
                climateclass_map[x][y] = macro_worldgen.CLIMATE_COMBINATION_MATRIX[wetness][temperature_class]
    return climateclass_map

def generate_all_maps():
    world_plates, plate_sizes = create_plates()
    plate_types = continents_gen(world_plates, plate_sizes)
    plate_velocities = assign_plate_velocities(plate_types)
    plates_density = move_plates(world_plates, plate_types, plate_velocities)
    tile_class = assign_tectonic_class(plates_density)
    elev_map = build_elevation_map(tile_class)
    waterclass_map = build_waterclass_map(elev_map)
    climate_map = build_climateclass_map(waterclass_map, elev_map)
    return world_plates, plates_density, tile_class, elev_map, waterclass_map, climate_map

def main():
    # earth_geology = io_util.transpose_matrix(io_util.load_matrix_from_csv("Earth/earth-geology.csv"))
    # earth_elev = build_elevation_map(earth_geology)
    # earth_water = build_waterclass_map(earth_elev)
    # earth_climate = build_climateclass_map(earth_water, earth_elev)
    # io_util.write_matrix_to_csv(earth_climate, "earth_climate.csv")

    wp, pd, tc, em, wm, cm = generate_all_maps()
    io_util.write_matrix_to_csv(cm, "climate_map.csv")


if __name__ == '__main__':
    main()
