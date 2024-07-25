# City

A city is a tile element representing a single administrative center for a region. 

A city has:
 - a population of people living in the region;
 - territory over which the city has influence;
 - a stock of resources* the city has produced or imported from aborad.

A city also has many other functions, including, but not limited to:
 - mustering soldiers;
 - trading resources;
 - growing and moving population.

### Work and Trade

Each citizen in a city has work that it does, either on a tile or in the city centre, which produces yields and resources.

Citizens in the city also consume resources:
- Most resources are consumed to produce yields. For example, lumber is converted into Materials.
- Each citizen cannot consume more than one of each resource per turn. 
- Materials are consumed by citizens to make Production, which is then used to create things in the city. 
- Food is consumed by citizens; otherwise they start to starve. If citizens starve for more than one turn, they die. 

After the above two have happened, the city trades; see trade*. 

Any resources that are not either consumed or exported are considered *left-over*. Left-over resources are converted into Commerce at a 2 : 1 ratio. 

Left-over Commerce is then inefficiently converted into Science and Culture, at a 2 : 1 ratio. 

### City Growth

Cities grow by attracting new people to live there. This happens through passive migration and active migration.

Both processes are affected by *appeal*, which is a factor based on:

- The total number of empty workable slots in the city;
- The amount of excess food and materials in the city;
- The diversity of luxury resources in the city;
- The culture of the city.

The first two points—the number of workable slots and excess food and materials—are called *potential*, and the second two points are called *favour*. 

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