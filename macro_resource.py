
"""
A 'Macro' file, which includes names and attributes of a certain aspect of the game
Index 0 for all entries is reserved for the 'NULL' entry, that is to be used in case of something being missing
This file is for resources; more specifically, what are called 'goods' in the rulebook
"""

CLASS_NAMES = "NULL Foodstuffs Livestock Material Energy1 Energy2 Luxury Military".split()

RESOURCE_NAMES = ("NULL Wheat Maize Rice Potato Banana Pineapple Deer Fish Cattle Sheep Swine Llama Timber Stone "
                  "Copper Tin Iron Steel Rubber Aluminium Plastic Horses Oil Coal Uranium Cocoa Sugar Spice Dye "
                  "Pharmaceuticals ConsumerGoods Fur Ivory Silk Wine Cotton Gold Gems Whale Firearms Missiles").split()

RESOURCE_CLASS = [0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6,
                  6, 6, 6, 6, 6, 6, 7, 7]

RESOURCE_NATURAL = [False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
                    True, True, False, True, True, False, True, True, True, True, True, True, True, True, False, False,
                    True, True, True, True, True, True, True, True, False, False]

RESOURCE_PLANTABLE = [False, True, True, True, True, True, True, False, False, True, True, True, True, False, False,
                      False, False, False, False, True, False, False, True, False, False, False, True, True, True, True,
                      False, False, False, False, True, True, True, False, False, False, False, False]

