import macro_terrain
import macro_resource

# Describes the degree to which each resource is attached to certain terrain types.
# Rows are resources, columns are terrains.
# Terrain: NULL Coast Ocean Grassland Plains Tundra Desert Forest Savannah Taiga Jungle
RESOURCE_TERRAIN_FAVOR = [
    # N    c    O    g    p    u    d    F    S    T    J
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # NULL Resource
    [0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],  # Wheat
    [0.0, 0.0, 0.0, 1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Maize
    [0.0, 0.0, 0.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Rice
    [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Potato
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0],  # Banana
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0],  # Pineapple
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0],  # Deer
    [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Fish
    [0.0, 0.0, 0.0, 1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Cattle
    [0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],  # Sheep
    [0.0, 0.0, 0.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Swine
    [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Llama
    [0.0, 0.0, 0.0, 0.5, 0.2, 0.0, 0.0, 2.0, 1.0, 2.0, 1.0],  # Timber
    [0.0, 0.0, 0.0, 0.4, 1.0, 2.0, 2.0, 0.5, 0.5, 0.5, 0.5],  # Stone
    [0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 0.5, 0.5, 0.5, 0.5],  # Copper
    [0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 0.5, 0.5, 0.5, 0.5],  # Tin
    [0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 0.5, 0.5, 0.5, 0.5],  # Iron
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Steel (synthetic)
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 2.0],  # Rubber
    [0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 0.5, 0.5, 0.5, 0.5],  # Aluminium
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Plastic
    [0.0, 0.0, 0.0, 1.0, 1.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0],  # Horses
    [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.5, 1.0],  # Oil
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0],  # Coal
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],  # Uranium
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 2.0],  # Cocoa
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 2.0],  # Sugar
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 2.0],  # Spice
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 2.0],  # Dye
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Pharmaceuticals (synthetic)
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Consumer Goods (synthetic)
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],  # Fur
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],  # Ivory
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],  # Silk
    [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Wine
    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Cotton
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],  # Gold
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],  # Gems
    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Whale
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Firearms (Synthetic)
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Missiles (synthetic)
]

# Whether the resource appears specifically on a single continental mass or not.
RESOURCE_CONTINENTAL = [
    # 6 food crops. 2 other foods. 4 livestock. 5 minerals/metals.
    True, True, True, True, True, True, False, False, True, True, True, True, False, False, False, False, False,
    # 7 strategic resources. 4 tropical luxuries. 2 synthetics. 5 special luxuries.
    False, False, False, False, False, False, False, True, True, True, True, False, False, True, True, True, True, True,
    # 3 dispersed luxuries. 2 military.
    False, False, False, False, False
]
