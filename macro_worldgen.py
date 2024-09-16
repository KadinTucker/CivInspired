
"""
A 'Macro' file, which includes names and attributes of a certain aspect of the game
Index 0 for all entries is reserved for the 'NULL' entry, that is to be used in case of something being missing
This file is for parameters used in world generation
"""

# In the below 'climate' macros, the first list is the upper boundaries in latitude,
# while the second is the index of the quantity
# The second list has one more entry than the first, because the last is if the latitude exceeds any of the others
CLIMATE_EAST_COAST_LATITUDE = [10, 25, 40, 60]
CLIMATE_EAST_COAST_WETNESS = [3, 2, 2, 1, 0]

CLIMATE_WEST_COAST_LATITUDE = [10, 15, 30, 40, 60]
CLIMATE_WEST_COAST_WETNESS = [3, 1, 0, 1, 2, 3]

CLIMATE_TEMPERATURE_LATITUDE = [25, 40, 60, 75]
CLIMATE_TEMPERATURE_CLASS = [4, 3, 2, 1, 0]

# the rows are wetness indices (dry to wet), and the columns are temperatures (cold to hot)
CLIMATE_COMBINATION_MATRIX = [
    ["I", "u", "p", "d", "d"],   # Dry
    ["I", "u", "p", "g", "S"],   # Medium-Dry
    ["I", "T", "F", "g", "S"],   # Medium-Wet
    ["I", "T", "F", "J", "J"]    # Wet
]  # ice; cold cool warm hot
