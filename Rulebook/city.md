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

### A City's Process

A city's turn happens in three phases:
 - Production Phase: cities individually produce yields and goods.
 - Trade Phase: all cities trade with each other.
 - Resolution Phase: cities individually consume resources, handle migration, and resolve lefover Commerce, as well as Culture, and Science.

#### Production Phase

Each citizen in a city has work that it does, either on a tile or in the city centre, which produces yields and resources.

Resources that are transferable (all goods and some yields) are stored, and others are recorded as produced, to be used in the Resolution Phase.

#### Trade Phase

See Trade*. 

#### Resolution Phase

First, citizens in the city consume resources:
- Most resources are consumed to produce yields. For example, lumber is converted into Materials.
- Each citizen cannot consume more than one of each resource per turn. 
- Materials are consumed by citizens to make Production, which is then used to create things in the city. 
- Food is consumed by citizens; otherwise they start to starve. If citizens starve for more than one turn, they die. 

Food is special: food that is left-over cannot be stored, and is converted to Passive Migration Progress, representing additional benefits of having excess food available. 

The city then resolves both passive and active migration; see below.

The remaining yields are then resolved.

Left-over Commerce is partitioned into four different categories:
 - Treasury: the Commerce goes directly to the player controlling the city (unlocks with the Currency* technology);
 - Coffers: the Commerce is stored to be used in trade again the next turn (unlocks with the Currency* technology);
 - Philosophy: the Commerce is converted into Science and Culture, rather inefficiently;
   - This can be separated into Science and Culture individually after unlocking the right technology (Enlightenment). 
 - Military: contributes the Commerce to the local militia, who can be mustered into soldiers.

Culture is resolved; see Culture*. 

Lastly, Science generated through yields and through trade is resolved, being allocated to technologies as appropriate. See Technology* for more details.

### City Growth

Cities grow by attracting new people to live there. This happens through passive migration and active migration.

Both processes are affected by *appeal*, which is a factor based on:

- The total number of empty workable slots in the city;
- The amount of excess food and materials yielded in the city last turn;
- The diversity of luxury resources in the city;
- The culture of the city;
- Any grievances the city has reduces appeal.

The first two points—the number of workable slots and excess food and materials—are called *potential*, and the last three points are called *favour*. 

#### Passive Migration

In passive migration, a city grows in population from its own borders. This represents a combination of people gradually settling down from their nomadic ways and assimilating to your culture, as well as typical population growth. 

The rate of passive growth of a city is proportional to:
- The total number of tiles within the city's boundaries minus the city population (not below 0);
- The appeal of the city.

The main consequence of this is that the larger borders grow, the larger population grows. 

Passive migration points also accumulate at a slow rate with excess food in the city.

Passive migration is the main way cities grow early in the game, but its relevance drops off as populations grow more dense. 

#### Active Migration

Active migration is the movement of population points between cities. This happens similarly to trade, but with key differences. 

Active migration occurs through the accumulation of migration points from one city to another. Once the number of migration points exceeds a certain threshold, the origin city loses a population and the destination city gains a population of the origin city's culture.

The rate of migration is decided by two factors:

- Desirability: the desirability of a destination is determined by the trade distance, shared culture, governance, and any policies that affect migration.
- Appeal Gradient: migration occurs from cities of low appeal to high appeal. If the potential destination has lower appeal, then the gradient is negative. 

Finally, the total number of migration points accumulated is the desirability times the appeal gradient, rounded down. This may be negative, which causes the number of migration points to drop, but it will never drop below zero. 