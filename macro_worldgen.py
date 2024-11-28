
"""
A 'Macro' file, which includes names and attributes of a certain aspect of the game
Index 0 for all entries is reserved for the 'NULL' entry, that is to be used in case of something being missing
This file is for parameters used in world generation
"""


# The width and height of the world
# Ratio of 2 - 1 is preferred
LENX = 200
LENY = 100

# The number of tectonic plates to generate.
# 20-40 makes for a chunky distribution, and 60+ makes for a somewhat "gory" distribution
N_PLATES = LENX * LENY // 250
# Approximately what fraction of the world's land should be continental plates
LAND_COVER = 0.35
# How many tiles plates move maximally, with a base velocity, and an extra velocity depending on the type
PLATE_VELOCITY = LENX / 75
CONTINENT_VELOCITY = PLATE_VELOCITY / 2
OCEAN_VELOCITY = PLATE_VELOCITY

# The amount by which elevation increases for each tile going inland
ELEV_GAIN = 10 / LENX
# The elevation units at which the sea ends
SEA_LEVEL = 1.0
# The base elevation units continents have before uplift
CONTINENT_LEVEL = SEA_LEVEL - 3 * ELEV_GAIN
# The base elevation of rifts between divergent plates
RIFT_LEVEL = CONTINENT_LEVEL - 5 * ELEV_GAIN

# In the below 'geology' macros, there is the chance of a geological feature occurring in a relevant location,
# the elevation gained if the feature occurs, and the elevation spread (shared) to neighboring tiles
MOUNTAIN_CHANCE = 1.0
MOUNTAIN_ELEV = 2.0
MOUNTAIN_SHARING = 0.5
VOLCANO_CHANCE = 1.0
VOLCANO_ELEV = 1.5
VOLCANO_SHARING = 0.3
#ISLAND_CHANCE = 0.2 * 200 / LENX
ISLAND_CHANCE = 1.0
ISLAND_ELEV = CONTINENT_LEVEL - ELEV_GAIN
ISLAND_SHARING = ELEV_GAIN

# The equivalent distance in tiles needed to travel before the rainshadow effect occurs and water is no longer sourced
# from a nearby body
RAINSHADOW_DISTANCE = LENX // 5
# The amount by which an increase in elevation by 1 counts as distance for the rainshadow effect
DISTANCE_PER_ELEV = 20.0

# For the purposes of getting climate temperature, by how much does an elevation unit, above sea level, increase
# the latitude
LATITUDE_PER_ELEV = 7.5

# In the below 'climate' macros, the first list is the upper boundaries in latitude,
# while the second is the index of the quantity
# The second list has one more entry than the first, because the last is if the latitude exceeds any of the others
CLIMATE_EAST_COAST_LATITUDE = [10, 25, 40, 60]
CLIMATE_EAST_COAST_WETNESS = [3, 2, 2, 1, 3]

CLIMATE_WEST_COAST_LATITUDE = [10, 15, 30, 40, 60]
CLIMATE_WEST_COAST_WETNESS = [3, 1, 0, 1, 2, 2]

CLIMATE_TEMPERATURE_LATITUDE = [25, 40, 60, 70]
CLIMATE_TEMPERATURE_CLASS = [4, 3, 2, 1, 0]

# the rows are wetness indices (dry to wet), and the columns are temperatures (cold to hot)
CLIMATE_COMBINATION_MATRIX = [
    ["I", "u", "p", "d", "d"],   # Dry
    ["I", "u", "p", "g", "S"],   # Medium-Dry
    ["I", "T", "F", "g", "S"],   # Medium-Wet
    ["I", "T", "F", "J", "J"]    # Wet
]  # ice; cold cool warm hot

WATER_CLIMATE_CONTRIBUTION = {
    "I": 1.0,
    "u": 1.0,
    "T": 1.5,
    "p": 0.5,
    "d": 0.1,
    "F": 1.5,
    "g": 1.0,
    "S": 1.0,
    "J": 1.5
}
