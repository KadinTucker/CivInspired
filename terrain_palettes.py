import palette_make

# Colors are five samples taken from a LANDSAT image of the biome on earth, sampled in a few different places

JUNGLE = [(44, 71, 48), (49, 79, 55), (43, 72, 47), (36, 68, 39), (44, 70, 49)]
SCRUB = [(57, 88, 56), (82, 112, 73), (128, 133, 107), (83, 99, 74), (90, 87, 78)]
DESERT = [(169, 139, 124), (202, 146, 97), (221, 204, 166), (176, 133, 101), (183, 178, 157)]
GRASSLAND = [(86, 110, 80), (110, 128, 105), (67, 96, 66), (124, 144, 123), (59, 84, 64)]
FOREST = [(44, 71, 53), (64, 96, 74), (43, 66, 39), (31, 62, 40), (25, 50, 34)]
PLAINS = [(149, 141, 118), (173, 162, 138), (139, 129, 110), (165, 166, 153), (142, 135, 116)]
TAIGA = [(59, 80, 66), (52, 74, 55), (37, 55, 49), (60, 80, 65), (71, 87, 67)]
TUNDRA = [(106, 106, 80), (88, 99, 76), (137, 135, 121), (78, 87, 68), (75, 81, 78)]
ICE = [(189, 194, 188), (208, 214, 208), (217, 217, 216), (200, 202, 189), (189, 205, 223)]
OCEAN = [(30, 48, 104), (57, 79, 139), (29, 51, 118), (22, 40, 82), (61, 84, 142)]
COAST = [(94, 113, 175), (72, 95, 158), (73, 96, 153), (73, 94, 148), (87, 112, 171)]

# Extended palettes that make the sampled colors combine randomly

JUNGLE_E = palette_make.create_expanded_palette(JUNGLE)
SCRUB_E = palette_make.create_expanded_palette(SCRUB)
DESERT_E = palette_make.create_expanded_palette(DESERT, [1, 0, 3, 0, 0])
GRASSLAND_E = palette_make.create_expanded_palette(GRASSLAND)
FOREST_E = palette_make.create_expanded_palette(FOREST, [0, 1, 1, 0, 0])
PLAINS_E = palette_make.create_expanded_palette(PLAINS)
TAIGA_E = palette_make.create_expanded_palette(TAIGA)
TUNDRA_E = palette_make.create_expanded_palette(TUNDRA)
ICE_E = palette_make.create_expanded_palette(ICE)
OCEAN_E = palette_make.create_expanded_palette(OCEAN, [1, 2, 0, 0, 1])
COAST_E = palette_make.create_expanded_palette(COAST, [1, 2, 0, 1, 0])
