
"""
A 'Macro' file, which includes names and attributes of a certain aspect of the game
Index 0 for all entries is reserved for the 'NULL' entry, that is to be used in case of something being missing
This file is for physical terrain.
"""


TERRAIN_NAMES = "NULL Coast Ocean Grassland Plains Tundra Desert Forest Savannah Taiga Jungle".split()

# Yields are sorted into food, material, commerce.
TERRAIN_YIELDS = [(0, 0, 0), (1, 0, 2), (0, 0, 2), (2, 0, 1), (1, 1, 1), (1, 0, 1), (0, 1, 1), (1, 2, 0), (2, 1, 0),
                  (1, 1, 0), (1, 1, 0)]

