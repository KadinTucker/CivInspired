# City

A city is a tile element representing a single administrative center for a region. 

A city has:
 - a population of people living in the region;
 - territory over which the city has influence;
 - a stock of resources* the city has produced or imported from aborad.

### City Growth

Cities grow by attracting new people to live there. This happens through passive migration and active migration.

Both processes are affected by *appeal*, which is a factor based on:

- The total number of empty workable slots in the city;
- The amount of excess food and materials in the city;
- The diversity of luxury resources in the city;
- The culture of the city.

#### Passive Migration

In passive migration, a city grows in population from its own borders. This represents a combination of people gradually settling down from their nomadic ways and assimilating to your culture, as well as typical population growth. 

The rate of passive growth of a city is proportional to:
- The total number of tiles within the city's boundaries minus the city population (not below 0);
- The appeal of the city.

The main consequence of this is that the larger borders grow, the larger population grows. 

Passive migration is the main way cities grow early in the game, but its relevance drops off as populations grow more dense. 

#### Active Migration

Active migration is the movement of population points between cities. This happens similarly to trade, but with key differences. 

Active migration occurs through the accumulation of migration points from one city to another. Once the number of migration points exceeds a certain threshold, the origin city loses a population and the destination city gains a population of the origin city's culture.

The rate of migration is decided by two factors:

- Desirability: the desirability of a destination is determined by the trade distance, shared culture, governance, and any policies that affect migration.
- Appeal Gradient: migration occurs from cities of low appeal to high appeal. If the potential destination has lower appeal, then the gradient is negative. 

Finally, the total number of migration points accumulated is the desirability times the appeal gradient, rounded down. This may be negative, which causes the number of migration points to drop, but it will never drop below zero. 