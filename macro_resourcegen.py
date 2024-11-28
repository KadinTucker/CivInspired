import macro_terrain
import macro_resource

# Describes the degree to which each resource is attached to certain terrain types.
# Rows are resources, columns are terrains.
# Terrain: NULL Coast Ocean Grassland Plains Tundra Desert Forest Savannah Taiga Jungle
RESOURCE_TERRAIN_FAVOR = [
    # N    c    O    g    p    u    d    F    S    T    J    I
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # NULL Resource
    [0.0, 0.0, 0.0, 3.0, 3.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Wheat
    [0.0, 0.0, 0.0, 3.0, 6.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Maize
    [0.0, 0.0, 0.0, 6.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Rice
    [0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Potato
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 3.0, 0.0],  # Banana
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 3.0, 0.0],  # Pineapple
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 0.0, 8.0, 0.0, 0.0],  # Deer
    [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Fish
    [0.0, 0.0, 0.0, 3.0, 6.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Cattle
    [0.0, 0.0, 0.0, 3.0, 3.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Sheep
    [0.0, 0.0, 0.0, 6.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Swine
    [0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Llama
    [0.0, 0.0, 0.0, 0.5, 0.2, 0.0, 0.0, 2.0, 1.0, 3.0, 1.0, 0.0],  # Timber
    [0.0, 0.0, 0.0, 0.4, 1.0, 2.0, 2.0, 0.5, 0.5, 0.5, 0.5, 0.0],  # Stone
    [0.0, 0.0, 0.0, 0.5, 0.5, 1.0, 1.0, 0.2, 0.2, 0.2, 0.2, 0.0],  # Copper
    [0.0, 0.0, 0.0, 0.5, 0.5, 1.0, 1.0, 0.2, 0.2, 0.2, 0.2, 0.0],  # Tin
    [0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 0.5, 0.5, 0.5, 0.5, 0.0],  # Iron
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Steel (synthetic)
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 1.5, 0.0, 3.0, 0.0],  # Rubber
    [0.0, 0.0, 0.0, 0.5, 0.5, 1.0, 1.0, 0.2, 0.2, 0.2, 0.2, 0.0],  # Aluminium
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Plastic
    [0.0, 0.0, 0.0, 0.3, 0.3, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0],  # Horses
    [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.5, 1.0, 0.0],  # Oil
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 0.0],  # Coal
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0],  # Uranium
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 1.5, 0.0],  # Cocoa
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 1.5, 0.0],  # Sugar
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 1.5, 0.0],  # Spice
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 1.5, 0.0],  # Dye
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Pharmaceuticals (synthetic)
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Consumer Goods (synthetic)
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0],  # Fur
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],  # Ivory
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],  # Silk
    [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Wine
    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Cotton
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0],  # Gold
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0],  # Gems
    [0.0, 0.1, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Whale
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Firearms (Synthetic)
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Missiles (synthetic)
]

# Which "continent" group each resource belongs to.
# Belonging to a continent group means a resource will not appear on the same "continent" as another resource in the
# same group.
# The group 0 means no continental distribution happens.
RESOURCE_CONTINENTAL_GROUP = [
    # 1 NULL, 4 food crops. 2 tropical foods. 2 other foods. 4 livestock. 6 materials.
    0, 1, 1, 1, 1, 2, 2, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0,
    # 7 strategic resources. 4 tropical luxuries. 2 synthetics. 5 special luxuries.
    0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0,
    # 3 dispersed luxuries. 2 military.
    0, 0, 0, 0, 0
]

# Continents are defined as being divided by certain terrain types.
# Each group has different continental divisions defined, with the following terrain types picked.
CONTINENT_GROUP_TERRAIN_BLACKLIST = [
    [1, 2, 7, 8, 9, 10, 11],  # Foodstuffs
    [1, 2, 3, 4, 5, 6, 7, 9, 11],  # Tropical Foods
    [1, 2, 7, 8, 9, 10, 11],  # Livestock
    [1, 2, 3, 4, 5, 6, 7, 9, 11],  # Tropical Luxuries
]

# The "dual" of the list RESOURCE_CONTINENTAL_GROUP:
# For each group, which resources, by index, are in each group.
CONTINENT_GROUP_MEMBERS = [
    [1, 2, 3, 4],
    [5, 6],
    [9, 10, 11, 12],
    [26, 27, 28, 29]
]

# How many distinct continents should be defined for each group
CONTINENT_GROUP_DIVISIONS = [
    4, 6, 4, 2
]

print(len(RESOURCE_TERRAIN_FAVOR))