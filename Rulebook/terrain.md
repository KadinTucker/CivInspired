# Terrain

The physical terrain of the world has an effect on how civilisations function. 

There are three main classes of terrain.
 - Normal: land terrain that is generally habitable by humans and useful to them. 
 - Hostile: land terrain that is more difficult for humans to inhabit, but often has unique resources to be found.
 - Aquatic: ocean terrain. Yields a lot of Commerce when worked by citizens. 

Terrain can also be classed as open or not open. Open terrain is easier for traders and units to move through, and additionally yields Commerce when worked by citizens.

The following table summarises all terrain types:

| Terrain   | Class   | Open? | Food Yield | Material Yield | Resources                                      | Special                                               |  
|-----------|---------|-------|------------|----------------|------------------------------------------------|-------------------------------------------------------|
| Grassland | Normal  | Yes   | 2          | 0              | Foodstuffs, Livestock, Horses                  |                                                       |
| Plains    | Normal  | Yes   | 1          | 1              | Livestock, Foodstuffs, Horses                  |                                                       |
| Forest    | Normal  | No    | 1          | 1              | Lumber, Deer                                   | Exists on top of another terrain type; can be cleared |
| Hills     | Normal  | No    | 1          | 1              | Stone, Minerals                                |                                                       |
| Tundra    | Hostile | Yes   | 1          | 0              | Minerals, Deer, Furs, Horses                   |                                                       |
| Desert    | Hostile | Yes   | 0          | 1              | Minerals, Stone, Incense, Horses               |                                                       |
| Jungle    | Hostile | No    | 1          | 0              | Tropical Wood, Bananas, Cassava, Many Luxuries | Can be cleared to reveal plains                       |
| Mountains | Hostile | No    | 0          | 1              | Minerals, Stone                                |                                                       |
| Ice Cap   | Hostile | No    | 0          | 0              | None                                           |                                                       |
| Coast     | Aquatic | Yes   | 1          | 0              | Fish, Pearls, Whale                            |                                                       |
| Ocean     | Aquatic | Yes   | 1          | 0              | Fish                                           |                                                       |
| Sea Ice   | Aquatic | No    | 0          | 0              | None                                           |                                                       |
